#!/usr/bin/env python3
"""source-section batch — Apr 2026 Cyrus Janssen × Macgregor (Iran ground invasion).

Land: source-macgregor-cyrus-janssen-us-launching-iran-ground-invasion-2026-04-17.md
Verify anchors: python scripts/patch_2026_04_17_macgregor_janssen_sections.py --check-anchors
Apply:          python scripts/patch_2026_04_17_macgregor_janssen_sections.py --apply
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
    "source-archive/statecraft/2026-04-17/"
    "source-macgregor-cyrus-janssen-us-launching-iran-ground-invasion-2026-04-17.md"
)

SPEC = {
    "titles": [
        "Studio Open — US Blockade and Red Sea Threat",
        "Global Energy Complex — Fertilizer Shortfall and Tanker Queue",
        "Petrodollar Collapse — Yuan Trade and Houthi Pipeline Risk",
        "Roy Cohn Trump — Attack Deny Victory and Zionist Money",
        "Failed Air Metrics — Underground Iran and Ceasefire Rearm",
        "Israeli Demands — Destroy Iraq Slip and Monday Bombing",
        "Ground Troops Delusion — School Buses and Island Seizure",
        "Regional Cascade — Turkey Egypt and Nuclear Escalation",
        "Trump Stability — 25th Amendment and Epstein Class",
        "Disengage Fantasy — Keane Metrics and Montreux Model",
        "Close — Substack Plug and PIA Outro",
    ],
    "anchors": [
        "the global energy complex consists",
        "The petrodollar has been the source",
        "was a man named Roy Cohn",
        "So, we're going to attack Iran",
        "utterly destroy Iraq because he thinks",
        "Everybody everybody gets excited over the troops",
        "Then you have Egypt, and Egypt is a boiling pot",
        "Colonel, what about Donald Trump? I mean, as you're looking at him",
        "my suspicion is that General Keane, who is the uh essentially",
        "Colonel, I just want to say thank you so much for your incredible time today",
    ],
    "note": (
        "Operator-paste with >> turn markers; Private Internet Access mid-roll "
        "preserved verbatim. 'destroy Iraq' ASR slip preserved in archive."
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
