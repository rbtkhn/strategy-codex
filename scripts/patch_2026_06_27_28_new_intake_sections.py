#!/usr/bin/env python3
"""Source-section ship — Aguilar, Diesen×Johnson, breaking DW×Johnson (2026-06-27/28 intake)."""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    prepare_section_patch_body,
    validate_section_anchors,
    write_interview_section_patch_capture,
)

ARCHIVE = ROOT / "source-archive" / "statecraft"

@dataclass(frozen=True)
class CaptureSpec:
    rel_path: str
    host: str
    guest: str
    titles: tuple[str, ...]
    anchors: tuple[str, ...]
    resection_note: str

SPECS: tuple[CaptureSpec, ...] = (
    CaptureSpec(
        "2026-06-27/source-dialogue-works-anthony-aguilar-us-airstrikes-southern-iran-tehran-retaliation-us-bases-2026-06-27.md",
        "Nima Alkhorshid",
        "Anthony Aguilar",
        (
            "Show Open — Sirik Strikes And MOU Facade",
            "Escalation Ask — Fifth Fleet And Strike Origins",
            "MOU Clause One — Rubio Lebanon Side Quest",
            "Singapore Vessel — US Iran Strait Parity",
            "Strike Routes — Jordan Saudi Airspace Map",
            "Carrier Vs Land Bases — Gulf State Complicity",
            "Jordan Base — Capability Versus Political Will",
            "Trump Threat — US Cannot Be Trusted",
            "Lebanon Map — Yellow Line Occupation",
            "Rubio Vance Dual Track — MOU Clause Collision",
            "Gaza Annexation — Israel Escalation Loop",
            "Lebanon Puppet — Hezbollah Calculus",
            "Close — Negotiations Dead Displacement Scale",
        ),
        (
            ">> What do they want to achieve, Tony?",
            ">> When it comes to clause one,",
            "And what better time than now uh well, there's this negotiation going on",
            ">> Now, just let me bring the map here because I want to know",
            ">> You you Let me bring up the Indian Ocean basically here.",
            ">> Isn't that amazing that we've heard nothing from the government in Jordan so far?",
            ">> Here is what Donald Trump tweeted just moments ago.",
            ">> Yes. >> And here is you see the yellow line in the map",
            "While you have JD Vance supposedly negotiating this MOU between the United States of America and Iran",
            ">> Yeah. >> So much for that ceasefire.",
            ">> The Lebanese government has shown itself to be its true uh true face",
            ">> There would be no third round of negotiations because nothing has happened so far.",
        ),
        " · source-section pass 2026-06-28 (13 sections)",
    ),
    CaptureSpec(
        "2026-06-27/source-glenn-diesen-larry-johnson-putin-warns-west-russia-ready-war-2026-06-27.md",
        "Glenn Diesen",
        "Larry Johnson",
        (
            "Show Open — NATO Proxy And Petersburg Strikes",
            "Karaganov Ladder — Anchorage Diplomacy Dead",
            "War Fictions — Propaganda And Tactical Nukes",
            "Putin Barbarossa — Preempt Not Wait",
            "Charter 2021 — February 2022 Preemption",
            "Putin German Taunt — British Nuclear Poking",
            "Europe Safe Zone — Proxy War Design Flaw",
            "Putin Catch Up — Medvedev Public Pressure",
            "Europe Chihuahua — Mass Psychosis Censorship",
            "Hormuz Fuel Shock — World By July 15",
            "BRICS CIPS — Rubio Versus Kissinger",
            "US Cannot Fight Russia — Burevestnik Scenario",
            "Close — CENTCOM Redeploy Order",
        ),
        (
            "I was wondering what is your take though on this speech?",
            "It's been so many fictions all along.",
            "Uh I did notice in Putin's speech he did refer to operation um Barbarossa",
            "Yeah, this is an important part of that is if Russia thinks it's going to be attacked",
            "Well, I I don't know if you saw Putin issued a response to the Germans the other day",
            "Well, one can understand though why well especially the British because they appear",
            "Um but uh I was wondering how do you see Putin's changed over time because last year",
            "If the Russians wait much longer then they might have more capabilities.",
            "Well, there's actually a reality that's going to descend on Europe within the next two to three weeks",
            "Um, I did want to ask about the Marco Rubio in Anchorage though.",
            "but yeah my last question was Russia strikes Europe in retaliation to restore it the turns",
            "So hey, let me let me leave you. I got unrelated to this, but we'll call it breaking news.",
        ),
        " · source-section pass 2026-06-28 (13 sections)",
    ),
    CaptureSpec(
        "2026-06-28/source-dialogue-works-larry-johnson-breaking-explosions-bahrain-kuwait-kiev-2026-06-28.md",
        "Nima Alkhorshid",
        "Larry Johnson",
        (
            "Breaking Open — Bahrain Kiev Dual Track",
            "UKMTO Route — MOU Double Game",
            "Theater Vs Hard Hit — Escalation Cycle",
            "Velos Escort — OSINT Ship Tracker",
            "Oman Channel — June 24 Protocol",
            "Marinetra Live — Velos Atlantis Debunk",
            "Kuwait Ballistic — Boot Club Interlude",
            "Gulf Blinder — Qatar Saudi UAE Deals",
            "Kiev Strike Question — Largest Hit In A While",
            "Ukraine Desperation — Europe Strike Risk",
            "Russia Credibility — Putin Barbarossa Warning",
            "Kiev Targeting — Odessa Radioactive Trace",
            "Kiev Live Wrap — Iskander Kinzhal Hits",
            "Trump Statement — Al Isa Kuwait Hits",
            "Hormuz Choice — Iran Procedure Versus Breach",
            "IRGC Statement Read — Islamabad Navigation MOU",
            "Bully Debate — Proportional Versus Disproportionate",
            "Aircraft Escort — Open Source Ship Debunk",
            "Hormuz Fees — Two Million Barrels Stuck",
            "Proportional Versus Fox — Trump Nuclear Bluff",
            "Assembly Of Experts — Ten Point Red Lines",
            "Parallel Lebanon Deal — Trump Aoun Undermine MOU",
            "CENTCOM Footage — Sand Strikes Versus Bases",
            "Ukraine Front Arc — Parenthesis Advance Map",
            "Netanyahu Lebanon — No Withdrawal Pledge",
            "Merged Fronts — World War Risk",
            "Italy Airspace — Meloni Trump Close",
        ),
        (
            ">> Uh the world's going crazy.",
            "However, today, earlier today, uh, Iran struck Bahrain even before the current",
            "So today Larry there was a situation where a separate to the vessel that got hit",
            "In the meantime, while I'm getting that up, um, what's what's your thoughts about the Omanis?",
            "there's one one that's uh the the Atlantis is transited is coming out of the straight",
            "warning sirens in Kuwait. Ballistic missiles",
            ">> So, The other element of this is Larry uh it makes sense that I mean they keep hitting Bahin",
            "But just Larry, the um the question to you is this. We basically have a scenario",
            "Well, it's absolutely out of desperation and it's with the full encouragement",
            "Russia doesn't do bluster. Russia is not a bullshitter.",
            "And in terms of within Kiev, what have been the specific targets",
            "So, just for the audience, we have heard that there are major strikes",
            "Going back to specifically uh Iran, the latest news on that is the base in Kuwait has been hit.",
            "Yeah. Well, you know, the US had a choice.",
            "we have got a statement by uh the IRGC and they've said the following quote.",
            "Actually, I'm very happy with this response because I do believe that the way you deal with bullies",
            "Now, it was escorting not with a naval vessel. That's the key.",
            "True, Larry. wants to if it wants to go out",
            "You got to Larry, my kids watch it",
            "Yeah. So Larry, there was today and I and I do I'm not sure if this had an impact on the decision-m or not",
            "But just before we do, Larry, um quickly conversation about Lebanon",
            "Okay, let me show you this guys as well as Larry",
            "Now, um coming back to uh Okay, so more breaking news",
            "Um, Larry, Netanyahu came out today once again and said they will not be withdrawing from Lebanon.",
            "I know the it doesn't it isn't really called a war, but okay. Two conflicts, two wars",
            "Um, actually, uh, okay, I'll talk to you about next time, but there was this report about Italy",
        ),
        " · source-section re-section pass 2026-06-28 (27 sections; Oman marinetra split)",
    ),
)

