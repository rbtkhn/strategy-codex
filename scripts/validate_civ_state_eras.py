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

REQUIRED_SECONDARY_HEADINGS = [
    "## What This Secondary Shelf Is For",
    "## Core Clarifiers",
    "## Counterweights And Corrections",
    "## Use Rule",
    "## Where To Go Next",
]

REQUIRED_SWITCHBOARD_PHRASES = [
    "stay in the primary shelf",
    "open the era-matched secondary shelf",
    "return to the primary shelf",
    "move upward into",
]

ROLE_TAXONOMY = [
    "`chronology`",
    "`provenance`",
    "`translation`",
    "`institutional_context`",
    "`counterweight`",
    "`misreading_correction`",
]

RECURRENCE_TAXONOMY = [
    "`cross_civilizational_recurring`",
    "`civilization_specific_recurring`",
    "`era_local`",
]

PROMOTION_TAXONOMY = [
    "`local`",
    "`promotable`",
    "`promoted`",
]

INDEX_FILES = {
    "failure-mode-routes": REPO_ROOT / "statecraft" / "civ-state" / "indexes" / "failure-mode-routes.md",
    "interpretive-difficulty-map": REPO_ROOT / "statecraft" / "civ-state" / "indexes" / "interpretive-difficulty-map.md",
    "recurring-secondary-sources": REPO_ROOT / "statecraft" / "civ-state" / "indexes" / "recurring-secondary-sources.md",
    "secondary-source-promotion-ledger": REPO_ROOT / "statecraft" / "civ-state" / "indexes" / "secondary-source-promotion-ledger.md",
    "paired-reading-wedge-template": REPO_ROOT / "statecraft" / "civ-state" / "indexes" / "paired-reading-wedge-template.md",
}

PILOT_WEDGE_FILES = [
    REPO_ROOT / "statecraft" / "civ-state" / "indexes" / "paired-reading-wedge-america-medieval.md",
    REPO_ROOT / "statecraft" / "civ-state" / "indexes" / "paired-reading-wedge-rome-ancient.md",
    REPO_ROOT / "statecraft" / "civ-state" / "indexes" / "paired-reading-wedge-persia-cybernetic.md",
]

REQUIRED_WEDGE_HEADINGS = [
    "## Two Primary Anchors",
    "## One Clarifier",
    "## One Counterweight",
    "## Use Rule",
    "## Return Path",
]

SOURCE_SUPPORT_BLOCK_FILES = [
    REPO_ROOT / "statecraft" / "civ-state" / "volumes" / "civ-state-america" / "statecraft-america.md",
    REPO_ROOT / "statecraft" / "civ-state" / "volumes" / "civ-state-rome" / "statecraft-rome.md",
    REPO_ROOT / "statecraft" / "civ-state" / "persia" / "hormuz-recognition-transit-restraint.md",
    REPO_ROOT / "statecraft" / "bridges" / "marandi-civ-state-retrieval-adapter.md",
]

