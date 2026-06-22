#!/usr/bin/env python3
"""Backfill source-archive links from legacy statecraft/daily/ paths."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"

RULES = [
    (
        re.compile(r"statecraft/daily/(\d{4}-\d{2}-\d{2}-wire-verify-matrix\.md)"),
        r"statecraft/notes/wire/\1",
    ),
    (
        re.compile(r"statecraft/daily/(\d{4}-\d{2}-\d{2}-72h-watch-run\.md)"),
        r"statecraft/notes/watch/\1",
    ),
    (
        re.compile(r"statecraft/daily/(\d{4}-\d{2}-\d{2}-intake-readiness\.md)"),
        r"statecraft/notes/intake/\1",
    ),
    (
        re.compile(r"statecraft/daily/(\d{4}-\d{2}-\d{2})\.md"),
        r"statecraft/synthesis/day/\1.md",
    ),
    (
        re.compile(r"statecraft/daily/(\d{4}-\d{2}-week\d+-start-here\.md)"),
        r"statecraft/notes/reentry/\1",
    ),
    (
        re.compile(r"statecraft/daily/([^\s)\]]+\.md)"),
        r"statecraft/notes/\1",
    ),
]


def main() -> int:
    files = 0
    for path in ARCHIVE_ROOT.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "statecraft/daily/" not in text:
            continue
        new = text
        for pat, sub in RULES:
            new = pat.sub(sub, new)
        if new != text:
            path.write_text(new, encoding="utf-8")
            files += 1
    print(f"backfill_archive_synthesis_links: updated {files} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
