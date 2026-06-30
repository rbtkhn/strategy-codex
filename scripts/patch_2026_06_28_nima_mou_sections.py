#!/usr/bin/env python3
"""Source-section ship — 2026-06-28 Nima Alkhorshid solo MOU attrition / Hormuz."""
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

DAY = ROOT / "source-archive/statecraft/2026-06-28"

CAPTURE = (
    "source-dialogue-works-nima-alkhorshid-mou-war-of-attrition-us-iran-2026-06-28.md"
)

SECTION_TITLES = [
    "Show Open — Sunday Date And US Strikes On Iran",
    "IRGC Response — Kuwait And Bahrain Retaliation",
    "Project Freedom And MOU Frame — Why Attacks Continue",
    "Trump Escalation Ladder — Blockade To MOU Sign",
    "Oman Mechanism — Rubio Pressure And Hormuz Fees",
    "Tanker Tit For Tat — Singapore Flag And Escalation Cycle",
    "War Of Attrition — Carriers GCC Airspace Sustainability",
    "MOU Article One — Oman IRGC And Hollow Gains",
    "Iranian Air Defense — Bavar Arash And Asaluyeh",
    "Lebanon Deal — Yellow Line Occupation And Rubio",
    "West Bank Parallel — Abbas Trap And Government Betrayal",
    "Attrition Analogy — Ukraine Russia And GCC Survival Pivot",
    "GCC Reconstruction — Iran Preparedness And Integrated Air Defense",
    "China Iran Axis — Hormuz Closure And Friendly Countries",
    "Europe Vassal Read — Germany NATO And Kurdistan Front",
    "Hormuz Control — Base Westward Move Lebanon Graveyard Close",
]

SECTION_ANCHORS = [
    "Then the Iranian attacks came after the live last night",
    "So the reason that we are having these sort of attacks between Iran and the United States",
    "Then Donald Trump came back said okay everything let's sign a document MOU",
    "So that's why you see Marco Rubio going to the region talking with countries like Bahrain",
    "So, we had an attack on a Singaporean flag, Singaporean flag tanker",
    "This is a war of attrition. What the United States is trying to do this hit for tat",
    "The first clause, let me read the first clause word by word",
    "And in the coming days, we have some reports in within the Iranian media",
    "And when it comes to Lebanon, it's so critical in my opinion",
    "remember we have the same case in the West Bank",
    "And the war of attrition is like the war between Ukraine and Russia",
    "And to my understanding is that $300 billion dollars",
    "I think we have learned a lot during the war that the communication between China and Iran",
    "You may ask yourself why the chancellor of Germany has changed his mind",
    "The British government came to Armenia",
]

RESECTION_NOTE = (
    " · source-section re-section pass 2026-06-29 (16 sections; split §12 strategic outlook mega)"
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
        resection=True,
    )
    doc = path.read_text(encoding="utf-8")
    if RESECTION_NOTE.strip() not in doc:
        doc = doc.replace(
            "GCC/Oman.\"",
            f"GCC/Oman.{RESECTION_NOTE}\"",
        )
        path.write_text(doc, encoding="utf-8", newline="\n")

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
