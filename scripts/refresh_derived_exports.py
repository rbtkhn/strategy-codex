#!/usr/bin/env python3
"""
Refresh all derived artifacts checked by validate-integrity.py (derived export freshness).

`process_approved_candidates.py` runs this automatically before merge integrity preflight, so
manual refresh is mainly for local edits, CI, or recovery when `validate-integrity.py` reports staleness.

Same order as `process_approved_candidates.py` post-merge exports (post-merge also re-runs PRP + subset refresh).

  python3 scripts/refresh_derived_exports.py
  python3 scripts/validate-integrity.py --json
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

from repo_io import profile_dir


def _prp_output_path(user_id: str) -> Path:
    if profile_dir(user_id) == REPO_ROOT:
        return REPO_ROOT / "self-llm.txt"
    return profile_dir(user_id) / f"{user_id}-llm.txt"


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate manifest, PRP, fork manifest, runtime bundle.")
    parser.add_argument("-u", "--user", default="strategy-codex", help="Profile id")
    args = parser.parse_args()
    uid = args.user.strip() or "strategy-codex"
    profile = profile_dir(uid)
    py = sys.executable

    steps: list[list[str]] = [
        [
            py,
            str(REPO_ROOT / "scripts" / "export.py"),
            "prp",
            "--",
            "-u",
            uid,
            "-n",
            "Abby",
            "-o",
            str(_prp_output_path(uid)),
        ],
        [py, str(REPO_ROOT / "scripts" / "export.py"), "manifest", "--", "-u", uid, "-o", str(platform/profile)],
        [py, str(REPO_ROOT / "scripts" / "fork_checksum.py"), "-u", uid, "--manifest"],
        [
            py,
            str(REPO_ROOT / "scripts" / "export.py"),
            "bundle",
            "--",
            "-u",
            uid,
            "-o",
            str(profile / "runtime/bundle"),
        ],
    ]

    for cmd in steps:
        label = " ".join(cmd[-4:])
        print(f"Running: {label}", file=sys.stderr)
        r = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
        if r.returncode != 0:
            print(f"FAILED: {cmd}", file=sys.stderr)
            return r.returncode

    print("Derived exports refreshed.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
