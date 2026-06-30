#!/usr/bin/env python3
"""Generate statecraft/channels/<slug>/<slug>-index.md from archive captures."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHANNELS = REPO / "statecraft" / "channels"
ARCHIVE = REPO / "source-archive" / "statecraft"
INDEX_JSON = CHANNELS / "channel-index.json"

sys.path.insert(0, str(REPO / "scripts"))
from build_statecraft_archive_navigation import (  # noqa: E402
    _channel_registry_key,
    canonical_channel_index_slug,
    iter_all_day_dirs,
)
from statecraft_day_archive import is_youtube_capture, iter_source_files, norm_scalar, parse_frontmatter  # noqa: E402
from statecraft_youtube_discovery import load_index_slug_canonical  # noqa: E402

VOICE_PRIMARY = {
    "alexander-mercouris": ("mercouris", "Alexander Mercouris"),
    "glenn-diesen": ("diesen", "Glenn Diesen"),
}

TITLE_TRUNC = 80
FILENAME_LINK_THRESHOLD = 50

def load_roster() -> dict[str, dict]:
    data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    return {ch["slug"]: ch for ch in data["channels"]}

def title_from_meta(path: Path) -> str:
    text = path.read_text(encoding="utf-8")[:1200]
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.M)
    if m:
        t = m.group(1).strip()
        return t[:TITLE_TRUNC] + ("…" if len(t) > TITLE_TRUNC else "")
    return path.stem

def rel_link(day: str, name: str) -> str:
    return f"../../../source-archive/statecraft/{day}/{name}"

def collect_by_slug(root: Path) -> dict[str, list[tuple[str, str, str]]]:
    canonical_map = load_index_slug_canonical()
    grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for day_dir in iter_all_day_dirs(root):
        day = day_dir.name
        for path in iter_source_files(day_dir):
            meta = parse_frontmatter(path)
            if not is_youtube_capture(meta):
                continue
            slug, _label, _explicit = _channel_registry_key(meta, path.name)
            index_slug = canonical_channel_index_slug(slug, canonical_map)
            if index_slug == "unknown":
                continue
            grouped[index_slug].append((day, path.name, title_from_meta(path)))
    for slug in grouped:
        grouped[slug].sort(key=lambda row: (row[0], row[1]))
    return grouped

def month_key(day: str) -> str:
    return day[:7]

def build_index_body(slug: str, ch: dict, rows: list[tuple[str, str, str]]) -> str:
    label = ch["label"]
    url = ch.get("channel_url", "")
    voice_block = ""
    if slug in VOICE_PRIMARY:
        voice_slug, voice_label = VOICE_PRIMARY[slug]
        voice_block = f"""
## Analyst shelf (primary)

Whole-analyst continuity: [`statecraft/voices/{voice_slug}/`](../../voices/{voice_slug}/README.md) · [`{voice_slug}-source-index.md`](../../voices/{voice_slug}/{voice_slug}-source-index.md).

This channel index lists **host-channel captures** (`channel_slug: {slug}`). Mechanism depth for {voice_label} solo work lives on the voice shelf.
"""

    use_filename = len(rows) > FILENAME_LINK_THRESHOLD
    by_month: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for row in rows:
        by_month[month_key(row[0])].append(row)

    lines = [
                "",
        f"# {label} Index",
        "",
        f"Purpose: route map for materialized **{label}** captures on disk (`channel_slug: {slug}`).",
        "",
    ]
    if url:
        lines.append(f"Channel: [{label}]({url})")
        lines.append("")
    if voice_block:
        lines.extend(voice_block.strip().splitlines())
        lines.append("")

    for month in sorted(by_month):
        lines.append(f"## {month}")
        lines.append("")
        for day, name, title in by_month[month]:
            href = rel_link(day, name)
            if use_filename:
                lines.append(f"- [{name}]({href})")
            else:
                lines.append(f"- [{day} — {title}]({href})")
        lines.append("")

    lines.extend(
        [
            "## Reading rule",
            "",
            "- use this index for **host-channel** routing — guest mechanism depth lives on **`statecraft/voices/<guest>/`** when applicable",
            "- same guest on another host = separate host read — do not dedupe by guest alone",
            "",
        ]
    )
    return "\n".join(lines)

def patch_open_first(path: Path, slug: str, label: str) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    link = f"[{slug}-index.md]({slug}-index.md)"
    if link in text:
        return False
    needle = "## Open first\n\n"
    if needle not in text:
        needle = "## Open First\n\n"
    if needle not in text:
        return False
    insert = needle + f"- {link}\n"
    if "## Open first" in text:
        insert = insert.replace("Open First", "Open first")
    new = text.replace(needle, insert, 1)
    if new == text:
        return False
    path.write_text(new, encoding="utf-8", newline="\n")
    return True

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", action="append", help="Only these channel slugs (repeatable)")
    parser.add_argument("--skip-existing", action="store_true", help="Skip if {slug}-index.md exists")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    roster = load_roster()
    grouped = collect_by_slug(ARCHIVE)
    targets = sorted(args.slug) if args.slug else sorted(roster)
    written = 0
    for slug in targets:
        if slug not in roster:
            print(f"skip unknown slug: {slug}", file=sys.stderr)
            continue
        out = CHANNELS / slug / f"{slug}-index.md"
        if args.skip_existing and out.is_file():
            print(f"skip existing {out.relative_to(REPO)}")
            continue
        rows = grouped.get(slug, [])
        body = build_index_body(slug, roster[slug], rows)
        if args.dry_run:
            print(f"would write {out.relative_to(REPO)} ({len(rows)} captures)")
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(body, encoding="utf-8", newline="\n")
        patch_open_first(CHANNELS / slug / "index.md", slug, roster[slug]["label"])
        patch_open_first(CHANNELS / slug / "README.md", slug, roster[slug]["label"])
        print(f"wrote {out.relative_to(REPO)} ({len(rows)} captures)")
        written += 1
    print(f"done written={written}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
