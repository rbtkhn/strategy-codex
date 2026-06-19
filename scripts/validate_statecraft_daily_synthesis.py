#!/usr/bin/env python3
"""Validate the narrow structural contract for ``statecraft/daily`` synthesis notes.

This validator intentionally enforces only deterministic structure:

- active-contract daily note required section order
- monthly note required section order
- five-volume section presence and fixed bullet order
- monthly ``Functional Convergence`` labels limited to the fixed set
- explicit ``Quote anchor:`` lines meeting the 12-word floor

It does not attempt to judge synthesis quality, convergence quality, or whether a
five-volume insight is intellectually strong enough. Those remain human-audited.

Important boundary: daily validation is opt-in for files already using the active
five-volume contract. This avoids falsely failing older daily notes that have not
yet been retrofitted to the current method. The validator still reports migrated
versus legacy daily-note coverage so the shelf's contract boundary remains visible.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DAILY_DIR = REPO_ROOT / "statecraft" / "daily"

DAILY_FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
MONTHLY_FILENAME_RE = re.compile(r"^\d{4}-\d{2}\.md$")
HEADING_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
FIVE_VOLUME_LABEL_RE = re.compile(r"^\s*-\s+`([^`]+)`:", re.MULTILINE)
INLINE_QUOTE_RE = re.compile(r'"([^"\n]+)"')
WORD_RE = re.compile(r"\b[\w']+\b")

DAILY_REQUIRED_SECTIONS: tuple[str, ...] = (
    "Source Base",
    "Executive Read",
    "Dominant Themes",
    "Lane Read",
    "Five-Volume CIV-STATE Read",
    "Speaker Value From This Batch",
    "Tensions And Falsifiers",
    "Best Next Moves",
)

DAILY_OPTIONAL_TAIL: tuple[str, ...] = (
    "Companion Notes",
    "Archival Note",
)

MONTHLY_REQUIRED_SECTIONS: tuple[str, ...] = (
    "Source Base",
    "Executive Read",
    "Functional Convergence",
    "Month Arcs",
    "Lane Ownership Across The Month",
    "Five-Volume CIV-STATE Read",
    "Best Re-entry Days",
    "What The Month Clarified",
    "What The Month Still Did Not Settle",
    "Best Next Companion Notes",
)

FIVE_VOLUME_ORDER: tuple[str, ...] = (
    "China",
    "Persia",
    "Rome",
    "Russia",
    "America",
)

MONTHLY_FUNCTION_LABELS: frozenset[str] = frozenset(
    {
        "trap",
        "threshold",
        "architecture",
        "implementation",
        "battlefield",
        "legitimacy",
        "falsifier",
    }
)


def is_migrated_daily_text(text: str) -> bool:
    return "## Five-Volume CIV-STATE Read" in text


def heading_sequence(text: str) -> list[str]:
    return [m.group(1).strip() for m in HEADING_RE.finditer(text)]


def section_body(text: str, heading: str) -> str | None:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        return None
    start = match.end()
    next_match = HEADING_RE.search(text, start)
    end = next_match.start() if next_match else len(text)
    return text[start:end]


def extract_five_volume_labels(body: str) -> list[str]:
    return [m.group(1).strip() for m in FIVE_VOLUME_LABEL_RE.finditer(body)]


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def validate_quote_anchor_line(line: str, *, min_words: int = 12) -> str | None:
    if "Quote anchor:" not in line:
        return None
    quotes = INLINE_QUOTE_RE.findall(line)
    if not quotes:
        return "explicit Quote anchor line missing quoted excerpt"
    quote_text = quotes[0]
    words = count_words(quote_text)
    if words < min_words:
        return f"Quote anchor has {words} words; requires at least {min_words}"
    return None


def validate_daily_section_order(headings: list[str]) -> list[str]:
    errors: list[str] = []
    if headings[: len(DAILY_REQUIRED_SECTIONS)] != list(DAILY_REQUIRED_SECTIONS):
        errors.append(
            "required daily section order mismatch: expected "
            + " -> ".join(DAILY_REQUIRED_SECTIONS)
        )
        return errors
    remaining = headings[len(DAILY_REQUIRED_SECTIONS) :]
    expected_tail: list[str] = []
    idx = 0
    for allowed in DAILY_OPTIONAL_TAIL:
        if idx < len(remaining) and remaining[idx] == allowed:
            expected_tail.append(allowed)
            idx += 1
    if remaining != expected_tail:
        errors.append(
            "unexpected daily trailing sections: found "
            + " -> ".join(remaining)
            + "; allowed tail is Companion Notes -> Archival Note"
        )
    return errors


def validate_daily_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    headings = heading_sequence(text)
    errors.extend(validate_daily_section_order(headings))

    five_body = section_body(text, "Five-Volume CIV-STATE Read")
    if five_body is None:
        errors.append("missing Five-Volume CIV-STATE Read section")
    else:
        labels = extract_five_volume_labels(five_body)
        if labels != list(FIVE_VOLUME_ORDER):
            errors.append(
                "Five-Volume CIV-STATE Read labels mismatch: expected "
                + " -> ".join(FIVE_VOLUME_ORDER)
                + ", found "
                + " -> ".join(labels)
            )

    for line_no, line in enumerate(text.splitlines(), start=1):
        quote_err = validate_quote_anchor_line(line)
        if quote_err:
            errors.append(f"line {line_no}: {quote_err}")

    return errors


def validate_monthly_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    headings = heading_sequence(text)
    if headings != list(MONTHLY_REQUIRED_SECTIONS):
        errors.append(
            "required monthly section order mismatch: expected "
            + " -> ".join(MONTHLY_REQUIRED_SECTIONS)
        )

    five_body = section_body(text, "Five-Volume CIV-STATE Read")
    if five_body is None:
        errors.append("missing Five-Volume CIV-STATE Read section")
    else:
        labels = extract_five_volume_labels(five_body)
        if labels != list(FIVE_VOLUME_ORDER):
            errors.append(
                "Five-Volume CIV-STATE Read labels mismatch: expected "
                + " -> ".join(FIVE_VOLUME_ORDER)
                + ", found "
                + " -> ".join(labels)
            )

    convergence_body = section_body(text, "Functional Convergence")
    if convergence_body is None:
        errors.append("missing Functional Convergence section")
    else:
        labels = extract_five_volume_labels(convergence_body)
        if not labels:
            errors.append("Functional Convergence has no explicit function bullets")
        invalid = [label for label in labels if label not in MONTHLY_FUNCTION_LABELS]
        if invalid:
            errors.append(
                "Functional Convergence contains invalid labels: "
                + ", ".join(invalid)
            )
    return errors


def validate_daily_dir(daily_dir: Path) -> list[str]:
    errors: list[str] = []
    if not daily_dir.is_dir():
        return [f"{daily_dir}: missing daily synthesis directory"]

    for path in sorted(daily_dir.glob("*.md")):
        name = path.name
        if DAILY_FILENAME_RE.fullmatch(name):
            text = path.read_text(encoding="utf-8")
            if not is_migrated_daily_text(text):
                continue
            for err in validate_daily_file(path):
                errors.append(f"{path.relative_to(REPO_ROOT)}: {err}")
        elif MONTHLY_FILENAME_RE.fullmatch(name):
            for err in validate_monthly_file(path):
                errors.append(f"{path.relative_to(REPO_ROOT)}: {err}")
    return errors


def collect_daily_shelf_counts(daily_dir: Path) -> tuple[int, int, int]:
    migrated_daily = 0
    legacy_daily = 0
    monthly = 0

    for path in sorted(daily_dir.glob("*.md")):
        if DAILY_FILENAME_RE.fullmatch(path.name):
            text = path.read_text(encoding="utf-8")
            if is_migrated_daily_text(text):
                migrated_daily += 1
            else:
                legacy_daily += 1
        elif MONTHLY_FILENAME_RE.fullmatch(path.name):
            monthly += 1

    return migrated_daily, legacy_daily, monthly


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--daily-dir",
        type=Path,
        default=DEFAULT_DAILY_DIR,
        help="Directory containing statecraft daily/monthly synthesis notes",
    )
    args = parser.parse_args()

    daily_dir = args.daily_dir.resolve()
    errors = validate_daily_dir(daily_dir)
    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        print(
            f"validate_statecraft_daily_synthesis: {len(errors)} error(s)",
            file=sys.stderr,
        )
        return 1

    migrated_daily_count, legacy_daily_count, monthly_count = collect_daily_shelf_counts(
        daily_dir
    )
    print(
        "ok: state synthesis validated "
        f"({migrated_daily_count} migrated daily note(s), "
        f"{legacy_daily_count} legacy daily note(s), "
        f"{monthly_count} month note(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
