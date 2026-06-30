#!/usr/bin/env python3
"""source-section batch — Dec 2025 Cyrus Janssen × Macgregor (Venezuela disaster).

Land: source-macgregor-cyrus-janssen-why-venezuela-americas-next-disaster-2025-12-20.md
Verify anchors: python scripts/patch_2025_12_20_macgregor_janssen_sections.py --check-anchors
Apply:          python scripts/patch_2025_12_20_macgregor_janssen_sections.py --apply
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
    "source-archive/statecraft/2025-12-20/"
    "source-macgregor-cyrus-janssen-why-venezuela-americas-next-disaster-2025-12-20.md"
)

SPEC = {
    "titles": [
        "Cold Open — Coup Logic and Oil Blockade Montage",
        "Studio Open — Diplomatic Solvability and Maduro Oil Offer",
        "Coup Fantasy — CIA Mercenaries and Stabilization Delusion",
        "Sanctions Failure — DEA Data and Congress Absent",
        "Blockade as War — International Law and Drug Pretext",
        "Netanyahu Convergence — Venezuela Anti-Semitism Frame",
        "Occupation Math — Lebanon Analogy and Guard Syria Casualties",
        "China Diet — Not Imperial Japan and Taiwan Existential",
        "Close — Holidays and Citizen Journalism Outro",
    ],
    "anchors": [
        "Well, uh, Colonel, this is the perfect transition",
        "you touched on a really good point was the sanctions",
        "you mentioned earlier before, you know, we we about the drugs",
        "One last point. There's something else happening here",
        "I mean, and that's a tough one with Netanyahu",
        "And Colonel, I want to I want to kind of talk a little bit about Venezuela because I do think",
        "But Colonel I want to kind of the last question here",
        "Colonel, I always um always love our chats",
    ],
    "note": (
        "Janssen cold-open montage before studio welcome; >> turn markers preserved. "
        "Nomad-free capture."
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
