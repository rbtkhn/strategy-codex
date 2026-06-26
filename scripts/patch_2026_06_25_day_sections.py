#!/usr/bin/env python3
"""source-section batch for 2026-06-25 statecraft intakes (thematic titles + anchors)."""
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

DAY = ROOT / "source-archive/statecraft/2026-06-25"

CAPTURES: dict[str, dict] = {
    "source-glenn-diesen-marandi-trump-lost-iran-war-must-sell-victory-2026-06-25.md": {
        "titles": [
            "Show Open — MOU Framework and Ten-Point Plan",
            "MOU Progress — Siege Lifted and Khamenei Ceiling Signal",
            "Hormuz Traffic — Iranian Exports and Trump Threats",
            "Walk Back vs Noise — MOU Text vs Trump Rhetoric",
            "Energy Crisis — Four-Week Reserves and MOU Fragility",
            "US Rhetoric Shift — Iran Legitimacy and Netanyahu Risk",
            "Hormuz Leverage — Month-One Sequencing and Insurance",
            "Zionism Erosion — Tucker, Epstein Class, False Flag",
            "Criticism Permanence — Israel Dissent and Iran Cards",
        ],
        "anchors": [
            "Americans were they needed an urgent agreement, but the",
            "were they were higher especially the the tank",
            "been intensifying the slaughter in Gaza. And the the cr",
            "of his advisers were unhappy that he said that aloud be",
            "the the way they're legitimizing Iran now, they say by",
            "that leverage is going to remain there for the time bei",
            "you know, we had more more instances, and then even Van",
            "of the box, it's very hard to put it back in. So, I thi",
        ],
    },
    "source-lascaris-helmer-trump-goal-destroy-russia-iran-2026-06-25.md": {
        "titles": [
            "Show Open — Voronezh Strike and Academy Speech",
            "Putin Green Light — NATO Airspace Assurances",
            "European Politics — Putin Misreads Germany and UK",
            "Imperialism Blind Spot — US and Europe vs Russia",
            "Trump Bold Ukraine — Kyiv Independent and G7 Line",
            "Witkoff-Kushner Deception — Kremlin Welcome Split",
            "Trump MOU Bribery — Hormuz Threat and Kushner Scheme",
            "Bribery Architecture — MOU Violation and Russia Reserves",
            "Iran Hormuz Leverage — US Voter Gas Pain",
        ],
        "anchors": [
            "to a question from a colonel",
            "president of the United States.",
            "themselves and all the other NATO supplies come in. It'",
            "uh that Ukraine now believes it has secured White House",
            "against Iran since last year",
            "impose a toll or any form of charge on the passage of o",
            "of the ways in which you can act unpredictably is to te",
            "not learning? It's it's extraordina",
        ],
    },
    "source-mario-nawfal-barnes-breaking-gcc-attack-iran-rubio-meeting-iran-strike-vessel-hormuz-2026-06-25.md": {
        "titles": [
            "Show Open — Hormuz Strike and Rubio GCC Statement",
            "Trump War Regret — Vance as MOU Architect",
            "Iran Leverage — Rug-Pull Economics and Vance MOU",
            "MOU Sabotage — Israel Lobby and Confabulation Risk",
            "Trump Confabulation — Fox News and MOU Continuity",
            "Vance Evolution — Day-One Hawk to Anti-War",
            "Vance Arc — Iran Hawk to Strategic Divorce",
            "Vance Divorce — Trita Parsi and Strategic Shift",
            "Thiel Question — Vance Biography and Palantir Ask",
            "Thiel Palantir — Vance Ohio and Thiel Backing",
            "Rubio Counter-Signal — CENTCOM and Gulf Sabotage",
            "Rubio Sabotage — Deal Fundamentals and Gulf Shift",
            "Gulf Realignment — Islamic NATO Without Washington",
            "Islamic NATO — Colby and Israel Lobby Fight",
            "China Ceiling — Hormuz Leverage and Kinetic Odds",
            "Hezbollah Reality — Lebanon Sovereignty Limits",
            "Lebanon Front — Netanyahu Escalation Ladder",
            "Netanyahu Box — NY Primaries and Strategic Options",
            "Israel Leash — NDAA Fusion Bills and Mamdani",
            "NDAA Fusion — Mamdani and Public Slap BB",
            "Iran Trust — Vance Dual Track and Gulf Shift",
            "Iran Trust — Dual Track and Event Close",
        ],
        "anchors": [
            "And so he entered this war against everyone's advice. He ent",
            "border wall, the wall just got two feet higher. Well, Iran, every time Trump",
            "So the uh I think it was a line in lockto stock uh two smoki",
            "then he'll flip to the other side. Then flip to this side. Then flip to the other side",
            "So just on Vance because I know you've been like very positi",
            "this little country that only lives because we because we support them.",
            "Then when they call them proxies, well, by that definition,",
            "the Peter Thiel connection. It's this technocratic Palantir connection.",
            "So, Peter Thiel backed him, Blake Masters, and I forget who the t",
            "The and Musk are much more alike than they are like everybody else in big tech.",
            "My biggest hope is I never thought Trump could because he's driven by fear now.",
            "and marginalizes and puts BB back in a box even if he doesn't want to be in a box.",
            "So, expect a lot of nonsense and shenanigans before Vance is ever ever able to get this ball",
            "that they took out I assume that ship that was traveling the Omani route.",
            "If if we're going to make a big deal about Iran's compliance with the nuclear non-prololiferation treaty",
            "Hezbollah. What fantasy land are they in? So all they're doing is wasting time grandstanding",
            "especially the more younger ones. The the data shows it's overwhelmingly when it comes to even the Jewish community",
            "sensitive military technology.",
            "So for me like I'm very skeptical about this alleged friction between the two.",
            "Well, that's interesting. Now, in terms of um coming for coming forward now",
        ],
    },
    "source-dialogue-works-larry-johnson-us-directly-calling-iran-vance-switzerland-bombshell-2026-06-25.md": {
        "titles": [
            "Show Open \u2014 June 25 Welcome",
            "Rutte NATO \u2014 Iran Complicity Claim",
            "Trump Europe \u2014 Passive Landing Rights",
            "Hormuz MarineTraffic \u2014 Outbound Only",
            "Oil Economics \u2014 Heavy Crude and Aviation",
            "Rutte White House \u2014 Trump Brand Salesman",
            "BRICS New Delhi \u2014 NSA Meeting and Yuan SIPs",
            "BRICS India \u2014 Hormuz Impact and Pakistan Path",
            "Pakistan Munir \u2014 SEO and US Control Myth",
            "Pakistan Munir \u2014 Imran Khan and Gulf Architecture",
            "Vance Channel \u2014 Switzerland Military Line",
            "Oman Hormuz \u2014 Mechanism Friction",
            "Netanyahu Lebanon \u2014 Offramp and Insanity",
            "Turkey NATO \u2014 Ukraine Second Front",
        ],
        "anchors": [
            "response from the spokesperson of Iranian foreign minis",
            "Trump got into a nasty back and forth with Maloney, Geo",
            "there's a website called marinetra.com. It shows real t",
            "20% of the supply was shut down. So what what happened ",
            "You stay here. I go over to these boards here because I",
            "India hosted the 16 BRICS National Security Advisors, N",
            "But the the problem with the Strait of Hormuz is that the",
            "Pakistan is a full member of the SEO Larry. >> Yeah >> ",
            "So here we now got Munir and yes Munir um ousted uh Immad",
            "JD Vance told unheard, you know, that one of the most s",
            "process of new the new mechanism is you is happening as",
            "Benjamin Net said that we have we removed an immediate ",
            "The next NATO summit is going to be in Turkey, Larry. a",
        ],
    },
    "source-judging-freedom-blumenthal-israel-in-panic-2026-06-25.md": {
        "titles": [
            "Israel Panic \u2014 Quinnipiac and US Support",
            "Netanyahu Perception \u2014 Successor Bench",
            "Zionism Structure \u2014 Colonial Dream Failed",
            "Hezbollah FPV \u2014 Southern Lebanon Front",
            "NYC Primaries \u2014 AIPAC Defeats",
            "Randy Fine \u2014 Republican Fissures and Vance",
        ],
        "anchors": [
            "Well, if you if you want to know how he's perceived in ",
            "Well, I've been saying that I think Netanyahu, while he",
            "What kind of shape is Hezbollah in today? Hezbollah has",
            "How do you I'm switching gears, Max. How do you read th",
            "Here is um the prince of the American Zionists in the U",
        ],
    },
    "source-alexander-mercouris-lukashenko-no-to-zelensky-belarus-stands-with-russia-russian-troops-enter-sumy-eu-no-to-kiev-entry-2026-06-25.md": {
        "titles": [
            "Show Open \u2014 Zelensky Belarus Threats",
            "Russian Security Council \u2014 Neighbors and Stability",
            "Lukashenko Minsk \u2014 Zelensky Warning and War Escalation",
            "Lukashenko Minsk \u2014 Vorobyov Alliance and Peace Stance",
            "Lukashenko Minsk \u2014 Relay Stations and Attack Deception",
            "Lavrov and Medvedev \u2014 Negotiations Stop",
            "Marat Khairullin \u2014 Substack Intro and Crimea Drones",
            "Marat Khairullin \u2014 Trump Narrative and Media Diversion",
            "Marat Khairullin \u2014 Donbass Fortified Line and Urban Sprawl",
            "Marat Khairullin \u2014 Fall Timeline and Odessa Demands",
            "Sumy Breakthrough \u2014 Frontline Entry and Evacuation Block",
            "Sumy Front \u2014 Kinburn Stunt and Kiev Battle Prep",
            "EU Membership \u2014 Ukraine Bargaining Chip",
            "Voronezh Strike \u2014 Dirty Dagger Missile",
            "Persian Gulf \u2014 MOU as Minsk Agreement",
        ],
        "anchors": [
            "We have two questions today. Our concerns internal secu",
            "Zelensky's representatives were here at this very spot,",
            "Now, the other interesting thing about these comments fr",
            "I do not believe, by the way, that the relay stations have been s",
            "Meanwhile, other Russian officials have been speaking a",
            "Marat Khairullin whom I have consistently considered the best rep",
            "He also says that the drone offensive is intended to impress one individual",
            "Anyway, put all that aside, Khairullin then does discuss that whe",
            "And Khairullin said that he expects certainly the whole of Donbass",
            "So that was what Khairullin said. Now interestingly there have be",
            "Elsewhere, the the Ukrainians continued to carry out their variou",
            "Apparently, at the last EU Council meeting, the one tha",
            "A few days ago, there was a attack, a strike on Verones",
            "Now, I do want to say a little bit more about the situation in th",
        ],
    },
    "source-daniel-davis-mearsheimer-russia-red-lines-crossed-2026-06-25.md": {
        "titles": [
            "Show Open \u2014 Rubio Side and Vance 2028 Game",
            "Tide Turned Narrative \u2014 Diplomatic Pain Not Defeat Russia",
            "Battlefield vs Mother Russia \u2014 Donbas Win by Fall",
            "Karaganov Logic \u2014 Europe Strikes and Nuclear Ladder",
            "Article 5 Blind Spot \u2014 Russian Hawks Deny Red Lines",
            "Rutte White House \u2014 Trump Trillion and Ukraine Hardball",
            "Drone War Not Artillery \u2014 Ammunition Dearth Rebuttal",
            "von der Leyen Drones \u2014 Europe Declared War Frame",
            "Merz Prevail Clip \u2014 Magic Formula Technology Leverage",
            "Delusional Escalation \u2014 Suicidal Article 5 Bet",
            "Peskov Nuclear Ace \u2014 Putin Clip and Red Line Fog",
            "Media Tide-Turned Blind Spot \u2014 Karaganov Majority",
            "East Asia Pivot \u2014 China Competition and Three Theaters",
            "East Asia Maritime \u2014 Taiwan Blockade and South China Sea",
            "Taiwan Porcupine \u2014 Multipolar Frame and Weapons Ask",
            "Taiwan Write-Off Debate \u2014 Realist Close and Substack",
        ],
        "anchors": [
            "we have this new narrative uh that the tide has turned",
            "let's distinguish, Danny, between what's happening on the battlefield",
            "Sergey Karaganov has famously made this argument",
            "hard to believe we're even having this conversation today",
            "Mark Rutte in the White House just lathering up",
            "dearth of of ammunition weapons",
            "Ursula von der Leyen seems to be uh completely backing up",
            "Chancellor Merz at that same conference added this",
            "Why do we think that a few more drones from the West",
            "we would let Vladimir Putin speak for himself",
            "And Gary, I'm sorry, Gary, can I get you to scroll up",
            "But listen, I want to shift gears real quick",
            "Furthermore, in the South China Sea they have slowly",
            "Taiwan presses Washington for billions in weapons",
            "what do you say about the the concept that says",
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
        print(f"OK {name} ({len(CAPTURES[name]["titles"])} sections)")
        if not args.dry_run:
            write_sectioned_capture(
                path,
                CAPTURES[name]["titles"],
                CAPTURES[name]["anchors"],
            )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
