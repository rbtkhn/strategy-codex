#!/usr/bin/env python3
"""source-section batch — Mar 2026 Davis × Pape escalation-trap interview (outline pinned).

Status: OUTLINE ONLY — do not run until operator approves section map.
Verify anchors: python scripts/patch_2026_03_10_davis_pape_sections.py --check-anchors
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    find_anchor_pos,
    write_sectioned_capture,
)

REL = (
    "source-archive/statecraft/2026-03-10/"
    "source-daniel-davis-pape-escalation-trap-2026-03-10.md"
)

BODY_MARKER = "## Cleaned, Unabridged Transcript\n"

SPEC = {
    "titles": [
        "Show Open — Davis Intro and Blumenthal Ground-Troop Warning",
        "Victory Narrative vs Escalation Reality — Foreign Affairs Frame",
        "Negotiation Breakdown — Trump and Araghchi Clips, Axis of Evil",
        "Smart Bomb Trap — Stages One and Two Through Ground Inevitability",
        "Keane Rebuttal — Enriched Uranium Core vs Missile Periphery",
        "Stage Three Ground Trap — Limited Territorial Control and Mosaic Plan",
        "Graham and Netanyahu Clips — Normalization and Regime-Change Failure",
        "Venezuela Comparison — Maduro Objective Lost and Advisor Bubble",
        "Horizontal Escalation — Parallel Attack and Coalition Wedges",
        "Time Favors Iran — Sadat Problem and Strategic Setback Frame",
        "Off-Ramp and Close — Friday Deal, Rubicon Timeline, Substack Plug",
    ],
    "anchors": [
        "victory narrative at odds with escalation reality",
        "Let's start off with President Trump from last night",
        "axis of evil speech in 2002",
        "soundbite from General Jack Keane",
        "Stage three, which is what I call limited territorial control",
        "Lindsey Graham here because",
        "what happened in Venezuela",
        "Horizontal escalation is all about",
        "number five here",
        "two minutes before you have to bail",
    ],
    "note": (
        "Operator-paste with **Speaker:** labels and clip blocks. "
        "Body marker `## Cleaned, Unabridged Transcript` (non-default). "
        "Load-bearing escalation-trap spine — pair with pape-forecast-ledger-2026.md."
    ),
}

def extract_body(doc: str) -> str:
    if BODY_MARKER not in doc:
        raise ValueError(f"missing body marker: {BODY_MARKER!r}")
    return doc.split(BODY_MARKER, 1)[1]

def check_spec(path: Path, spec: dict) -> bool:
    doc = path.read_text(encoding="utf-8")
    flat = " ".join(extract_body(doc).split())
    pos = 0
    ok = True
    print(f"=== {path.name} ({len(spec['titles'])} sections) ===")
    for i, anchor in enumerate(spec["anchors"], start=1):
        try:
            pos = find_anchor_pos(flat, anchor, pos) + len(anchor)
            print(f"  anchor {i} -> section {i + 1}: {spec['titles'][i]}")
        except ValueError as exc:
            ok = False
            print(f"  {i}. FAIL — {exc}")
    print(f"  -> {spec['titles'][-1]} (EOF)")
    if spec.get("note"):
        print(f"  note: {spec['note']}")
    print()
    return ok

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write sectioned capture (operator-approved ship only)",
    )
    parser.add_argument(
        "--check-anchors",
        action="store_true",
        help="Verify all anchors resolve; no file writes",
    )
    args = parser.parse_args()

    path = ROOT / REL
    if args.check_anchors or not args.apply:
        ok = check_spec(path, SPEC)
        if not args.apply:
            print("OUTLINE ONLY — pass --apply after operator approval to ship.")
        return 0 if ok else 1

    write_sectioned_capture(
        path,
        SPEC["titles"],
        SPEC["anchors"],
        body_marker=BODY_MARKER,
    )
    print(f"sectioned {REL}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
