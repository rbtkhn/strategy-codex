#!/usr/bin/env python3
"""Strip deprecated WORK/Record phrasing from scripts/ docstrings and string literals."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"

SKIP_FILES = frozenset(
    {
        "check_work_record_doctrine.py",
        "sweep_script_emitters.py",
        "sweep_work_record_docstrings.py",
    }
)

REPLACEMENTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"^\s*WORK only; not Record\.\s*", re.MULTILINE | re.IGNORECASE), ""),
    (re.compile(r"WORK only; not Record\.\s*", re.IGNORECASE), ""),
    (re.compile(r"WORK only — not Record\.?\s*", re.IGNORECASE), ""),
    (re.compile(r"\(WORK only; not Record\)", re.IGNORECASE), "(non-authoritative)"),
    (re.compile(r"\(WORK only\)", re.IGNORECASE), "(non-authoritative)"),
    (re.compile(r";\s*WORK only\b", re.IGNORECASE), ""),
    (re.compile(r",\s*WORK only\b", re.IGNORECASE), ""),
    (re.compile(r" — WORK only\b[^.]*\.?", re.IGNORECASE), ""),
    (re.compile(r"\*\*WORK only\*\* — not Record\.?", re.IGNORECASE), ""),
    (re.compile(r"WORK only\b(?=[,;.)\s])", re.IGNORECASE), "non-authoritative"),
)


def clean_text(text: str) -> str:
    out = text
    for pattern, repl in REPLACEMENTS:
        out = pattern.sub(repl, out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def main() -> int:
    changed = 0
    for path in sorted(SCRIPTS.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix not in {".py", ".md"}:
            continue
        if path.name in SKIP_FILES:
            continue
        original = path.read_text(encoding="utf-8", errors="replace")
        updated = clean_text(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed += 1
            print(f"[apply] {path.relative_to(REPO_ROOT).as_posix()}")
    print(f"sweep_work_record_docstrings: changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
