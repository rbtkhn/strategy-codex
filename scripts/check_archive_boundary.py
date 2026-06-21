#!/usr/bin/env python3
"""Warn when primary-path docs contain long Grace-Mar sections without archive pointer."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ARCHIVE_POINTER = "docs/archive/grace-mar.md"
DEEP_RULES_POINTER = "docs/agent-rules/deep-rules.md"
ARCHIVE_POINTERS = (ARCHIVE_POINTER, DEEP_RULES_POINTER)

PRIMARY_GLOBS = (
    "README.md",
    "AGENTS.md",
    "contributing.md",
    "instance-doctrine.md",
    "docs/start-here.md",
    "docs/product-identity.md",
    "docs/harness-architecture-map.md",
    "docs/root-directory-map.md",
    "docs/grace-mar-instance-boundary.md",
)

SKIP_PREFIXES = (
    "docs/archive/",
    "archive/",
)

SKIP_EXACT = {
    ".cursor/rules/grace-mar.mdc",
}

TOPIC_RE = re.compile(
    r"Grace-Mar|grace-mar|fork revive|fork-revive|\bRecord\b|\bVoice\b|recursion-gate|companion-self",
    re.I,
)

DEFAULT_MAX_BLOCK = 8
DEFAULT_MAX_MENTIONS = 6


def _iter_primary_files() -> list[Path]:
    out: set[Path] = set()
    for pattern in PRIMARY_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            if not path.is_file():
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel in SKIP_EXACT or any(rel.startswith(p) for p in SKIP_PREFIXES):
                continue
            out.add(path)
    rules = REPO_ROOT / ".cursor" / "rules"
    if rules.is_dir():
        for path in rules.glob("*.mdc"):
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel in SKIP_EXACT:
                continue
            out.add(path)
    return sorted(out)


def _has_pointer(text: str) -> bool:
    norm = text.replace("\\", "/")
    return any(p in norm for p in ARCHIVE_POINTERS)


def _scan_file(path: Path, *, max_block: int, max_mentions: int) -> list[str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    issues: list[str] = []

    mentions = len(TOPIC_RE.findall(text))
    if mentions > max_mentions and not _has_pointer(text):
        issues.append(f"{rel}: {mentions} topic mentions without {ARCHIVE_POINTER}")

    block_start = None
    block_len = 0
    for idx, line in enumerate(lines):
        if TOPIC_RE.search(line):
            if block_start is None:
                block_start = idx
                block_len = 1
            else:
                block_len += 1
        else:
            if block_start is not None and block_len > max_block:
                window = "\n".join(lines[block_start : idx + 1])
                if not _has_pointer(window):
                    issues.append(
                        f"{rel}:{block_start + 1}-{idx}: {block_len}-line Grace-Mar block without archive pointer"
                    )
            block_start = None
            block_len = 0
    if block_start is not None and block_len > max_block:
        window = "\n".join(lines[block_start:])
        if not _has_pointer(window):
            issues.append(
                f"{rel}:{block_start + 1}-end: {block_len}-line Grace-Mar block without archive pointer"
            )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any issue")
    parser.add_argument("--max-block", type=int, default=DEFAULT_MAX_BLOCK)
    parser.add_argument("--max-mentions", type=int, default=DEFAULT_MAX_MENTIONS)
    args = parser.parse_args()

    all_issues: list[str] = []
    for path in _iter_primary_files():
        all_issues.extend(
            _scan_file(path, max_block=args.max_block, max_mentions=args.max_mentions)
        )

    if all_issues:
        for issue in all_issues:
            print(f"archive-boundary: {issue}", file=sys.stderr)
        print(f"archive-boundary: {len(all_issues)} issue(s)", file=sys.stderr)
        return 1 if args.strict else 0

    print("ok: archive boundary check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
