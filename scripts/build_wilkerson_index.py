#!/usr/bin/env python3
"""Rebuild statecraft/voices/wilkerson/wilkerson-index.md from archive Wilkerson captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "wilkerson" / "wilkerson-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from statecraft_day_archive import read_text  # noqa: E402


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
    host = (meta.get("host") or "").casefold()
    show = (meta.get("show") or "").casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if "dialogue-works" in name or slug == "dialogue-works":
        return "Dialogue Works"
    if "judging-freedom" in name or slug == "judging-freedom":
        return "Napolitano"
    if "neutrality-studies" in name:
        return "Neutrality Studies"
    if "glenn-diesen" in name or "diesen-" in name:
        return "Diesen"
    if name.startswith("source-wilkerson-"):
        return "Napolitano"
    if "napolitano" in host or "judging freedom" in show:
        return "Napolitano"
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
        m = re.search(
            r"\]\((?:\.\./\.\./\.\./source-archive/statecraft/\d{4}-\d{2}-\d{2}/([^)]+))\)(.*)$",
            line,
        )
        if not m:
            continue
        suffix = m.group(2).strip()
        if suffix.startswith("—"):
            out[m.group(1)] = suffix
    return out


def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("wilkerson", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("wilkerson", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows


def render_june_cadence_table() -> list[str]:
    """Curated routing overlay — not part of archive parity rows."""
    return [
        "## June 2026 cadence (landed)",
        "",
        "Hormuz / destroyer / Israel-strategy collapse week — one row per pub day; full archive list in **2026-06** above.",
        "",
        "| Pub date | Host | Type | Mechanism lane |",
        "|----------|------|------|----------------|",
        "| Jun 02 | Dialogue Works · Mario Nawfal | Solo + breaking | Quds Force chief / Red Sea chokepoint; Pakistan offered Iran nukes |",
        "| Jun 05 | Dialogue Works w/ Johnson | Solo | Destroyers hit; US ships flee Indian Ocean |",
        "| Jun 08 | Diesen | Guest | Israel bet everything on war; Iran won lane |",
        "| Jun 09 | Dialogue Works (Alkhorshid) | Solo | Israel grand strategy coming apart |",
        "| Jun 11 | Napolitano | Solo | Israel collapsing strategy |",
        "| Jun 12 | Dialogue Works w/ Johnson | Solo | US-guided ships; Trump final decision — [archive](../../../source-archive/statecraft/2026-06-12/source-dialogue-works-johnson-wilkerson-iran-fired-us-guided-ships-trump-final-decision-2026-06-12.md) |",
        "",
        "May lane closes [2026-05-28](../../../source-archive/statecraft/2026-05-28/source-judging-freedom-wilkerson-what-remains-of-international-law-2026-05-28.md) (international law); no Wilkerson on disk after Jun 12 in June.",
        "",
    ]


def render_index(rows: list[tuple[str, Path, dict]], annotations: dict[str, str]) -> str:
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in rows:
        pub = row[0]
        month = pub[:7] if len(pub) >= 7 else pub
        by_month[month].append(row)

    lines = [
        "# Wilkerson source index",
        "",
        "WORK only; not Record.",
        "",
        "Purpose: exhaustive canonical route map for Lawrence Wilkerson guest appearances and direct archive anchors on the Wilkerson shelf.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index wilkerson` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "Host-arc routing (transformations): [wilkerson-routing.md](wilkerson-routing.md) · [Diesen × Wilkerson](../../notes/arc-wilkerson-diesen-host.md) · [Dialogue Works × Wilkerson](../../notes/arc-wilkerson-nima-host.md) · [Napolitano × Wilkerson](../../notes/arc-wilkerson-napolitano-host.md).",
        "",
        "Compat alias: [wilkerson-source-index.md](wilkerson-source-index.md) redirects here.",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk",
        "- Rebuild: `python scripts/build_wilkerson_index.py`",
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

    lines.extend(render_june_cadence_table())
    lines.extend(
        [
            "## Boundary Notes",
            "",
            "- host-local arcs still own chronology and first-open transformations",
            "- this file is the canonical source-index and therefore the ordinary source bench, not a month atlas",
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
    print(f"wrote {OUT} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
