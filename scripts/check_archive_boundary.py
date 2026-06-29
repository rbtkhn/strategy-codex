#!/usr/bin/env python3
"""Warn when primary-path docs exceed Grace-Mar mention budget or lack archive pointer."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# SSOT: docs/complexity-budget.md — Grace-Mar / fork-revive mention budget
CANONICAL_ARCHIVE_POINTER = (
    "Grace-Mar is archived/frozen. Active strategy-codex work does not grow the fork. "
    "See docs/archive/grace-mar.md."
)

ARCHIVE_POINTER = "docs/archive/grace-mar.md"
DEEP_RULES_POINTER = "docs/agent-rules/deep-rules.md"
ARCHIVE_POINTERS = (ARCHIVE_POINTER, DEEP_RULES_POINTER)

PRIMARY_GLOBS = (
    "README.md",
    "AGENTS.md",
    "contributing.md",
    "instance-doctrine.md",
    "docs/start-here.md",
    "docs/architecture.md",
    "docs/product-identity.md",
    "docs/harness-architecture-map.md",
    "docs/root-directory-map.md",
    "docs/grace-mar-instance-boundary.md",
)

# Core onboarding surfaces — canonical pointer + tight narrative cap
MENTION_BUDGET_FILES = frozenset(
    {
        "README.md",
        "AGENTS.md",
        "contributing.md",
        "docs/start-here.md",
        "docs/architecture.md",
    }
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

NARRATIVE_RE = re.compile(r"Grace-Mar|grace-mar|fork revive|fork-revive", re.I)

OPERATIONAL_LINE_RE = re.compile(
    r"archive/grace-mar-instance|process_approved_candidates|\[gated-merge\]|"
    r"Fork revive only|fork revive only|fork-revive|"
    r"Door \*\*A\*\*|Companion \(fork revive|grace-mar-instance-boundary|"
    r"recursion-gate\.md|bot/prompt\.py|self\.md|self-archive\.md|"
    r"Archive / Grace-Mar / fork|Record and pipeline \(fork revive|"
    r"`-u grace-mar`|Deprecated alias: `grace-mar`|"
    r"## Frozen sidecar \(Grace-Mar\)|\.fork revive only\.|"
    r"Fork revive only:|fork-gate candidates",
    re.I,
)

DEFAULT_MAX_BLOCK = 8
DEFAULT_MAX_MENTIONS = 6
DEFAULT_MAX_NARRATIVE = 1


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


def _has_archive_link(text: str) -> bool:
    norm = text.replace("\\", "/")
    return any(p in norm for p in ARCHIVE_POINTERS)


def _has_canonical_pointer(text: str) -> bool:
    collapsed = " ".join(text.split())
    pointer = " ".join(CANONICAL_ARCHIVE_POINTER.split())
    if pointer in collapsed:
        return True
    if (
        "grace-mar is archived/frozen" in collapsed.lower()
        and "does not grow the fork" in collapsed.lower()
        and ARCHIVE_POINTER in text.replace("\\", "/")
    ):
        return True
    return False


def _is_operational_line(line: str) -> bool:
    if OPERATIONAL_LINE_RE.search(line):
        return True
    if re.search(
        r"\[[^\]]*\]\([^)]*(?:archive/grace-mar|docs/archive/grace-mar)[^)]*\)",
        line,
        re.I,
    ):
        return True
    if re.search(r"`[^`]*grace-mar[^`]*`", line, re.I):
        return True
    return False


def _is_pointer_line(line: str) -> bool:
    collapsed = " ".join(line.split())
    if "archived/frozen" in collapsed.lower() and "does not grow the fork" in collapsed.lower():
        return True
    return CANONICAL_ARCHIVE_POINTER in collapsed


def _count_narrative_mentions(text: str) -> int:
    total = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("---") or stripped.startswith("<!--"):
            continue
        if _is_operational_line(line) or _is_pointer_line(line):
            continue
        total += len(NARRATIVE_RE.findall(line))
    return total


def _scan_mention_budget(rel: str, text: str, *, max_narrative: int) -> list[str]:
    if rel not in MENTION_BUDGET_FILES:
        return []

    issues: list[str] = []
    narrative = _count_narrative_mentions(text)

    if narrative > 0 and not _has_canonical_pointer(text):
        issues.append(
            f"{rel}: {narrative} narrative mention(s) without canonical archive pointer"
        )
    if narrative > max_narrative:
        issues.append(
            f"{rel}: {narrative} narrative mention(s) exceed budget ({max_narrative})"
        )
    return issues


def _scan_file(
    path: Path,
    *,
    max_block: int,
    max_mentions: int,
    max_narrative: int,
) -> list[str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    issues: list[str] = []

    issues.extend(_scan_mention_budget(rel, text, max_narrative=max_narrative))

    mentions = len(TOPIC_RE.findall(text))
    if mentions > max_mentions and not _has_archive_link(text):
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
                window = "\n".join(lines[block_start:idx])
                if not _has_archive_link(window):
                    issues.append(
                        f"{rel}:{block_start + 1}-{idx}: {block_len}-line Grace-Mar block without archive pointer"
                    )
            block_start = None
            block_len = 0
    if block_start is not None and block_len > max_block:
        window = "\n".join(lines[block_start:])
        if not _has_archive_link(window):
            issues.append(
                f"{rel}:{block_start + 1}-end: {block_len}-line Grace-Mar block without archive pointer"
            )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any issue")
    parser.add_argument("--max-block", type=int, default=DEFAULT_MAX_BLOCK)
    parser.add_argument("--max-mentions", type=int, default=DEFAULT_MAX_MENTIONS)
    parser.add_argument("--max-narrative", type=int, default=DEFAULT_MAX_NARRATIVE)
    args = parser.parse_args()

    all_issues: list[str] = []
    for path in _iter_primary_files():
        all_issues.extend(
            _scan_file(
                path,
                max_block=args.max_block,
                max_mentions=args.max_mentions,
                max_narrative=args.max_narrative,
            )
        )

    if all_issues:
        for issue in all_issues:
            print(f"archive-mention-budget: {issue}", file=sys.stderr)
        print(f"archive-mention-budget: {len(all_issues)} issue(s)", file=sys.stderr)
        return 1 if args.strict else 0

    print("ok: archive mention budget check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
