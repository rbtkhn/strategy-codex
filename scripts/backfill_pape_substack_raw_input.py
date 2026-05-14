#!/usr/bin/env python3
"""Backfill Pape Escalation Trap Substack into strategy-notebook raw-input/.

Thin wrapper around ``backfill_substack_raw_input.py`` with Pape defaults.
Use targeted ``--url`` / ``--slug`` captures by default. The public archive
contains substantive essays, event notifications, livestream links, and
interview pointers; it is not a raw-input backlog.
WORK only; not Record.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from backfill_substack_raw_input import DEFAULT_RAW_ROOT, run

DEFAULT_HOSTNAME = "escalationtrap.substack.com"
DEFAULT_THREAD = "pape"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hostname", default=DEFAULT_HOSTNAME)
    ap.add_argument("--year", type=int, default=2026)
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest_date in frontmatter")
    ap.add_argument("--thread", type=str, default=DEFAULT_THREAD)
    ap.add_argument("--slug", action="append", default=[], help="Target one Escalation Trap post slug; repeatable")
    ap.add_argument("--url", action="append", default=[], help="Target one Escalation Trap /p/<slug> URL; repeatable")
    ap.add_argument(
        "--archive-scan",
        action="store_true",
        help="Explicitly scan the archive; Pape archive posts are not all raw-input candidates",
    )
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=30)
    args = ap.parse_args()

    if not args.slug and not args.url and not args.archive_scan:
        print(
            "Refusing broad Pape archive scan by default. "
            "Use --url/--slug for a specific substantive post, or add "
            "--archive-scan for intentional discovery. Notifications, livestream "
            "links, and interview pointers are not raw-input backlog.",
            file=sys.stderr,
        )
        return 2

    ingest = (
        datetime.strptime(args.ingest_date, "%Y-%m-%d").date()
        if args.ingest_date
        else date.today()
    )

    return run(
        hostname=args.hostname,
        year=args.year,
        raw_root=args.root,
        ingest_date=ingest,
        thread=args.thread,
        apply=args.apply,
        limit=max(1, min(args.limit, 50)),
        slugs=args.slug,
        urls=args.url,
        publication_slug=args.thread,
    )


if __name__ == "__main__":
    raise SystemExit(main())
