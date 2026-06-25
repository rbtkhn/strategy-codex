#!/usr/bin/env python3
"""Lightweight membrane policy checks for governed-adjacent prose and complement paths.

Enforces two membrane rules:
1. Governed-adjacent markdown must not cite runtime/artifacts as canonical authority.
2. runtime/runtime-complements files must stay inside allowed inbox/export subtrees.

Generated-surface labeling (runtime / derived membrane class) is enforced separately by
scripts/check_generated_surfaces.py (--headers-only), which check_repo_health.py already runs.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

RUNTIME_ARTIFACTS_RE = re.compile(r"runtime/artifacts/", re.I)
AUTHORITY_PHRASES = (
    "canonical",
    "record truth",
    "authoritative",
    "canonically true",
)
DOCS_SKIP_PREFIXES = (
    "docs/archive/",
    "archive/",
)

GOVERNED_SCAN_GLOBS = (
    "statecraft/synthesis/day/*.md",
    "statecraft/research/bridges/*.md",
)
GOVERNED_SCAN_FILES = (
    "docs/work-membrane-v2.md",
    "docs/harness-architecture-map.md",
    "docs/runtime-vs-record.md",
    "docs/intelligence-harness.md",
)

NEGATION_RE = re.compile(
    r"(?:\bnot\b|\bnon[-_]|do not|does not|don't|never|not a substitute)",
    re.I,
)

COMPLEMENTS_ROOT = REPO_ROOT / "runtime" / "runtime-complements"
COMPLEMENTS_ALLOWED_PREFIXES = (
    "inbox/",
    "exports/",
    "receipts/",
    "examples/",
)
COMPLEMENTS_ALLOWED_FILES = frozenset({"README.md"})


def _iter_governed_adjacent_markdown() -> list[Path]:
    paths: list[Path] = []
    for pattern in GOVERNED_SCAN_GLOBS:
        paths.extend(REPO_ROOT.glob(pattern))
    for rel in GOVERNED_SCAN_FILES:
        path = REPO_ROOT / rel
        if path.is_file():
            paths.append(path)
    return sorted(set(paths))


def _line_claims_runtime_as_authoritative(line: str) -> str | None:
    if not RUNTIME_ARTIFACTS_RE.search(line):
        return None
    if NEGATION_RE.search(line):
        return None
    lowered = line.lower()
    for phrase in AUTHORITY_PHRASES:
        if phrase in lowered:
            return phrase
    return None


def check_runtime_artifacts_not_canonical() -> list[str]:
    errors: list[str] = []
    for path in _iter_governed_adjacent_markdown():
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            errors.append(f"{path.relative_to(REPO_ROOT)}: read failed: {exc}")
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        for lineno, line in enumerate(lines, start=1):
            phrase = _line_claims_runtime_as_authoritative(line)
            if phrase:
                errors.append(
                    f"{rel}:{lineno}: runtime/artifacts cited with authority phrase "
                    f"'{phrase}' — runtime/derived is not canonical"
                )
    return errors


def _complement_rel_allowed(rel_posix: str) -> bool:
    if rel_posix in COMPLEMENTS_ALLOWED_FILES:
        return True
    return any(rel_posix.startswith(prefix) for prefix in COMPLEMENTS_ALLOWED_PREFIXES)


def check_complement_paths() -> list[str]:
    errors: list[str] = []
    if not COMPLEMENTS_ROOT.is_dir():
        return errors
    for path in COMPLEMENTS_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".json"}:
            continue
        rel = path.relative_to(COMPLEMENTS_ROOT).as_posix()
        if not _complement_rel_allowed(rel):
            errors.append(
                f"runtime/runtime-complements/{rel}: file outside allowed complement "
                "subtrees (inbox/, exports/, receipts/, examples/, README.md)"
            )
    return errors


def run_checks() -> list[str]:
    errors: list[str] = []
    errors.extend(check_runtime_artifacts_not_canonical())
    errors.extend(check_complement_paths())
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    errors = run_checks()
    if errors:
        print("membrane policy light check failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("ok: membrane policy light")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
