#!/usr/bin/env python3
"""Source-section ship — 2026-06-29 Daniel Davis × Ted Postol Patriot video-evidence interview."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    prepare_section_patch_body,
    validate_section_anchors,
    write_interview_section_patch_capture,
)

DAY = ROOT / "source-archive/statecraft/2026-06-29"
CAPTURE = "source-daniel-davis-ted-postol-patriot-missiles-fail-video-evidence-2026-06-29.md"
HOST = "Daniel Davis"
GUEST = "Ted Postol"

SPEC = {
    "titles": [
        "Show Open — Three Pillars And Ninety Percent Claim",
        "Gulf War 1991 — Ninety Six Percent And Decision Maker Deception",
        "Lewis Postol Paper — APS Panel And Video Contradiction",
        "Pack Two Objection — Video Evidence For PAC Two And Three",
        "PAC Radar Geometry — Slides Six Through Nine",
        "Drone Economics — Inventory Question And Tel Aviv Setup",
        "Frame Physics — Sky And Ground Detonation Signatures",
        "Tel Aviv Video One — PAC Two Misses And Ground Hit",
        "Salvo Video Two — One Intercept In Mass Incoming",
        "Countermeasures — Submunitions Spirals And Scoring Method",
        "Contractor Data Gap — Congress And Trillion Dollar Patriot",
        "THAAD And ATACMS — Europe Risk And Close",
    ],
    "anchors": [
        "Incidentally, we had uh an experience similar to this during the Gulf War of 1991",
        "Gary, could you um put on the first slide, slide number two?",
        "What do you say to that?",
        "Actually, let's uh let's just jump to that right now. Uh Gary, could you go to slide six?",
        "and I'm sorry, Ted, real quick before you leave that topic.",
        "All right. Um slide four shows you what happens when you have a detonation of a high explosive in the sky.",
        "Why don't we uh take take a shot at this, Gary? This is a real time.",
        "So, okay. So, let's go to uh um a a much more uh elaborate video, the video two.",
        "Here's another sequence I can show you. Lots of things happen here when you look at it uh in real time",
        "what I have been told by all of these people unanimously from different institutions",
        ">> And by the way, let me since Gary brought that up. Uh he's talking about THADs there.",
    ],
    "note": (
        " · source-section pass 2026-06-29 (12 sections; 1991 APS/Tel Aviv video/salvo/THAAD arc)"
    ),
    "manual_asr": (
        ("Rathon", "Raytheon"),
        ("Lheed", "Lockheed"),
        ("Aerrol", "Arrow"),
        ("Azerban", "Azerbaijan"),
        ("Atacums", "ATACMS"),
    ),
}


def validate_capture(path: Path) -> list[str]:
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_section_patch_body(
            doc,
            manual_asr=SPEC["manual_asr"],
            interview_host=HOST,
            interview_guest=GUEST,
        )
    except ValueError as exc:
        return [str(exc)]
    return validate_section_anchors(body, SPEC["titles"], SPEC["anchors"])


def write_capture(path: Path) -> int:
    return write_interview_section_patch_capture(
        path,
        SPEC["titles"],
        SPEC["anchors"],
        manual_asr=SPEC["manual_asr"],
        manual_asr_spot_fix="2026-06-29 — Raytheon/Lockheed/Arrow/Azerbaijan/ATACMS",
        resection_note=SPEC["note"],
        interview_host=HOST,
        interview_guest=GUEST,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = DAY / CAPTURE
    if not path.is_file():
        print(f"missing {path}")
        return 1

    errs = validate_capture(path)
    if errs:
        print(f"FAIL {CAPTURE}:")
        for e in errs:
            print(f"  - {e}")
        return 1

    if args.dry_run:
        print(f"OK {CAPTURE}: {len(SPEC['titles'])} sections, anchors valid")
        return 0

    rc = write_capture(path)
    print(f"wrote {CAPTURE} exit={rc}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
