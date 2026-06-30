#!/usr/bin/env python3
"""Source-section ship — 2026-06-27 Dialogue Works Aguilar Kuwait/Bahrain breaking interview."""
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

DAY = ROOT / "source-archive/statecraft/2026-06-27"

CAPTURE = (
    "source-dialogue-works-anthony-aguilar-iran-strike-kuwait-bahrain-russia-strikes-kharkov-kiev-2026-06-27.md"
)

HOST = "Nima Alkhorshid"
GUEST = "Anthony Aguilar"

SECTION_TITLES = [
    "Breaking Open — Bahrain Kuwait And Kiev Dual Track",
    "MOU Collapse — Lebanon Yellow Line Versus Hormuz",
    "Singapore Vessel — Strait Channel Parity",
    "Sirri Qeshm Strikes — Peace Interval Bad Faith",
    "Bahrain Kuwait Response — Kid Gloves Versus Hard Hit",
    "Abyss Of Failure — MOU Moot And Munich Analogy",
    "IRGC Navy Statement — Escalation Levers Matrix",
    "Air Escort Attempt — AWACS Piracy And MOU Breach",
    "US Options — Capitulate Escalate Or Fuel Limits",
    "Russia Kiev Barrage — Missile Mix And Intercepts",
    "Zircon Escalation — Dark Eagle Message To Washington",
    "Lebanon MOU Collision — Treatise Pari And Hezbollah",
    "CENTCOM Footage — Fox Reconstitution Debunk",
    "Close — Hormuz Leverage And America First Campaign",
]

SECTION_ANCHORS = [
    "particularly the memorandum of understanding which again was not in and of itself",
    "Now with the straight of Hormuz, no no coincidence",
    "Now what happens now with the escalatory nature of these strikes",
    ">> And we saw that today, right? Because I have been a bit critical",
    ">> Well, uh, in a way the United States has kind of cut the safety line",
    ">> So, we've got a statement from the um so we read the statement for the IIGC.",
    "If you can explain militarily why they were trying to do that because Larry thought that was foolish",
    ">> Yeah, let's see. Yeah, I mean that makes sense cuz US has only got two options.",
    "Now, there is obviously another um another element I wanted to speak to you about.",
    "So you you mentioned the the 3M22 um Zirkcon um hypersonic.",
    "Now coming >> yeah now coming back to uh Iran you've got the Lebanon",
    "So I just want to show you this. This is the video that Sencom brought out.",
    ">> Okay, interesting. We shall see. Lieutenant Colonel Anthony",
]

RESECTION_NOTE = " · source-section pass 2026-06-29 (14 sections; breaking Kuwait/Bahrain + Kiev Zircon arc)"

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
