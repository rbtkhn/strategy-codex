#!/usr/bin/env python3
"""Fail when fork/Record residue appears in active strategy-codex paths."""

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
)

ROOT_FILES = ("README.md", "AGENTS.md", "LLM-ROUTING.md", "memory.md", "repo-map.yaml")

SKIP_UNDER_DOCS = ("docs/archive/",)

FORBIDDEN = (
    (re.compile(r"LIB-\d+"), "LIB-* catalog id"),
    (re.compile(r"self-memory", re.I), "self-memory naming"),
    (re.compile(r"SELF-LIBRARY"), "SELF-LIBRARY surface"),
    (re.compile(r"self-knowledge", re.I), "self-knowledge"),
    (re.compile(r"\bIX-[ABC]\b"), "IX-A/B/C Record section"),
    (re.compile(r"operator-books-index"), "operator-books-index dashboard"),
    (re.compile(r"operator-books-registry"), "operator-books-registry"),
)

PRODUCT_FORK = re.compile(r"cognitive\s+fork", re.I)

# Museum path literals are allowed in active docs when pointing at frozen bundle.
_MUSEUM_PATH = re.compile(
    r"(?:\.\./)*(?:docs/)?archive/[\w./\-]+",
    re.I,
)


def _sanitize_for_scan(text: str) -> str:
    return _MUSEUM_PATH.sub("MUSEUM_PATH", text)


def _rel(p: Path) -> str:
    try:
        return p.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(p)


def _should_scan(path: Path) -> bool:
    rel = _rel(path)
    if rel.startswith("docs/archive/"):
        return False
    if rel.startswith("archive/"):
        return False
    if "/archive/" in rel.replace("\\", "/"):
        return False
    return True


def _scan_file(path: Path) -> list[str]:
    if not _should_scan(path):
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    rel = _rel(path)
    scan_text = _sanitize_for_scan(text)
    hits: list[str] = []
    for pat, label in FORBIDDEN:
        if pat.search(scan_text):
            hits.append(f"{rel}: forbidden {label} ({pat.pattern})")
    if PRODUCT_FORK.search(scan_text):
        if "not a cognitive" in text.lower() or "was a cognitive" in text.lower():
            pass
        elif "museum" in text.lower() or "frozen" in text.lower() or "archaeolog" in text.lower():
            pass
        else:
            hits.append(f"{rel}: cognitive fork as product description")
    return hits


def iter_files() -> list[Path]:
    out: list[Path] = []
    for root_name in SCAN_ROOTS:
        root = REPO_ROOT / root_name
        if not root.is_dir():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".md", ".mdc", ".yaml", ".yml", ".py"}:
                out.append(p)
    for name in ROOT_FILES:
        p = REPO_ROOT / name
        if p.is_file():
            out.append(p)
    return sorted(set(out))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    violations: list[str] = []
    for path in iter_files():
        violations.extend(_scan_file(path))
    if violations:
        print("check_record_surface_retirement: FAIL", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        return 1
    msg = f"check_record_surface_retirement: ok ({len(iter_files())} files scanned)"
    print(msg if args.verbose else "check_record_surface_retirement: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
