#!/usr/bin/env python3
"""Fix path-rewrite corruption (double paths, src variable names)."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FIXES = [
    ("platform/", "platform/"),
    ("runtime/", "runtime/"),
    ("research/", "research/"),
    (
        "archive/grace-mar-instance/",
        "archive/grace-mar-instance/",
    ),
    ("archive/placeholders/", "archive/placeholders/"),
    ("archive/queues/", "archive/queues/"),
    ("templates/", "templates/"),
    ("ts_src", "ts_src"),
    ("rid_src", "rid_src"),
    ('item["src"]', 'item["src"]'),
    ('e.get("src"', 'e.get("src"'),
    ('"src": "Inbox', '"src": "Inbox'),
    ('"src": "Marker', '"src": "Marker'),
    ('"src": "Heuristic', '"src": "Heuristic'),
    ("miniapp", "miniapp"),
]

ROOTS = [
    "scripts",
    "tests",
    "docs",
    "platform",
    "research",
    "runtime",
    "archive",
    "skills",
    "schemas",
    "templates",
    ".github",
    ".cursor",
    "contributing.md",
    "README.md",
    "LLM-ROUTING.md",
    "AGENTS.md",
    "pyproject.toml",
]


def main() -> int:
    count = 0
    for item in ROOTS:
        path = REPO_ROOT / item
        files = [path] if path.is_file() else list(path.rglob("*")) if path.is_dir() else []
        for f in files:
            if not f.is_file() or ".git" in f.parts:
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            new = text
            for old, rep in FIXES:
                new = new.replace(old, rep)
            if new != text:
                f.write_text(new, encoding="utf-8")
                count += 1
    print(f"fixed {count} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
