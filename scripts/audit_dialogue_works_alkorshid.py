#!/usr/bin/env python3
"""Audit Dialogue Works / Alkorshid / Nima archive routing."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from statecraft_day_archive import parse_frontmatter, read_text  # noqa: E402

ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"
AUDIT_DIR = REPO_ROOT / "statecraft" / "audits"

PREFIXES = (
    "source-alkorshid-",
    "source-nima-alkorshid-",
    "source-dialogue-works-",
)

DIALOGUE_WORKS_SLUGS = frozenset({"dialogue-works", "dialogueworks"})
DANIEL_DAVIS_SLUGS = frozenset({"daniel-davis", "deep-dive", "deepdive"})
NAWFAL_SLUGS = frozenset({"nawfal", "mario-nawfal"})

# Known Daniel Davis YouTube channel id (from mis-filed 2026-05-29 capture).
DANIEL_DAVIS_CHANNEL_IDS = frozenset({"UCkF-6h_Zgf9zXNUmUB-MzTw"})

NIMA_GUEST_OPENING_RES = [
    re.compile(r"thank you for inviting me,?\s+carl\b", re.I),
    re.compile(r"back with the show.*nima\s+alk", re.I),
    re.compile(r"from dialogue works.*thank you for inviting me", re.I | re.S),
]

NIMA_HOST_OPENING_RES = [
    re.compile(r"^Hi everybody", re.I | re.M),
    re.compile(r"our dear friend.*(?:is here|welcome back)", re.I),
    re.compile(r"thank you very much for inviting me.*your show", re.I),
]

DAVIS_HOST_OPENING_RES = [
    re.compile(r"thank you for inviting me,?\s+carl", re.I),
    re.compile(r"pardon me.*nima.*from dialogue works", re.I),
]


@dataclass
class AuditRow:
    path: str
    youtube_id: str
    channel_slug: str
    channel_url: str
    host: str
    guest: str
    threads: str
    class_: str
    dedup_action: str
    notes: str
    target_prefix: str = ""


def threads_str(meta: dict[str, Any]) -> str:
    raw = meta.get("threads")
    if isinstance(raw, (list, tuple)):
        return "|".join(str(v) for v in raw)
    if raw:
        return str(raw)
    thread = meta.get("thread")
    return str(thread or "")


def slug_from_url(url: str) -> str:
    url_l = url.lower()
    if "dialogueworks" in url_l or "/@dialogueworks" in url_l:
        return "dialogue-works"
    if "danieldavis" in url_l or "deepdive" in url_l:
        return "daniel-davis"
    if "nawfal" in url_l:
        return "nawfal"
    for ch_id in DANIEL_DAVIS_CHANNEL_IDS:
        if ch_id.lower() in url_l:
            return "daniel-davis"
    return ""


def opening_role(body: str) -> str:
    """Return nima-host | nima-guest | unknown."""
    sample = body[:12000]
    guest_hits = sum(1 for p in NIMA_GUEST_OPENING_RES if p.search(sample))
    host_hits = sum(1 for p in NIMA_HOST_OPENING_RES if p.search(sample))
    davis_host = any(p.search(sample) for p in DAVIS_HOST_OPENING_RES)
    if davis_host and not re.search(r"^Hi everybody", sample[:800], re.I | re.M):
        return "nima-guest"
    if guest_hits and guest_hits >= host_hits:
        return "nima-guest"
    if host_hits:
        return "nima-host"
    return "unknown"


def infer_effective_channel(meta: dict[str, Any], path: Path, body: str) -> str:
    slug = str(meta.get("channel_slug") or "").strip().lower()
    url = str(meta.get("channel_url") or meta.get("source_url") or "")
    url_slug = slug_from_url(url)
    if slug in DANIEL_DAVIS_SLUGS or url_slug == "daniel-davis":
        return "daniel-davis"
    if slug in NAWFAL_SLUGS or url_slug == "nawfal":
        return "nawfal"
    if slug in DIALOGUE_WORKS_SLUGS or url_slug == "dialogue-works":
        return "dialogue-works"
    name = path.name.lower()
    if name.startswith("source-dialogue-works-"):
        return "dialogue-works"
    if name.startswith("source-alkorshid-") or name.startswith("source-nima-alkorshid-"):
        show = str(meta.get("show") or meta.get("show_title") or "").lower()
        if "dialogue works" in show:
            return "dialogue-works"
    return slug or "unknown"


def is_solo(meta: dict[str, Any]) -> bool:
    form = str(meta.get("source_form") or "").lower()
    if form == "solo":
        return True
    guest = meta.get("guest") or meta.get("guest_people")
    if guest in (None, "", "[]", []):
        return True
    return False


def yaml_inverted(meta: dict[str, Any], effective_channel: str, open_role: str) -> bool:
    host = str(meta.get("host") or "").lower()
    yaml_nima_host = "nima" in host or "alkhorshid" in host or "alkorshid" in host
    if effective_channel == "daniel-davis" and open_role == "nima-guest" and yaml_nima_host:
        return True
    if effective_channel == "nawfal" and open_role == "nima-guest" and yaml_nima_host:
        return True
    if effective_channel == "dialogue-works" and open_role == "nima-guest" and yaml_nima_host:
        return True
    if effective_channel == "dialogue-works" and open_role == "nima-host" and not yaml_nima_host:
        return True
    return False


def classify(meta: dict[str, Any], path: Path, body: str) -> tuple[str, str, str]:
    """Return (class, notes, target_prefix)."""
    effective = infer_effective_channel(meta, path, body)
    open_role = opening_role(body)
    solo = is_solo(meta)
    name = path.name.lower()
    inverted = yaml_inverted(meta, effective, open_role)
    notes: list[str] = []
    if inverted:
        notes.append("inverted-yaml")
    if open_role != "unknown":
        notes.append(f"opening:{open_role}")

    if effective == "daniel-davis" and open_role in ("nima-guest", "unknown"):
        return "davis-guest", "; ".join(notes), "source-daniel-davis-alkorshid"
    if effective == "nawfal" and open_role in ("nima-guest", "unknown"):
        return "nawfal-guest", "; ".join(notes), "source-nawfal-alkorshid"
    if effective == "dialogue-works":
        if solo:
            return "dw-solo", "; ".join(notes), "source-dialogue-works"
        if open_role == "nima-guest":
            return "inverted-yaml", "; ".join(notes + ["dw-channel-but-nima-guest"]), "source-daniel-davis-alkorshid"
        return "dw-host", "; ".join(notes), "source-dialogue-works"
    if name.startswith("source-alkorshid-") or name.startswith("source-nima-alkorshid-"):
        return "other-host-guest", "; ".join(notes + [f"effective:{effective}"]), "source-dialogue-works"
    if name.startswith("source-dialogue-works-"):
        if inverted:
            return "inverted-yaml", "; ".join(notes), "source-daniel-davis-alkorshid"
        return "dw-host" if not solo else "dw-solo", "; ".join(notes), "source-dialogue-works"
    return "other-host-guest", "; ".join(notes), ""


def needs_rename(path: Path, target_prefix: str) -> bool:
    if not target_prefix:
        return False
    name = path.name.lower()
    if target_prefix == "source-dialogue-works":
        if name.startswith("source-dialogue-works-"):
            return False
        return name.startswith("source-alkorshid-") or name.startswith("source-nima-alkorshid-")
    return not name.startswith(target_prefix + "-")


def audit_file(path: Path) -> AuditRow | None:
    meta = parse_frontmatter(path)
    if not meta:
        return None
    body = read_text(path)
    fm_end = body.find("\n---", 4)
    transcript = body[fm_end + 4 :] if fm_end > 0 else body
    class_, notes, target_prefix = classify(meta, path, transcript)
    rel = path.relative_to(REPO_ROOT).as_posix()
    return AuditRow(
        path=rel,
        youtube_id=str(meta.get("youtube_id") or ""),
        channel_slug=str(meta.get("channel_slug") or ""),
        channel_url=str(meta.get("channel_url") or ""),
        host=str(meta.get("host") or ""),
        guest=str(meta.get("guest") or ""),
        threads=threads_str(meta),
        class_=class_,
        dedup_action="keep",
        notes=notes,
        target_prefix=target_prefix,
    )


def assign_dedup(rows: list[AuditRow]) -> None:
    by_yt: dict[str, list[AuditRow]] = defaultdict(list)
    for row in rows:
        if row.youtube_id:
            by_yt[row.youtube_id].append(row)
    for yt, group in by_yt.items():
        if len(group) < 2:
            continue
        group.sort(key=lambda r: (len(r.path), r.path))
        keeper = max(group, key=lambda r: r.path.count("/") + len(r.path))
        for row in group:
            if row is keeper:
                row.dedup_action = "keep"
            else:
                row.dedup_action = f"merge-into:{keeper.path}"
                row.notes = (row.notes + f"; duplicate-yt:{yt}").strip("; ")


def iter_capture_paths(root: Path) -> list[Path]:
    out: list[Path] = []
    for prefix in PREFIXES:
        out.extend(sorted(root.rglob(f"{prefix}*.md")))
    return out


def write_csv(path: Path, rows: list[AuditRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "path",
                "youtube_id",
                "channel_slug",
                "channel_url",
                "host",
                "guest",
                "threads",
                "class",
                "dedup_action",
                "target_prefix",
                "needs_rename",
                "notes",
            ]
        )
        for row in rows:
            p = REPO_ROOT / row.path
            writer.writerow(
                [
                    row.path,
                    row.youtube_id,
                    row.channel_slug,
                    row.channel_url,
                    row.host,
                    row.guest,
                    row.threads,
                    row.class_,
                    row.dedup_action,
                    row.target_prefix,
                    needs_rename(p, row.target_prefix),
                    row.notes,
                ]
            )


def write_summary(path: Path, rows: list[AuditRow], audit_date: str) -> None:
    counts = Counter(r.class_ for r in rows)
    rename_count = sum(
        1 for r in rows if needs_rename(REPO_ROOT / r.path, r.target_prefix)
    )
    inverted = [r for r in rows if "inverted-yaml" in r.notes or r.class_ == "inverted-yaml"]
    lines = [
        f"# Dialogue Works / Alkorshid audit — {audit_date}",
        "",
        f"Total captures scanned: **{len(rows)}**",
        "",
        "## Class counts",
        "",
        "| class | count |",
        "|-------|------:|",
    ]
    for cls, n in sorted(counts.items()):
        lines.append(f"| `{cls}` | {n} |")
    lines.extend(
        [
            "",
            f"**Needs rename:** {rename_count}",
            f"**Inverted YAML / opening:** {len(inverted)}",
            "",
            "## Flagged inversions",
            "",
        ]
    )
    for row in inverted:
        lines.append(f"- `{row.path}` — {row.notes}")
    if not inverted:
        lines.append("- _(none)_")
    lines.extend(
        [
            "",
            "## Dedup groups",
            "",
        ]
    )
    dup_rows = [r for r in rows if r.dedup_action.startswith("merge-into:")]
    if dup_rows:
        for row in dup_rows:
            lines.append(f"- `{row.path}` → {row.dedup_action}")
    else:
        lines.append("- _(no youtube_id duplicates)_")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Audit date stamp for output filenames",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ARCHIVE_ROOT,
        help="Statecraft archive root",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write CSV and summary under statecraft/audits/",
    )
    args = parser.parse_args()

    paths = iter_capture_paths(args.root)
    rows: list[AuditRow] = []
    for path in paths:
        row = audit_file(path)
        if row:
            rows.append(row)
    assign_dedup(rows)
    rows.sort(key=lambda r: r.path)

    if args.write:
        csv_path = AUDIT_DIR / f"dialogue-works-alkorshid-audit-{args.date}.csv"
        md_path = AUDIT_DIR / f"dialogue-works-alkorshid-audit-{args.date}.md"
        write_csv(csv_path, rows)
        write_summary(md_path, rows, args.date)
        print(f"Wrote {csv_path.relative_to(REPO_ROOT)}")
        print(f"Wrote {md_path.relative_to(REPO_ROOT)}")

    counts = Counter(r.class_ for r in rows)
    rename_count = sum(
        1 for r in rows if needs_rename(REPO_ROOT / r.path, r.target_prefix)
    )
    print(f"Scanned {len(rows)} files; rename candidates: {rename_count}")
    for cls, n in sorted(counts.items()):
        print(f"  {cls}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
