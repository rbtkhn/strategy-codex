#!/usr/bin/env python3
"""source-section batch — 2026-06-26 MOU articles 1/5/11 cluster (Pape, Aguilar, Barnes, Parsi)."""
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

DAY = ROOT / "source-archive/statecraft/2026-06-26"

CAPTURES: dict[str, dict] = {
    "source-moral-resistance-robert-pape-us-strike-iran-lebanon-deal-violates-mou-2026-06-26.md": {
        "titles": [
            "Show Open — Escalation Trap and MOU Article 1",
            "Balance of Power — US, Israel, and Iran After 116 Days",
            "Lebanon and Unfrozen Assets — Power Beyond Paper",
            "Three Violations — Barnes, Rubio, and Articles 1/5/11",
            "Oil Glut — Floating Storage and Trader Jawboning",
            "Hormuz Protection Racket — Business Model vs Power",
            "CENTCOM Strikes — Iran Response and Non-Ceasefire",
            "Oman Article 5 — Red Lines and Southern Passage",
            "Israel Trauma and Regional Close — Drones, Fourth Center, Sparta",
        ],
        "anchors": [
            "The big framework here to keep in mind is the balance of power",
            "Now, in this particular case, it's actually the case that the balance of power",
            "But America and Israel, they've got to accept that",
            "Number one, they're violating article one",
            "So taking that into consideration, you're talking about this power dynamic",
            "See, a lot of people think that what's going on here is a straightforward business deal",
            "So talking about this like power dynamic today we had it where",
            "Israel's been whatever the MOU and that's why I never thought the MOU was going to succeed",
        ],
    },
    "source-dialogue-works-anthony-aguilar-us-airstrikes-inside-iran-escalation-2026-06-26.md": {
        "titles": [
            "Show Open — CENTCOM Strikes and Singapore Ship",
            "MOU Article 1 — Lebanon Occupation Violation",
            "MOU Article 5 — Channel Control Before Point Five",
            "NDAA Rearm — Wartime Stock Replenishment",
            "Sir and Sirik — Hormuz Strike Belt",
            "Rubio Gulf Tour — Oman and Article 5 Politics",
            "Iran Response — Kuwait, Bahrain, and Jordan",
            "Lebanon Tripartite — Civil War and Occupation Trap",
            "Syria Infection — Chaos as Pretense",
            "Powder Keg — Israel First vs MOU",
            "Kashm Island — Same Geographic Targeting",
            "PLO Model — Disarm Hezbollah Trap",
            "Gaza UN Report — GHF Amir, IRGC Comms, and Close",
        ],
        "anchors": [
            "Well, on the other hand, the United States and Israel uh completely ignore",
            "So when you look at uh further down the list at point number five",
            "So, it's clear to me that the United States has once again used negotiation",
            ">> Here is what was reported on Iranian media, Tony",
            "I think Tony, one of the problems right now is that the United States is trying to manipulate",
            "I think if they if they respond, it's going to be on Bahrain, Kuwait, and Jordan",
            ">> Yeah. Part of the problem, Tony, is in Lebanon",
            ">> Yeah. Here is PBS News reported, Tony, that a US official reported",
            ">> And if you look at these roads that the United States is now going down",
            ">> Yeah. The new report shows that the American attack they they hit the Kashma Island",
            ">> Yes. They literally did the same, you know, disarmament and talking and talking",
            "remember when you you you got back from Gaza and we talk about what is happening",
        ],
    },
    "source-dialogue-works-robert-barnes-iran-drones-ship-without-state-approval-2026-06-26.md": {
        "titles": [
            "Open — Hormuz Drones and Lebanon Washington Deal",
            "US Exit — Bahrain Bases and Low Kinetic Odds",
            "China SPR — Hormuz Leverage Ceiling",
            "Vance MOU Architect — Trump and Iran Negotiation",
            "Lebanon Proxy — Reagan Precedent and Hezbollah",
            "Article 5 Fees — Montreux and Service Charges",
            "Hormuz Control — Routes, Fees, and Leverage",
            "GCC Realignment — Islamic NATO and Regional Powers",
            "NDAA 224 and 662 — Israel Lobby and Vance Divorce",
            "Midterms and Israel — Electoral Liability",
            "Tucker Surge — Third Party, UK Parallel, and Close",
        ],
        "anchors": [
            "Secondly, the what Larry Johnson and others have been reporting",
            "And you aggregate those factors, China was not in a position to afford",
            "What Vice President Vance, who's the entire architect of this deal",
            "Yeah, you can raise to the ground Gaza style a whole bunch of homes",
            ">> Yeah. One of the main problems as it was mentioned by Marco Rubio",
            "Once Iran fully appreciated that, they weren't going to give that up",
            ">> So two different things have happened.",
            "We have two sections, remember 224 and 662, the military and intelligence",
            ">> Yeah. Robert, do you think that what how what would be your response",
            "What is your assessment of the new movement within the Republican party?",
        ],
    },
    "source-mario-nawfal-trita-parsi-israel-lebanon-peace-agreement-mou-breach-2026-06-26.md": {
        "titles": [
            "Show Open — Netanyahu Readout and MOU Article 1",
            "Deal Text Gap — Bifurcated US Foreign Policy",
            "Lebanon Government — Hezbollah vs Occupation",
            "Al-Shara Rumors — Syria Border Buildup",
            "Regional Architecture — Riyadh Security Meeting",
            "Turkey Threat — Israeli Minister Quotes",
            "Israel-Iran Reversal — Periphery Doctrine Since 1991",
            "Anti-Abraham Accords — Pan-Islamic Axis",
            "Oman Bloomberg — Fees and Pre-War Status Quo",
            "Moshaba Risk — Funeral, Assassination, and Close",
        ],
        "anchors": [
            "So, again, um, want to be careful not to comment too much until I've seen the actual text",
            "Lebanese government right now and its standing is uh one that we should take a close look",
            ">> You mentioned something that is is is I'm just trying to make sense of it",
            "at the same time, I think um we're moving very fast in this effort by regional states",
            ">> let me read it. Israeli minister the Israeli minister of science technology",
            "But he even continued, at least the facto in the 1980s when the Islamic Republic came into existence",
            ">> Yeah, we're talking about that. Think about it. We're talking about that axis",
            "Israel appears to be emerging as the biggest loser in this war",
            "I completely missed that. Did you see that?",
        ],
    },
}

