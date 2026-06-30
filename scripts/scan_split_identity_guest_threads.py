#!/usr/bin/env python3
"""Scan split-identity guest voice indexes for cross-thread parity gaps."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_statecraft_archive_index as audit  # noqa: E402
import shelf_index_utils as s  # noqa: E402
from build_alkhorshid_guest_index import parse_head as parse_alk  # noqa: E402
from build_davis_guest_index import parse_head as parse_davis  # noqa: E402
from build_diesen_guest_index import parse_head as parse_diesen  # noqa: E402

from build_mercouris_guest_index import parse_head as parse_merc  # noqa: E402

ARCH = REPO / "source-archive" / "statecraft"

SLUGS: dict[str, tuple] = {
    "alkhorshid": (s.is_alkhorshid_guest_index_capture, parse_alk),
    "davis": (s.is_davis_guest_index_capture, parse_davis),
    "diesen": (s.is_diesen_guest_index_capture, parse_diesen),
    "mercouris": (s.is_mercouris_guest_index_capture, parse_merc),
}

def rel(p: Path) -> str:
    return p.relative_to(REPO).as_posix()

def main() -> int:
    rc = 0
    for slug, (is_guest, parse_head) in SLUGS.items():
        index = REPO / "statecraft" / "voices" / slug / f"{slug}-index.md"
        text = index.read_text(encoding="utf-8")
        guest_caps: list[Path] = []
        cross_thread: list[tuple[Path, dict]] = []
        for path in sorted(ARCH.glob("**/source-*.md")):
            meta = parse_head(path)
            if not is_guest(meta, path):
                continue
            guest_caps.append(path)
            thread = (meta.get("thread") or "").strip().casefold()
            if (
                thread
                and thread != slug
                and slug not in path.name.casefold()
                and not s.slug_token_in_capture_filename(slug, path.name)
            ):
                cross_thread.append((path, meta))

        eligible = [
            p
            for p in audit.iter_archive_captures_for_shelf(slug, ARCH)
            if not s.shelf_capture_excluded(
                slug, p, audit.parse_frontmatter(p), audit.read_text(p)[:8000]
            )
        ]
        index_count = sum(1 for _t, _r, dest in audit.parse_shelf_index_links(index) if dest)
        missing = [p for p in guest_caps if p.name not in text and rel(p) not in text]

        print(f"=== {slug} ===")
        print(
            f"guest captures: {len(guest_caps)} | eligible: {len(eligible)} | "
            f"index links: {index_count}"
        )
        print(f"cross-thread (no filename token): {len(cross_thread)}")
        for path, meta in cross_thread:
            print(f"  {rel(path)}")
            print(
                f"    thread={meta.get('thread')!r} guest={meta.get('guest')!r} "
                f"host={meta.get('host')!r} channel={meta.get('channel_slug')!r}"
            )
        if missing:
            rc = 1
            print(f"MISSING from index: {len(missing)}")
            for path in missing:
                print(f"  {rel(path)}")
        elif len(guest_caps) == len(eligible) == index_count:
            print("parity: guest == eligible == index")
        else:
            rc = 1
            print(
                f"parity mismatch: guest={len(guest_caps)} eligible={len(eligible)} "
                f"index={index_count}"
            )
        print()
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
