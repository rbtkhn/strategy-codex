#!/usr/bin/env python3
"""Build generated day-index inventory notes for statecraft day archives."""

from __future__ import annotations

import argparse
import errno
import re
from pathlib import Path

from statecraft_day_archive import (  # noqa: F401 re-exported for tests/importers
    DAY_INDEX_FILENAME,
    DEFAULT_ROOT,
    DEFAULT_YEAR,
    ArchiveFile,
    DaySummary,
    as_values,
    build_day_index,
    build_day_readme,
    build_day_readme_stub,
    classify_day_captures,
    collect_archive_file,
    counter_to_list,
    fmt_counter as _fmt_counter,
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

MONTH_RE = re.compile(r"^\d{4}-\d{2}$")

def _write_text(path: Path, rendered: str, *, check: bool) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    changed = existing != rendered
    if changed and not check:
        try:
            path.write_text(rendered, encoding="utf-8", newline="\n")
        except PermissionError as exc:
            if exc.errno == errno.EACCES:
                raise PermissionError(
                    f"permission denied writing {path}; run with --check first to detect stale indices, "
                    "then rerun the specific --day or --month write in an unsandboxed shell"
                ) from exc
            raise
    return changed

def write_day_index(day_dir: Path, *, check: bool = False) -> tuple[Path, bool]:
    index_path = day_dir / DAY_INDEX_FILENAME
    readme_path = day_dir / "README.md"
    index_changed = _write_text(index_path, build_day_index(day_dir), check=check)
    stub_changed = _write_text(readme_path, build_day_readme_stub(day_dir), check=check)
    return index_path, index_changed or stub_changed

def iter_day_dirs_for_scope(root: Path, *, year: str, month: str | None) -> list[Path]:
    day_dirs = _iter_day_dirs(root, year)
    if not month:
        return day_dirs
    if not MONTH_RE.match(month):
        raise ValueError(f"invalid month (expected YYYY-MM): {month}")
    return [path for path in day_dirs if path.name.startswith(f"{month}-")]

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft source-archive root.")
    ap.add_argument("--year", type=str, default=DEFAULT_YEAR, help="Year prefix to index, default: 2026.")
    ap.add_argument("--month", type=str, default=None, help="Optional YYYY-MM month filter.")
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

    year = args.month[:4] if args.month else args.year
    day_dirs = iter_day_dirs_for_scope(root, year=year, month=args.month)
    changed_paths: list[Path] = []
    for day_dir in day_dirs:
        out_path, changed = write_day_index(day_dir, check=args.check)
        if changed:
            changed_paths.append(out_path)
            if args.check:
                print(f"stale {out_path}")
    if args.check:
        if not changed_paths:
            scope = args.month or args.year
            print(f"ok 0 day indices under {root} ({scope})")
            return 0
        print(f"stale {len(changed_paths)} day indices under {root}")
        return 1
    if not changed_paths:
        scope = args.month or args.year
        print(f"unchanged 0 day indices under {root} ({scope})")
        return 0
    print(f"wrote {len(changed_paths)} day indices under {root}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
