#!/usr/bin/env python3
"""Repair over-aggressive sweep substitutions (paths and filenames)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REPAIRS: tuple[tuple[str, str], ...] = (
    (
        "boundary-museum identity knowledge (archive)-self-library",
        "archive/boundary-self-knowledge-self-library",
    ),
    (
        "docs/boundary-museum identity knowledge (archive)-self-library",
        "docs/archive/boundary-self-knowledge-self-library",
    ),
    ("museum identity knowledge (archive).md", "archive/grace-mar-instance/self-knowledge.md"),
    ("COMPANION-SELF-legacy operator-books symlink shelf (removed)-ALIGNMENT", "COMPANION-SELF-SELF-LIBRARY-ALIGNMENT"),
    ("legacy operator-books symlink shelf (removed)", "removed operator-books symlink"),
    ("legacy symlink shelf (removed)/", ""),
    ("[`self-library.md`](../self-library.md)", "[museum `self-library.md`](../archive/grace-mar-instance/self-library.md)"),
)


def main() -> int:
    roots = [".cursor", "codex", "docs", "singularity", "skills", "library", "statecraft", "research", "README.md", "AGENTS.md", "LLM-ROUTING.md", "instance-doctrine.md"]
    changed = 0
    for root_name in roots:
        paths: list[Path]
        p = REPO_ROOT / root_name
        if p.is_file():
            paths = [p]
        elif p.is_dir():
            paths = [f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in {".md", ".mdc", ".yaml", ".yml", ".json", ".py"}]
        else:
            continue
        for path in paths:
            if "docs/archive/" in path.as_posix():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            new = text
            for old, rep in REPAIRS:
                new = new.replace(old, rep)
            if new != text:
                path.write_text(new, encoding="utf-8")
                changed += 1
                print(path.relative_to(REPO_ROOT))
    print(f"repair_sweep_damage: {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
