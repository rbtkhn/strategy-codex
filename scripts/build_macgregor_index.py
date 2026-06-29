#!/usr/bin/env python3
"""Rebuild statecraft/voices/macgregor/macgregor-index.md from archive Macgregor captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "macgregor" / "macgregor-index.md"
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
    if n.startswith("source-daniel-davis-"):
        rest = stem[len("source-daniel-davis-") :]
        if "col-doug" in n or "col-douglas" in n:
            return f"youtube-daniel-davis-deep-dive-{rest}"
        if rest.startswith("macgregor-"):
            return f"transcript-davis-{rest}"
        if rest.startswith("douglas-macgregor-"):
            return f"transcript-davis-{rest}"
        return f"transcript-davis-macgregor-{rest}"
    if n.startswith("source-glenn-diesen-"):
        return "youtube-" + stem[len("source-") :]
    if n.startswith("source-macgregor-cyrus-janssen-"):
        return "youtube-macgregor-cyrus-janssen-" + stem[len("source-macgregor-cyrus-janssen-") :]
    if n.startswith("source-mario-nawfal-macgregor-"):
        return "youtube-macgregor-mario-nawfal-" + stem[len("source-mario-nawfal-macgregor-") :]
    if n.startswith("source-macgregor-mario-nawfal-"):
        return "youtube-macgregor-mario-nawfal-" + stem[len("source-macgregor-mario-nawfal-") :]
    if n.startswith("source-redacted-"):
        return "transcript-redacted-" + stem[len("source-redacted-") :]
    if n.startswith("source-tucker-"):
        return "transcript-tucker-" + stem[len("source-tucker-") :]
    if n.startswith("source-diesen-"):
        return "transcript-diesen-" + stem[len("source-diesen-") :]
    if n.startswith("source-macgregor-"):
        return "transcript-macgregor-" + stem[len("source-macgregor-") :]
    if n.startswith("source-johnson-"):
        return "transcript-johnson-" + stem[len("source-johnson-") :]
    if n.startswith("source-neutrality-studies-"):
        return "transcript-neutrality-studies-" + stem[len("source-neutrality-studies-") :]
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
    for path in iter_archive_captures_for_shelf("macgregor", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("macgregor", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows


def render_boundary() -> list[str]:
    return [
        "## Boundary Notes",
        "",
        "- Macgregor is a dense cross-host expert whose chronology is still primarily host-owned, so this index is intentionally broader than any single shelf.",
        "- The main canonical host transformations are Davis, Diesen, and Napolitano, with the durable `Diesen + Davis` pair carrying the main helix.",
        "- The shorthand day files remain listed because they are distinct raw-input surfaces on disk, even when a fuller host capture exists nearby.",
        "- The shorthand day files are support-tier provenance surfaces, not preferred citation anchors when a fuller transcript-bearing file exists for the same nearby Macgregor lane.",
        "- The aired-pending surface is included because it is a real on-disk Macgregor routing surface, but it should not be treated as fully settled chronology without a later materialization pass.",
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
        "# Macgregor Source Index",
        "",
        "WORK only; not Record.",
        "",
        "Purpose: exhaustive route map for every resolved Macgregor appearance currently materialized in Statecraft Archive, including host transcripts, shorthand day files, and aired-pending surfaces.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index macgregor` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk ({date_span} + aired-pending)",
        "- Rebuild: `python scripts/build_macgregor_index.py`",
        "- Month-grouped exhaustive list; host arcs (Davis, Diesen, Napolitano) own first-open transformations",
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
