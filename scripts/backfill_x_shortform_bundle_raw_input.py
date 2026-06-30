#!/usr/bin/env python3
"""Backfill X short-form bundles into strategy-notebook raw-input/.

Thin wrapper around ``backfill_shortform_bundle_raw_input.py`` with X defaults.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from backfill_shortform_bundle_raw_input import DEFAULT_RAW_ROOT, run

def _default_profile_url(account: str) -> str:
    handle = account.strip().lstrip("@")
    return f"https://x.com/{handle}"

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--account", required=True, help="X account / source author label, e.g. @handle")
    ap.add_argument("--profile-url", default=None, help="X profile URL (defaults to https://x.com/<account>)")
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest date in frontmatter")
    ap.add_argument("--pub-date", type=str, required=True, help="YYYY-MM-DD source publication date")
    ap.add_argument("--thread", type=str, default=None)
    ap.add_argument("--title", type=str, default=None)
    ap.add_argument("--body-file", type=Path, required=True, help="OCR / short-form bundle body markdown")
    ap.add_argument(
        "--screenshot",
        action="append",
        default=[],
        help="screenshot path or URL; repeat for multiple screenshots",
    )
    ap.add_argument("--output", type=Path, default=None)
    ap.add_argument("--source-url", default=None, help="bundle source URL (defaults to profile URL)")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    ingest = (
        datetime.strptime(args.ingest_date, "%Y-%m-%d").date()
        if args.ingest_date
        else date.today()
    )
    profile_url = args.profile_url or _default_profile_url(args.account)

    dest = run(
        raw_root=args.root,
        ingest_date=ingest,
        pub_date=datetime.strptime(args.pub_date, "%Y-%m-%d").date(),
        source_platform="x",
        account_author=args.account,
        source_url_profile=profile_url,
        source_url=args.source_url,
        thread=args.thread,
        title=args.title,
        body_file=args.body_file,
        screenshot_refs=args.screenshot,
        output=args.output,
        apply=args.apply,
    )
    if not args.apply:
        print(f"would write: {dest}")
    else:
        print(f"wrote: {dest}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
