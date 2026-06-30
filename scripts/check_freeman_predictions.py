#!/usr/bin/env python3
"""Validate statecraft/voices/freeman/freeman-predictions.md against Freeman pilot notes."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.md"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from freeman_prediction_pilot import (  # noqa: E402
    FREEMAN_PILOT_EVENT_ORDER,
    FREEMAN_SPEAKER,
    JAN_21_CAPTURE,
)
from prediction_lib import collect_prediction_notes  # noqa: E402

SECTION_RE = re.compile(r"^## ([a-z][a-z0-9_]+)\s*$", re.M)
TABLE_HEADER = "| date | speech_act | stance | capture | note |"
CAPTURE_LINK_RE = re.compile(r"\]\((\.\./\.\./\.\./source-archive/statecraft/[^)]+)\)")
NOTE_LINK_RE = re.compile(r"\]\(\.\./\.\./notes/predictions/([^)]+)\)")

def table_rows_for_section(text: str, event_id: str) -> list[str]:
    marker = f"## {event_id}"
    start = text.find(marker)
    if start < 0:
        return []
    chunk = text[start:]
    nxt = chunk.find("\n## ", len(marker))
    if nxt >= 0:
        chunk = chunk[:nxt]
    rows: list[str] = []
    for line in chunk.splitlines():
        if line.startswith("| 20") and "|" in line[1:]:
            rows.append(line)
    return rows

def run_check(*, path: Path) -> tuple[list[str], list[str]]:
    issues: list[str] = []
    warnings: list[str] = []
    if not path.is_file():
        return [f"missing {path.relative_to(REPO_ROOT)}"], warnings

    text = path.read_text(encoding="utf-8")
    sections = SECTION_RE.findall(text)
    if sections != list(FREEMAN_PILOT_EVENT_ORDER):
        issues.append(
            f"expected sections {list(FREEMAN_PILOT_EVENT_ORDER)!r}; got {sections!r}"
        )

    pilot_notes = [
        n
        for n in collect_prediction_notes()
        if n.speaker == FREEMAN_SPEAKER and n.event_id in FREEMAN_PILOT_EVENT_ORDER
    ]
    note_paths_in_file: set[str] = set()
    total_rows = 0
    jan21_sections = 0
    jan21_notes: set[str] = set()

    for event_id in FREEMAN_PILOT_EVENT_ORDER:
        chunk_start = text.find(f"## {event_id}")
        chunk = text[chunk_start:] if chunk_start >= 0 else ""
        if TABLE_HEADER not in chunk:
            issues.append(f"{event_id}: missing column header")
        rows = table_rows_for_section(text, event_id)
        expected = sum(1 for n in pilot_notes if n.event_id == event_id)
        if len(rows) != expected:
            issues.append(f"{event_id}: expected {expected} table rows, found {len(rows)}")
        total_rows += len(rows)
        for row in rows:
            cap = CAPTURE_LINK_RE.search(row)
            note = NOTE_LINK_RE.search(row)
            if not cap:
                issues.append(f"{event_id}: missing capture link in row")
            elif not (REPO_ROOT / cap.group(1).replace("\\", "/").removeprefix("../../../")).is_file():
                issues.append(f"{event_id}: bad capture link in row {row[:60]}...")
            if note:
                note_paths_in_file.add(note.group(1))
            if cap and cap.group(1).endswith(
                "source-judging-freedom-amb-chas-freeman-a-ceasefire-or-a-pause-2025-01-21.md"
            ):
                jan21_sections += 1
                if note:
                    jan21_notes.add(note.group(1))

    if total_rows != len(pilot_notes):
        issues.append(f"total rows {total_rows} != pilot notes {len(pilot_notes)}")

    for note in pilot_notes:
        if Path(note.file).name not in note_paths_in_file:
            issues.append(f"missing note in shelf: {note.file}")

    if jan21_sections < 2:
        issues.append("Jan 21 capture must appear in at least 2 event sections")
    if len(jan21_notes) < 2:
        issues.append("Jan 21 rows must link to distinct prediction notes")

    return issues, warnings

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=DEFAULT_PATH)
    args = ap.parse_args()
    issues, warnings = run_check(path=args.path)
    for line in warnings:
        print(f"[warn] {line}")
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"check_freeman_predictions: {len(issues)} violation(s)", file=sys.stderr)
        return 1
    print("[ok] freeman-predictions.md valid")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
