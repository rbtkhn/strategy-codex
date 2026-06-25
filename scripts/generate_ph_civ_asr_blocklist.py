#!/usr/bin/env python3
"""Regenerate volume-ii ASR blocklist JSON from the ph-civ pilot normalizer script."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PILOT = REPO_ROOT / "public/predictive-history/scripts/_pilot_asr_normalize_civ01_civ07.py"
OUT = (
    REPO_ROOT
    / "public/predictive-history/data/asr-blocklist/volume-ii-pilot.json"
)

SKIP_LITERALS = frozenset(
    {
        "Egon",
        "eanon",
        "ptia",
        "yonia",
        "SES",
        "ues",
        "ues is",
        "Ides",
        "Europe",
        "Europe is",
        "Pol",
        "peles",
        "polies",
        "polist",
        "achilles",
        "achillus",
        "ailles",
        "parmenion",
        "helenistic",
        "uel Kant",
        "Emanuel Khan",
        "the economy okay",
        "they sell off",
        "place called Canaan",
        "the Bacchae is",
        "King Xerxes",
    }
)

PILOT_SLUGS = [f"civ-{n:02d}" for n in range(1, 19)]

ALLOWED_RESIDUALS = [
    {"literal": "effing", "note": "Pygmy forest-spirit gloss; civ-03 pilot left uncertain"},
    {"literal": "zad", "note": "uncertain proper noun; civ-07 pilot left unresolved"},
    {"literal": "Macedone", "note": "uncertain; civ-01 pilot left unresolved"},
    {"literal": "Gobekli Tepes", "note": "goes-corruption artifact; re-run repair_goes_corruption"},
]


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:56] or "pattern"


def extract_pairs(source: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for old, new in re.findall(r'\("([^"]+)",\s*"([^"]+)"\)', source):
        if old == new or old in seen:
            continue
        seen.add(old)
        pairs.append((old, new))
    return pairs


def build_entries(pairs: list[tuple[str, str]]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    used_ids: set[str] = set()
    for old, new in sorted(pairs, key=lambda item: (-len(item[0]), item[0])):
        if old in SKIP_LITERALS:
            continue
        if len(old) < 4:
            continue
        entry_id = slugify(old)
        if entry_id in used_ids:
            entry_id = f"{entry_id}-{len(used_ids)}"
        used_ids.add(entry_id)
        entries.append({"id": entry_id, "literal": old, "replacement": new})
    return entries


def main() -> None:
    source = PILOT.read_text(encoding="utf-8")
    payload = {
        "version": "2026-06-09",
        "scope": "volume-ii civ-01..18",
        "pilot_slugs": PILOT_SLUGS,
        "source_script": "public/predictive-history/scripts/_pilot_asr_normalize_civ01_civ07.py",
        "allowed_residuals": ALLOWED_RESIDUALS,
        "entries": build_entries(extract_pairs(source)),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)} ({len(payload['entries'])} entries)")


if __name__ == "__main__":
    main()
