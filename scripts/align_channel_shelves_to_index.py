#!/usr/bin/env python3
"""Align statecraft/channels/ folders to channel-index.json slugs (WORK only).

Renames legacy host folders (davis, napolitano, nima) to archive channel_slug names,
creates README + index stubs for missing roster channels, rewrites path strings.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHANNELS = REPO / "statecraft" / "channels"
INDEX_JSON = REPO / "statecraft" / "channels" / "channel-index.json"

RENAME_MAP = {
    "davis": "daniel-davis",
    "napolitano": "judging-freedom",
    "nima": "dialogue-works",
}

PATH_REPLACEMENTS = [
    ("statecraft/channels/davis/", "statecraft/channels/daniel-davis/"),
    ("statecraft/channels/napolitano/", "statecraft/channels/judging-freedom/"),
    ("statecraft/channels/nima/", "statecraft/channels/dialogue-works/"),
    ("../channels/davis/", "../channels/daniel-davis/"),
    ("../channels/napolitano/", "../channels/judging-freedom/"),
    ("../channels/nima/", "../channels/dialogue-works/"),
    ("(davis/README.md)", "(daniel-davis/README.md)"),
    ("(napolitano/README.md)", "(judging-freedom/README.md)"),
    ("(nima/README.md)", "(dialogue-works/README.md)"),
]

SKIP_DIRS = {".git", ".git-local", "node_modules", "__pycache__", "runtime/artifacts/speaker-routing"}
TEXT_SUFFIXES = {".md", ".mdc", ".py", ".yaml", ".yml", ".json", ".toml", ".txt"}

VOICE_PRIMARY = {
    "alexander-mercouris": ("mercouris", "Alexander Mercouris solo channel — whole-analyst SSOT lives under `statecraft/voices/mercouris/`."),
    "glenn-diesen": ("diesen", "Glenn Diesen channel — whole-analyst SSOT lives under `statecraft/voices/diesen/`."),
}


def load_channels() -> list[dict]:
    data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    return list(data["channels"])


def rename_folders() -> None:
    for old, new in RENAME_MAP.items():
        src = CHANNELS / old
        dst = CHANNELS / new
        if src.is_dir() and not dst.exists():
            src.rename(dst)
            print(f"renamed {old} -> {new}")


def stub_readme(slug: str, label: str, channel_url: str, file_count: int, watchlist: bool) -> str:
    voice_note = ""
    if slug in VOICE_PRIMARY:
        voice_slug, note = VOICE_PRIMARY[slug]
        voice_note = f"""
## Analyst shelf (primary)

Whole-analyst continuity: [`statecraft/voices/{voice_slug}/`](../../voices/{voice_slug}/README.md).

{note}
"""
    return f"""WORK only; not Record.

# {label}

Canonical live **channel shelf** for archive key **`{slug}`** (`channel_slug` in source captures).

- **Channel index roster:** [`channel-index.json`](../channel-index.json)
- **Archive captures:** `{file_count}` files · `source-{slug}-*` filename family
- **YouTube:** [{label}]({channel_url})
- **Watchlist:** {"yes" if watchlist else "no"}
{voice_note}
## Open first

- [index.md](index.md)

## Host role

Open this shelf when the job is **host-conditioned guest transformation** on **{label}** — how the show frames the guest — not whole-speaker identity (→ `statecraft/voices/<guest>/`) or verbatim capture (→ `source-archive/statecraft/`).

## Archive routing

- **YAML:** `channel_slug: {slug}`
- **Day inventory:** `source-archive/statecraft/YYYY-MM-DD/day-index.md`

## Boundary

Host-law and routing only. Guest mechanism depth lives on **`statecraft/voices/<guest>/`**, not here.
"""


def stub_index(slug: str, label: str) -> str:
    return f"""WORK only; not Record.

# {label} Index

Purpose: front door for **`{slug}`** on the statecraft channel shelf layer.

## Open first

- [README.md](README.md)

## Current live rule

Route here when capture frontmatter has **`channel_slug: {slug}`** (or equivalent show/host label in [channel-index.md](../channel-index.md)).

## Boundary

Index = routing + archive anchors. Promote guest arcs under `stream/` when repeated host×guest continuity justifies it.
"""


def create_stubs(roster: list[dict]) -> None:
    existing = {p.name for p in CHANNELS.iterdir() if p.is_dir()}
    for ch in roster:
        slug = ch["slug"]
        if slug in existing:
            continue
        folder = CHANNELS / slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "README.md").write_text(
            stub_readme(
                slug,
                ch["label"],
                ch["channel_url"],
                ch["file_count"],
                ch["watchlist"],
            ),
            encoding="utf-8",
            newline="\n",
        )
        (folder / "index.md").write_text(
            stub_index(slug, ch["label"]),
            encoding="utf-8",
            newline="\n",
        )
        print(f"created stub {slug}/")


def rewrite_paths() -> int:
    changed = 0
    for path in REPO.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO).as_posix()
        if any(rel.startswith(skip) for skip in SKIP_DIRS):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if rel == "scripts/align_channel_shelves_to_index.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = text
        for old, new_part in PATH_REPLACEMENTS:
            new = new.replace(old, new_part)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
    return changed


def patch_state_set() -> None:
    manifest = CHANNELS / "daniel-davis" / "state-set.toml"
    if not manifest.exists():
        return
    text = manifest.read_text(encoding="utf-8")
    text = text.replace('slug = "davis"', 'slug = "daniel-davis"')
    text = text.replace("statecraft/channels/davis/", "statecraft/channels/daniel-davis/")
    manifest.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    if not INDEX_JSON.is_file():
        print(f"missing {INDEX_JSON}", file=sys.stderr)
        return 1
    roster = load_channels()
    rename_folders()
    create_stubs(roster)
    patch_state_set()
    n = rewrite_paths()
    print(f"path_rewrite_files={n}")
    slugs = sorted(p.name for p in CHANNELS.iterdir() if p.is_dir())
    expected = sorted(ch["slug"] for ch in roster)
    missing = set(expected) - set(slugs)
    extra = set(slugs) - set(expected)
    if missing:
        print(f"MISSING folders: {sorted(missing)}", file=sys.stderr)
        return 1
    if extra:
        print(f"note: extra folders (not in main index): {sorted(extra)}")
    print(f"channels folders: {len(slugs)} (index main roster: {len(expected)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
