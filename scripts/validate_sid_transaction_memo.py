#!/usr/bin/env python3
"""Validate SID Transaction Memo structure (partner-review shape).

Checks frontmatter, required sections, pin-cite table, falsifiers, and disclaimer.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
EMBARGO_VALUES = frozenset({"public-ok", "client-only", "internal-only"})
REQUIRED_SECTIONS: tuple[str, ...] = (
    "Matter Question",
    "Executive Read",
    "Escalation Ladder",
    "Pin-Cites (receipts)",
    "Falsifiers",
    "Off-Ramp / Review Trigger",
    "Disclaimer",
)
DISCLAIMER_PHRASES = (
    "not legal counsel",
    "judgment support",
    "internal professional use",
)

def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields

def section_headings(text: str) -> list[str]:
    return HEADING_RE.findall(text)

def validate_pin_cite_table(text: str) -> list[str]:
    errors: list[str] = []
    if "## Pin-Cites" not in text:
        return ["missing Pin-Cites section"]
    pin_section = text.split("## Pin-Cites", 1)[1]
    if "## Falsifiers" in pin_section:
        pin_section = pin_section.split("## Falsifiers", 1)[0]
    rows = [
        line
        for line in pin_section.splitlines()
        if line.strip().startswith("|") and not re.match(r"^\|\s*[-:| ]+\|", line.strip())
    ]
    data_rows = [r for r in rows if "Claim" not in r or "Grade" not in r]
    if len(data_rows) < 1:
        errors.append("Pin-Cites table needs at least one data row")
    return errors

def validate_falsifiers(text: str) -> list[str]:
    if "## Falsifiers" not in text:
        return ["missing Falsifiers section"]
    section = text.split("## Falsifiers", 1)[1]
    if "## Off-Ramp" in section:
        section = section.split("## Off-Ramp", 1)[0]
    bullets = [line for line in section.splitlines() if line.strip().startswith("-")]
    if not bullets:
        return ["Falsifiers section needs at least one bullet"]
    return []

def validate_disclaimer(text: str) -> list[str]:
    lowered = text.lower()
    missing = [phrase for phrase in DISCLAIMER_PHRASES if phrase not in lowered]
    if missing:
        return [f"Disclaimer missing expected phrase: {missing[0]}"]
    return []

def validate_memo_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    fm = parse_frontmatter(text)
    if not fm:
        errors.append("missing YAML frontmatter (--- block)")
    else:
        if fm.get("sid_deliverable") != "transaction-memo":
            errors.append("frontmatter sid_deliverable must be transaction-memo")
        embargo = fm.get("embargo", "")
        if embargo and embargo not in EMBARGO_VALUES:
            errors.append(
                f"embargo must be one of {sorted(EMBARGO_VALUES)}; got {embargo!r}"
            )
        if not fm.get("theater"):
            errors.append("frontmatter theater is required")
        if not fm.get("matter_date"):
            errors.append("frontmatter matter_date is required")

    headings = section_headings(text)
    for section in REQUIRED_SECTIONS:
        if section not in headings:
            errors.append(f"missing required section: ## {section}")

    errors.extend(validate_pin_cite_table(text))
    errors.extend(validate_falsifiers(text))
    errors.extend(validate_disclaimer(text))
    return errors

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, required=True, help="Memo markdown file")
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    path = args.path.resolve()
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1
    errors = validate_memo_file(path)
    if errors:
        for err in errors:
            print(f"FAIL {path.name}: {err}", file=sys.stderr)
        return 1
    print(f"OK {path.name}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
