#!/usr/bin/env python3
"""source-section batch — May 2026 Breaking Points × Pape guest capture (8-section map).

Status: OUTLINE ONLY — do not run until operator approves section map.
Verify anchors: python scripts/patch_2026_05_27_breaking_points_pape_sections.py --check-anchors

Ship note: capture already has `## Transcript`; operator-paste `>>` block (no speaker labels).
Merged §8+§9: Iran State TV six-point framework + mid-60s Brent commitment gap + close.
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
    "source-archive/statecraft/2026-05-27/"
    "source-pape-breaking-points-iran-drivers-seat-shocking-deal-emerges-2026-05-27.md"
)

SPEC = {
    "titles": [
        "Show Open — Breaking Points Welcome and Busboys Left-Right Bridge",
        "Monday Post Setup — Nuclear Dust Concession vs Missile Site Strikes",
        "Iran in the Driver's Seat — Chaos, Strategic Defeat, and July 15 Inventory Wall",
        "Stage IV Escalation Trap — Feb 27 Reversal, Downblending, and Own-the-L Politics",
        "RGC 24–48 Hour Window — Modest Reaction vs Oil-Supply Brushback Leverage",
        "Ground Force Option — Nonlinear War Model and Escalation Track Instability",
        "Negotiate the Oil Price — Pre-War Brent Laser vs Zero-Sum Detail Trap",
        "Iran Framework and Oil Price Gap — Six Points, Surrender Terms, and Mid-60s Brent Commitment",
    ],
    "anchors": [
        "Well, let's start with this post from Monday",
        "Uh, I think that it seems totally chaotic",
        "Yeah. Yeah. And just so uh people understand the kind of concession",
        "Well, right now as we're awaiting the RGC's potential response",
        "And so uh earlier in the in the conflict, you had said",
        "which is that I do think there's something that we should focus on in the negotiations",
        "And we have some breaking news here where Iran State TV",
    ],
    "note": (
        "Eight-section map (merged six-point read + Brent gap + close). "
        "Pair §4–§7 with May 27 Substack oil-price wedge and forecast ledger."
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

def normalize_for_section_ship(doc: str) -> tuple[str, str, str]:
    """Return head, marker, body; insert ## Transcript when legacy shape."""
    if TRANSCRIPT_MARKER in doc:
        head, marker, body = split_transcript_document(doc)
        return head, marker, body
    if LEGACY_SPLIT not in doc:
        raise ValueError("missing legacy --- split for transcript body")
    head, body = doc.split(LEGACY_SPLIT, 1)
    head = head.rstrip() + "\n\n" + TRANSCRIPT_MARKER
    return head, TRANSCRIPT_MARKER, body.lstrip("\n")

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
