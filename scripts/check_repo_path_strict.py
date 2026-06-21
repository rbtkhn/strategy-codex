#!/usr/bin/env python3
"""Warn on legacy repo path layouts (Sprint 4 — warn mode; --strict fails CI)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import REPO_PATH_CLASSIFICATION, scan_legacy_path_layout  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when any legacy or dual-layout path key is present",
    )
    args = parser.parse_args()

    issues = scan_legacy_path_layout()
    if not issues:
        print("ok: no active legacy repo path layouts detected")
        return 0

    for issue in issues:
        key = issue.split(":", 1)[0]
        bucket = REPO_PATH_CLASSIFICATION.get(key, "unclassified")
        print(f"repo-path-strict: [{bucket}] {issue}", file=sys.stderr)
    print(f"repo-path-strict: {len(issues)} issue(s)", file=sys.stderr)
    return 1 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
