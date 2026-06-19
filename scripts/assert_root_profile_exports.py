#!/usr/bin/env python3
"""Fail when profile-derived exports still exist at repository root."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import PROFILE_DERIVED_EXPORTS, REPO_ROOT  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-legacy",
        action="store_true",
        help="Skip check (soak only; do not use in CI)",
    )
    args = parser.parse_args()
    if args.allow_legacy:
        print("assert_root_profile_exports: skipped (--allow-legacy)")
        return 0

    offenders = [name for name in PROFILE_DERIVED_EXPORTS if (REPO_ROOT / name).is_file()]
    if offenders:
        print(
            "assert_root_profile_exports: profile exports must not live at repo root:\n  "
            + "\n  ".join(offenders),
            file=sys.stderr,
        )
        return 1
    print(f"assert_root_profile_exports: ok ({len(PROFILE_DERIVED_EXPORTS)} basenames)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
