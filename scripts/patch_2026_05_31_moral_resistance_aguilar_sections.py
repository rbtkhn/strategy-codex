#!/usr/bin/env python3
"""source-section batch — May 2026 Moral Resistance × Aguilar guest capture (9-section map).

Status: OUTLINE ONLY — do not run until operator approves section map.
Verify anchors: python scripts/patch_2026_05_31_moral_resistance_aguilar_sections.py --check-anchors

Ship note: ~9.3k-word operator-paste; `## Transcript` present. Merged §9–§11: GHF/§224 + tech
merger/parasite/AIPAC + Massie close in one NDAA stack block. Pair with Jun 12/18 Aguilar MR passes.
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
    "source-archive/statecraft/2026-05-31/"
    "source-moral-resistance-u-s-military-attacks-vessels-in-strait-of-hormuz-5-u-s-casualties-in-hor-2026-05-31.md"
)

SPEC = {
    "titles": [
        "Show Open — Three Breaking Items and §224 Introduction",
        "Kuwait Strike — Camp Arifjan Logic and Ceasefire Collapse",
        "Hidden Casualty Toll — DCAS Receipts and Imminent Three-Pronged Attack",
        "Degraded Air Defense — Decoy Arrays and Adapted Iranian Strike Doctrine",
        "Sledgehammer Objectives — Uranium Grab, Isfahan Raid, and Hegseth Walk-Back",
        "Hormuz Vessel Neutralization — Distant Blockade, Toll Corridor, and Island Seizure Leverage",
        "Trump Nuclear Concession — Buy-a-Bomb Precedent and Global Strategic Loss",
        "Drone Losses — Triton Cyber Capture and Predator Recon for DU Sites",
        "NDAA §224 Stack — GHF Gaza, Tech Merger, Parasite Frame, and Massie Close",
    ],
    "anchors": [
        "Yeah, and we're definitely going to talk about that because",
        "Well, what this goes to show is that I I personally believe",
        "Well, it's clear that the that the United States regional anti-missile",
        "No. No. And and to the point we haven't we haven't run out",
        "Exactly. So when you look at this and and it goes back",
        "Um guys, a couple of things as well",
        "Another question I've got for you is this",
        "Now, the other thing I want to talk to you about was um so you went to Gaza",
    ],
    "note": (
        "Nine-section map (merged NDAA legislative stack + close). "
        "Pair §2–§4 with wire on Kuwait casualties/DCAS; §9 with Jun 12/18 §224 arc."
    ),
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
    flat = " ".join(extract_flat_body(doc).split())
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


def apply_spec(path: Path, spec: dict) -> None:
    write_sectioned_capture(
        path,
        spec["titles"],
        spec["anchors"],
        reject_if_sectioned=False,
    )


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

    apply_spec(path, SPEC)
    print(f"sectioned {REL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
