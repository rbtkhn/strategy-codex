#!/usr/bin/env python3
"""Build generated inventory-style README indices for statecraft day archives."""

from __future__ import annotations

import argparse
from pathlib import Path

from statecraft_day_archive import (  # noqa: F401 re-exported for tests/importers
    DEFAULT_ROOT,
    DEFAULT_YEAR,
    KNOWN_FAMILY_PREFIXES,
    ArchiveFile,
    DaySummary,
    as_values,
    build_day_readme,
    collect_archive_file,
    counter_to_list,
    fallback_counter as _fallback_counter,
    fmt_counter as _fmt_counter,
    infer_family_label,
    iter_day_dirs as _iter_day_dirs,
    normalize_channel_label,
    normalize_person_label,
    parse_day_readme,
    parse_frontmatter as _parse_frontmatter,
    parse_scalar as _parse_scalar,
    parse_simple_frontmatter_block as _parse_simple_frontmatter_block,
    rollup_values as _rollup_values,
    summarize_day_dir,
)


def write_day_index(day_dir: Path) -> Path:
    out_path = day_dir / "README.md"
    out_path.write_text(build_day_readme(day_dir), encoding="utf-8", newline="\n")
    return out_path


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft source-archive root.")
    ap.add_argument("--year", type=str, default=DEFAULT_YEAR, help="Year prefix to index, default: 2026.")
    ap.add_argument("--day", type=str, default=None, help="Specific YYYY-MM-DD day to rebuild.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if args.day:
        day_dir = root / args.day
        if not day_dir.is_dir():
            raise SystemExit(f"day directory not found: {day_dir}")
        write_day_index(day_dir)
        print(f"wrote {day_dir / 'README.md'}")
        return 0

    day_dirs = _iter_day_dirs(root, args.year)
    for day_dir in day_dirs:
        write_day_index(day_dir)
    print(f"wrote {len(day_dirs)} day indices under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
