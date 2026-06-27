#!/usr/bin/env python3
"""source-section batch — May 2026 Switzer × Pape guest capture (outline pinned).

Status: OUTLINE ONLY — do not run until operator approves section map.
Verify anchors: python scripts/patch_2026_05_28_switzer_pape_sections.py --check-anchors
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
    "source-archive/statecraft/2026-05-28/"
    "source-pape-switzer-the-mirage-of-peace-2026-05-28.md"
)

SPEC = {
    "titles": [
        "Show Open — Switzer Welcome and Mearsheimer Three Options Setup",
        "Escalation Trap Thesis — Tactical Wins and Hormuz Oil Leverage",
        "Peace Mirage — Pingpong, Pizza Indicator, and Surrender Cost",
        "Hardliner Coercion — Punishment Logic and Libya Counterexample",
        "Lost Off-Ramp — Week-One Declare Victory Window Closed",
        "Post-American Order — 1991 Inverse and Ally Bailout Ask",
        "China Rise Test — Demographic Skepticism vs Industrial Uplift",
        "Violent Populism — Book Pivot and Normalized Political Violence",
        "Demographic Tipping Point — White Minority Transition and Polarization",
        "1960s Parallel — Softer Landing and Assimilation Pace",
        "Close — Book Release and Framework Optimism",
    ],
    "anchors": [
        "I think we're going to bounce around",
        "peace deal was imminent",
        "Republican hardliners",
        "realistic ramp this offramp",
        "post American order or era",
        "China is its population is now 1.3 billion",
        "our own worst enemies",
        "is it all come down to Trump",
        "you could go back to the late 60s",
        "we've got to go, but",
    ],
    "note": (
        "Operator-paste YouTube transcript (>> turn markers; not speaker-normalized). "
        "Optional source-clean for Tyran/Mishimemer ASR before ship. "
        "Second half pivots to violent-populism book — keep §8–§11 separate from Iran arc."
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
    args = parser.parse_args()

    path = ROOT / REL
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
