#!/usr/bin/env python3
"""source-section batch — Apr 2026 Cyrus Janssen × Pape guest capture (outline pinned).

Land: source-pape-cyrus-janssen-us-has-no-idea-what-is-coming-next-2026-04-16.md
Verify anchors: python scripts/patch_2026_04_16_janssen_pape_sections.py --check-anchors
Apply:          python scripts/patch_2026_04_16_janssen_pape_sections.py --apply
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
    "source-archive/statecraft/2026-04-16/"
    "source-pape-cyrus-janssen-us-has-no-idea-what-is-coming-next-2026-04-16.md"
)

SPEC = {
    "titles": [
        "Cold Open — Fourth Center Teaser and Janssen Welcome",
        "Escalation Trap Lock-In — Bombing Failed and Trump Clean-Win Narrative",
        "Blockade Framework — Day 46, Three Stages, and May/June Checkpoints",
        "Stage Four Fork — Fourth Center, Vance Uranium, and Oil Hegemon Path",
        "Israel as Spoiler — Prisoner's Dilemma, May 2025, and Rubio February",
        "Long War and Ground Odds — Iran Strategy, 70% to 80%, and Pakistan Flip",
        "Close — Chuck Hagel Event, Substack Plug, and Janssen Outro",
    ],
    "anchors": [
        "what in the world is the United States doing",
        "Within 10 days, parts of the global economy",
        "I've seen your analysis and in stage four",
        "Israel has basically been",
        "Iran has figured out that we cannot beat them",
        "Chuck Hagel Lectures at the University of Chicago",
    ],
    "note": (
        "Operator-paste with >> turn markers; Nomad Capitalist mid-roll + trailing "
        "event B-roll preserved verbatim. Cold-open non-linear lead preserved."
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
