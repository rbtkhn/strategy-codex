#!/usr/bin/env python3
"""One-shot helper: replace codex/ path references with continuity/ in scoped trees."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

SCAN_ROOTS = (
    REPO / "continuity",
    REPO / "docs",
    REPO / "statecraft",
    REPO / ".cursor",
    REPO / "tests",
    REPO / "essays",
    REPO / "singularity",
    REPO / "skills",
    REPO / "scripts",
    REPO / ".github",
    REPO / "research",
    REPO / "public",
    REPO,
)

SKIP_FILES = {
    REPO / "docs" / "codex-to-continuity-rename.md",
    REPO / "codex" / "README.md",
}

REPLACEMENTS = (
    ("../codex/", "../continuity/"),
    ("./codex/", "./continuity/"),
    ("`codex/", "`continuity/"),
    ("(codex/", "(continuity/"),
    ("codex/", "continuity/"),
)

EXTENSIONS = {".md", ".mdc", ".py", ".yaml", ".yml", ".json"}


def should_skip(path: Path) -> bool:
    if path.resolve() in {p.resolve() for p in SKIP_FILES}:
        return True
    rel = path.relative_to(REPO).as_posix()
    if rel.startswith("scripts/audit_continuity_rename"):
        return True
    if rel.startswith("scripts/patch_continuity_path_refs"):
        return True
    if rel.startswith("scripts/migrate_codex"):
        return True
    if rel.startswith("scripts/build_external_codex"):
        return True
    if rel.startswith("scripts/external_codex"):
        return True
    if rel.startswith("scripts/strategy_codex_config"):
        return True
    if rel.startswith("scripts/validate_strategy_codex_transition"):
        return True
    if rel.startswith("scripts/continuity_paths"):
        return True
    if rel == "codex/README.md":
        return True
    parts = path.parts
    if "archive" in parts or "node_modules" in parts:
        return True
    return False


def patch_file(path: Path) -> bool:
    if should_skip(path) or path.suffix.lower() not in EXTENSIONS:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = 0
    for root in SCAN_ROOTS:
        if not root.is_dir() and root != REPO:
            continue
        if root == REPO:
            for path in REPO.iterdir():
                if path.is_file() and patch_file(path):
                    changed += 1
                    print(path.relative_to(REPO))
            continue
        for path in root.rglob("*"):
            if path.is_file() and patch_file(path):
                changed += 1
                print(path.relative_to(REPO))
    print(f"patched {changed} files", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
