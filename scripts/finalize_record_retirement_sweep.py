#!/usr/bin/env python3
"""Final LIB-* and product-language cleanup for record-surfaces retirement."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = (
    ("LIB-0156", "`docs/skill-work/work-strategy/history-notebook/`"),
    ("LIB-0159", "`docs/skill-work/work-strategy/theology-notebook/`"),
    ("LIB-0140..0148", "museum theology entries (archive)"),
    ("cognitive fork", "interpretive machine"),
    ("Cognitive fork", "Interpretive machine"),
    ("SELF-LIBRARY", "museum library shelf"),
    ("self-knowledge", "museum-knowledge"),
    ("SELF-KNOWLEDGE", "museum knowledge"),
    ("self-memory", "memory"),
)

LIB_RE = re.compile(r"LIB-\d+")


def _targets() -> list[Path]:
    roots = ("codex", "docs", "singularity", "skills", ".cursor", "library", "statecraft", "research")
    out: list[Path] = []
    for r in roots:
        root = REPO_ROOT / r
        if not root.is_dir():
            continue
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if "docs/archive/" in p.as_posix():
                continue
            if p.suffix.lower() in {".md", ".mdc", ".yaml", ".yml"}:
                out.append(p)
    for name in ("README.md", "AGENTS.md", "LLM-ROUTING.md", "instance-doctrine.md"):
        p = REPO_ROOT / name
        if p.is_file():
            out.append(p)
    return sorted(set(out))


def main() -> int:
    changed = 0
    for path in _targets():
        text = path.read_text(encoding="utf-8", errors="replace")
        new = text
        for old, rep in REPLACEMENTS:
            new = new.replace(old, rep)
        new = LIB_RE.sub("", new)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
            print(path.relative_to(REPO_ROOT))
    print(f"finalize_record_retirement_sweep: {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