def validate_spec(spec: CaptureSpec) -> list[str]:
    path = ARCHIVE / spec.rel_path
    if not path.is_file():
        return [f"missing {path}"]
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_section_patch_body(
            doc,
            manual_asr=(),
            interview_host=spec.host,
            interview_guest=spec.guest,
        )
    except ValueError as exc:
        return [str(exc)]
    return validate_section_anchors(body, spec.titles, spec.anchors)

def ship_spec(spec: CaptureSpec) -> int:
    path = ARCHIVE / spec.rel_path
    return write_interview_section_patch_capture(
        path,
        spec.titles,
        spec.anchors,
        manual_asr=(),
        manual_asr_spot_fix="",
        resection_note=spec.resection_note,
        interview_host=spec.host,
        interview_guest=spec.guest,
    )

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--only",
        choices=[s.rel_path for s in SPECS],
        action="append",
        dest="only",
        help="Repeatable; default all specs",
    )
    args = parser.parse_args()
    selected = [s for s in SPECS if not args.only or s.rel_path in args.only]
    if not selected:
        print("no captures selected")
        return 1

    failed = False
    for spec in selected:
        errs = validate_spec(spec)
        if errs:
            failed = True
            print(f"FAIL {spec.rel_path}:")
            for err in errs:
                print(f"  - {err}")
            continue
        print(f"OK {spec.rel_path} ({len(spec.titles)} sections)")
        if not args.dry_run:
            ship_spec(spec)
            print(f"  shipped {spec.rel_path}")

    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
