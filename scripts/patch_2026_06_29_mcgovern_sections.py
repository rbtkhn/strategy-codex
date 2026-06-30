#!/usr/bin/env python3
"""Source-section ship — 2026-06-29 Judging Freedom Ray McGovern interview."""
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

DAY = ROOT / "source-archive/statecraft/2026-06-29"
CAPTURE = "source-judging-freedom-mcgovern-zelensky-goad-putin-overact-2026-06-29.md"
HOST = "Andrew Napolitano"
GUEST = "Ray McGovern"

SPEC = {
    "titles": [
        "Show Open — Iran MOU And Lebanon First Paragraph",
        "False Flag — Nuclear Fear And Israel Cornered",
        "Gulf Hedging — Sullivan Quote And Bahrain Fifth Fleet",
        "Narrative Control — Media Censorship And Bucha WaPo",
        "Ukraine Drones — Putin Zarubin And Front Line Truth",
        "Broken Anchorage — Real Estate Brokers And Battlefield Win",
        "Latvia Warning — SVR Coordinates And Duma Elections",
        "Lugansk Retaliation — Teachers College And Starlink",
        "Media Propaganda — Langley Game And Maria Frame",
        "Close — Taylor Swift MSG Wedding Lineup",
    ],
    "anchors": [
        ">> Do you still fear a false flag from the Israelis, Ray?",
        ">> You uh mentioned a few minutes ago uh the other Gulf states not concerned about um Lebanon.",
        ">> is the United States military as secretive as the IDF when it comes to censoring damage to itself?",
        ">> How damaging to Russia have been the Ukraine uh drone attacks of late?",
        ">> But the US is not an honest broker.",
        "one of the things that he warned, that is the Russian intelligence service warned about was this notion",
        "Meanwhile, has there been any uh satisfactory response, otherwise known as vengeance, for the drone attack that killed 125",
        "What's behind the um persistent impression given by the media in the west that Russia is suddenly losing?",
        "Okay. Thank you, my dear friend. Much appreciated.",
    ],
    "note": (
        " · source-section pass 2026-06-29 (10 sections; MOU/Lebanon/Gulf/Bucha/Ukraine/Latvia arc)"
    ),
    "manual_asr": (
        ("Npalitano", "Napolitano"),
        ("Zilinski", "Zelensky"),
        ("Isra Israel", "Israel"),
        ("gulfy", "Gulf"),
        (" about BHA,", " about Bucha,"),
        ("people in BHA,", "people in Bucha,"),
        ("Baris Johnson", "Boris Johnson"),
        ("Puchin", "Putin"),
        ("Puchi", "Putin"),
        ("Pooie", "Putin"),
        ("Latians", "Latvians"),
        ("Latafians", "Latvians"),
        ("in Ria.", "in Riga."),
        ("Bella Uso", "Belousov"),
        ("Maria Zakarova", "Maria Zakharova"),
        ("Maria Zahara", "Maria Zakharova"),
        ("futless", "futile"),
    ),
}

def validate_capture(path: Path) -> list[str]:
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_section_patch_body(
            doc,
            manual_asr=SPEC["manual_asr"],
            interview_host=HOST,
            interview_guest=GUEST,
        )
    except ValueError as exc:
        return [str(exc)]
    return validate_section_anchors(body, SPEC["titles"], SPEC["anchors"])

def write_capture(path: Path) -> int:
    return write_interview_section_patch_capture(
        path,
        SPEC["titles"],
        SPEC["anchors"],
        manual_asr=SPEC["manual_asr"],
        manual_asr_spot_fix="",
        resection_note=SPEC["note"],
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
    print(f"OK {CAPTURE} ({len(SPEC['titles'])} sections, anchors validated)")
    if args.dry_run:
        return 0
    words = write_capture(path)
    print(f"wrote {CAPTURE} ({words} words, {len(SPEC['titles'])} sections)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
