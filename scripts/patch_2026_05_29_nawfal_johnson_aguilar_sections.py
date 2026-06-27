#!/usr/bin/env python3
"""source-section batch — May 29, 2026 Nawfal Hormuz-ops pair (Johnson + Aguilar).

Verify: python scripts/patch_2026_05_29_nawfal_johnson_aguilar_sections.py --check-anchors
Apply:  python scripts/patch_2026_05_29_nawfal_johnson_aguilar_sections.py --apply
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    find_anchor_pos,
    normalize_for_anchor,
    write_sectioned_capture,
)

CAPTURES: dict[str, dict] = {
    "johnson": {
        "rel": (
            "source-archive/statecraft/2026-05-29/"
            "source-mario-nawfal-larry-johnson-breaking-us-declares-military-operations-in-hormuz-2026-05-29.md"
        ),
        "titles": [
            "Show Open — Boy Who Cried Wolf and Blockade Post Collapse",
            "Deal Collapse — National Security Team, MQ-9 #25, Situation Room",
            "Hormuz Skirmish Loop — Three-Day Escalation and Market Manipulation",
            "Iran Unwavering — Galibbuff Demands, Reactive Diplomatic High Ground",
            "Gulf Split — Oman Picks Iran, WSJ UAE Covert Strikes",
            "Lebanon Hezbollah — Treat UAE Horizontal Retaliation Option",
            "Russia-Ukraine Pivot — Lavrov Warning, Romania Drone, NATO Risk",
            "Ukraine Culminating Point — PAC-3 Shipments vs Attrition Reality",
            "Wagner Mutiny — Prigozhin Played, Putin Escalation Green Light",
            "Sentcom Hormuz Ops — Project Freedom 2.0 and NDAA §224 Close",
        ],
        "anchors": [
            "Well, initially he convened the national security team to go over the proposed deal.",
            "So this is um but but what's interesting is the this this effort to provoke Iran started three days ago.",
            "What do we do? What do we do? Tell Alz we have no idea what he's talking about.",
            "Yeah. Okay. Makes sense. Um let's pivot to the Gulf.",
            "And then and then treaty put out a piece on a substack.",
            "Um and more concerning area. So, at least there's indications of a possible deal.",
            "What do the facts tell us? Is Ukraine receiving more money from the West or less?",
            "And then the um by the way, what's your take? I've never asked you about this completely unrelated.",
            "Just came in now as you were speaking. US Navy Central Command has warned mariners",
        ],
        "note": "Ten sections. Pair §10 with Aguilar §1–§3; leads May 31 Johnson §4 Hormuz arc.",
    },
    "aguilar": {
        "rel": (
            "source-archive/statecraft/2026-05-29/"
            "source-mario-nawfal-anthony-aguilar-breaking-trump-orders-military-action-2026-05-29.md"
        ),
        "titles": [
            "CENTCOM Warning — Operation Sledgehammer Foreseen, Toll Endstate",
            "Toll Booth Contention — Trump Absolute Surrender vs Iran Leverage",
            "Island Seizure Frame — CNO Cannot Escort, Penetrate the Strait",
            "Announce Without Strike — Recon by Fire, Mars Raiders on Kashm/Abu Musa",
            "Optics Victory — Toll Albatross and Guns of August Framing",
            "Operation Sledgehammer — Title 10 Authority vs Project Freedom",
            "MARAD Notice Read — Operations Order Situation and Iranian Influence",
            "Demining Phase — Iranian Asymmetric Sea Drone Response",
            "Horizontal Gulf Strikes — Kuwait/UAE, Oman Joint Control, Strategic Blunder Close",
        ],
        "anchors": [
            "So, am I is it fair for me to say, and look, if I'm getting it wrong or you disagree, perfect.",
            "Holy So you think this is more than just escorting ships?",
            "Uh well, the the immediate operations to to seize or control operationally beneficial islands",
            "Exactly. >> The perception >> Can you finish that sentence sign?",
            "project freedom right remember it didn't get an operational name.",
            "Now that we read the whole thing with the context, uh can you shed some light on it?",
            "I just don't understand. I just I'm I'm just struggling to understand.",
            "Well, the thing is now when it comes to the UAE and Saudi Arabia and Qatar and and that the gloves are off.",
        ],
        "note": "Nine sections. Pair §1–§3 with Johnson May 29 §10; foreshadows MR May 31 §2–§5 Sledgehammer.",
    },
}

TRANSCRIPT_MARKER = "## Transcript\n"
LEGACY_SPLIT = "---\n\n"


def extract_flat_body(doc: str) -> str:
    if TRANSCRIPT_MARKER in doc:
        return doc.split(TRANSCRIPT_MARKER, 1)[1]
    if LEGACY_SPLIT in doc:
        return doc.split(LEGACY_SPLIT, 1)[1]
    raise ValueError("no transcript body (expected ## Transcript or legacy --- split)")


def check_spec(path: Path, spec: dict) -> bool:
    doc = path.read_text(encoding="utf-8")
    body = extract_flat_body(doc).strip()
    pos = 0
    ok = True
    print(f"=== {path.name} ({len(spec['titles'])} sections) ===")
    for i, anchor in enumerate(spec["anchors"], start=1):
        try:
            pos = find_anchor_pos(body, anchor, pos) + len(normalize_for_anchor(anchor))
            print(f"  anchor {i} -> section {i + 1}: {spec['titles'][i]}")
        except ValueError as exc:
            ok = False
            print(f"  {i}. FAIL — {exc}")
    print(f"  -> {spec['titles'][-1]} (EOF)")
    if spec.get("note"):
        print(f"  note: {spec['note']}")
    print()
    return ok


def apply_spec(path: Path, spec: dict) -> None:
    write_sectioned_capture(
        path,
        spec["titles"],
        spec["anchors"],
        reject_if_sectioned=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--check-anchors", action="store_true")
    parser.add_argument("--only", choices=sorted(CAPTURES))
    args = parser.parse_args()

    keys = [args.only] if args.only else list(CAPTURES)
    ok_all = True
    for key in keys:
        spec = CAPTURES[key]
        path = ROOT / spec["rel"]
        if not path.is_file():
            print(f"MISSING {spec['rel']}", file=sys.stderr)
            ok_all = False
            continue
        if args.apply:
            apply_spec(path, spec)
            print(f"sectioned {spec['rel']}")
        else:
            ok_all = check_spec(path, spec) and ok_all

    if not args.apply:
        print("Pass --apply after operator approval to ship.")
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
