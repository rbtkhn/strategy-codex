#!/usr/bin/env python3
"""Beginner-friendly daily journal draft helper for cici-ai OB1 members.

This script turns simple tagged notes into the shared daily journal template.
It does not commit, push, or publish anything. The human must review the draft
before saving it into GitHub.

Usage examples:
  python scripts/cici_daily_journal_helper.py --date 2026-05-07 --notes-file notes.txt
  type notes.txt | python scripts/cici_daily_journal_helper.py --date 2026-05-07
  python scripts/cici_daily_journal_helper.py --date 2026-05-07 --note "worked on: ..."
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import date as date_cls, datetime
from pathlib import Path
import sys


DEFAULT_OUTPUT_DIR = Path("docs/personal/daily-journal")

SECTION_ALIASES = {
    "worked on": "worked_on",
    "worked": "worked_on",
    "change": "changed",
    "changed": "changed",
    "blocked": "blocked",
    "blocker": "blocked",
    "next": "next",
    "plan": "next",
    "plan next": "next",
    "evidence": "evidence",
    "notes": "evidence",
}

SECTION_ORDER = ["worked_on", "changed", "blocked", "next", "evidence"]
SECTION_TITLES = {
    "worked_on": "What I worked on",
    "changed": "What changed",
    "blocked": "What is blocked",
    "next": "What I plan to do next",
    "evidence": "Evidence or notes",
}


@dataclass
class JournalDraft:
    date: str
    sections: dict[str, list[str]] = field(
        default_factory=lambda: {key: [] for key in SECTION_ORDER}
    )
    leftovers: list[str] = field(default_factory=list)


def _normalize_date(raw: str | None) -> str:
    if not raw:
        return date_cls.today().isoformat()
    parsed = datetime.strptime(raw, "%Y-%m-%d").date()
    return parsed.isoformat()


def _read_notes(args: argparse.Namespace) -> list[str]:
    notes: list[str] = []
    if args.note:
        notes.extend(args.note)
    if args.notes_file:
        notes_text = Path(args.notes_file).read_text(encoding="utf-8")
        notes.extend(notes_text.splitlines())
    if not notes and not sys.stdin.isatty():
        notes.extend(sys.stdin.read().splitlines())
    return notes


def _strip_bullet_prefix(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith(("- ", "* ", "• ")):
        return stripped[2:].strip()
    return stripped


def _match_section(line: str) -> tuple[str | None, str]:
    if ":" not in line:
        return None, line
    prefix, rest = line.split(":", 1)
    key = SECTION_ALIASES.get(prefix.strip().lower())
    if not key:
        return None, line
    return key, rest.strip()


def build_draft(draft_date: str, raw_lines: list[str]) -> JournalDraft:
    draft = JournalDraft(date=draft_date)
    current_section: str | None = None

    for raw in raw_lines:
        line = raw.rstrip()
        if not line.strip():
            current_section = None
            continue

        section_key, content = _match_section(line)
        if section_key:
            current_section = section_key
            if content:
                draft.sections[section_key].append(_strip_bullet_prefix(content))
            continue

        item = _strip_bullet_prefix(line)
        if current_section and item:
            draft.sections[current_section].append(item)
        elif item:
            draft.leftovers.append(item)

    if draft.leftovers:
        if not draft.sections["worked_on"]:
            draft.sections["worked_on"].extend(draft.leftovers)
        else:
            draft.sections["evidence"].extend(draft.leftovers)

    if not draft.sections["blocked"]:
        draft.sections["blocked"].append("None noted")
    if not draft.sections["next"]:
        draft.sections["next"].append("Needs follow-up")
    if not draft.sections["evidence"]:
        draft.sections["evidence"].append("Needs follow-up")
    return draft


def render_markdown(draft: JournalDraft) -> str:
    lines = [f"# Daily Journal - {draft.date}", ""]
    for key in SECTION_ORDER:
        lines.append(f"## {SECTION_TITLES[key]}")
        items = draft.sections[key]
        if not items:
            lines.append("- Needs follow-up")
        else:
            for item in items:
                lines.append(f"- {item}")
        lines.append("")
    lines.append("Review before saving, then commit and push to GitHub.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Draft a beginner-friendly daily journal entry from simple notes."
    )
    parser.add_argument(
        "--date",
        help="Journal date in YYYY-MM-DD format. Defaults to today.",
    )
    parser.add_argument(
        "--notes-file",
        help="Path to a text file with rough notes.",
    )
    parser.add_argument(
        "--note",
        action="append",
        help="Add one note line directly on the command line. Can be repeated.",
    )
    parser.add_argument(
        "--output",
        help="Write the markdown draft to this file instead of printing it.",
    )
    args = parser.parse_args()

    draft_date = _normalize_date(args.date)
    raw_lines = _read_notes(args)
    draft = build_draft(draft_date, raw_lines)
    markdown = render_markdown(draft)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
