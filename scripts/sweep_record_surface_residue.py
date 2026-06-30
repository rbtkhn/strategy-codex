#!/usr/bin/env python3
"""Apply mechanical residue replacements for record-surfaces retirement (active paths only)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SCAN_ROOTS = (
    "docs",
    ".cursor",
    "statecraft",
    "singularity",
    "codex",
    "research",
    "skills",
    "library",
    "scripts",
)

ROOT_FILES = ("README.md", "AGENTS.md", "LLM-ROUTING.md", "memory.md", "repo-map.yaml", "instance-doctrine.md")

SKIP_PREFIXES = (
    "docs/archive/",
    "archive/",
)

# Order matters: longer / more specific first.
REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("LIB-0153", "strategy-codex (`codex/`)"),
    ("LIB-0149", "predictive-history (`codex/predictive-history/`)"),
    ("LIB-0154", "cici notebook (`singularity/work-cici/cici-notebook/`)"),
    ("LIB-0155", "dev journal (`docs/skill-work/work-dev/dev-notebook/work-dev/journal/`)"),
    ("LIB-0151", "Predictive History YouTube library (`research/external/youtube-channels/predictive-history/`)"),
    ("prune_self_memory.py", "prune_memory.py"),
    ("resolve_self_memory_path", "resolve_memory_path"),
    ("self-memory.md", "memory.md"),
    ("SELF-LIBRARY/", "legacy symlink shelf (removed)/"),
    ("SELF-LIBRARY", "legacy operator-books symlink shelf (removed)"),
    ("self-knowledge", "museum identity knowledge (archive)"),
    ("self-memory", "memory"),
    (r"\bIX-A\b", "museum knowledge section A"),
    (r"\bIX-B\b", "museum knowledge section B"),
    (r"\bIX-C\b", "museum knowledge section C"),
)

def _rel(p: Path) -> str:
    try:
        return p.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(p)

def _should_scan(path: Path) -> bool:
    rel = _rel(path)
    for prefix in SKIP_PREFIXES:
        if rel.startswith(prefix):
            return False
    if rel == "scripts/sweep_record_surface_residue.py":
        return False
    if rel == "scripts/check_record_surface_retirement.py":
        return False
    return True

def _iter_files() -> list[Path]:
    out: list[Path] = []
    for name in ROOT_FILES:
        p = REPO_ROOT / name
        if p.is_file():
            out.append(p)
    for root_name in SCAN_ROOTS:
        root = REPO_ROOT / root_name
        if not root.is_dir():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".md", ".mdc", ".py", ".yaml", ".yml", ".json"}:
                if _should_scan(p):
                    out.append(p)
    return sorted(set(out))

def _apply(text: str) -> str:
    for old, new in REPLACEMENTS:
        if old.startswith(r"\b") or "\\b" in old:
            text = re.sub(old, new, text)
        else:
            text = text.replace(old, new)
    return text

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        ap.error("use --dry-run or --apply")

    changed = 0
    for path in _iter_files():
        try:
            orig = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        new = _apply(orig)
        if new != orig:
            changed += 1
            print(_rel(path))
            if args.apply:
                path.write_text(new, encoding="utf-8")
    print(f"sweep_record_surface_residue: {changed} file(s) {'updated' if args.apply else 'would change'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
