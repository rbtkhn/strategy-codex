#!/usr/bin/env python3
"""Source-section ship — 2026-06-29 Alexander Mercouris solo Putin/Donbas/Odessa."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    prepare_section_patch_body,
    validate_section_anchors,
    write_sectioned_capture,
)

DAY = ROOT / "source-archive/statecraft/2026-06-29"

CAPTURE = (
    "source-alexander-mercouris-putin-rejects-talks-odessa-donbas-drones-abate-2026-06-29.md"
)

SECTION_TITLES = [
    "Show Open — Putin Silence And Frenetic Return",
    "Valdai And United Russia — Lukashenko And Belarus Deployments",
    "Information War — Western Narrative And Putin Response",
    "Energy And Drones — Refineries Panic And Authority Play",
    "Zarubin Interview — Kremlin Transcript And No Talks",
    "Anchorage Dead — Rubio Denial And Concession Withdrawal",
    "Rejected Ceasefires — Costa Proposals And Kursk History",
    "War Aims — Donbass Novorossiya Odessa And Unity",
    "Crimea And Drones — AD Ramp And Gordon Hahn",
    "Battlefield Account — Konstantinovka Lyman Kramatorsk Sumy",
    "Putin Warlord — Regime Change And Deterrence Debate",
    "West Delusion — Pokrovsk Pressure And Close",
]

SECTION_ANCHORS = [
    "Firstly he went to Valdai in Nogarod region",
    "So intense and very public activity",
    "So Putin at the further meeting, the one to discuss the energy situation",
    "Then he gave this interview to Parl Zarabin and it is extremely interesting",
    "Now Marco Rubio the US Secretary of State has said that there was no actual agreement",
    "And then Putin did discuss various diplomatic proposals which have been made to the Russians over the last few weeks",
    "But I thought it I found it very interesting that Putin himself did not set out any ceasefire proposals",
    "Now, Putin did discuss other things. He did admit that there is a more serious problem with energy in Crimea",
    "But he was careful again to reiterate that the main point of decision is going to be what happens on the battlefields itself",
    "So this is Putin in effect. What we see is further evidence now of Putin the warlord",
    "Well, I have to say I think that Putin is absolutely right that the Russians are indeed close closer than many people realize to winning the war.",
]

RESECTION_NOTE = (
    " · source-section pass 2026-06-29 (12 sections; Putin burst/Anchorage/Donbas/Odessa arc)"
)

def validate_capture(path: Path) -> list[str]:
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_section_patch_body(doc, manual_asr=())
    except ValueError as exc:
        return [str(exc)]
    return validate_section_anchors(body, SECTION_TITLES, SECTION_ANCHORS)

def write_capture(path: Path) -> None:
    write_sectioned_capture(
        path,
        SECTION_TITLES,
        SECTION_ANCHORS,
        reject_if_sectioned=False,
    )
    doc = path.read_text(encoding="utf-8")
    if RESECTION_NOTE.strip() not in doc:
        doc = doc.replace(
            'source_note: "Operator source-intake 2026-06-29',
            f'source_note: "Operator source-intake 2026-06-29',
        )
        if "source-section pass 2026-06-29" not in doc:
            doc = doc.replace(
                "· source-clean pass 2026-06-29.",
                f"· source-clean pass 2026-06-29.{RESECTION_NOTE}",
            )
            doc = doc.replace(
                'editorial_note: "AI-assisted source-clean',
                f'editorial_note: "AI-assisted source-clean',
            )
            if RESECTION_NOTE.strip() not in doc.split("editorial_note:", 1)[-1][:200]:
                doc = doc.replace(
                    "not human-verified verbatim; verify before quotation.\"",
                    f"not human-verified verbatim; verify before quotation.{RESECTION_NOTE}\"",
                )
        path.write_text(doc, encoding="utf-8")

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

    print(f"OK {CAPTURE} ({len(SECTION_TITLES)} sections)")
    if not args.dry_run:
        write_capture(path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
