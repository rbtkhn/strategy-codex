#!/usr/bin/env python3
"""
Warn if routing logic appears outside canonical front doors.

Front doors:
- docs/start-here.md
- LLM-ROUTING.md
- repo-map.yaml
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

NON_ALLOWED = [
    "README.md",
    "contributing.md",
    "docs/architecture.md",
]

KEYWORDS = [
    "Choose your path",
    "routing table",
    "find things in this repo",
]

def scan_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    return [k for k in KEYWORDS if k.lower() in text]

def main() -> int:
    warnings: list[str] = []

    for rel in NON_ALLOWED:
        p = REPO_ROOT / rel
        if not p.exists():
            continue

        hits = scan_file(p)
        if hits:
            warnings.append(f"{rel}: contains routing surface hints {hits}")

    if warnings:
        print("[warn] routing front-door violations detected:")
        for w in warnings:
            print(" -", w)
        return 0  # warn-only for now

    print("[ok] routing front-door check clean")
    return 0

if __name__ == "__main__":
    sys.exit(main())
