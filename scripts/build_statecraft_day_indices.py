#!/usr/bin/env python3
"""Build generated inventory-style README indices for statecraft day archives."""

from __future__ import annotations

import argparse
import errno
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


def write_day_index(day_dir: Path, *, check: bool = False) -> tuple[Path, bool]:
    out_path = day_dir / "README.md"
    rendered = build_day_readme(day_dir)
    existing = out_path.read_text(encoding="utf-8") if out_path.exists() else None
    changed = existing != rendered
    if changed and not check:
        try:
            out_path.write_text(rendered, encoding="utf-8", newline="\n")
        except PermissionError as exc:
            if exc.errno == errno.EACCES:
                raise PermissionError(
                    f"permission denied writing {out_path}; run with --check first to detect stale indices, "
                    "then rerun the specific --day or --year write in an unsandboxed shell"
                ) from exc
            raise
    return out_path, changed


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft source-archive root.")
    ap.add_argument("--year", type=str, default=DEFAULT_YEAR, help="Year prefix to index, default: 2026.")
    ap.add_argument("--day", type=str, default=None, help="Specific YYYY-MM-DD day to rebuild.")
    ap.add_argument(
        "--check",
        action="store_true",
        help="Read and compare generated day indices without writing them.",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if args.day:
        day_dir = root / args.day
        if not day_dir.is_dir():
            raise SystemExit(f"day directory not found: {day_dir}")
        out_path, changed = write_day_index(day_dir, check=args.check)
        if args.check:
            print(f"{'stale' if changed else 'ok'} {out_path}")
            return 1 if changed else 0
        print(f"{'wrote' if changed else 'unchanged'} {out_path}")
        return 0

    day_dirs = _iter_day_dirs(root, args.year)
    changed_paths: list[Path] = []
    for day_dir in day_dirs:
        out_path, changed = write_day_index(day_dir, check=args.check)
        if changed:
            changed_paths.append(out_path)
            if args.check:
                print(f"stale {out_path}")
    if args.check:
        if not changed_paths:
            print(f"ok 0 day indices under {root}")
            return 0
        print(f"stale {len(changed_paths)} day indices under {root}")
        return 1
    if not changed_paths:
        print(f"unchanged 0 day indices under {root}")
        return 0
    print(f"wrote {len(changed_paths)} day indices under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
