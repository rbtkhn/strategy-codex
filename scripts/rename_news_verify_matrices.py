#!/usr/bin/env python3
"""Rename wire-verify-matrix artifacts to news-verify-matrix (term-law DOCSYNC).

Usage:
    python scripts/rename_news_verify_matrices.py --dry-run
    python scripts/rename_news_verify_matrices.py --apply
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIRE_DIR = REPO_ROOT / "statecraft" / "notes" / "wire"

SKIP_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
}

TEXT_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"-wire-verify-matrix\.md"), "-news-verify-matrix.md"),
    (re.compile(r"# Wire Verify Matrix"), "# News Verify Matrix"),
    (re.compile(r"\bWire Verify Matrix\b"), "News Verify Matrix"),
    (re.compile(r"wire-verify-matrix"), "news-verify-matrix"),
    (re.compile(r"\bwire-verify matrix\b"), "news-verify matrix"),
    (re.compile(r"\*\*Wire-verify\b"), "**News-verify"),
    (re.compile(r"\bWire-verify\b"), "News-verify"),
]

SCAN_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".tsv", ".csv", ".mdc"}

def should_scan(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() not in SCAN_SUFFIXES:
        return False
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return False
    if path.name == "rename_news_verify_matrices.py":
        return False
    return True

def iter_scan_files() -> list[Path]:
    out: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if should_scan(path):
            out.append(path)
    return sorted(out)

def rename_matrix_files(*, apply: bool) -> list[tuple[str, str]]:
    moves: list[tuple[str, str]] = []
    for old in sorted(WIRE_DIR.glob("*-wire-verify-matrix.md")):
        new = old.with_name(old.name.replace("-wire-verify-matrix.md", "-news-verify-matrix.md"))
        if new.exists():
            continue
        rel_old = old.relative_to(REPO_ROOT).as_posix()
        rel_new = new.relative_to(REPO_ROOT).as_posix()
        moves.append((rel_old, rel_new))
        if apply:
            subprocess.run(["git", "mv", rel_old, rel_new], cwd=REPO_ROOT, check=True)
    return moves

def rewrite_text(*, apply: bool) -> list[Path]:
    changed: list[Path] = []
    for path in iter_scan_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = text
        for pat, sub in TEXT_REPLACEMENTS:
            new = pat.sub(sub, new)
        if new != text:
            changed.append(path)
            if apply:
                path.write_text(new, encoding="utf-8")
    return changed

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply renames and text edits")
    parser.add_argument("--dry-run", action="store_true", help="Report only (default)")
    args = parser.parse_args()
    apply = args.apply and not args.dry_run
    if not args.apply and not args.dry_run:
        args.dry_run = True

    moves = rename_matrix_files(apply=apply)
    print(f"matrix renames: {len(moves)}")
    for old, new in moves:
        print(f"  {'mv' if apply else 'would mv'} {old} -> {new}")

    changed = rewrite_text(apply=apply)
    print(f"text files touched: {len(changed)}")
    if args.dry_run and changed:
        for p in changed[:20]:
            print(f"  would edit {p.relative_to(REPO_ROOT).as_posix()}")
        if len(changed) > 20:
            print(f"  ... and {len(changed) - 20} more")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
