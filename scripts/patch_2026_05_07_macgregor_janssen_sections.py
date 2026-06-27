#!/usr/bin/env python3
"""source-section batch — May 2026 Cyrus Janssen × Macgregor (Iran week 10).

Land: source-macgregor-cyrus-janssen-trump-not-prepared-for-what-iran-does-next-2026-05-07.md
Verify anchors: python scripts/patch_2026_05_07_macgregor_janssen_sections.py --check-anchors
Apply:          python scripts/patch_2026_05_07_macgregor_janssen_sections.py --apply
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
    "source-archive/statecraft/2026-05-07/"
    "source-macgregor-cyrus-janssen-trump-not-prepared-for-what-iran-does-next-2026-05-07.md"
)

SPEC = {
    "titles": [
        "Studio Open — Week 10 Drama and Express Elevator to Hell",
        "Iran Stockpiling — Chinese Sorties and Ground Raid Risk",
        "Operation Freedom — GPS Escort and 24-Hour Pause",
        "Strategy Vacuum — Mossad Uprising Lie and Decapitation Pivot",
        "Destroy Iranian State — Soleimani Surge and Target Everything",
        "China Stands Up — Sanctions Defiance and BRICS Pivot",
        "Rubio Pretense — Heroic Iran and Hormuz Authority Plan",
        "Blockade Fallacy — Robin Brooks and Land Routes",
        "Unconquerable Iran — Nuclear Off Table and Oval Exit Speech",
        "Close — Substack and National Conversation Outro",
    ],
    "anchors": [
        "Colonel, what do you think about Iran and and what they've been doing",
        "Colonel, I'd like to talk about this Operation Freedom",
        "Well, Cyrus, I think we have to accept the reality that there has never been",
        "Uh Colonel, you touched on something important there, which is of course China",
        "Speak to the importance of that",
        "Colonel, I I have a good interesting question. We saw Secretary of State Marco Rubio",
        "Colonel, I want to talk a little bit about the blockade because I've seen",
        "now that the nuclear weapon is off the table as President Trump did point out",
        "Colonel, I just want to say thank you so much for your incredible insights",
    ],
    "note": (
        "Operator-paste with >> turn markers and [clears throat] cues preserved. "
        "Sargon ASR host name preserved in archive."
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
