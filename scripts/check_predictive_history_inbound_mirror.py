#!/usr/bin/env python3
"""Fail when public/predictive-history/ changes without an inbound-sync commit tag."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIRROR_PREFIX = "public/predictive-history/"
SYNC_TAG = "[predictive-history-sync]"
ALLOWLIST = {
    f"{MIRROR_PREFIX}MIRROR-RECEIPT.md",
    f"{MIRROR_PREFIX}DO-NOT-EDIT.md",
}


def git_output(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(REPO_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or "unknown git error"
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout.strip()


def changed_mirror_files(base: str) -> list[str]:
    out = git_output(["diff", "--name-only", f"{base}...HEAD"])
    if not out:
        return []
    return [
        line.replace("\\", "/")
        for line in out.splitlines()
        if line.replace("\\", "/").startswith(MIRROR_PREFIX)
    ]


def commit_messages(base: str) -> str:
    return git_output(["log", "--format=%B", f"{base}..HEAD"])


def check(base: str) -> tuple[bool, list[str]]:
    changed = changed_mirror_files(base)
    if not changed:
        return True, []

    disallowed = sorted(path for path in changed if path not in ALLOWLIST)
    if not disallowed:
        return True, []

    messages = commit_messages(base)
    if SYNC_TAG in messages:
        return True, []

    return False, disallowed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default="origin/main",
        help="Git ref to compare against (default: origin/main)",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Check staged changes against HEAD (pre-commit mode)",
    )
    args = parser.parse_args(argv)

    try:
        if args.staged:
            out = git_output(["diff", "--cached", "--name-only"])
            changed = [
                line.replace("\\", "/")
                for line in (out.splitlines() if out else [])
                if line.replace("\\", "/").startswith(MIRROR_PREFIX)
            ]
            disallowed = sorted(path for path in changed if path not in ALLOWLIST)
            if disallowed:
                print(
                    f"ERROR: staged edits under {MIRROR_PREFIX} are inbound-only.\n"
                    f"Edit in PREDICTIVE_HISTORY_ROOT; sync with "
                    f"sync_predictive_history_mirror.py and commit with {SYNC_TAG}.\n"
                    f"Blocked paths:\n  " + "\n  ".join(disallowed),
                    file=sys.stderr,
                )
                return 1
            return 0

        ok, paths = check(args.base)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if ok:
        return 0

    print(
        f"ERROR: manual edits under {MIRROR_PREFIX} without {SYNC_TAG}.\n"
        "Author in rbtkhn/predictive-history; refresh via sync_predictive_history_mirror.py.\n"
        "See docs/predictive-history-operator-workspace.md\n"
        f"Changed paths:\n  " + "\n  ".join(paths),
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
