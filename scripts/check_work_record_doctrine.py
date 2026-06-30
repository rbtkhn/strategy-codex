#!/usr/bin/env python3
"""Fail if deprecated WORK/Record banner appears outside allowlisted paths."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

BANNER_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"^WORK only; not Record\.\s*$", re.IGNORECASE), "WORK only; not Record."),
    (re.compile(r"^work only; not Record\.\s*$"), "work only; not Record."),
    (re.compile(r"^\*\*Work only; not Record\.\*\*\s*$", re.IGNORECASE), "**Work only; not Record.**"),
    (re.compile(r"^\*\*WORK only; not Record\.\*\*\s*$"), "**WORK only; not Record.**"),
    (re.compile(r"^WORK only — not Record\s*$", re.IGNORECASE), "WORK only — not Record"),
)

ALLOWLIST_PREFIXES: tuple[str, ...] = (
    "docs/archive/",
    "archive/grace-mar-instance/",
    "archive/grace-mar-corpus/",
    "public/predictive-history/",
    ".git/",
    "node_modules/",
)

SKIP_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip"})

SUBSTRING_SKIP_FILES = frozenset(
    {
        "check_work_record_doctrine.py",
        "sweep_script_emitters.py",
        "sweep_work_record_docstrings.py",
    }
)

SUBSTRING_PATTERN = re.compile(r"WORK only|work only; not Record", re.IGNORECASE)


def is_allowlisted(rel: str) -> bool:
    rel_posix = rel.replace("\\", "/")
    return any(rel_posix.startswith(prefix) for prefix in ALLOWLIST_PREFIXES)


def scan_file(path: Path) -> list[str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if is_allowlisted(rel):
        return []
    if path.suffix.lower() in SKIP_SUFFIXES:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    issues: list[str] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pattern, label in BANNER_PATTERNS:
            if pattern.match(line.rstrip()):
                issues.append(f"{rel}:{line_no}: deprecated banner `{label}`")
    return issues


def iter_scan_roots() -> list[Path]:
    roots = [
        REPO_ROOT / "statecraft",
        REPO_ROOT / "docs",
        REPO_ROOT / "codex",
        REPO_ROOT / "scripts",
        REPO_ROOT / "skills",
        REPO_ROOT / ".cursor",
        REPO_ROOT / "README.md",
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "contributing.md",
    ]
    out: list[Path] = []
    for root in roots:
        if root.is_file():
            out.append(root)
        elif root.is_dir():
            out.extend(p for p in root.rglob("*") if p.is_file())
    return out


def scan_scripts_substring(path: Path) -> list[str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if not rel.startswith("scripts/") or path.name in SUBSTRING_SKIP_FILES:
        return []
    if path.suffix != ".py":
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    issues: list[str] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if SUBSTRING_PATTERN.search(line):
            issues.append(f"{rel}:{line_no}: deprecated WORK/Record phrasing in script")
    return issues


def run_check() -> int:
    issues: list[str] = []
    for path in iter_scan_roots():
        issues.extend(scan_file(path))
        issues.extend(scan_scripts_substring(path))
    if issues:
        for line in sorted(issues):
            print(line, file=sys.stderr)
        print(f"check_work_record_doctrine: {len(issues)} violation(s)", file=sys.stderr)
        return 1
    print("[ok] work/record doctrine banner check passed")
    return 0


REPLACEMENT_NOTE = "This surface is non-authoritative and subject to revision."


def sweep_file(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if is_allowlisted(rel) or path.suffix.lower() in SKIP_SUFFIXES:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)
    changed = False
    new_lines: list[str] = []
    for line in lines:
        stripped = line.rstrip("\r\n")
        matched = False
        for pattern, _ in BANNER_PATTERNS:
            if pattern.match(stripped):
                matched = True
                changed = True
                if rel.endswith("README.md") or "/notes/README.md" in rel:
                    new_lines.append(REPLACEMENT_NOTE + "\n")
                break
        if not matched:
            new_lines.append(line)
    if changed:
        path.write_text("".join(new_lines), encoding="utf-8", newline="\n")
    return changed


def run_sweep(*, apply: bool) -> int:
    changed = 0
    for path in iter_scan_roots():
        if apply and sweep_file(path):
            changed += 1
            print(f"[apply] {path.relative_to(REPO_ROOT).as_posix()}")
        elif not apply:
            issues = scan_file(path)
            if issues:
                for issue in issues:
                    print(f"[plan] {issue}")
                changed += len(issues)
    print(f"sweep_work_record_doctrine: {'changed' if apply else 'issues'}={changed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Remove/replace banner lines")
    args = parser.parse_args()
    if args.apply:
        return run_sweep(apply=True)
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
