#!/usr/bin/env python3
"""Fail on stale ``statecraft/daily/`` path references outside the redirect stub.

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SCAN_ROOTS = (
    REPO_ROOT / "statecraft",
    REPO_ROOT / "docs",
    REPO_ROOT / ".cursor",
    REPO_ROOT / "skills",
    REPO_ROOT / "tests",
    REPO_ROOT / "scripts",
)

ALLOWLIST_SUBSTRINGS = (
    "statecraft/daily/README.md",
    "migrate_statecraft_synthesis_layout.py",
    "validate_statecraft_path_layout.py",
    "backfill_archive_synthesis_links.py",
    "statecraft-synthesis-migrate-manifest",
    "statecraft-synthesis-link-rewrite",
)

WARN_ONLY_SUBSTRINGS = (
    "source-archive/statecraft",
    "runtime/artifacts",
    "recursive-learning-journal.md",
)

SCAN_SUFFIXES = {".md", ".mdc", ".py", ".yml", ".yaml", ".json"}


def should_scan(path: Path) -> bool:
    if path.suffix not in SCAN_SUFFIXES:
        return False
    rel = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    for allow in ALLOWLIST_SUBSTRINGS:
        if allow in rel:
            return False
    return True


def scan(*, warn_archive: bool = True) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    needle = "statecraft/daily/"
    for root in SCAN_ROOTS:
        if not root.is_dir() and root.is_file():
            paths = [root]
        elif root.is_dir():
            paths = list(root.rglob("*"))
        else:
            continue
        for path in paths:
            if not path.is_file() or not should_scan(path):
                continue
            rel = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if needle not in text:
                continue
            if any(w in rel for w in WARN_ONLY_SUBSTRINGS):
                if warn_archive:
                    warnings.append(rel)
                continue
            errors.append(rel)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--warn-archive",
        action="store_true",
        help="Print warn-only hits (archive, runtime artifacts, RLJ)",
    )
    args = parser.parse_args()
    errors, warnings = scan(warn_archive=args.warn_archive)
    if args.warn_archive and warnings:
        for w in warnings:
            print(f"warn: stale path reference in {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"error: stale path reference in {e}", file=sys.stderr)
        print(
            f"validate_statecraft_path_layout: {len(errors)} error(s)",
            file=sys.stderr,
        )
        return 1
    print("ok: no stale statecraft/daily/ references in active operator surfaces")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
