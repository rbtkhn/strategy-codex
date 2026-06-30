#!/usr/bin/env python3
"""source-section batch — May 2026 Nawfal × Pape guest captures (outline pinned).

Status: OUTLINE ONLY — do not run until operator approves section maps.
Verify anchors: python scripts/patch_2026_05_nawfal_pape_guest_sections.py --check-anchors
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    find_anchor_pos,
    split_transcript_document,
    write_sectioned_capture,
)

CAPTURES: dict[str, dict] = {
    "source-archive/statecraft/2026-05-12/source-pape-mario-nawfal-trump-s-next-iran-steps-revealed-2026-05-12.md": {
        "titles": [
            "Show Open — Ceasefire Illusion and Escalation Ladder Check-in",
            "Escalation Trap Stages — Fork Between Path Three and Four",
            "Fourth Center Branch — Hormuz and Strategic Consolidation",
            "Iran Toll Demands — Fees, Sanctions, and Forcing Trump Back",
            "Humiliation Strategy — Reputation for Power",
            "Emerging Force Center — Moscow Security Architecture Talks",
            "US Fork — Accept Regional Hegemon or Bleed On",
            "Medium-Term Strategy — Tactics vs State Planning",
            "Decapitation and Personal Targeting — Smart Bomb Trap Close",
        ],
        "anchors": [
            "pleasure to speak to you again",
            "stage one of the escalation trap",
            "become an emerging fourth center of",
            "they want to charge a fee to the",
            "humiliate President Trump",
            "emerging force center of world",
            "accept Iran as a new",
            "people are bouncing around tactics.",
        ],
        "note": "ASR auto-caption body; optional source-clean before ship. §9 runs tactics → decapitation → personal targeting → close.",
    },
    "source-archive/statecraft/2026-05-20/source-pape-mario-nawfal-iran-warns-u-s-of-surprises-xi-putin-meet-in-beijing-2026-05-20.md": {
        "titles": [
            "Show Open — Xi-Putin Beijing Summit Readout",
            "Russia-China Alignment — Energy Bypass and No Gulf Bailout",
            "Off-Ramps and Survival — Pape Modeling Credibility",
            "UAE Showing Strikes — Coercion Reversal",
            "Pizza Indicator — Leadership Strikes and Retaliation Branches",
            "Asymmetric Nation-State — Calibrated Iran Retaliation",
            "Non-Linear War — Stage Three Ground Dilemma and Gulf Architecture",
            "Walking Away, Ukraine Casualties — Putin Escalation Trap Parallel",
        ],
        "anchors": [
            "Putin described his visit",
            "Russia and China have been moving closer",
            "survival trumps economic incentives",
            "nuclear power plant in the UAE",
            "pizza indicator",
            "tactics of ISIS and the Afghan Taliban",
            "wars are not linear",
        ],
    },
    "source-archive/statecraft/2026-05-29/source-mario-nawfal-pape-breaking-trump-teases-lifting-iran-blockade-2026-05-29.md": {
        "titles": [
            "Show Open — Deal Rumors and Iran in the Driver's Seat",
            "Escalation Trap — Signing Loss vs Victory Spin",
            "New Era of Instability — Blockade and Saddam Analogy",
            "Gulf Double Mechanism — US Guarantor Fail and Instability Strategy",
            "Oil Inventory Countdown — Multipolar Fragmentation",
            "Three Pillars — Trap, Instability, and Horizontal Escalation",
            "Horizontal Escalation — Lebanon, Houthis, and Red Sea",
            "Regional War Risk — Red Lines Crossed",
            "Nuclear Timeline and Trump Blockade Breaking — MOU Odds Close",
        ],
        "anchors": [
            "Iran is in the driver's seat",
            "escalation trap in real time",
            "we're in a new era",
            "United States is not the guaranter",
            "inventory countdown in weeks not months",
            "three great concepts",
            "encourage the Houthis to shut down Red Sea",
            "How how high is the risk for a regional war",
        ],
    },
}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write sectioned captures (operator-approved ship only)",
    )
    parser.add_argument(
        "--check-anchors",
        action="store_true",
        help="Verify all anchors resolve; no file writes",
    )
    args = parser.parse_args()

    if args.check_anchors or not args.apply:
        ok = True
        for rel, spec in CAPTURES.items():
            path = ROOT / rel
            doc = path.read_text(encoding="utf-8")
            _, _, body = split_transcript_document(doc)
            flat = " ".join(body.split())
            pos = 0
            print(f"=== {path.name} ({len(spec['titles'])} sections) ===")
            for i, anchor in enumerate(spec["anchors"], start=1):
                try:
                    pos = find_anchor_pos(flat, anchor, pos) + len(anchor)
                    print(f"  anchor {i} -> section {i + 1}: {spec['titles'][i]}")
                except ValueError as exc:
                    ok = False
                    print(f"  {i}. FAIL — {exc}")
            print(f"  -> {spec['titles'][-1]} (EOF)")
            print()
        if not args.apply:
            print("OUTLINE ONLY — pass --apply after operator approval to ship.")
        return 0 if ok else 1

    for rel, spec in CAPTURES.items():
        path = ROOT / rel
        doc = path.read_text(encoding="utf-8")
        write_sectioned_capture(
            path,
            spec["titles"],
            spec["anchors"],
        )
        print(f"sectioned {rel}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
