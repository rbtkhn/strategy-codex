#!/usr/bin/env python3
"""source-section batch — Mar 2026 Cyrus Janssen × Macgregor (day 11 Iran war).

Land: source-macgregor-cyrus-janssen-worst-of-iran-war-still-ahead-2026-03-10.md
Verify anchors: python scripts/patch_2026_03_10_macgregor_janssen_sections.py --check-anchors
Apply:          python scripts/patch_2026_03_10_macgregor_janssen_sections.py --apply
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
    "source-archive/statecraft/2026-03-10/"
    "source-macgregor-cyrus-janssen-worst-of-iran-war-still-ahead-2026-03-10.md"
)

SPEC = {
    "titles": [
        "Cold Open — Netanyahu Demands and Last Act in the Middle East",
        "Day 11 Open — Oil Futures, Hegseth vs Trump, and Insane Conflict",
        "Air Campaign — Decapitation Failed and Vietnam-Style Metrics",
        "Gulf Shock — 27 Bases Destroyed, Refineries, and Idle Tankers",
        "Global Cascade — Fertilizer, China Oil, and Energy Poverty",
        "Victory Vacuum — Regime-Change Flip-Flop and Netanyahu's War Aim",
        "Munitions and Support — Missile Burn Rate and Under-50 Skepticism",
        "Ground Invasion — Fantasy Land, Draft, and Post-9/11 Tehran Vigil",
        "School Strike — Tomahawk Double Tap and Targeting Error",
        "Naval and Air Munitions — Magazine Reload and March-April Depletion",
        "Escalation Ceiling — Persians vs Arabs and Netanyahu Nuclear Fork",
        "Russia Beneficiary — Europe Turnover and Middle East Exit Frame",
        "Close — Substack Plug and Janssen Outro",
    ],
    "anchors": [
        "Well, everyone, we're very honored to welcome back into the studio",
        "we are entering in to day 11 of this conflict",
        "decapitation strikes designed to eliminate leaders",
        "27 plus US bases completely destroyed",
        "25% of the world's oil is offline",
        "what a successful campaign would be",
        "we've probably run through most of the high-end missiles",
        "potential ground invasion is an option",
        "Iranian school that was bombed, 165 young ladies",
        "ships that launch these missiles, they're vertical launchers",
        "biggest misconception that most Americans have about Iran",
        "biggest beneficiary of what's going on right now in the Middle East",
    ],
    "note": (
        "Operator-paste with cold-open lead before studio welcome; >> turn markers "
        "preserved. Nomad-free capture."
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
