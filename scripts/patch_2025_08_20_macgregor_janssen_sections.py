#!/usr/bin/env python3
"""source-section batch — Aug 2025 Cyrus Janssen × Macgregor (Russia-Ukraine end state).

Land: source-macgregor-cyrus-janssen-russia-ukraine-war-will-end-2025-08-20.md
Verify anchors: python scripts/patch_2025_08_20_macgregor_janssen_sections.py --check-anchors
Apply:          python scripts/patch_2025_08_20_macgregor_janssen_sections.py --apply
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
    "source-archive/statecraft/2025-08-20/"
    "source-macgregor-cyrus-janssen-russia-ukraine-war-will-end-2025-08-20.md"
)

SPEC = {
    "titles": [
        "Studio Open — Alaska Summit and Ukrainian Front Collapse",
        "Washington Reality TV — Vassal States and Trust Problem",
        "Ceasefire vs Peace — German Precedent and Fighting While Talking",
        "Zelensky Unpopularity — European Humiliation and Border States",
        "Security Guarantees Farce — Article 5 Workaround and Venezuela Task Force",
        "Putin-Zelensky Meeting — Dead End and Aid Suspension",
        "Washington Verdict — Russia Wins on Ground and Europe's Future",
        "Close — Nomad Plug and Janssen Outro",
    ],
    "anchors": [
        "Colonel, I want to talk about uh this difference between a peace agreement",
        "You know what's interesting, Colonel?",
        "Um, I think NATO membership is off the table",
        "Colonel, I've seen multiple reports",
        "Colonel, I've got one final question here",
        "Colonel, one more question. Do you feel that this time in Washington",
        "Well, Colonel, I want to thank you so much for these insights today",
    ],
    "note": (
        "Operator-paste with >> turn markers; Nomad Capitalist mid-roll preserved "
        "verbatim. McGregor ASR spelling preserved in archive."
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
