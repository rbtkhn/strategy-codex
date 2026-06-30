#!/usr/bin/env python3
"""Report current vs target root folder layout and optional path-reference counts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import REPO_PATH_MIGRATIONS, TARGET_ROOT_FOLDERS  # noqa: E402

SCAN_ROOTS = ("scripts", "tests", "docs", ".github", ".cursor", "platform/apps", "platform")
SKIP_PARTS = {".git", ".venv", "node_modules", "public", "source-archive", "statecraft", "singularity"}

def list_root_dirs() -> list[str]:
    return sorted(p.name for p in REPO_ROOT.iterdir() if p.is_dir())

def count_hits(legacy_segment: str) -> int:
    pattern = re.compile(re.escape(legacy_segment))
    total = 0
    for root_name in SCAN_ROOTS:
        root = REPO_ROOT / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            if path.suffix not in {".py", ".md", ".mdc", ".yml", ".yaml", ".toml", ".json", ".sh"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            total += len(pattern.findall(text))
    return total

def main() -> int:
    parser = argparse.ArgumentParser(description="Root layout inventory")
    parser.add_argument("--hits", action="store_true", help="Count legacy path string hits")
    args = parser.parse_args()

    current = list_root_dirs()
    target = sorted(TARGET_ROOT_FOLDERS)
    print(f"Root folders: {len(current)} current, {len(target)} target")
    print("\n## Current")
    for name in current:
        print(f"- {name}")
    print("\n## Target")
    for name in target:
        print(f"- {name}")
    extra = sorted(set(current) - set(target))
    missing = sorted(set(target) - set(current))
    if extra:
        print(f"\n## Extra vs target ({len(extra)})")
        for name in extra:
            print(f"- {name}")
    if missing:
        print(f"\n## Missing vs target ({len(missing)})")
        for name in missing:
            print(f"- {name}")

    if args.hits:
        print("\n## Legacy path hits (sample scan)")
        for key, (canonical, *legacy) in REPO_PATH_MIGRATIONS.items():
            for leg in legacy:
                hits = count_hits(leg)
                if hits:
                    print(f"- {leg}: {hits} hits -> {canonical}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
