#!/usr/bin/env python3
"""Rebuild statecraft/voices/hoh/hoh-index.md from archive Hoh captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "hoh" / "hoh-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from statecraft_day_archive import read_text  # noqa: E402

LINK_SUFFIX_RE = re.compile(
    r"\]\((?:\.\./\.\./\.\./source-archive/statecraft/(?:\d{4}-\d{2}-\d{2}|_aired-pending)/([^)]+))\)(.*)$"
)
LABEL_RE = re.compile(
    r"- \[([^\]]+)\]\([^)]*/([^/)]+)\)"
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

def is_aired_pending(path: Path) -> bool:
    return path.parent.name == "_aired-pending"

def archive_rel_link(path: Path) -> str:
    if is_aired_pending(path):
        return f"../../../source-archive/statecraft/_aired-pending/{path.name}"
    return f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"

def slug_label(path: Path) -> str:
    stem = path.name.removesuffix(".md")
    if not stem.startswith("source-"):
        return stem
    n = stem.casefold()
    if n.startswith("source-judging-freedom-"):
        return "transcript-napolitano-" + stem[len("source-judging-freedom-") :]
    if n.startswith("source-hoh-dialogue-works-"):
        return "youtube-hoh-dialogue-works-" + stem[len("source-hoh-dialogue-works-") :]
    if n.startswith("source-dialogue-works-matthew-hoh-"):
        return "youtube-dialogue-works-matthew-hoh-" + stem[len("source-dialogue-works-matthew-hoh-") :]
    if n.startswith("source-daniel-davis-"):
        rest = stem[len("source-daniel-davis-") :]
        return f"youtube-daniel-davis-deep-dive-{rest}"
    return stem.removeprefix("source-")

def load_label_map(index_path: Path) -> dict[str, str]:
    if not index_path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in read_text(index_path).splitlines():
        m = LABEL_RE.search(line)
        if not m:
            continue
        fn = m.group(2)
        if len(m.group(1)) > len(out.get(fn, "")):
            out[fn] = m.group(1)
    return out

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

def row_label(path: Path, labels: dict[str, str]) -> str:
    text = labels.get(path.name) or slug_label(path)
    rel = archive_rel_link(path)
    return f"- [{text}]({rel})"

def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("hoh", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("hoh", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows

def render_boundary() -> list[str]:
    return [
        "## Boundary notes",
        "",
        "- The May–June 2026 cluster is the strongest current Hoh entry point.",
        "- Dialogue Works and Judging Freedom are currently the main Iran-facing lanes on disk.",
        "- Daniel Davis Deep Dive guest appearances carry crossover Ukraine/Iran lanes.",
        "- Host arcs (Napolitano, Dialogue Works, Davis) own first-open transformations; this index lists every eligible archive capture for parity.",
        "",
    ]

def render_index(
    rows: list[tuple[str, Path, dict]],
    labels: dict[str, str],
    annotations: dict[str, str],
) -> str:
    dated = [r for r in rows if not is_aired_pending(r[1])]
    pending = [r for r in rows if is_aired_pending(r[1])]
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in dated:
        pub = row[0]
        month = pub[:7] if len(pub) >= 7 else pub
        by_month[month].append(row)

    date_span = f"{dated[0][0]} → {dated[-1][0]}" if dated else "—"

    lines = [
        "# Hoh Source Index",
        "",
                "",
        "Purpose: exhaustive route map for every resolved Matthew Hoh appearance currently materialized in Statecraft Archive.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index hoh` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk ({date_span})",
        "- Rebuild: `python scripts/build_hoh_index.py`",
        "- Month-grouped exhaustive list; Napolitano / Dialogue Works / Davis guest lanes own first-open label transforms",
        "",
    ]

    for month in sorted(by_month):
        lines.append(f"## {month}")
        lines.append("")
        for _pub, path, _meta in by_month[month]:
            line = row_label(path, labels)
            ann = annotations.get(path.name)
            if ann:
                line += f" {ann}"
            lines.append(line)
        lines.append("")

    if pending:
        lines.append("## Aired Pending")
        lines.append("")
        for _pub, path, _meta in pending:
            line = row_label(path, labels)
            ann = annotations.get(path.name)
            if ann:
                line += f" {ann}"
            lines.append(line)
        lines.append("")

    lines.extend(render_boundary())
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

    labels = load_label_map(OUT)
    annotations = load_annotation_map(OUT)
    body = render_index(rows, labels, annotations)
    if args.check:
        print(f"rows: {len(rows)}")
        print(f"labels preserved: {len(labels)}")
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(rows)} rows, {len(labels)} labels preserved)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
