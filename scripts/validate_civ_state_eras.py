#!/usr/bin/env python3
"""
Validate CIV-STATE era structure and chronology doctrine.

Usage:
  python scripts/validate_civ_state_eras.py
  python scripts/validate_civ_state_eras.py --json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOLUMES_DIR = REPO_ROOT / "statecraft" / "civ-state" / "volumes"

EXPECTED_VOLUMES = {
    "civ-state-china": ["ancient", "medieval", "colonial", "industrial", "cybernetic"],
    "civ-state-persia": ["ancient", "medieval", "colonial", "industrial", "cybernetic"],
    "civ-state-rome": ["ancient", "medieval", "colonial", "industrial", "cybernetic"],
    "civ-state-russia": ["medieval", "colonial", "industrial", "cybernetic"],
    "civ-state-america": ["medieval", "colonial", "industrial", "cybernetic"],
}

REQUIRED_SHELF_READER_HEADINGS = [
    "## What This Shelf Is For",
    "## How To Read The Eras",
    "## What Each Era Is Doing",
    "## What To Look For",
    "## Where To Go Next",
]

DOCTRINE_FILES = [
    REPO_ROOT / "statecraft" / "README.md",
    REPO_ROOT / "statecraft" / "civ-state" / "README.md",
    REPO_ROOT / "statecraft" / "civ-state" / "power-truth-time-retrieval-checklist.md",
    REPO_ROOT / "statecraft" / "civ-state" / "power-truth-time-annex.md",
]

STALE_PATTERNS = [
    r"Industrial`?\s*->\s*`?1945",
    r"Cybernetic`?\s*->\s*`?1945-present",
    r"post-1945 age",
    r"post-1945 object",
]


def count_primary_source_entries(text: str) -> int:
    count = 0
    in_primary = False
    for raw in text.splitlines():
        line = raw.strip()
        if line == "## Primary Sources":
            in_primary = True
            continue
        if not in_primary:
            continue
        if line.startswith("## Retrieval Priority") or "retrieval priority:" in line.lower():
            break
        if re.match(r"^\d+\.\s+", line):
            count += 1
            continue
        if line.startswith("- "):
            item = line[2:].strip()
            if item and not item.endswith(":"):
                count += 1
    return count


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate() -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    for volume, eras in EXPECTED_VOLUMES.items():
        volume_dir = VOLUMES_DIR / volume
        bibliography = volume_dir / f"{volume}-bibliography.md"
        if not bibliography.exists():
            issues.append({"path": str(bibliography.relative_to(REPO_ROOT)), "level": "error", "message": "Missing bibliography index"})
            continue

        bibliography_text = read_text(bibliography)
        if volume in {"civ-state-russia", "civ-state-america"} and "three-era" in bibliography_text:
            issues.append({"path": str(bibliography.relative_to(REPO_ROOT)), "level": "error", "message": "Stale three-era language remains"})

        shelf_reader = volume_dir / f"{volume}-shelf-reader.md"
        if not shelf_reader.exists():
            issues.append({"path": str(shelf_reader.relative_to(REPO_ROOT)), "level": "error", "message": "Missing shelf-reader file"})
        else:
            shelf_text = read_text(shelf_reader)
            for heading in REQUIRED_SHELF_READER_HEADINGS:
                if heading not in shelf_text:
                    issues.append({"path": str(shelf_reader.relative_to(REPO_ROOT)), "level": "error", "message": f"Missing required shelf-reader heading: {heading}"})

        for era in eras:
            era_path = volume_dir / f"{volume}-primary-sources-{era}.md"
            if not era_path.exists():
                issues.append({"path": str(era_path.relative_to(REPO_ROOT)), "level": "error", "message": f"Missing {era} primary-sources file"})

        ancient_path = volume_dir / f"{volume}-primary-sources-ancient.md"
        if volume in {"civ-state-russia", "civ-state-america"} and ancient_path.exists():
            issues.append({"path": str(ancient_path.relative_to(REPO_ROOT)), "level": "error", "message": "Late-opening volume should not have an Ancient primary-sources file"})

        industrial_path = volume_dir / f"{volume}-primary-sources-industrial.md"
        if industrial_path.exists():
            industrial_text = read_text(industrial_path)
            if "1991" not in industrial_text:
                issues.append({"path": str(industrial_path.relative_to(REPO_ROOT)), "level": "error", "message": "Industrial shelf does not mention the 1991 endpoint"})

        cybernetic_path = volume_dir / f"{volume}-primary-sources-cybernetic.md"
        if cybernetic_path.exists():
            cybernetic_text = read_text(cybernetic_path)
            cybernetic_count = count_primary_source_entries(cybernetic_text)
            if cybernetic_count != 25:
                issues.append({"path": str(cybernetic_path.relative_to(REPO_ROOT)), "level": "error", "message": f"Cybernetic shelf must contain exactly 25 primary-source entries, found {cybernetic_count}"})
            if "post-1991" not in cybernetic_text and "after the 1991 industrial endpoint" not in cybernetic_text and "1991 as industrial endpoint" not in cybernetic_text:
                issues.append({"path": str(cybernetic_path.relative_to(REPO_ROOT)), "level": "error", "message": "Cybernetic shelf does not state its post-1991 opening clearly"})

        readme_path = volume_dir / "README.md"
        if readme_path.exists():
            readme_text = read_text(readme_path)
            if volume in {"civ-state-russia", "civ-state-america"} and re.search(r"^## Ancient\s*$", readme_text, re.MULTILINE):
                issues.append({"path": str(readme_path.relative_to(REPO_ROOT)), "level": "error", "message": "Late-opening volume README still exposes an Ancient era section"})

    for path in DOCTRINE_FILES:
        text = read_text(path)
        for pattern in STALE_PATTERNS:
            if re.search(pattern, text):
                issues.append({"path": str(path.relative_to(REPO_ROOT)), "level": "error", "message": f"Stale era doctrine pattern found: {pattern}"})
        if "1991" not in text:
            issues.append({"path": str(path.relative_to(REPO_ROOT)), "level": "warn", "message": "Doctrine file does not mention the 1991 boundary"})

    return issues


def format_text(issues: list[dict[str, str]]) -> str:
    if not issues:
        return "CIV-STATE era doctrine valid."
    lines: list[str] = []
    for issue in issues:
        marker = "ERROR" if issue["level"] == "error" else "WARN"
        lines.append(f"[{marker}] {issue['path']}: {issue['message']}")
    lines.append(f"\n{len(issues)} issue(s) found.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CIV-STATE era structure and chronology doctrine.")
    parser.add_argument("--json", action="store_true", help="Output issues as JSON")
    args = parser.parse_args()

    issues = validate()
    if args.json:
        print(json.dumps(issues, indent=2))
    else:
        print(format_text(issues))
    return 1 if any(issue["level"] == "error" for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
