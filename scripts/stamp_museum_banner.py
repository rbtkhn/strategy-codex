#!/usr/bin/env python3
"""Prepend museum banner to Grace-Mar Record files under archive/grace-mar-instance/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MUSEUM_DIR = REPO_ROOT / "archive" / "grace-mar-instance"
BANNER = (
    "<!-- MUSEUM: Not active SSOT for strategy-codex. "
    "See docs/archive/grace-mar-record-museum.md -->\n\n"
)
TARGETS = (
    "self.md",
    "museum identity knowledge (archive).md",
    "self-library.md",
    "self-skills.md",
    "self-archive.md",
    "memory.md",
)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    changed = 0
    for name in TARGETS:
        path = MUSEUM_DIR / name
        if not path.is_file():
            print(f"skip missing {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if "MUSEUM: Not active SSOT" in text[:400]:
            print(f"already stamped {name}")
            continue
        new_text = BANNER + text
        if args.dry_run:
            print(f"would stamp {name}")
        else:
            path.write_text(new_text, encoding="utf-8")
            print(f"stamped {name}")
        changed += 1
    print(f"stamp_museum_banner: {changed} file(s)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
