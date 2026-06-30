#!/usr/bin/env python3
"""source-section batch — May 2026 Cyrus Janssen × Ritter (Hormuz energy shock).

Land: source-ritter-cyrus-janssen-iran-hormuz-energy-shock-2026-05-10.md
Verify anchors: python scripts/patch_2026_05_10_ritter_janssen_sections.py --check-anchors
Apply:          python scripts/patch_2026_05_10_ritter_janssen_sections.py --apply
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

REL = (
    "source-archive/statecraft/2026-05-10/"
    "source-ritter-cyrus-janssen-iran-hormuz-energy-shock-2026-05-10.md"
)

SPEC = {
    "titles": [
        "Studio Open — Let's Talk Geopolitics, Alex Host, and Conflict Frame",
        "Objectives Failed — White House Victory Claims vs Strait Control",
        "Global Energy Catastrophe — Supply Chain, June Shock, and China Diplomacy",
        "Market Pain — Vegas Diesel, GDP Oil Dependence, and Manipulation",
        "Petrochemical Standstill — Fertilizer, Helium, and Aviation Fuel Crisis",
        "Military Myth Collapse — Trump Delusion, China Rearm, and Europe Exposed",
        "Market Rigging Graph — Derivatives Trillions and Party Credibility",
        "Cult of Personality — NPD Diagnosis, Golden Statue, and Trump Phone Scam",
        "Undersea Cables — Submarine Interdiction and Gulf Toll Mirror",
        "Iran Holds Cards — China Offramp, Xi Meeting, and Deal Terms",
        "JCPOA Realism — Omani February Deal and East Pivot Embrace",
        "Moscow Question and Close — Answer Missing in Operator Paste",
    ],
    "anchors": [
        "Scott, would you agree with that statement?",
        "we've accomplished none of the objectives of this conflict",
        "Well, yeah, a lot of market manipulation is what I've been seeing",
        "Not in recent history. We've, you know, the oil economy",
        "China now today has answered some very fundamental questions. America sucks",
        "Scott, you know, you mentioned the economy and how important it is to Americans. I'm going to bring up a a video",
        "It may have destroyed the credibility of all political parties",
        "Scott, I got a question for you. Uh now we're seeing a story coming out that Iran could potentially seize control",
        "Iran holds all the cards",
        "that deal was um had had some some problems as well from a optic standpoint",
        "Scott, we're getting a lot of questions from people in the comment section",
    ],
    "note": (
        "LTG panel format with Alex Reportify; speaker-label transcript preserved. "
        "Tail §12 merges Moscow question + host close; Ritter Moscow answer not in operator paste."
    ),
}

def check_spec(path: Path, spec: dict) -> bool:
    doc = path.read_text(encoding="utf-8")
    _, _, body = split_transcript_document(doc)
    flat = " ".join(body.split())
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
    parser.add_argument(
        "--outline",
        action="store_true",
        help="Print section map only",
    )
    args = parser.parse_args()

    path = ROOT / REL
    if args.outline:
        for i, title in enumerate(SPEC["titles"], start=1):
            print(f"  {i}. {title}")
        return 0

    if args.check_anchors or not args.apply:
        ok = check_spec(path, SPEC)
        if not args.apply:
            print("OUTLINE ONLY — pass --apply after operator approval to ship.")
        return 0 if ok else 1

    write_sectioned_capture(path, SPEC["titles"], SPEC["anchors"])
    print(f"sectioned {REL}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
