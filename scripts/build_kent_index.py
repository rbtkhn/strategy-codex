#!/usr/bin/env python3
"""Rebuild statecraft/voices/kent/kent-index.md from archive Kent captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "kent" / "kent-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from statecraft_day_archive import read_text  # noqa: E402

LINK_SUFFIX_RE = re.compile(
    r"\]\((?:\.\./\.\./\.\./source-archive/statecraft/\d{4}-\d{2}-\d{2}/([^)]+))\)(.*)$"
)
LABEL_RE = re.compile(
    r"- \[([^\]]+)\]\([^)]*/([^/)]+)\)"
)

SUPPORT_TIER_FNS = frozenset(
    {
        "source-glenn-diesen-daniel-davis-military-options-kent-2026-03-18.md",
        "source-barnes-kent-exit-ramp-qt-2026-04-21.md",
    }
)

DEFAULT_SUPPORT_ANNOTATIONS: dict[str, str] = {
    "source-glenn-diesen-daniel-davis-military-options-kent-2026-03-18.md": (
        "— **support-tier:** Davis × Diesen on Kent resignation / war narrative; Kent not on mic"
    ),
    "source-barnes-kent-exit-ramp-qt-2026-04-21.md": (
        "— **support-tier:** Barnes X-post QT of Kent; primary route [Barnes index](../barnes/barnes-index.md)"
    ),
}

def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:5000]
    out: dict = {}
    for key in (
        "title",
        "pub_date",
        "date",
        "kind",
        "source_form",
        "host",
        "show",
        "channel_slug",
        "thread",
    ):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    if not out.get("title"):
        hm = re.search(r"^#\s+(.+)$", text, re.M)
        if hm:
            out["title"] = hm.group(1).strip()
    return out

def pub_date_key(meta: dict, path: Path) -> str:
    pub = meta.get("pub_date") or meta.get("date") or ""
    if pub and len(pub) >= 10:
        return pub[:10]
    day = path.parent.name
    if re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        return day
    return day

def default_label(meta: dict, path: Path) -> str:
    pub = pub_date_key(meta, path)
    name = path.name.casefold()
    if "diesen-daniel-davis-military-options-kent" in name:
        return f"transcript-diesen-davis-military-options-kent-{pub}"
    if "barnes-kent-exit-ramp" in name:
        return f"transcript-barnes-kent-exit-ramp-qt-{pub}"
    if "daniel-davis-kent-hormuz" in name:
        return f"transcript-davis-kent-hormuz-blockade-walkaway-{pub}"
    if "nawfal-kent-trumps-life" in name:
        return f"transcript-nawfal-kent-trumps-life-is-under-threat-{pub}"
    if "judging-freedom-kent" in name:
        tail = path.stem.removeprefix("source-judging-freedom-kent-")
        return f"youtube-napolitano-kent-{tail}"
    if "dialogue-works-kent" in name:
        tail = path.stem.removeprefix("source-dialogue-works-kent-")
        return f"youtube-alkorshid-kent-{tail}"
    if "redacted-kent" in name:
        tail = path.stem.removeprefix("source-redacted-kent-")
        return f"youtube-redacted-kent-{tail}"
    if "mario-nawfal-kent-" in name:
        tail = path.stem.removeprefix("source-mario-nawfal-kent-")
        return f"youtube-nawfal-kent-{tail}"
    if "tucker-carlson" in name and "kent" in name:
        tail = path.stem.removeprefix("source-tucker-carlson-")
        return f"youtube-tucker-carlson-{tail}"
    if "glenn-diesen-joe-kent" in name:
        tail = path.stem.removeprefix("source-glenn-diesen-")
        return f"youtube-{tail}"
    if "daniel-davis" in name and "kent" in name:
        stem = path.stem.removeprefix("source-daniel-davis-")
        if stem.startswith("joe-kent-"):
            return f"youtube-daniel-davis-deep-dive-joe-kent-{stem.removeprefix('joe-kent-')}"
        if "latest-goals" in stem:
            return (
                "youtube-daniel-davis-deep-dive-latest-goals-in-iran-war-"
                "lt-col-daniel-davis-joe-kent-2026-04-02"
            )
        if "controlled-by-the-donor" in stem:
            return (
                "youtube-daniel-davis-deep-dive-controlled-by-the-donor-class-"
                "us-iran-negotiations-joe-kent-lt-col-danie-2026-05-08"
            )
        return f"youtube-daniel-davis-deep-dive-{stem}"
    if "mario-nawfal" in name and "kent" in name:
        tail = path.stem.removeprefix("source-mario-nawfal-")
        return f"youtube-mario-nawfal-{tail}"
    return path.stem.removeprefix("source-")

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

def row_suffix(path: Path, annotations: dict[str, str]) -> str:
    if path.name in annotations:
        return annotations[path.name]
    return DEFAULT_SUPPORT_ANNOTATIONS.get(path.name, "")

def row_label(meta: dict, path: Path, labels: dict[str, str], annotations: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    line = f"- [{text}]({rel})"
    suffix = row_suffix(path, annotations)
    if suffix:
        line += f" {suffix}"
    return line

def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("kent", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("kent", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows

def month_heading(month: str) -> str:
    return f"## {month}"

def render_curated_overlays() -> list[str]:
    return [
        "## Host routing",
        "",
        "| Host | Index |",
        "| --- | --- |",
        "| Tucker Carlson | [carlson-kent-speaker-arc.md](carlson-kent-speaker-arc.md) · [tucker-carlson channel](../../channels/tucker-carlson/tucker-carlson-channel-index.md) |",
        "| Daniel Davis | [kent-routing.md](kent-routing.md) · [daniel-davis channel](../../channels/daniel-davis/daniel-davis-channel-index.md) |",
        "| Glenn Diesen | [glenn-diesen channel](../../channels/glenn-diesen/glenn-diesen-channel-index.md) |",
        "| Mario Nawfal | [nawfal-kent-speaker-arc.md](nawfal-kent-speaker-arc.md) · [mario-nawfal channel](../../channels/mario-nawfal/mario-nawfal-channel-index.md) |",
        "| Dialogue Works / Alkorshid | [dialogue-works channel](../../channels/dialogue-works/dialogue-works-channel-index.md) |",
        "| Judging Freedom / Napolitano | [judging-freedom channel](../../channels/judging-freedom/judging-freedom-channel-index.md) |",
        "| Redacted | [redacted-news channel](../../channels/redacted-news/redacted-news-channel-index.md) |",
        "",
        "## Boundary notes",
        "",
        "- The March through May 2026 cluster is the strongest current Kent entry point — see [kent-march-may-2026-cluster-note.md](kent-march-may-2026-cluster-note.md).",
        "- Tucker Carlson, Daniel Davis, Glenn Diesen, Mario Nawfal, Napolitano, Nima Alkhorshid, and Redacted are the main current host lanes on disk.",
        "- This index is a starter provenance bench, not evidence that the shelf already owns a full speaker chronology.",
        "- Support-tier rows (Davis×Diesen “about Kent,” Barnes QT) are listed for audit parity — not guest appearances.",
        "- Object / helix routing: [kent-speaker-object.md](kent-speaker-object.md) · [kent-helix.md](kent-helix.md)",
        "",
    ]

def render_index(
    rows: list[tuple[str, Path, dict]],
    labels: dict[str, str],
    annotations: dict[str, str],
) -> str:
    date_span = f"{rows[0][0]} → {rows[-1][0]}" if rows else "—"
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in rows:
        pub = row[0]
        month = pub[:7] if len(pub) >= 7 else pub
        by_month[month].append(row)

    support_n = sum(1 for r in rows if r[1].name in SUPPORT_TIER_FNS)

    lines = [
        "# Kent Source Index",
        "",
                "",
        "Purpose: provide the current canonical route map for materialized Joe Kent appearances on disk.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index kent` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk ({date_span}), including **{support_n}** support-tier parity rows (about-Kent panel + Barnes QT)",
        "- Rebuild: `python scripts/build_kent_index.py`",
        "",
    ]

    for month in sorted(by_month, reverse=True):
        lines.append(month_heading(month))
        lines.append("")
        for _pub, path, meta in sorted(by_month[month], key=lambda t: (t[0], t[1].name)):
            lines.append(row_label(meta, path, labels, annotations))
        lines.append("")

    lines.extend(render_curated_overlays())
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
        print(f"annotations preserved: {len(annotations)}")
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(rows)} rows, {len(labels)} labels preserved)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
