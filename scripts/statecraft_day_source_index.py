#!/usr/bin/env python3
"""Print the canonical statecraft archive day source-index (ingest register).

One bounded path — no repo scan:
  source-archive/statecraft/YYYY-MM-DD/README.md

Optional intake queue report for the same day (read-only).

Usage:
    python scripts/statecraft_day_source_index.py --day 2026-06-17
    python scripts/statecraft_day_source_index.py --latest
    python scripts/statecraft_day_source_index.py --day 2026-06-17 --queue
    python scripts/statecraft_day_source_index.py --day 2026-06-17 --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from statecraft_day_archive import DEFAULT_ROOT  # noqa: E402

DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def day_readme_path(day: str, root: Path = DEFAULT_ROOT) -> Path:
    if not DAY_RE.match(day):
        raise ValueError(f"invalid day (expected YYYY-MM-DD): {day}")
    return root / day / "README.md"


def resolve_day(args: argparse.Namespace) -> str:
    if args.day:
        return args.day.strip()
    from check_statecraft_intake_daily_sync import resolve_latest_captured_day  # noqa: PLC0415

    latest = resolve_latest_captured_day(root=args.root)
    if not latest:
        raise SystemExit("no captured archive days found")
    return latest


def load_day_index(day: str, *, root: Path = DEFAULT_ROOT) -> tuple[Path, str]:
    path = day_readme_path(day, root)
    if not path.is_file():
        raise FileNotFoundError(
            f"day source-index not found: {path.relative_to(REPO_ROOT).as_posix()} "
            f"(rebuild: python scripts/build_statecraft_day_indices.py --day {day})"
        )
    return path, path.read_text(encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day", help="Archive day YYYY-MM-DD.")
    parser.add_argument("--latest", action="store_true", help="Use latest captured archive day.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft archive root.")
    parser.add_argument("--queue", action="store_true", help="Append intake queue report.")
    parser.add_argument("--json", action="store_true", help="Emit JSON (readme path + body; optional queue).")
    parser.add_argument(
        "--allow-desync",
        action="store_true",
        help="Include queue report even when archive/daily desync.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.latest and args.day:
        print("error: use --day or --latest, not both", file=sys.stderr)
        return 1
    if not args.day and not args.latest:
        print("error: supply --day YYYY-MM-DD or --latest", file=sys.stderr)
        return 1

    try:
        day = resolve_day(args)
        readme_path, readme_text = load_day_index(day, root=args.root)
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    queue_human: str | None = None
    queue_payload: dict | None = None
    if args.queue:
        try:
            from statecraft_intake_queue import (  # noqa: PLC0415
                build_queue_report,
                format_human,
            )
            from dataclasses import asdict

            rows, sync = build_queue_report(day, root=args.root, allow_desync=args.allow_desync)
            queue_human = format_human(day, rows, sync)
            queue_payload = {
                "sync_status": sync.status,
                "archive_count": sync.archive_count,
                "rows": [asdict(row) for row in rows],
            }
        except (FileNotFoundError, RuntimeError) as exc:
            print(f"queue report skipped: {exc}", file=sys.stderr)

    rel = readme_path.relative_to(REPO_ROOT).as_posix()
    if args.json:
        payload = {
            "day": day,
            "readme_path": rel,
            "readme_markdown": readme_text,
        }
        if queue_payload:
            payload["queue"] = queue_payload
        print(json.dumps(payload, indent=2))
        return 0

    print(f"statecraft day source-index — {day}")
    print(f"path: {rel}")
    print("")
    print(readme_text.rstrip())
    if queue_human:
        print("")
        print(queue_human.rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
