#!/usr/bin/env python3
"""Bulk-rewrite legacy root path strings after consolidation (one-time migration aid)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import REPO_PATH_MIGRATIONS  # noqa: E402

DEFAULT_SCAN = (
    "scripts",
    "tests",
    "docs",
    ".github",
    ".cursor",
    "platform",
    "runtime",
    "archive",
    "research",
    "skills",
    "schemas",
    "templates",
    "contributing.md",
    "README.md",
    "pyproject.toml",
    "LLM-ROUTING.md",
    "repo-map.yaml",
    "AGENTS.md",
    "instance-doctrine.md",
)

SUFFIXES = {".py", ".md", ".mdc", ".yml", ".yaml", ".toml", ".json", ".sh", ".txt"}

def replacements() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for _key, entry in REPO_PATH_MIGRATIONS.items():
        canonical = entry[0]
        for legacy in entry[1:]:
            if legacy == canonical:
                continue
            pairs.append((legacy + "/", canonical + "/"))
            if legacy == "bin":
                continue
            pairs.append((legacy + '"', canonical + '"'))
            pairs.append((legacy + "'", canonical + "'"))
            pairs.append(("`" + legacy + "/", "`" + canonical + "/"))
            pairs.append(("`" + legacy + "`", "`" + canonical + "`"))
            pairs.append((legacy + ")", canonical + ")"))
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    return pairs

def iter_files(scan: tuple[str, ...]):
    for item in scan:
        path = REPO_ROOT / item
        if path.is_file():
            yield path
            continue
        if not path.is_dir():
            continue
        for f in path.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix.lower() not in SUFFIXES and f.name not in {"AGENTS.md", "LLM-ROUTING.md"}:
                continue
            if ".git" in f.parts:
                continue
            yield f

def main() -> int:
    parser = argparse.ArgumentParser(description="Rewrite legacy root paths")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("Specify --dry-run or --apply")
    pairs = replacements()
    changed = 0
    for path in iter_files(DEFAULT_SCAN):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        new = text
        for old, new_val in pairs:
            new = new.replace(old, new_val)
        if new != text:
            changed += 1
            rel = path.relative_to(REPO_ROOT)
            if args.dry_run:
                print(f"would update {rel}")
            else:
                path.write_text(new, encoding="utf-8")
                print(f"updated {rel}")
    print(f"{'would change' if args.dry_run else 'changed'} {changed} files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
