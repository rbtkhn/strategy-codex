#!/usr/bin/env python3
"""Rebuild statecraft/voices/weichert/weichert-index.md from archive Weichert captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "weichert" / "weichert-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from statecraft_day_archive import read_text  # noqa: E402

LINK_SUFFIX_RE = re.compile(
    r"\]\((?:\.\./\.\./\.\./source-archive/statecraft/\d{4}-\d{2}-\d{2}/([^)]+))\)(.*)$"
)

def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:5000]
    out: dict = {}
    for key in ("title", "pub_date", "kind", "source_form", "host", "show", "channel_slug", "thread"):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    if not out.get("title"):
        hm = re.search(r"^#\s+(.+)$", text, re.M)
        if hm:
            out["title"] = hm.group(1).strip()
    return out

def pub_date_key(meta: dict, path: Path) -> str:
    pub = meta.get("pub_date", "")
    if pub and len(pub) >= 10:
        return pub[:10]
    day = path.parent.name
    if re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        return day
    return day

def host_short(meta: dict, path: Path) -> str:
    name = path.name.casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if "mario-nawfal" in name or "nawfal" in name:
        if name.endswith(".cleaned.md"):
            return "Mario Nawfal (cleaned)"
        return "Mario Nawfal"
    if "breaking-points" in name or slug == "breaking-points":
        return "Breaking Points"
    if "redacted" in name:
        return "Redacted"
    if "tucker-carlson" in name or "tucker" in name:
        return "Tucker Carlson"
    if meta.get("show"):
        return meta["show"]
    if meta.get("host"):
        return meta["host"]
    return "Other"

def row_label(meta: dict, path: Path) -> str:
    pub = pub_date_key(meta, path)
    host = host_short(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    return f"- [{pub} {host}]({rel})"

def load_annotation_map(index_path: Path) -> dict[str, str]:
    if not index_path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in read_text(index_path).splitlines():
        m = LINK_SUFFIX_RE.search(line)
        if not m:
            continue
        suffix = m.group(2).strip()
        if not suffix.startswith("—"):
            continue
        fn = m.group(1)
        if len(suffix) > len(out.get(fn, "")):
            out[fn] = suffix
    return out

def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("weichert", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("weichert", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows

def render_adjacent_notes() -> list[str]:
    return [
        "## Adjacent notes (not source floor)",
        "",
        "- [weichert-on-ai.md](../../notes/weichert-on-ai.md)",
        "- [trend-china-ai-implementation.md](../../notes/trend-china-ai-implementation.md)",
        "- [Speaker profile](weichert-profile.md) · routing: [weichert-routing.md](weichert-routing.md) · compat: [weichert-source-index.md](weichert-source-index.md)",
        "",
        "Seed shelf — Nawfal lane is primary; Breaking Points / Redacted / Tucker captures are listed for audit parity. Arc, helix, and month ladders remain Phase 2+.",
        "",
    ]

def render_index(rows: list[tuple[str, Path, dict]], annotations: dict[str, str]) -> str:
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in rows:
        pub = row[0]
        month = pub[:7] if len(pub) >= 7 else pub
        by_month[month].append(row)

    lines = [
        "# Weichert source index",
        "",
                "",
        "Purpose: exhaustive canonical route map for Brandon Weichert guest appearances and direct archive anchors on the Weichert shelf.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index weichert` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk",
        "- Rebuild: `python scripts/build_weichert_index.py`",
        "- Primary lane: **Mario Nawfal × Weichert**; other hosts listed for full archive parity",
        "",
    ]

    for month in sorted(by_month):
        lines.append(f"## {month}")
        lines.append("")
        for _pub, path, meta in by_month[month]:
            line = row_label(meta, path)
            ann = annotations.get(path.name)
            if ann:
                line += f" {ann}"
            lines.append(line)
        lines.append("")

    lines.extend(render_adjacent_notes())
    lines.extend(
        [
            "## Boundary Notes",
            "",
            "- this file is the canonical source-index and ordinary source bench for Weichert retrieval",
            "- AI architecture prose stays in weichert-on-ai.md — not duplicated here",
            "- open source-bearing files before quoting or making claim-grade factual use",
            "",
        ]
    )
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print row count only")
    parser.add_argument("--check", action="store_true", help="Compare row count to index links")
    args = parser.parse_args()

    rows = collect_rows()
    if args.dry_run:
        print(f"rows: {len(rows)}")
        return 0

    annotations = load_annotation_map(OUT)
    body = render_index(rows, annotations)
    if args.check:
        print(f"rows: {len(rows)}")
        print(f"annotations preserved: {len(annotations)}")
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(rows)} rows, {len(annotations)} annotations preserved)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
