#!/usr/bin/env python3
"""Source-section ship — 2026-06-29 Judging Freedom Crooke + Johnson interviews."""
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
HOST = "Andrew Napolitano"

CAPTURES: dict[str, dict] = {
    "source-judging-freedom-crooke-russia-ready-for-war-with-europe-2026-06-29.md": {
        "guest": "Alastair Crooke",
        "titles": [
            "Show Open — Iran MOU Before Russia Pivot",
            "Assembly Of Experts — Negotiating Team Crisis",
            "Hormuz Optics — Tankers AWACS And Distillates",
            "Iraq Turmoil — Sudani Arrests And Kurdish Foothold",
            "Lebanon Document — Unconstitutional And Valueless",
            "MOU Step By Step — Trump Redefine And Midterm Pivot",
            "Insurance And Hegemony — Bessent And Currency War",
            "US Withdrawal — Israeli Grand Strategy In Ruins",
            "Putin Warning — G7 European Three Optics",
            "Battlespace Fake — Kellogg Pressure And Close",
        ],
        "anchors": [
            "The assembly of experts, this is the assembly that oversees",
            "So the whole thing is becoming really quite crazy because even if",
            "Um because have you probably seen in Iraq there is great turmoil",
            "we haven't discussed Lebanon um where you know Trump has produced",
            "So, but the MOU but the MOU itself is substantially similar",
            "One or two more questions. One or two more questions on Iran before we get to uh Ukraine.",
            "Does a powerful US military presence in the Middle East any longer make sense?",
            "Let's transition to Russia.",
            "I assume you believe that that's a farce.",
        ],
        "note": (
            " · source-section pass 2026-06-29 (10 sections; MOU/Assembly/Hormuz/Iraq/Lebanon/Russia arc)"
        ),
    },
    "source-judging-freedom-johnson-trump-mou-unraveling-2026-06-29.md": {
        "guest": "Larry Johnson",
        "titles": [
            "Show Open — Putin Warning And Barbarossa Parallel",
            "Honest Brokers — Anchorage Dead And Front Shift",
            "Kiev Pressure — Gerasimov And Medvedev Brakes",
            "Information Gap — Maria And Russia Marketing",
            "Ukraine Money — Ponzi Pipeline To Congress",
            "MOU Violated — Weekend Hormuz Strike Theater",
            "Clause Five — Sullivan Derivatives And Iran Alone",
            "Insurance Sonar21 — Marinetraffic And Escort Physics",
            "US Withdrawal — CAOC Shaw And Base Evacuation",
            "Economic Reality — Helium Sulfur And SPR Drain",
            "Derivatives Quadrillion — Inflation And Close",
        ],
        "anchors": [
            "But how can the Russians be expected to view the Americans",
            "H do you think there's tremendous pressure on uh President Putin",
            "Larry. Now, Larry, now you're talking about another friend of ours, Maria.",
            "Well, and um in the meantime, who's paying American arms manufacturers",
            "Wow. Well, the uh memorandum of understanding it's falling apart, is it not?",
            ">> Right. Right. Here's someone surprisingly who agrees with you.",
            "There's uh another player here and you have written about this in a fascinating series",
            ">> Wow. I mean, does the Pentagon understand that a massive US presence",
            ">> Wow. How do you see this ending?",
            "Does the White House understand what you just explained?",
        ],
        "note": (
            " · source-section pass 2026-06-29 (11 sections; Putin/Ukraine/MOU clause-5/Hormuz/SPR arc)"
        ),
    },
}

def validate_capture(path: Path, spec: dict) -> list[str]:
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_section_patch_body(
            doc,
            manual_asr=(),
            interview_host=HOST,
            interview_guest=spec["guest"],
        )
    except ValueError as exc:
        return [str(exc)]
    return validate_section_anchors(body, spec["titles"], spec["anchors"])

def write_capture(path: Path, spec: dict) -> int:
    return write_interview_section_patch_capture(
        path,
        spec["titles"],
        spec["anchors"],
        manual_asr=(),
        manual_asr_spot_fix="",
        resection_note=spec["note"],
        interview_host=HOST,
        interview_guest=spec["guest"],
    )

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rc = 0
    for name, spec in CAPTURES.items():
        path = DAY / name
        if not path.is_file():
            print(f"missing {path}")
            rc = 1
            continue
        errs = validate_capture(path, spec)
        if errs:
            print(f"FAIL {name}:")
            for e in errs:
                print(f"  - {e}")
            rc = 1
            continue
        print(f"OK {name} ({len(spec['titles'])} sections, anchors validated)")
        if not args.dry_run:
            words = write_capture(path, spec)
            print(f"wrote {name} ({words} words, {len(spec['titles'])} sections)")
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
