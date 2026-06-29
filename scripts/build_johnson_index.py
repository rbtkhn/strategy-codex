#!/usr/bin/env python3
"""Rebuild statecraft/voices/johnson/johnson-index.md from archive Johnson captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "johnson" / "johnson-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from statecraft_day_archive import parse_frontmatter, read_text  # noqa: E402


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
    if "mario-nawfal" in name or "nawfal" in name:
        return "Mario Nawfal"
    if "macgregor" in name:
        return "Macgregor"
    if "glenn-diesen" in name or "diesen-" in name:
        return "Diesen"
    if "daniel-davis" in name or "davis-" in name:
        title = (meta.get("title") or "").casefold()
        if "deep dive" in title or "deep-dive" in name:
            return "Davis Deep Dive"
        return "Davis"
    if name.startswith("source-johnson-"):
        if "lets-talk-geopolitics" in name:
            return "Geopolitics"
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
    for path in iter_archive_captures_for_shelf("johnson", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("johnson", path, meta, body):
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
        "Dense Hormuz / MOU / round-three week — one row per pub day; full archive list in **2026-06** above.",
        "",
        "| Pub date | Host | Type | Mechanism lane |",
        "|----------|------|------|----------------|",
        "| Jun 01 | Dialogue Works (Alkhorshid) | Solo w/ Wilkerson | Hormuz ticking time bomb; US-Iran threw down |",
        "| Jun 02 | Mario Nawfal | Breaking | Iran attacks Kuwait |",
        "| Jun 03 | Napolitano | Solo | Does Iran have the bomb (part 2) |",
        "| Jun 05 | Dialogue Works · Napolitano × McGovern | Solo + intel roundtable | Destroyers hit; US ships flee Indian Ocean; weekly wrap 5-June |",
        "| Jun 08 | Dialogue Works (Alkhorshid) | Solo | Missiles rain on northern Israel |",
        "| Jun 10 | Dialogue Works (Alkhorshid) | Breaking | American attack on Iran has begun |",
        "| Jun 11 | Davis · Dialogue Works | Deep dive + solo | Trump wants blown negotiations vs Iran forces concession |",
        "| Jun 12 | Dialogue Works · Diesen · Napolitano × McGovern | Solo + guest + roundtable | US-guided ships; US-Iran close to deal; weekly wrap 12-June |",
        "| Jun 14 | Dialogue Works w/ Marandi | Solo | US-Iran deal — full details |",
        "| Jun 15 | Dialogue Works · Napolitano | Solo ×2 | Israel sabotage backfires; is this any way to negotiate |",
        "| Jun 16 | Dialogue Works (Alkhorshid) | Breaking | $150B Iran / $300B reparations spent |",
        "| Jun 17 | Dialogue Works ×2 w/ Marandi | Dual same-day | White House 14-point MOU; surrender-document framing |",
        "| Jun 18 | Dialogue Works ×2 | Dual same-day | Iran cancels talks / Israel bombs Lebanon; Vance slams Netanyahu |",
        "| Jun 19 | Dialogue Works w/ Marandi · Napolitano × McGovern | Solo + roundtable | Geneva talks shut; MOU week; weekly wrap 19-June — [archive](../../../source-archive/statecraft/2026-06-19/source-judging-freedom-johnson-mcgovern-intel-roundtable-weekly-wrap-19-june-2026-06-19.md) |",
        "| Jun 20 | Dialogue Works (Alkhorshid) | Solo | Hormuz closed; Israel combat ops end; US rushes talks |",
        "| Jun 22 | Napolitano · Neutrality Studies | Solo + interview | Hormuz control lane; negotiation disaster / Russia full war mode |",
        "| Jun 24 | Davis · Dialogue Works | Deep dive + solo | Trump making up Iran deal; Yemen prep / Hormuz stack — [Davis](../../../source-archive/statecraft/2026-06-24/source-daniel-davis-larry-johnson-iran-deal-trump-making-it-up-2026-06-24.md) · [Dialogue Works](../../../source-archive/statecraft/2026-06-24/source-dialogue-works-johnson-israel-next-war-preparing-bomb-yemen-2026-06-24.md) |",
        "| Jun 25 | Dialogue Works (Alkhorshid) | Solo | US calling Iran direct; Vance Switzerland bombshell |",
        "| Jun 26 | Napolitano × McGovern | Intel roundtable | Weekly wrap 26-June |",
        "| Jun 27 | Dialogue Works · Diesen | Solo + guest | Sirik bombs / Tehran counterstrike; Putin warns West |",
        "| Jun 28 | Dialogue Works (Alkhorshid) | Breaking | Explosions Bahrain / Kuwait / Kiev |",
        "",
        "May Nawfal Hormuz lane closes [2026-05-31](../../../source-archive/statecraft/2026-05-31/source-mario-nawfal-larry-johnson-israel-asks-trump-to-escalate-2026-05-31.md); next Davis Deep Dive after Jun 24 is none on disk in June.",
        "",
    ]


def render_index(rows: list[tuple[str, Path, dict]], annotations: dict[str, str]) -> str:
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in rows:
        pub = row[0]
        month = pub[:7] if len(pub) >= 7 else pub
        by_month[month].append(row)

    lines = [
        "# Johnson source index",
        "",
        "WORK only; not Record.",
        "",
        "Purpose: exhaustive canonical route map for Larry C. Johnson guest appearances and direct archive anchors on the Johnson shelf.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index johnson` — author/guest parity; skill **`audit index`**. Post-land: `python scripts/shelf_index_from_capture.py --path <capture> --apply`. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "Backward extension context (2025 roots, atlas-prep): [johnson-backward-extension-note.md](johnson-backward-extension-note.md).",
        "",
        f"## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk",
        "- Rebuild: `python scripts/build_johnson_index.py`",
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
            "- host-local arcs still own chronology",
            "- this file is the canonical source-index and therefore the ordinary source bench, not a month atlas",
            "- shorthand and generic captures remain valid raw-input surfaces but do not replace canonical month shelves or the dense-core thread atlas",
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