SOURCE_SUPPORT_FIELDS = [
    "`primary_anchor`",
    "`secondary_support_role`",
    "`secondary_support_work`",
    "`counterweight_used`",
    "`failure_mode_checked`",
    "`current_carrier_relation`",
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


def extract_section(text: str, heading: str) -> str:
    pattern = rf"^{re.escape(heading)}\s*$"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def expected_secondary_paths(volume: str, eras: list[str]) -> list[str]:
    return [f"{volume}-secondary-sources-{era}.md" for era in eras]


def extract_subsections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^##\s+(.+)$", text, re.MULTILINE))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((title, text[start:end].strip()))
    return sections


def count_list_items(section_text: str, prefix_pattern: str) -> int:
    return sum(1 for line in section_text.splitlines() if re.match(prefix_pattern, line.strip()))


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
            if "secondary-sources" not in shelf_text:
                issues.append({"path": str(shelf_reader.relative_to(REPO_ROOT)), "level": "error", "message": "Shelf-reader does not mention the secondary-sources layer"})
            for phrase in REQUIRED_SWITCHBOARD_PHRASES:
                if phrase not in shelf_text:
                    issues.append({"path": str(shelf_reader.relative_to(REPO_ROOT)), "level": "error", "message": f"Shelf-reader switchboard phrase missing: {phrase}"})

        for era in eras:
            era_path = volume_dir / f"{volume}-primary-sources-{era}.md"
            if not era_path.exists():
                issues.append({"path": str(era_path.relative_to(REPO_ROOT)), "level": "error", "message": f"Missing {era} primary-sources file"})

            secondary_path = volume_dir / f"{volume}-secondary-sources-{era}.md"
            if not secondary_path.exists():
                issues.append({"path": str(secondary_path.relative_to(REPO_ROOT)), "level": "error", "message": f"Missing {era} secondary-sources file"})
            else:
                secondary_text = read_text(secondary_path)
                for heading in REQUIRED_SECONDARY_HEADINGS:
                    if heading not in secondary_text:
                        issues.append({"path": str(secondary_path.relative_to(REPO_ROOT)), "level": "error", "message": f"Missing required secondary-sources heading: {heading}"})

                where_to_go_next = extract_section(secondary_text, "## Where To Go Next")
                expected_primary_name = f"{volume}-primary-sources-{era}.md"
                expected_bibliography_name = f"{volume}-bibliography.md"
                chapter_targets = [
                    f"civilization-{volume.removeprefix('civ-state-')}.md",
                    f"empire-{volume.removeprefix('civ-state-')}.md",
                    f"statecraft-{volume.removeprefix('civ-state-')}.md",
                ]

                if expected_primary_name not in where_to_go_next:
                    issues.append({"path": str(secondary_path.relative_to(REPO_ROOT)), "level": "error", "message": "Where To Go Next does not link back to the matching primary-source file"})
                if expected_bibliography_name not in where_to_go_next:
                    issues.append({"path": str(secondary_path.relative_to(REPO_ROOT)), "level": "error", "message": "Where To Go Next does not link back to the bibliography"})
                if not any(target in where_to_go_next for target in chapter_targets):
                    issues.append({"path": str(secondary_path.relative_to(REPO_ROOT)), "level": "error", "message": "Where To Go Next does not include a chapter-surface return path"})

        ancient_path = volume_dir / f"{volume}-primary-sources-ancient.md"
        if volume in {"civ-state-russia", "civ-state-america"} and ancient_path.exists():
            issues.append({"path": str(ancient_path.relative_to(REPO_ROOT)), "level": "error", "message": "Late-opening volume should not have an Ancient primary-sources file"})
        ancient_secondary_path = volume_dir / f"{volume}-secondary-sources-ancient.md"
        if volume in {"civ-state-russia", "civ-state-america"} and ancient_secondary_path.exists():
            issues.append({"path": str(ancient_secondary_path.relative_to(REPO_ROOT)), "level": "error", "message": "Late-opening volume should not have an Ancient secondary-sources file"})

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

        for secondary_name in expected_secondary_paths(volume, eras):
            if secondary_name not in bibliography_text:
                issues.append({"path": str(bibliography.relative_to(REPO_ROOT)), "level": "error", "message": f"Bibliography does not link to expected secondary-sources file: {secondary_name}"})

    for path in DOCTRINE_FILES:
        text = read_text(path)
        for pattern in STALE_PATTERNS:
            if re.search(pattern, text):
                issues.append({"path": str(path.relative_to(REPO_ROOT)), "level": "error", "message": f"Stale era doctrine pattern found: {pattern}"})
        if "1991" not in text:
            issues.append({"path": str(path.relative_to(REPO_ROOT)), "level": "warn", "message": "Doctrine file does not mention the 1991 boundary"})

    reader_guide = REPO_ROOT / "statecraft" / "civ-state" / "reader-guide.md"
    hybrid_references = REPO_ROOT / "statecraft" / "civ-state" / "hybrid-references.md"
    for taxonomy_file in [reader_guide, hybrid_references]:
        text = read_text(taxonomy_file)
        for term in ROLE_TAXONOMY + RECURRENCE_TAXONOMY + PROMOTION_TAXONOMY:
            if term not in text:
                issues.append({"path": str(taxonomy_file.relative_to(REPO_ROOT)), "level": "error", "message": f"Taxonomy term missing: {term}"})

    indexes_readme = REPO_ROOT / "statecraft" / "civ-state" / "indexes" / "README.md"
    indexes_readme_text = read_text(indexes_readme)
    for name, path in INDEX_FILES.items():
        if not path.exists():
            issues.append({"path": str(path.relative_to(REPO_ROOT)), "level": "error", "message": f"Missing required index surface: {name}"})
        elif path.name not in indexes_readme_text:
            issues.append({"path": str(indexes_readme.relative_to(REPO_ROOT)), "level": "error", "message": f"Indexes README does not link to {path.name}"})

    failure_routes = INDEX_FILES["failure-mode-routes"]
    if failure_routes.exists():
        for title, section in extract_subsections(read_text(failure_routes)):
            if "primary-sources" not in section:
                issues.append({"path": str(failure_routes.relative_to(REPO_ROOT)), "level": "error", "message": f"Failure-mode route '{title}' does not link a primary shelf"})
            if "secondary-sources" not in section:
                issues.append({"path": str(failure_routes.relative_to(REPO_ROOT)), "level": "error", "message": f"Failure-mode route '{title}' does not link a secondary shelf"})
            if not re.search(r"(statecraft|civilization|empire)-[a-z]+\.md", section):
                issues.append({"path": str(failure_routes.relative_to(REPO_ROOT)), "level": "error", "message": f"Failure-mode route '{title}' does not link a chapter surface"})

    difficulty_map = INDEX_FILES["interpretive-difficulty-map"]
    if difficulty_map.exists():
        for title, section in extract_subsections(read_text(difficulty_map)):
            if "primary-sources" not in section:
                issues.append({"path": str(difficulty_map.relative_to(REPO_ROOT)), "level": "error", "message": f"Interpretive difficulty section '{title}' does not link a primary shelf"})
            if "secondary-sources" not in section:
                issues.append({"path": str(difficulty_map.relative_to(REPO_ROOT)), "level": "error", "message": f"Interpretive difficulty section '{title}' does not link a secondary shelf"})
            if not re.search(r"statecraft-[a-z]+\.md", section):
                issues.append({"path": str(difficulty_map.relative_to(REPO_ROOT)), "level": "error", "message": f"Interpretive difficulty section '{title}' does not link a chapter surface"})

    recurring_sources = INDEX_FILES["recurring-secondary-sources"]
    if recurring_sources.exists():
        recurring_text = read_text(recurring_sources)
        for term in ROLE_TAXONOMY + RECURRENCE_TAXONOMY + PROMOTION_TAXONOMY:
            if term not in recurring_text:
                issues.append({"path": str(recurring_sources.relative_to(REPO_ROOT)), "level": "error", "message": f"Recurring-secondary-sources file missing taxonomy term: {term}"})
        for phrase in ["Will Durant", "Churchill, A History of the English-Speaking Peoples"]:
            if phrase not in recurring_text:
                issues.append({"path": str(recurring_sources.relative_to(REPO_ROOT)), "level": "error", "message": f"Recurring-secondary-sources file missing governed note: {phrase}"})

    promotion_ledger = INDEX_FILES["secondary-source-promotion-ledger"]
    if promotion_ledger.exists():
        promotion_text = read_text(promotion_ledger)
        for term in PROMOTION_TAXONOMY:
            if term not in promotion_text:
                issues.append({"path": str(promotion_ledger.relative_to(REPO_ROOT)), "level": "error", "message": f"Promotion ledger missing status term: {term}"})

    wedge_template = INDEX_FILES["paired-reading-wedge-template"]
    if wedge_template.exists():
        wedge_template_text = read_text(wedge_template)
        for heading in REQUIRED_WEDGE_HEADINGS:
            if heading not in wedge_template_text:
                issues.append({"path": str(wedge_template.relative_to(REPO_ROOT)), "level": "error", "message": f"Wedge template missing heading: {heading}"})

    for wedge_path in PILOT_WEDGE_FILES:
        if not wedge_path.exists():
            issues.append({"path": str(wedge_path.relative_to(REPO_ROOT)), "level": "error", "message": "Missing pilot paired reading wedge"})
            continue
        wedge_text = read_text(wedge_path)
        for heading in REQUIRED_WEDGE_HEADINGS:
            if heading not in wedge_text:
                issues.append({"path": str(wedge_path.relative_to(REPO_ROOT)), "level": "error", "message": f"Pilot wedge missing heading: {heading}"})
        primary_section = extract_section(wedge_text, "## Two Primary Anchors")
        clarifier_section = extract_section(wedge_text, "## One Clarifier")
        counterweight_section = extract_section(wedge_text, "## One Counterweight")
        return_section = extract_section(wedge_text, "## Return Path")
        if count_list_items(primary_section, r"^\d+\.\s+") != 2:
            issues.append({"path": str(wedge_path.relative_to(REPO_ROOT)), "level": "error", "message": "Pilot wedge must contain exactly 2 primary anchors"})
        if count_list_items(clarifier_section, r"^- ") != 1:
            issues.append({"path": str(wedge_path.relative_to(REPO_ROOT)), "level": "error", "message": "Pilot wedge must contain exactly 1 clarifier"})
        if count_list_items(counterweight_section, r"^- ") != 1:
            issues.append({"path": str(wedge_path.relative_to(REPO_ROOT)), "level": "error", "message": "Pilot wedge must contain exactly 1 counterweight"})
        if "primary-sources" not in return_section:
            issues.append({"path": str(wedge_path.relative_to(REPO_ROOT)), "level": "error", "message": "Pilot wedge return path must link a primary shelf"})
        if "secondary-sources" not in return_section:
            issues.append({"path": str(wedge_path.relative_to(REPO_ROOT)), "level": "error", "message": "Pilot wedge return path must link a secondary shelf"})
        if not re.search(r"(statecraft|civilization|empire)-[a-z]+\.md", return_section):
            issues.append({"path": str(wedge_path.relative_to(REPO_ROOT)), "level": "error", "message": "Pilot wedge return path must link a chapter surface"})

    retrieval_matrix = REPO_ROOT / "statecraft" / "civ-state" / "indexes" / "source-retrieval-matrix.md"
    retrieval_matrix_text = read_text(retrieval_matrix)
    for required_link in ["failure-mode-routes.md", "interpretive-difficulty-map.md", "recurring-secondary-sources.md"]:
        if required_link not in retrieval_matrix_text:
            issues.append({"path": str(retrieval_matrix.relative_to(REPO_ROOT)), "level": "error", "message": f"Source retrieval matrix missing comparative link: {required_link}"})
    if "## Source-Support Block Contract" not in retrieval_matrix_text:
        issues.append({"path": str(retrieval_matrix.relative_to(REPO_ROOT)), "level": "error", "message": "Source retrieval matrix missing source-support block contract"})

    for path in SOURCE_SUPPORT_BLOCK_FILES:
        text = read_text(path)
        block = extract_section(text, "## Source Support Block")
        if not block:
            issues.append({"path": str(path.relative_to(REPO_ROOT)), "level": "error", "message": "Missing source support block"})
            continue
        for field in SOURCE_SUPPORT_FIELDS:
            if field not in block:
                issues.append({"path": str(path.relative_to(REPO_ROOT)), "level": "error", "message": f"Source support block missing field: {field}"})

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
