#!/usr/bin/env python3
"""Batch post-land hooks for one statecraft archive day (one process, one index refresh).

Replaces per-file shell loops of caption wrapper + family opening normalize + index refresh.

Usage:
    python3 scripts/post_land_statecraft_batch.py --day 2026-06-11 --sync-daily 2026-06-11
    python3 scripts/post_land_statecraft_batch.py --path source-archive/statecraft/2026-06-11/foo.md
    python3 scripts/post_land_statecraft_batch.py --day 2026-06-11 --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from post_land_statecraft_family import apply_statecraft_capture_scaffold  # noqa: E402
from statecraft_day_archive import DEFAULT_ROOT  # noqa: E402

def _landed_files_for_day(day: str) -> list[Path]:
    day_dir = DEFAULT_ROOT / day
    if not day_dir.is_dir():
        raise FileNotFoundError(f"day folder not found: {day_dir}")
    files = sorted(
        p
        for p in day_dir.glob("*.md")
        if p.is_file() and p.name.lower() != "readme.md"
    )
    if not files:
        raise FileNotFoundError(f"no capture files under {day_dir}")
    return files

def post_land_batch(
    paths: list[Path],
    *,
    dry_run: bool = False,
    sync_daily: str | None = None,
    skip_index: bool = False,
    force_mercouris_close: bool = False,
) -> int:
    exit_code = 0
    for path in paths:
        try:
            result = apply_statecraft_capture_scaffold(
                path,
                dry_run=dry_run,
                force_mercouris_close=force_mercouris_close,
            )
            for line in result.lines:
                print(line)
        except (FileNotFoundError, ValueError) as exc:
            print(exc, file=sys.stderr)
            exit_code = 1

    if sync_daily and not skip_index and not dry_run:
        import check_statecraft_intake_daily_sync as daily_sync
        import refresh_statecraft_archive_indices as refresh

        stale_count, _ = refresh.refresh_or_check(DEFAULT_ROOT, check=False)
        print(f"wrote {stale_count} archive navigation files under {DEFAULT_ROOT}")
        report = daily_sync.build_sync_report(sync_daily.strip())
        print(daily_sync.format_human(report))
        if report.exit_code != 0:
            exit_code = report.exit_code
    elif sync_daily and dry_run:
        print(f"dry-run: would refresh indices and --check-daily-sync {sync_daily}")

    return exit_code

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--day",
        metavar="YYYY-MM-DD",
        help="Run post-land hooks for all captures in source-archive/statecraft/<day>/",
    )
    parser.add_argument(
        "--path",
        type=Path,
        action="append",
        default=[],
        help="Single landed capture (repeatable). Ignored when --day is set.",
    )
    parser.add_argument(
        "--sync-daily",
        metavar="YYYY-MM-DD",
        help="After hooks, refresh archive indices once and verify daily sync for this pub_date.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--force-mercouris-close",
        action="store_true",
        help="Re-run Mercouris close trim even when mercouris_close_promo_trim_applied is set.",
    )
    parser.add_argument(
        "--skip-index",
        action="store_true",
        help="Normalize only; do not refresh archive indices (mid-batch throughput mode).",
    )
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    if not args.day and not args.path:
        print("error: specify --day or at least one --path", file=sys.stderr)
        return 2

    try:
        if args.day:
            paths = _landed_files_for_day(args.day.strip())
        else:
            paths = [(REPO_ROOT / p).resolve() if not p.is_absolute() else p.resolve() for p in args.path]
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    sync_daily = args.sync_daily or args.day
    if args.skip_index:
        sync_daily = None

    print(f"batch: {len(paths)} file(s)")
    return post_land_batch(
        paths,
        dry_run=args.dry_run,
        sync_daily=sync_daily,
        skip_index=args.skip_index,
        force_mercouris_close=args.force_mercouris_close,
    )

if __name__ == "__main__":
    raise SystemExit(main())
