#!/usr/bin/env python3
"""Regenerate founding-members ASR blocklist JSON from work_jiang replacement SSOT."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WJ_DIR = REPO_ROOT / "scripts" / "work_jiang"
if str(WJ_DIR) not in sys.path:
    sys.path.insert(0, str(WJ_DIR))

from asr_transcript_replacements import FOUNDING_MEMBERS_REPLACEMENTS  # noqa: E402

OUT = (
    REPO_ROOT
    / "statecraft/civ-lens/jiang/ph-civ/data/asr-blocklist/founding-members-pilot.json"
)

# Chat handles / uncertain tokens — presence is OK after cleanup.
ALLOWED_RESIDUALS = [
    {"literal": "Mr. label", "note": "livestream chat username; not a proper noun"},
    {"literal": "Wakar", "note": "chat username"},
    {"literal": "Ankodu", "note": "chat username"},
    {"literal": "Mikl G", "note": "chat username"},
    {"literal": "Sarin Coron", "note": "chat username"},
    {"literal": "Go to go", "note": "chat username"},
    {"literal": "Nome says", "note": "chat fragment"},
    {"literal": "Marin Nathal", "note": "Twitter handle spelling uncertain; verify against @"},
]

MIN_LITERAL_LEN = 4


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:56] or "pattern"


def build_entries(pairs: list[tuple[str, str]]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    used_ids: set[str] = set()
    allowed = {item["literal"] for item in ALLOWED_RESIDUALS}
    for old, new in sorted(pairs, key=lambda item: (-len(item[0]), item[0])):
        if old == new or old in allowed:
            continue
        if len(old) < MIN_LITERAL_LEN:
            continue
        entry_id = slugify(old)
        if entry_id in used_ids:
            entry_id = f"{entry_id}-{len(used_ids)}"
        used_ids.add(entry_id)
        entries.append({"id": entry_id, "literal": old, "replacement": new})
    return entries


def main() -> None:
    payload = {
        "version": "2026-06-10",
        "scope": "predictive-history founding-members livestreams (statecraft archive)",
        "pilot_slugs": ["founding-members-01"],
        "source_ssot": "scripts/work_jiang/asr_transcript_replacements.py:FOUNDING_MEMBERS_REPLACEMENTS",
        "regenerate": "python scripts/generate_founding_members_asr_blocklist.py",
        "apply": "python scripts/normalize_statecraft_source_asr.py <source.md> --write",
        "validate": "python scripts/validate_statecraft_asr_blocklist.py",
        "allowed_residuals": ALLOWED_RESIDUALS,
        "entries": build_entries(FOUNDING_MEMBERS_REPLACEMENTS),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)} ({len(payload['entries'])} entries)")


if __name__ == "__main__":
    main()
