#!/usr/bin/env python3
"""Source-section ship — 2026-06-28 Dialogue Works Aguilar Syria/Yemen breaking interview."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    prepare_section_patch_body,
    validate_section_anchors,
    write_interview_section_patch_capture,
)

DAY = ROOT / "source-archive/statecraft/2026-06-28"

CAPTURE = (
    "source-dialogue-works-anthony-aguilar-israel-ground-attack-syria-saudi-yemen-war-iran-ceasefire-2026-06-28.md"
)

HOST = "Nima Alkhorshid"
GUEST = "Anthony Aguilar"

SECTION_TITLES = [
    "Breaking Open — Ceasefire Doha Lebanon Yemen Syria",
    "Iran MOU Framework — Three Diplomatic Tracks",
    "Singapore Ship — Hormuz Channel And Doha Talks",
    "Escalation Loop — Spillover And Speed Analogy",
    "Syria Context — Jolani Factions And Abidin Resistance",
    "Abidin Jamla — Golan Incursion Detail",
    "Map Segment — Occupied Zone And Damascus Axis",
    "David Corridor — Greater Israel And Euphrates Bases",
    "Yemen HTA Buildup — Saudi Tribal Alliance Versus Houthis",
    "Houthi Saudi Invasion — Back Channel And Fifth Column",
    "US Base Inventory — Saudi Bahrain Jordan Targets",
    "Iran Asymmetric Map — US Bases And World War Expansion",
    "Lebanon Destruction — Gaza Tactics IDF Ground Limits",
    "Qatar Powder Keg — Clause One Dead Regional Fronts",
    "Jolani Condemnation — 1974 Disengagement Violations",
    "Trump Ceasefire — Manob School And Diplomacy Or War",
    "Iraq Kurdistan — Ground Invasion Buildup Theory",
    "War Midpoint Close — Highway To Hell And Campaign Plug",
]

SECTION_ANCHORS = [
    "What's the um I mean the ceasefire has been agreed",
    "So then we saw the the the ship, most notably the Singaporean ship",
    "So this pattern that we're now seeing, since we've seen since the the day this thing was signed",
    "So you talked about Syria and there is significant movement in Syria",
    "There was um so let's consider this uh what we woke up to",
    "So, let me just show the map just so you can explain to the audience",
    "Exactly. If you look at the terrain, the geography of where Israel is already occupying",
    "Now the other thing I wanted to speak to you about was again it made no sense to me",
    "There was these conversations I'm hearing it in the back channels actually that the Houthis may try and invade Saudi Arabia",
    "And really uh if you're if you're on the the Iranian side looking at that as a tactician",
    "So if you're if you're Iran and you're looking at this from the asymmetric standpoint",
    "Now, coming back to Lebanon, things are really really bad in Lebanon.",
    "Uh it it's a powder keg. And right now, as I said, where where where do we see",
    "And so we've just got some more news.",
    "And then the Iranian strikes were a lot more stronger.",
    "But there was an incident yesterday in Iraq and people can't tell.",
    "So what I think when you consider the the dynamics and what's happening in Lebanon",
]

RESECTION_NOTE = (
    " · source-section re-section pass 2026-06-29 (18 sections; split Yemen §9 + close §14 mega)"
)

def validate_capture(path: Path) -> list[str]:
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_section_patch_body(
            doc,
            manual_asr=(),
            interview_host=HOST,
            interview_guest=GUEST,
        )
    except ValueError as exc:
        return [str(exc)]
    return validate_section_anchors(body, SECTION_TITLES, SECTION_ANCHORS)

def write_capture(path: Path) -> int:
    return write_interview_section_patch_capture(
        path,
        SECTION_TITLES,
        SECTION_ANCHORS,
        manual_asr=(),
        manual_asr_spot_fix="",
        resection_note=RESECTION_NOTE,
        interview_host=HOST,
        interview_guest=GUEST,
    )

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = DAY / CAPTURE
    if not path.is_file():
        print(f"missing {path}")
        return 1
    errs = validate_capture(path)
    if errs:
        print(f"FAIL {CAPTURE}:")
        for e in errs:
            print(f"  - {e}")
        return 1
    print(f"OK {CAPTURE} ({len(SECTION_TITLES)} sections, anchors validated)")
    if not args.dry_run:
        write_capture(path)
        print(f"wrote {CAPTURE}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
