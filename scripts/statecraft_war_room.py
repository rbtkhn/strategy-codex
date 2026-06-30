#!/usr/bin/env python3
"""
Statecraft War Room — advisory rollup of live statecraft objects.

Read-only except report outputs. Does not create instrument compact directories.

See runtime/artifacts/statecraft-war-room/README.md and
docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_statecraft_intake_daily_sync import (  # noqa: E402
    DAILY_DIR,
    build_sync_report,
    resolve_latest_captured_day,
)
from operator_report_utils import (  # noqa: E402
    authority_header,
    markdown_table,
    utc_now_iso,
    write_report,
)
from repo_io import ARTIFACTS_DIR  # noqa: E402
from statecraft_day_archive import DEFAULT_ROOT, iter_all_day_dirs  # noqa: E402
from statecraft_intake_queue import (  # noqa: E402
    QUEUE_ROOT,
    SourceQueueRow,
    build_queue_report,
    load_sidecar,
    rel_repo_path,
)

DEFAULT_OUT = ARTIFACTS_DIR / "statecraft-war-room" / "latest.md"
DEFAULT_JSON = ARTIFACTS_DIR / "statecraft-war-room" / "latest.json"
def resolve_router_path(repo_root: Path = REPO_ROOT) -> Path:
    instrument = repo_root / "statecraft" / "sheets" / "instrument-router.md"
    legacy = repo_root / "statecraft" / "sheets" / "transaction-router.md"
    if instrument.is_file():
        return instrument
    return legacy

ROUTER_PATH = resolve_router_path()

EXACT_THRESHOLD = 0.45
NEAR_THRESHOLD = 0.25

RETURN_PATHS = [
    "statecraft/README.md",
    "docs/statecraft-intake-queue.md",
    "statecraft/sheets/instrument-router.md",
    "statecraft/sheets/transaction-router.md",
    "statecraft/patterns/README.md",
]

CONFIDENCE_RANK = {"explicit": 3, "inferred": 2, "weak": 1}

LANE_ALIASES = {
    "america": "America",
    "persia": "Persia",
    "iran": "Persia",
    "russia": "Russia",
    "china": "China",
    "cross-lane": "cross-lane",
    "cross_lane": "cross-lane",
}

TRANSACTION_LINK_RE = re.compile(
    r"\[[^\]]*\]\(([^)]*(?:\.\./(?:transactions|notes/compacts)/|statecraft/(?:transactions|notes/compacts)/)[^)]+)\)",
    re.IGNORECASE,
)
DOMINANT_OBJECT_RE = re.compile(
    r"dominant object[^—\n]*—\s*\*\*([^*]+)\*\*",
    re.IGNORECASE,
)
EXECUTIVE_BOLD_RE = re.compile(r"\*\*([^*]{8,120})\*\*")
ROUTER_TABLE_ROW_RE = re.compile(r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+)\|")

TOKEN_RE = re.compile(r"[a-z0-9]+")

@dataclass
class RouterEntry:
    name: str
    crisis_object: str
    use_when: str
    primary_lanes: str
    transaction_path: str

@dataclass
class TransactionFit:
    kind: str
    transaction_path: str | None
    reason: str
    operator_confirm: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class WarRoomObject:
    name: str
    slug: str
    lane: str
    lane_confidence: str
    object_confidence: str
    source_floor: list[dict[str, str]] = field(default_factory=list)
    transaction_fit: TransactionFit = field(
        default_factory=lambda: TransactionFit("none", None, "no router match", False)
    )
    status: str = "new"
    next_action: str = "Operator review required"
    falsifier: str | None = None
    text: str = ""
    threads: tuple[str, ...] = ()
    pub_date: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "name": self.name,
            "lane": self.lane,
            "lane_confidence": self.lane_confidence,
            "object_confidence": self.object_confidence,
            "source_floor": self.source_floor,
            "transaction_fit": self.transaction_fit.to_dict(),
            "status": self.status,
            "next_action": self.next_action,
            "falsifier": self.falsifier,
        }
        if self.pub_date:
            payload["pub_date"] = self.pub_date
        return payload

@dataclass
class WarRoomContext:
    days_scanned: list[str]
    latest_archive_day: str | None
    latest_daily_path: str | None
    sync_status: str
    queue_rows: list[SourceQueueRow]
    objects: list[WarRoomObject]

def token_set(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))

def overlap_score(left: str, right: str) -> float:
    a = token_set(left)
    b = token_set(right)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def normalize_slug(text: str) -> str:
    tokens = TOKEN_RE.findall(text.lower())
    return "-".join(tokens[:8]) if tokens else "object"

def normalize_transaction_path(raw: str, *, repo_root: Path = REPO_ROOT) -> str:
    path = raw.split("#", 1)[0].strip()
    if path.startswith("statecraft/"):
        return path
    candidate = (repo_root / "statecraft" / "sheets" / path).resolve()
    try:
        rel = candidate.relative_to(repo_root.resolve())
        return rel.as_posix()
    except ValueError:
        pass
    if path.startswith("../"):
        resolved = (ROUTER_PATH.parent / path).resolve()
        try:
            return resolved.relative_to(repo_root.resolve()).as_posix()
        except ValueError:
            return path.replace("\\", "/")
    return path.replace("\\", "/")

def parse_transaction_router(path: Path) -> list[RouterEntry]:
    if not path.is_file():
        return []
    entries: list[RouterEntry] = []
    in_index = False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip() == "## Router Index":
            in_index = True
            continue
        if in_index and line.startswith("## ") and line.strip() != "## Router Index":
            break
        if not in_index:
            continue
        if line.strip().startswith("| ---"):
            continue
        m = ROUTER_TABLE_ROW_RE.match(line.strip())
        if not m:
            continue
        name, link, crisis = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        use_when = parts[2] if len(parts) > 2 else ""
        primary_lanes = parts[3] if len(parts) > 3 else ""
        entries.append(
            RouterEntry(
                name=name,
                crisis_object=crisis,
                use_when=use_when,
                primary_lanes=primary_lanes,
                transaction_path=normalize_transaction_path(link),
            )
        )
    return entries

def find_explicit_transaction_link(text: str) -> str | None:
    for match in TRANSACTION_LINK_RE.finditer(text):
        return normalize_transaction_path(match.group(1))
    return None

def classify_transaction_fit(text: str, router: list[RouterEntry]) -> TransactionFit:
    explicit = find_explicit_transaction_link(text)
    if explicit:
        return TransactionFit(
            kind="exact",
            transaction_path=explicit,
            reason="explicit transaction link in source text",
            operator_confirm=True,
        )

    best_score = 0.0
    best_entry: RouterEntry | None = None
    for entry in router:
        crisis_score = overlap_score(text, entry.crisis_object)
        use_score = overlap_score(text, entry.use_when)
        combined = max(crisis_score, use_score * 0.85)
        if combined > best_score:
            best_score = combined
            best_entry = entry

    if best_entry is None:
        return TransactionFit("none", None, "no router match", False)

    if best_score >= EXACT_THRESHOLD:
        return TransactionFit(
            kind="exact",
            transaction_path=best_entry.transaction_path,
            reason=f"high lexical overlap ({best_score:.2f}) with {best_entry.name}",
            operator_confirm=True,
        )
    if best_score >= NEAR_THRESHOLD:
        return TransactionFit(
            kind="near",
            transaction_path=best_entry.transaction_path,
            reason=f"partial overlap ({best_score:.2f}) with {best_entry.name}",
            operator_confirm=True,
        )
    return TransactionFit("none", None, f"weak overlap ({best_score:.2f})", False)

def infer_lane(
    *,
    threads: tuple[str, ...],
    text: str,
    sidecar: dict[str, Any] | None,
    router_entry: RouterEntry | None,
) -> tuple[str, str]:
    lowered = text.lower()
    for prefix in ("statecraft/persia/", "persia/transactions/"):
        if prefix in lowered:
            return "Persia", "explicit"
    for thread in threads:
        key = thread.lower().replace("-", "_")
        if key in LANE_ALIASES:
            return LANE_ALIASES[key], "explicit"
        if key in {"america", "persia", "iran", "russia", "china"}:
            return LANE_ALIASES.get(key, thread.title()), "explicit"

    if sidecar:
        for region in sidecar.get("regions") or []:
            key = str(region).lower()
            if key in LANE_ALIASES:
                return LANE_ALIASES[key], "inferred"

    if router_entry and router_entry.primary_lanes:
        first = router_entry.primary_lanes.split(",")[0].strip()
        if first:
            return first, "inferred"

    for key, label in LANE_ALIASES.items():
        if key.replace("_", " ") in lowered or key in lowered:
            return label, "weak"

    return "cross-lane", "weak"

def load_sidecars_for_day(day: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    day_dir = QUEUE_ROOT / day
    if not day_dir.is_dir():
        return out
    for path in sorted(day_dir.glob("*.v1.json")):
        payload = load_sidecar(path)
        if payload:
            payload = dict(payload)
            payload["_sidecar_path"] = rel_repo_path(path)
            out.append(payload)
    return out

def extract_daily_objects(
    daily_path: Path,
    *,
    pub_date: str | None = None,
    router: list[RouterEntry] | None = None,
) -> list[WarRoomObject]:
    if not daily_path.is_file():
        return []
    text = daily_path.read_text(encoding="utf-8", errors="replace")
    rel_daily = rel_repo_path(daily_path)
    day = pub_date or daily_path.stem[:10]

    names: list[tuple[str, str]] = []
    dom = DOMINANT_OBJECT_RE.search(text)
    if dom:
        names.append((dom.group(1).strip(), "explicit"))
    else:
        exec_idx = text.find("## Executive Read")
        if exec_idx >= 0:
            section = text[exec_idx : exec_idx + 1200]
            for m in EXECUTIVE_BOLD_RE.finditer(section):
                candidate = m.group(1).strip()
                if len(candidate) > 12:
                    names.append((candidate, "inferred"))
                    break

    if not names:
        title_line = next((ln for ln in text.splitlines() if ln.startswith("# State Synthesis")), "")
        if title_line:
            names.append((title_line.replace("#", "").strip(), "inferred"))

    router_entries = router if router is not None else parse_transaction_router(ROUTER_PATH)
    explicit_tx = find_explicit_transaction_link(text)
    status = "transaction" if explicit_tx else "daily"
    objects: list[WarRoomObject] = []
    for name, conf in names[:2]:
        slug = normalize_slug(name)
        fit = classify_transaction_fit(text, router_entries)
        if explicit_tx:
            fit = TransactionFit(
                "exact",
                explicit_tx,
                "explicit transaction link in daily synthesis",
                True,
            )
        lane, lane_conf = infer_lane(threads=(), text=text, sidecar=None, router_entry=None)
        objects.append(
            WarRoomObject(
                name=name,
                slug=slug,
                lane=lane,
                lane_confidence=lane_conf,
                object_confidence=conf,
                source_floor=[{"path": rel_daily, "kind": "daily"}],
                transaction_fit=fit,
                status=status,
                next_action="Review daily synthesis and confirm transaction fit",
                text=text[:4000],
                pub_date=day,
            )
        )
    return objects

def object_from_queue_row(
    row: SourceQueueRow,
    *,
    day: str,
    sidecar: dict[str, Any] | None,
    router: list[RouterEntry],
) -> WarRoomObject:
    name = row.source_stem.replace("source-", "").replace("-", " ")[:80]
    if row.threads:
        name = f"{row.threads[0]} — {name[:50]}"
    text = " ".join([row.reasoning, *row.threads, *row.actors])
    slug = normalize_slug(name)
    fit = classify_transaction_fit(text, router)
    router_entry = None
    if fit.transaction_path:
        router_entry = next((e for e in router if e.transaction_path == fit.transaction_path), None)
    lane, lane_conf = infer_lane(
        threads=row.threads,
        text=text,
        sidecar=sidecar,
        router_entry=router_entry,
    )
    status = row.synthesis_status
    if sidecar and sidecar.get("transaction_candidate") and status != "daily":
        status = "review"
    floor = [{"path": row.source_path, "kind": "archive"}]
    if row.sidecar_path:
        floor.append({"path": row.sidecar_path, "kind": "sidecar"})
    if row.in_daily:
        floor.append({"path": f"statecraft/synthesis/day/{day}.md", "kind": "daily"})
    next_action = "Promote to daily synthesis or discard from queue"
    if status == "daily":
        next_action = "Monitor transaction fit and falsifiers"
    elif status == "review":
        next_action = "Operator confirm transaction candidate"
    return WarRoomObject(
        name=name,
        slug=slug,
        lane=lane,
        lane_confidence=lane_conf,
        object_confidence="inferred",
        source_floor=floor,
        transaction_fit=fit,
        status=status,
        next_action=next_action,
        text=text,
        threads=row.threads,
        pub_date=day,
    )

def build_objects_for_day(
    day: str,
    *,
    archive_root: Path = DEFAULT_ROOT,
    daily_dir: Path = DAILY_DIR,
    router: list[RouterEntry],
    allow_desync: bool = True,
) -> tuple[list[WarRoomObject], list[SourceQueueRow], str]:
    try:
        rows, sync = build_queue_report(
            day,
            root=archive_root,
            daily_dir=daily_dir,
            allow_desync=allow_desync,
        )
    except FileNotFoundError:
        return [], [], "no_archive"

    sync_status = sync.status
    sidecars_by_stem = {
        Path(sc.get("source_path", "")).stem: sc
        for sc in load_sidecars_for_day(day)
        if sc.get("source_path")
    }

    objects: list[WarRoomObject] = []
    daily_path = daily_dir / f"{day}.md"
    objects.extend(extract_daily_objects(daily_path, pub_date=day, router=router))

    for row in rows:
        if row.synthesis_status == "discarded":
            continue
        if row.in_daily and row.synthesis_status == "daily":
            continue
        if row.synthesis_status not in {"new", "queued"} and not row.sidecar_path:
            continue
        sidecar = sidecars_by_stem.get(row.source_stem)
        objects.append(
            object_from_queue_row(row, day=day, sidecar=sidecar, router=router)
        )

    return objects, rows, sync_status

def merge_objects(objects: list[WarRoomObject]) -> list[WarRoomObject]:
    merged: dict[str, WarRoomObject] = {}
    for obj in objects:
        key = obj.slug or normalize_slug(obj.name)
        existing = merged.get(key)
        if existing is None:
            merged[key] = obj
            continue
        if CONFIDENCE_RANK.get(obj.object_confidence, 0) > CONFIDENCE_RANK.get(
            existing.object_confidence, 0
        ):
            primary, secondary = obj, existing
        else:
            primary, secondary = existing, obj
        primary.source_floor = primary.source_floor + [
            sf for sf in secondary.source_floor if sf not in primary.source_floor
        ]
        if len(primary.text) < len(secondary.text):
            primary.text = secondary.text
        if primary.transaction_fit.kind == "none" and secondary.transaction_fit.kind != "none":
            primary.transaction_fit = secondary.transaction_fit
        if primary.status == "new" and secondary.status != "new":
            primary.status = secondary.status
        merged[key] = primary
    ranked = sorted(
        merged.values(),
        key=lambda o: (
            -CONFIDENCE_RANK.get(o.object_confidence, 0),
            o.status not in {"queued", "review", "new"},
            o.name,
        ),
    )
    return ranked

def select_days(
    *,
    latest_days: int,
    pin_day: str | None,
    archive_root: Path = DEFAULT_ROOT,
) -> list[str]:
    if pin_day:
        return [pin_day]
    all_days = [p.name for p in iter_all_day_dirs(archive_root)]
    if not all_days:
        return []
    return all_days[-latest_days:]

def build_war_room_context(
    repo_root: Path,
    *,
    latest_days: int = 7,
    pin_day: str | None = None,
    include_weak: bool = False,
    max_objects: int = 12,
) -> WarRoomContext:
    archive_root = repo_root / "source-archive" / "statecraft"
    daily_dir = repo_root / "statecraft" / "synthesis" / "day"
    router = parse_transaction_router(resolve_router_path(repo_root))

    days = select_days(latest_days=latest_days, pin_day=pin_day, archive_root=archive_root)
    all_objects: list[WarRoomObject] = []
    all_rows: list[SourceQueueRow] = []
    latest_archive = resolve_latest_captured_day(root=archive_root)
    latest_daily_path: str | None = None

    for day in reversed(days):
        objs, rows, _day_sync = build_objects_for_day(
            day,
            archive_root=archive_root,
            daily_dir=daily_dir,
            router=router,
            allow_desync=True,
        )
        all_objects.extend(objs)
        all_rows.extend(rows)

    sync_status = "no_archive"
    if latest_archive:
        sync_report = build_sync_report(latest_archive, root=archive_root, daily_dir=daily_dir)
        sync_status = sync_report.status
        daily_candidate = daily_dir / f"{latest_archive}.md"
        if daily_candidate.is_file():
            latest_daily_path = rel_repo_path(daily_candidate)

    merged = merge_objects(all_objects)
    if not include_weak:
        merged = [o for o in merged if o.object_confidence != "weak"]
    merged = merged[:max_objects]

    return WarRoomContext(
        days_scanned=days,
        latest_archive_day=latest_archive,
        latest_daily_path=latest_daily_path,
        sync_status=sync_status,
        queue_rows=all_rows,
        objects=merged,
    )

def build_markdown(ctx: WarRoomContext, *, generated_at: str) -> str:
    parts = [
        "# Statecraft War Room",
        "",
        authority_header(generated_at, RETURN_PATHS),
        "## 1. Strategic Posture",
        "",
        f"- Latest archive day: `{ctx.latest_archive_day or 'none'}`",
        f"- Latest daily synthesis: `{ctx.latest_daily_path or 'none'}`",
        f"- Sync status: **{ctx.sync_status}**",
        f"- Days scanned: {', '.join(f'`{d}`' for d in ctx.days_scanned) or 'none'}",
        f"- Active objects (capped): {len(ctx.objects)}",
        "",
    ]
    if ctx.sync_status == "desync":
        parts.append(
            "> Advisory: archive/daily desync detected — run intake review or daily synthesis before treating objects as current."
        )
        parts.append("")

    parts.extend(["## 2. Active Crisis Objects", ""])
    explicit_objs = [o for o in ctx.objects if o.object_confidence == "explicit"]
    inferred_objs = [o for o in ctx.objects if o.object_confidence != "explicit"]
    for label, subset in (("Explicit confidence", explicit_objs), ("Inferred confidence", inferred_objs)):
        parts.append(f"### {label}")
        parts.append("")
        rows = [
            {
                "Object": o.name,
                "Lane": o.lane,
                "Status": o.status,
                "Transaction fit": o.transaction_fit.kind,
                "Next action": o.next_action,
            }
            for o in subset
        ]
        parts.append(
            markdown_table(rows, ["Object", "Lane", "Status", "Transaction fit", "Next action"])
            if rows
            else "_None._\n"
        )
        parts.append("")

    parts.extend(["## 3. Intake Queue Watch", ""])
    watch_rows = [
        {
            "Day": row.source_path.split("/")[-2] if "/" in row.source_path else "",
            "Source": row.source_stem[:40],
            "Status": row.synthesis_status,
            "Threads": ", ".join(row.threads[:3]),
            "Suggested action": "Promote to daily or discard",
        }
        for row in ctx.queue_rows
        if row.queue_eligible
    ][:20]
    parts.append(
        markdown_table(
            watch_rows,
            ["Day", "Source", "Status", "Threads", "Suggested action"],
        )
    )

    parts.extend(["", "## 4. Transaction Fit Board", ""])
    fit_rows = [
        {
            "Object": o.name,
            "Fit": o.transaction_fit.kind,
            "Transaction": o.transaction_fit.transaction_path or "",
            "Reason": o.transaction_fit.reason,
            "Operator confirm": "yes" if o.transaction_fit.operator_confirm else "no",
        }
        for o in ctx.objects
    ]
    parts.append(markdown_table(fit_rows, ["Object", "Fit", "Transaction", "Reason", "Operator confirm"]))

    parts.extend(["", "## 5. Lane Ownership Map", ""])
    lane_rows = [
        {
            "Object": o.name,
            "Lane": o.lane,
            "Confidence": o.lane_confidence,
            "Review need": "yes" if o.lane_confidence == "weak" else "no",
        }
        for o in ctx.objects
    ]
    parts.append(markdown_table(lane_rows, ["Object", "Lane", "Confidence", "Review need"]))

    parts.extend(["", "## 6. Source Floor", ""])
    floor_rows: list[dict[str, str]] = []
    for o in ctx.objects:
        for sf in o.source_floor[:3]:
            floor_rows.append(
                {
                    "Object": o.name[:50],
                    "Kind": sf.get("kind", ""),
                    "Path": sf.get("path", ""),
                }
            )
    parts.append(markdown_table(floor_rows, ["Object", "Kind", "Path"]))

    parts.extend(["", "## 7. Return Paths", ""])
    for path in RETURN_PATHS:
        parts.append(f"- `{path}`")
    parts.append("")
    return "\n".join(parts)

def build_json_payload(ctx: WarRoomContext, *, generated_at: str) -> dict[str, Any]:
    return {
        "generated_at": generated_at,
        "authority": "runtime_derived",
        "latest_archive_day": ctx.latest_archive_day,
        "latest_daily_path": ctx.latest_daily_path,
        "sync_status": ctx.sync_status,
        "days_scanned": ctx.days_scanned,
        "active_objects": [o.to_dict() for o in ctx.objects],
    }

def generate_report(
    repo_root: Path,
    *,
    out: Path = DEFAULT_OUT,
    json_out: Path = DEFAULT_JSON,
    snapshot: bool = False,
    latest_days: int = 7,
    max_objects: int = 12,
    include_weak: bool = False,
    pin_day: str | None = None,
) -> tuple[int, dict[str, Any]]:
    """Build and write Statecraft War Room report; return (exit_code, json_payload)."""
    out_path = out if out.is_absolute() else (repo_root / out).resolve()
    json_path = json_out if json_out.is_absolute() else (repo_root / json_out).resolve()

    try:
        ctx = build_war_room_context(
            repo_root,
            latest_days=latest_days,
            pin_day=pin_day,
            include_weak=include_weak,
            max_objects=max_objects,
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2, {}

    generated_at = utc_now_iso()
    md = build_markdown(ctx, generated_at=generated_at)
    payload = build_json_payload(ctx, generated_at=generated_at)

    write_report(out_path, md, snapshot=snapshot)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {out_path}")
    print(f"wrote {json_path}")
    print(f"objects: {len(ctx.objects)} sync: {ctx.sync_status}")
    return 0, payload

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--latest-days", type=int, default=7)
    parser.add_argument("--max-objects", type=int, default=12)
    parser.add_argument("--include-weak", action="store_true")
    parser.add_argument("--day", help="Pin single archive day YYYY-MM-DD")
    args = parser.parse_args()

    code, _payload = generate_report(
        REPO_ROOT,
        out=args.out,
        json_out=args.json_out,
        snapshot=args.snapshot,
        latest_days=args.latest_days,
        max_objects=args.max_objects,
        include_weak=args.include_weak,
        pin_day=args.day,
    )
    return code

if __name__ == "__main__":
    raise SystemExit(main())
