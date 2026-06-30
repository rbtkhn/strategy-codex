#!/usr/bin/env python3
"""Remove local dev temp directories (pytest, codex) from the repo root. Safe: only known patterns."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PATTERNS = (
    ".tmp-pytest-*",
    "pytest-cache-files-*",
    ".codex-tmp",
    ".codex-platform/bin",
)

def _matches(name: str) -> bool:
    if name == ".codex-tmp" or name == ".codex-platform/bin":
        return True
    if name.startswith(".tmp-pytest-"):
        return True
    if name.startswith("pytest-cache-files-"):
        return True
    return False

def main() -> int:
    parser = argparse.ArgumentParser(description="Remove dev temp dirs from repository root")
    parser.add_argument("--dry-run", action="store_true", help="List targets only")
    parser.add_argument("--apply", action="store_true", help="Delete targets")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("Specify --dry-run or --apply")
    targets = [p for p in REPO_ROOT.iterdir() if p.is_dir() and _matches(p.name)]
    if not targets:
        print("No matching temp directories at repo root.")
        return 0
    for p in sorted(targets):
        if args.dry_run:
            print(f"would remove {p.relative_to(REPO_ROOT)}/")
        else:
            shutil.rmtree(p)
            print(f"removed {p.relative_to(REPO_ROOT)}/")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
