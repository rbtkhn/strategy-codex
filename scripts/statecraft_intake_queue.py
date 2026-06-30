#!/usr/bin/env python3
"""Report and optionally emit statecraft intake queue sidecars for one archive day.

Read-only by default. Sidecar and digest writes require explicit flags.

Usage:
    python3 scripts/statecraft_intake_queue.py --day 2026-06-14
    python3 scripts/statecraft_intake_queue.py --latest
    python3 scripts/statecraft_intake_queue.py --day 2026-06-14 --json
    python3 scripts/statecraft_intake_queue.py --day 2026-06-14 --emit-sidecars
    python3 scripts/statecraft_intake_queue.py --day 2026-06-14 --write-digest
    python3 scripts/statecraft_intake_queue.py --day 2026-06-14 --write-digest \\
        --digest-out runtime/artifacts/statecraft-intake-queue/digest-2026-06-14.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from repo_io import ARTIFACTS_DIR

from check_statecraft_intake_daily_sync import (  # noqa: E402
    build_sync_report,
    resolve_latest_captured_day,
)
from statecraft_day_archive import (  # noqa: E402
    DEFAULT_ROOT,
    as_values,
    iter_source_files,
    parse_frontmatter,
)

SCHEMA_VERSION = "statecraft-intake-sidecar.v1"
QUEUE_ROOT = ARTIFACTS_DIR / "statecraft-intake-queue"
SIDECAR_SUFFIX = ".v1.json"
WIRE_VERIFY_RE = re.compile(r"verify:wire-", re.IGNORECASE)
VALID_STATUSES = frozenset({"new", "queued", "daily", "discarded"})

@dataclass(frozen=True)
class SourceQueueRow:
    source_stem: str
    source_path: str
    synthesis_status: str
    threads: tuple[str, ...]
    actors: tuple[str, ...]
    source_url: str | None
    reasoning: str
    heuristic_score: int
    sidecar_path: str | None
    in_daily: bool

    @property
    def queue_eligible(self) -> bool:
        return self.synthesis_status in {"new", "queued"}

def sidecar_path_for(pub_date: str, source_stem: str) -> Path:
    return QUEUE_ROOT / pub_date / f"{source_stem}{SIDECAR_SUFFIX}"

def rel_repo_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()

def load_sidecar(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

def collect_actors(meta: dict[str, Any]) -> tuple[str, ...]:
    values: list[str] = []
    for key in ("host_people", "guest_people", "host", "guest"):
        for item in as_values(meta.get(key)):
            if item not in values:
                values.append(item)
    return tuple(values)

def collect_threads(meta: dict[str, Any]) -> tuple[str, ...]:
    values: list[str] = []
    for key in ("threads", "thread"):
        for item in as_values(meta.get(key)):
            if item not in values:
                values.append(item)
    return tuple(values)

def build_reasoning(meta: dict[str, Any], *, threads: tuple[str, ...]) -> str:
    parts: list[str] = []
    source_form = str(meta.get("source_form") or "").strip()
    if source_form:
        parts.append(f"source_form={source_form}")
    if threads:
        parts.append(f"threads={','.join(threads[:4])}")
    source_note = str(meta.get("source_note") or "")
    if WIRE_VERIFY_RE.search(source_note):
        parts.append("wire-verify tokens in source_note")
    if meta.get("thread_expert"):
        parts.append(f"thread_expert={meta.get('thread_expert')}")
    if not parts:
        parts.append("v0: archive frontmatter only; operator promotes manually")
    return "; ".join(parts)

def heuristic_score(meta: dict[str, Any], *, threads: tuple[str, ...]) -> int:
    score = 0
    source_form = str(meta.get("source_form") or "").casefold()
    if source_form == "interview":
        score += 2
    elif source_form == "solo":
        score += 1
    if meta.get("guest_people") or meta.get("guest"):
        score += 2
    if meta.get("thread_expert"):
        score += 2
    if len(threads) >= 2:
        score += 1
    source_note = str(meta.get("source_note") or "")
    if WIRE_VERIFY_RE.search(source_note):
        score += 3
    return score

def derive_status(
    *,
    in_daily: bool,
    sidecar: dict[str, Any] | None,
) -> str:
    if in_daily:
        return "daily"
    if sidecar:
        status = str(sidecar.get("synthesis_status") or "queued").strip()
        if status in VALID_STATUSES and status != "daily":
            return status
        return "queued"
    return "new"

def build_sidecar_payload(
    row: SourceQueueRow,
    *,
    pub_date: str,
    rated_at: str,
    synthesis_status: str,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "source_path": row.source_path,
        "pub_date": pub_date,
        "synthesis_status": synthesis_status,
        "rated_at": rated_at,
        "non_canonical": True,
        "source_url": row.source_url,
        "actors": list(row.actors),
        "regions": [],
        "mechanisms": [],
        "strategic_relevance": None,
        "confidence": None,
        "transaction_candidate": None,
        "reasoning": row.reasoning,
        "digest_rank": None,
    }

def build_queue_report(
    day: str,
    *,
    root: Path = DEFAULT_ROOT,
    daily_dir: Path | None = None,
    allow_desync: bool = False,
) -> tuple[list[SourceQueueRow], Any]:
    from check_statecraft_intake_daily_sync import DAILY_DIR, _parse_daily_source_slugs  # noqa: PLC0415

    effective_daily_dir = daily_dir if daily_dir is not None else DAILY_DIR
    day_dir = root / day
    if not day_dir.is_dir():
        raise FileNotFoundError(f"archive day not found: {day_dir}")

    sync = build_sync_report(day, root=root, daily_dir=effective_daily_dir)
    if sync.status == "desync" and not allow_desync:
        raise RuntimeError(f"archive/daily desync for {day}; use --allow-desync to report anyway")

    daily_slugs: set[str] = set()
    daily_path = effective_daily_dir / f"{day}.md"
    if daily_path.is_file():
        daily_text = daily_path.read_text(encoding="utf-8", errors="replace")
        daily_slugs = _parse_daily_source_slugs(daily_text, day)

    rows: list[SourceQueueRow] = []
    for path in iter_source_files(day_dir):
        meta = parse_frontmatter(path)
        stem = path.stem
        rel_path = rel_repo_path(path)
        in_daily = path.name in daily_slugs
        sc_path = sidecar_path_for(day, stem)
        sidecar = load_sidecar(sc_path)
        threads = collect_threads(meta)
        actors = collect_actors(meta)
        reasoning = build_reasoning(meta, threads=threads)
        score = heuristic_score(meta, threads=threads)
        status = derive_status(in_daily=in_daily, sidecar=sidecar)
        rows.append(
            SourceQueueRow(
                source_stem=stem,
                source_path=rel_path,
                synthesis_status=status,
                threads=threads,
                actors=actors,
                source_url=norm_optional_str(meta.get("source_url")),
                reasoning=reasoning,
                heuristic_score=score,
                sidecar_path=rel_repo_path(sc_path) if sc_path.is_file() else None,
                in_daily=in_daily,
            )
        )
    return rows, sync

def norm_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None

def emit_sidecars(day: str, rows: list[SourceQueueRow]) -> list[str]:
    written: list[str] = []
    rated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_dir = QUEUE_ROOT / day
    out_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        if row.synthesis_status == "daily":
            continue
        if row.synthesis_status == "discarded":
            continue
        target = sidecar_path_for(day, row.source_stem)
        if target.is_file():
            continue
        payload = build_sidecar_payload(row, pub_date=day, rated_at=rated_at, synthesis_status="queued")
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        written.append(rel_repo_path(target))
    return written

def format_digest(day: str, rows: list[SourceQueueRow], *, top_n: int = 5) -> str:
    eligible = [r for r in rows if r.queue_eligible]
    eligible.sort(key=lambda r: (-r.heuristic_score, r.source_stem))
    top = eligible[:top_n]

    lines = [
        f"# Statecraft Intake Digest — {day}",
        "",
        "Precursor to daily synthesis — not a substitute.",
        "",
        "Spec: [statecraft-intake-queue.md](../../docs/statecraft-intake-queue.md)",
        "",
        "## Top signals (queue)",
        "",
        "| Rank | Source | Status | Threads | Why it matters |",
        "| ---: | --- | --- | --- | --- |",
    ]
    if not top:
        lines.append("| — | _(none)_ | — | — | All sources in daily or discarded |")
    else:
        for idx, row in enumerate(top, start=1):
            thread_cell = ", ".join(row.threads[:3]) if row.threads else "—"
            short_stem = row.source_stem.replace(f"-{day}", "")
            if len(short_stem) > 48:
                short_stem = short_stem[:45] + "..."
            lines.append(
                f"| {idx} | `{short_stem}` | {row.synthesis_status} | {thread_cell} | {row.reasoning} |"
            )

    promote = [r for r in rows if r.synthesis_status == "queued"]
    hold = [r for r in rows if r.synthesis_status == "new"]
    discard = [r for r in rows if r.synthesis_status == "discarded"]

    lines.extend(["", "## Promote to daily synthesis", ""])
    if promote:
        for row in promote:
            lines.append(f"- [{row.source_stem}]({row.source_path}) — {row.reasoning}")
    else:
        lines.append("- _(none queued)_")

    lines.extend(["", "## Hold / watch", ""])
    if hold:
        for row in hold:
            lines.append(f"- [{row.source_stem}]({row.source_path}) — awaiting sidecar or operator review")
    else:
        lines.append("- _(none)_")

    lines.extend(["", "## Discard / low signal", ""])
    if discard:
        for row in discard:
            lines.append(f"- [{row.source_stem}]({row.source_path})")
    else:
        lines.append("- _(none)_")

    lines.extend(
        [
            "",
            "## Already in daily",
            "",
        ]
    )
    daily_rows = [r for r in rows if r.synthesis_status == "daily"]
    if daily_rows:
        for row in daily_rows:
            lines.append(f"- [{row.source_stem}]({row.source_path})")
    else:
        lines.append("- _(none)_")

    return "\n".join(lines) + "\n"

def format_human(day: str, rows: list[SourceQueueRow], sync: Any) -> str:
    counts = {status: 0 for status in sorted(VALID_STATUSES)}
    for row in rows:
        counts[row.synthesis_status] = counts.get(row.synthesis_status, 0) + 1

    lines = [
        f"statecraft intake queue — {day}",
        f"sync: {sync.status} · archive_count: {sync.archive_count}",
        f"new: {counts.get('new', 0)} · queued: {counts.get('queued', 0)} · "
        f"daily: {counts.get('daily', 0)} · discarded: {counts.get('discarded', 0)}",
        "",
        "stem                                          status    score  in_daily",
        "--------------------------------------------  --------  -----  --------",
    ]
    for row in rows:
        stem = row.source_stem
        if len(stem) > 44:
            stem = stem[:41] + "..."
        lines.append(
            f"{stem:<44}  {row.synthesis_status:8}  {row.heuristic_score:5}  "
            f"{'yes' if row.in_daily else 'no'}"
        )

    queue_rows = [r for r in rows if r.queue_eligible]
    if queue_rows:
        lines.extend(["", "queue detail (new + queued):"])
        for row in queue_rows:
            lines.append(f"- {row.source_stem}: {row.reasoning}")

    lines.extend(
        [
            "",
            "commands: --emit-sidecars · --write-digest · "
            "docs/statecraft-intake-queue.md",
        ]
    )
    return "\n".join(lines)

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    day_group = ap.add_mutually_exclusive_group(required=True)
    day_group.add_argument("--day", help="Publication date YYYY-MM-DD")
    day_group.add_argument(
        "--latest",
        action="store_true",
        help="Use the newest archive day folder with at least one source file",
    )
    ap.add_argument("--json", action="store_true", help="Emit JSON report")
    ap.add_argument(
        "--allow-desync",
        action="store_true",
        help="Report even when archive/daily lists desync",
    )
    ap.add_argument(
        "--emit-sidecars",
        action="store_true",
        help="Write sidecar JSON for new sources (skip daily/discarded)",
    )
    ap.add_argument(
        "--write-digest",
        action="store_true",
        help="Emit intake digest markdown",
    )
    ap.add_argument(
        "--digest-out",
        type=Path,
        help="Write digest to this path (implies --write-digest)",
    )
    ap.add_argument(
        "--top",
        type=int,
        default=5,
        help="Top N rows in digest table (default 5)",
    )
    return ap.parse_args()

def resolve_day(args: argparse.Namespace) -> str:
    if args.day:
        return args.day
    latest = resolve_latest_captured_day()
    if not latest:
        raise SystemExit("no captured archive days found")
    return latest

def main() -> int:
    args = parse_args()
    if args.digest_out:
        args.write_digest = True

    day = resolve_day(args)
    try:
        rows, sync = build_queue_report(day, allow_desync=args.allow_desync)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    written: list[str] = []
    if args.emit_sidecars:
        written = emit_sidecars(day, rows)

    if args.json:
        payload = {
            "day": day,
            "sync_status": sync.status,
            "archive_count": sync.archive_count,
            "rows": [asdict(row) for row in rows],
            "sidecars_written": written,
        }
        print(json.dumps(payload, indent=2))
    elif not args.write_digest:
        print(format_human(day, rows, sync))
        if written:
            print("")
            print(f"sidecars_written: {len(written)}")
            for path in written:
                print(f"  {path}")

    if args.write_digest:
        digest = format_digest(day, rows, top_n=args.top)
        if args.digest_out:
            out = args.digest_out
            if not out.is_absolute():
                out = REPO_ROOT / out
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(digest, encoding="utf-8")
            if not args.json:
                print(f"digest_written: {rel_repo_path(out)}")
        else:
            if not args.json:
                if written:
                    print("")
                print(digest.rstrip())

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
