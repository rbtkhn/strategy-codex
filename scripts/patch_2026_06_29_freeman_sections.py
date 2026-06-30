#!/usr/bin/env python3
"""Source-section ship — 2026-06-29 Glenn Diesen × Chas Freeman interview."""
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

CAPTURE = (
    "source-glenn-diesen-chas-freeman-us-iran-resume-war-israel-lebanon-civil-war-2026-06-29.md"
)

HOST = "Glenn Diesen"
GUEST = "Chas Freeman"

SECTION_TITLES = [
    "Show Open — MOU Misunderstanding And Strikes Resume",
    "Hormuz Control — MOU Violations And Gulf Retaliation",
    "Lebanon Deal — Pétain Parallel And Regional Chaos",
    "Rubio Gulf Tour — Grotius And Strait Precedent",
    "Attrition Frame — Forever War And Agreement Incapable",
    "Ukraine Pivot — British Strikes And European Talk",
    "Forever War Definition — Attrition Forces And Drone Twist",
    "Syria Turkey — Iraq Oil Route And Lebanon Document",
    "Oil Inventories — Switzerland Talks And US-Israel Split",
    "Israel Attrition — Multi-Front War And ICC Lawfare",
    "Policy Vacuum — Escalation Illusion And Washington Paralysis",
    "Predictable Catastrophe — Iran Russia Hawks And Putin Restraint",
    "Strategic Absence — Forever War Reinforcement And Close",
]

SECTION_ANCHORS = [
    "So we see all sorts of new terms being added by the United States",
    "Israel has successfully defied uh the uh American agreement with Iran",
    "I I should add that um the um reason that Donald Trump um fantasizes about the MOU",
    "But I think most people realize that the MOU wouldn't be necessarily followed",
    (
        "Donald Trump, having been frustrated uh in his pursuit of a notable victory "
        "in West Asia, seems to be pivoting back to Ukraine"
    ),
    "well there's no there is no trust in any of these dynamics",
    "I I I did want to switch a bit though to the Israeli component here",
    (
        "One other point and uh which is very relevant is not only is the traffic "
        "through the Strait of Hormuz disrupted"
    ),
    "You would think that with all the domestic problems, the Middle East on fire",
    "I I'm worried about the the escalation of the chaos here because I keep making the point",
    "Yeah, just uh it seems that all the conflicts we're heading into now, they're so predictable",
    (
        "No, I think um a rational examination of the record would demonstrate that "
        "um the exclusive use of force, military means to achieve uh objectives uh is counterproductive"
    ),
]

RESECTION_NOTE = (
    " · source-section pass 2026-06-29 (13 sections; split policy-vacuum close; "
    "MOU/Hormuz/Lebanon/Syria-Turkey/Ukraine/Israel arc)"
)

def validate_capture(path: Path) -> list[str]:
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_section_patch_body(
            doc,
            manual_asr=(),
            interview_host=HOST,
            interview_guest=GUEST,
        )
    except ValueError as exc:
        return [str(exc)]
    return validate_section_anchors(body, SECTION_TITLES, SECTION_ANCHORS)

def write_capture(path: Path) -> int:
    return write_interview_section_patch_capture(
        path,
        SECTION_TITLES,
        SECTION_ANCHORS,
        manual_asr=(),
        manual_asr_spot_fix="",
        resection_note=RESECTION_NOTE,
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
    print(f"OK {CAPTURE} ({len(SECTION_TITLES)} sections, anchors validated)")
    if not args.dry_run:
        before = len(path.read_text(encoding="utf-8").split())
        write_capture(path)
        after = len(path.read_text(encoding="utf-8").split())
        print(f"wrote {CAPTURE} (words ~{before} -> ~{after})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
