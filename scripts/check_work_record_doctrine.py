#!/usr/bin/env python3
"""Fail if deprecated WORK/Record banner appears outside allowlisted paths."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ALLOWLIST_PREFIXES: tuple[str, ...] = (
    "docs/archive/",
    "archive/grace-mar-instance/",
    "archive/grace-mar-corpus/",
    "public/predictive-history/",
)

SKIP_DIRS = frozenset({".git", "node_modules", "__pycache__", ".cursor/plans", ".tmp-pytest"})
SKIP_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip"})

CHECKER_SKIP_FILES = frozenset(
    {
        "check_work_record_doctrine.py",
        "sweep_script_emitters.py",
        "sweep_work_record_docstrings.py",
        "test_work_record_phrase_emitters.py",
    }
)

FORBIDDEN_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"work\s*only\s*[;—\-]\s*not\s+record", re.IGNORECASE),
    re.compile(r"\*\*WORK only\*\*\s*[—\-]?\s*not\s+record", re.IGNORECASE),
    re.compile(r"WORK only\s{2,}not\s+record", re.IGNORECASE),
)

BANNER_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"^WORK only; not Record\.\s*$", re.IGNORECASE), "WORK only; not Record."),
    (re.compile(r"^work only; not Record\.\s*$"), "work only; not Record."),
    (re.compile(r"^\*\*Work only; not Record\.\*\*\s*$", re.IGNORECASE), "**Work only; not Record.**"),
    (re.compile(r"^\*\*WORK only; not Record\.\*\*\s*$"), "**WORK only; not Record.**"),
    (re.compile(r"^WORK only — not Record\.?\s*$", re.IGNORECASE), "WORK only — not Record"),
    (re.compile(r"^WORK-only; not Record\.?\s*$", re.IGNORECASE), "WORK-only; not Record."),
)

SWEEP_REPLACEMENTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"^\s*WORK only; not Record\.\s*$", re.MULTILINE | re.IGNORECASE), ""),
    (re.compile(r"^\s*work only; not Record\.\s*$", re.MULTILINE), ""),
    (re.compile(r"^\s*\*\*WORK only; not Record\.\*\*\s*$", re.MULTILINE | re.IGNORECASE), ""),
    (re.compile(r"^\s*WORK only — not Record\.?\s*$", re.MULTILINE | re.IGNORECASE), ""),
    (re.compile(r"^\s*WORK-only; not Record\.?\s*$", re.MULTILINE | re.IGNORECASE), ""),
    (re.compile(r"WORK only; not Record\.\s*", re.IGNORECASE), ""),
    (re.compile(r"work only; not Record\.\s*"), ""),
    (re.compile(r"WORK only — not Record\.?\s*", re.IGNORECASE), ""),
    (re.compile(r"WORK-only; not Record\.?\s*", re.IGNORECASE), ""),
    (re.compile(r"\(WORK only; not Record\)", re.IGNORECASE), "(non-authoritative)"),
    (re.compile(r"\(WORK only\)", re.IGNORECASE), "(non-authoritative)"),
    (re.compile(r";\s*WORK only\b", re.IGNORECASE), ""),
    (re.compile(r",\s*WORK only\b", re.IGNORECASE), ""),
    (re.compile(r" — WORK only\b[^.]*\.?", re.IGNORECASE), ""),
    (re.compile(r"\*\*WORK only\*\* — not Record\.?", re.IGNORECASE), ""),
    (re.compile(r"\*\*WORK only\*\*; not Record\.?", re.IGNORECASE), ""),
    (re.compile(r"`WORK only; not Record\.`", re.IGNORECASE), "`instrumental work — not Record`"),
    (re.compile(r"\*\*WORK only\*\*\s*[—\-]?\s*not Record[^.\n]*\.?", re.IGNORECASE), ""),
    (re.compile(r"\*\*WORK only\*\*\s+not Record", re.IGNORECASE), "**instrumental work** — not Record"),
    (re.compile(r"^-\s+-\s+", re.MULTILINE), "- "),
    (re.compile(r"First line: ``\s*$", re.MULTILINE), ""),
    (re.compile(r"^\*\*Header fence:\*\* first line ``\s*$", re.MULTILINE | re.IGNORECASE), ""),
    (re.compile(r"WORK only\b(?=[,;.)\s])", re.IGNORECASE), "instrumental work"),
)

REPLACEMENT_NOTE = "instrumental work — not Record."


def is_allowlisted(rel: str) -> bool:
    rel_posix = rel.replace("\\", "/")
    return any(rel_posix.startswith(prefix) for prefix in ALLOWLIST_PREFIXES)


def should_skip_path(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if is_allowlisted(rel):
        return True
    if path.suffix.lower() in SKIP_SUFFIXES:
        return True
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    return rel.startswith(".tmp-pytest")


def is_checkable(path: Path) -> bool:
    if not path.is_file():
        return False
    if should_skip_path(path):
        return False
    if path.name in CHECKER_SKIP_FILES:
        return False
    return path.suffix.lower() in {".md", ".mdc", ".py", ".yaml", ".yml", ".json"}


def iter_repo_files() -> list[Path]:
    out: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if is_checkable(path):
            out.append(path)
    return out


def staged_paths() -> list[Path] | None:
    proc = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    paths: list[Path] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        path = REPO_ROOT / line
        if is_checkable(path):
            paths.append(path)
    return paths


def scan_file(path: Path) -> list[str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    issues: list[str] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(line):
                issues.append(f"{rel}:{line_no}: deprecated WORK/Record phrasing")
                break
    return issues


def clean_text(text: str) -> str:
    out = text
    for pattern, repl in SWEEP_REPLACEMENTS:
        out = pattern.sub(repl, out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def sweep_file(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if path.name in CHECKER_SKIP_FILES:
        return False
    original = path.read_text(encoding="utf-8", errors="replace")
    updated = clean_text(original)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8", newline="\n")
    return True


def run_check(paths: list[Path]) -> int:
    issues: list[str] = []
    for path in paths:
        issues.extend(scan_file(path))
    if issues:
        for line in sorted(set(issues)):
            print(line, file=sys.stderr)
        print(f"check_work_record_doctrine: {len(set(issues))} violation(s)", file=sys.stderr)
        return 1
    print("[ok] work/record doctrine banner check passed")
    return 0


def run_sweep(paths: list[Path]) -> int:
    changed = 0
    for path in paths:
        if path.suffix.lower() not in {".md", ".mdc", ".py", ".yaml", ".yml", ".json"}:
            continue
        if sweep_file(path):
            changed += 1
            print(f"[apply] {path.relative_to(REPO_ROOT).as_posix()}")
    print(f"sweep_work_record_doctrine: changed={changed}")
    return 0


def resolve_paths(*, staged: bool) -> list[Path]:
    if staged:
        paths = staged_paths()
        if paths is not None:
            return paths
    return iter_repo_files()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Remove/replace deprecated phrasing")
    parser.add_argument("--staged", action="store_true", help="Scan only git staged paths")
    args = parser.parse_args()
    paths = resolve_paths(staged=args.staged)
    if args.apply:
        return run_sweep(paths)
    return run_check(paths)


if __name__ == "__main__":
    raise SystemExit(main())