def validate_capture(path: Path, spec: dict) -> list[str]:
    errors: list[str] = []
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = split_transcript_document(doc)
    except ValueError as exc:
        return [str(exc)]
    if body.lstrip().startswith("### "):
        errors.append("already sectioned")
        return errors
    titles = spec["titles"]
    anchors = spec["anchors"]
    if len(titles) != len(anchors) + 1:
        errors.append(f"title/anchor count mismatch: {len(titles)} titles, {len(anchors)} anchors")
    cursor = 0
    for anchor in anchors:
        try:
            pos = find_anchor_pos(body, anchor, cursor)
            cursor = pos + 1
        except ValueError as exc:
            errors.append(str(exc))
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--path", action="append", help="Single capture filename under day folder")
    args = parser.parse_args()

    names = args.path or sorted(CAPTURES.keys())
    failed = 0
    for name in names:
        if name not in CAPTURES:
            print(f"skip {name} (no section map)")
            failed += 1
            continue
        path = DAY / name
        if not path.is_file():
            print(f"missing {path}")
            failed += 1
            continue
        errs = validate_capture(path, CAPTURES[name])
        if errs:
            print(f"FAIL {name}:")
            for e in errs:
                print(f"  - {e}")
            failed += 1
            continue
        print(f"OK {name} ({len(CAPTURES[name]['titles'])} sections)")
        if not args.dry_run:
            write_sectioned_capture(
                path,
                CAPTURES[name]["titles"],
                CAPTURES[name]["anchors"],
            )
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
