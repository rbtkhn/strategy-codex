#!/usr/bin/env python3
"""source-section batch for 2026-06-23 statecraft intakes."""
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

DAY = ROOT / "source-archive/statecraft/2026-06-23"

CAPTURES: dict[str, dict] = {
    "source-judging-freedom-freeman-should-iran-trust-trump-2026-06-23.md": {
        "titles": [
            "Show Open — Should Iran Trust Trump",
            "Hormuz MOU — Israel Lebanon Tether",
            "Trump Threats — War Crimes and Trust",
            "Ben Gvir — Lebanon Playground",
            "Israeli Public — No Introspection",
            "Vance Spin — IAEA Inspections",
            "Reflecting Pool — Corruption and Midterms",
            "PY Purge — Intelligence Hollowed Out",
            "Close — Farewell",
        ],
        "anchors": [
            "Ambassador Freeman, welcome",
            "within 48 hours of signing the memorandum",
            "What happens when the Israelis persistently continue to kill in Lebanon",
            "Does the Israeli public, as far as you can tell",
            "they have agreed to inspections",
            "reflecting pool controversy",
            "Mr. PY, the acting head of the National Intelligence",
            "Ambassador Chaz Freeman, thank you very much",
        ],
    },
    "source-judging-freedom-hoh-how-empire-recruits-soldiers-2026-06-23.md": {
        "titles": [
            "Show Open — Empire and Recruitment",
            "Hormuz Posturing — Iran Leverage",
            "Trump Trash Talk — Walkout",
            "MOU Real — Midterms and Legacy",
            "Lebanon — US Can Stop Israel",
            "Manab Slaughter — Pentagon Foot-Drag",
            "Plan B — No Escalation Room",
            "Recruitment — Propaganda and Belief",
            "Hollywood — Pentagon Script Authority",
            "MAGA Recruiting Ad — Cult of Personality",
            "Close — Farewell",
        ],
        "anchors": [
            "Matt, welcome here",
            'During negotiations, Trump tells says to Fox, "You close it,"',
            "Is the memorandum of opportunity real or just a pause",
            "Can the US stop uh Israeli slaughter in Lebanon",
            "Palanteer was the data processing system",
            "Plan B, judge, was the the fantastical invasion of the Kurds",
            "In an all volunteer army or military, how deceptive is recruitment",
            "What did you believe? I'm talking about big picture",
            "Does the Pentagon subsidize Hollywood movies",
            "the first ad put out by the quote department of war",
        ],
    },
    "source-judging-freedom-mearsheimer-netanyahu-and-israeli-decline-2026-06-23.md": {
        "titles": [
            "Show Open — Hormuz Basics",
            "February 27 — Misread Iranian Hand",
            "MOU Real — Economic Catastrophe",
            "Trump Trash Talk — Trust and Missiles",
            "Israel Lebanon — Deal at Risk",
            "Israeli Mindset — No Introspection",
            "Ben Gvir Clips — Playground Threat",
            "US Spigot — Dependency and Power",
            "Adelson — Betrayal Narrative",
            "Close — Farewell",
        ],
        "anchors": [
            "Professor Mir Shimemer, a pleasure as always",
            "on February 27th, uh the Iranians had no good sense",
            "Is in your view is the memorandum",
            "You close it, meaning hormuz",
            "What happens if the Israelis just keep marching",
            "do you detect any collective introspection",
            "here is um here are two clips from Ben Gabir",
            "Would they do all this if Donald Trump turned off the spigot",
            "the Israeli daily newspaper owned by Mrs. Adlesen",
        ],
    },
    "source-judging-freedom-ritter-russia-us-iran-mou-ukraine-attacks-moscow-2026-06-23.md": {
        "titles": [
            "Show Open — Russia Trip Impressions",
            "Donbas Front — Drones and Morale",
            "Europe Collapse — Then What Trap",
            "Storm Shadow — British Red Line",
            "Rabid Dog — To Kill a Mockingbird Panel",
            "SMO Endgame — Donetsk This Summer",
            "Brakestop — Long-Range Missile Tests",
            "Israel Host — MOU and Economy",
            "Hormuz Planning — Hegseth Cheerleaders",
            "Lavrov — Agreement Incapable",
        ],
        "anchors": [
            "I want to start with your general impressions",
            "I spent a considerable amount of time in the uh Donbas",
            "Keir Starmer's out. Merz is not long to follow",
            "Most likely it was Storm Shadow that Keir Starmer signed off on",
            "Europe is the equivalent of a rabid dog",
            "What are the prospects for a conclusion to the uh special military operation",
            "Britain tests long-range missiles to help Ukraine bomb Moscow",
            "Switching over to uh Iran and the memorandum of understanding",
            "The difference is Pete Hegseth",
        ],
    },
    "source-breaking-points-mearsheimer-slippery-slope-oblivion-russia-ukraine-2026-06-23.md": {
        "titles": [
            "Open — Ukrainian Strikes on Russia",
            "Red Lines — Russia Nuclear Frustration",
            "Ukrainian Theory — Stress Test",
            "Iran Parallel — Strait Versus Bombing",
            "G7 Trump — Rhetoric and Munitions",
            "Dalio Asia — Industrial Base Weakness",
            "Russian Strike Logic — Conventional Versus Nuclear",
            "Close — Thanks",
        ],
        "anchors": [
            "Russian red lines. They don't respect the fact",
            "stress test the Ukrainian theory",
            "closing down the straight",
            "Trump administration's approach",
            "expended so many munitions",
            "Ray Dalio is out with a new essay",
            "slippery slope to oblivion",
        ],
    },
    "source-breaking-points-mearsheimer-trump-lost-iran-spoils-sanctions-relief-2026-06-23.md": {
        "titles": [
            "Open — Iran Deal Spoils",
            "Lobby Lock — Economic Hammer Break",
            "Petrodollar — Sanctions Relief Clawback",
            "Deal Meaning — Israel Disaster",
            "Iran Power — Regional Balance",
            "Turkey Threat — Greater Israel Logic",
        ],
        "anchors": [
            "the Israel lobby controls everything",
            "primary sanctions relief actually allows Iran",
            "What would that deal mean for Israel",
            "could easily surpass Israel in a matter of a decade",
            "Turkey will be the new front in the greater Israel project",
        ],
    },
    "source-dialogue-works-helmer-vance-lebanon-mou-hormuz-putin-ukraine-2026-06-23.md": {
        "titles": [
            "Show Open — MOU Round Two",
            "Vance Lebanon — Deconfliction Mechanism",
            "Helmer — Vance Corruption Frame",
            "Israel Tether — Netanyahu Government",
            "Hormuz — Frozen Assets and Sanctions",
            "Putin Ukraine — War With West",
            "US Midterms — Catholic Voters",
            "Close — Farewell",
        ],
        "anchors": [
            "finally, we had the second round of negotiations",
            "deconliction mechanism",
            "Vance had to say about him is utterly corrupt",
            "Netanyahu government than than with uh everybody",
            "frozen assets and we have the sanction",
            "an appeal to the Roman Catholic voters who way outnumber",
            "Lavrov represents and the intelligence services",
        ],
    },
    "source-dialogue-works-henningsen-israels-losses-lebanon-hezbollah-iran-geneva-talks-2026-06-23.md": {
        "titles": [
            "Show Open — Geneva and Lebanon",
            "Hezbollah Losses — Southern Lebanon",
            "Israel Predictability — Escalation Pattern",
            "Farmers Clause — Frozen Assets Spin",
            "Trump Vance — Poll-Driven Policy",
            "Hezbollah Contained — Escalation Risk",
            "Israeli Perception — War Fatigue",
            "Close — Farewell",
        ],
        "anchors": [
            "Welcome back, Patrick",
            "Hezbollah operatives near the Ali Taher ridge",
            "They're very predictable, by the way",
            "food to feed the Iranian people and get American farmers rich",
            "Vance and Trump are pushing is because the poll numbers",
            "is contained at the moment between Hezbollah and uh Israel",
            "Israelis are perceived are getting to that point",
        ],
    },
    "source-dialogue-works-marandi-new-hormuz-mechanism-iaea-access-put-on-hold-2026-06-23.md": {
        "titles": [
            "Show Open — Frozen Assets",
            "Lebanon — Netanyahu Won't Leave",
            "Hormuz Mechanism — IAEA on Hold",
            "Russia FM — Trust and MOU",
            "Israeli Attack — Cooperation Punished",
            "Pakistan Route — China Links",
            "US Politics — Democrat Pressure",
            "Close — Farewell",
        ],
        "anchors": [
            "frozen assets and JD Vance the vice president",
            "Netanyahu said his forces are not leaving Lebanon",
            "when you see foreign minister of Russia talking this way",
            "status of the new mechanism of this trade of Hermos",
            "Israelis carried out this attack to punish",
            "links to China uh are go through Central Asia",
            "he wanted to to bring about any changes because the both the Demo",
        ],
    },
    "source-duran-mercouris-rubicon-crossed-zelensky-targets-belarus-2026-06-23.md": {
        "titles": [
            "Show Open — Project Ukraine",
            "Storm Shadow — Voronezh Signal",
            "Poland Row — Melnik Provocation",
            "UK Missile Program — Moscow Target",
            "Rubicon Crossed — Tehran Precedent",
            "Gordon Hahn — Irrational Hawks",
            "Belarus Front — Zelensky Ultimatum",
            "Odessa Thesis — Post Donbas",
        ],
        "anchors": [
            "storm shadow missiles uh hitting Varonish",
            "this row with uh Zalinski and Navroski",
            "testing long range missiles to bomb to help Ukraine bomb Moscow",
            "Rubicon was crossed um the the neocons",
            "Gordon Han, who we've done programs with",
            "take these warnings from um Zalinski extremely seriously",
            "they care about say say Kiev and Odessa",
        ],
    },
    "source-daniel-davis-macgregor-pressure-remove-trump-from-office-growing-2026-06-23.md": {
        "titles": [
            "Show Open — Remove Trump Pressure",
            "Future Warfare — Star Wars Delusion",
            "Supply Chain — Sanctions Blowback",
            "Iran Damage — Zionist Regime",
            "Trump Wins — MOU Spin",
            "Arab World — Perpetual Conflict",
            "Lebanon Security Zone — Israel",
            "Close — Thanks",
        ],
        "anchors": [
            "mastered capabilities that make that an impossibility",
            "future of warfare looking like Star",
            "Supply chain redundancy from ju",
            "damaged as a result of the US military aggression",
            "he's won. So, he just continues to say these things that are true",
            "keep the Arab world weak by keeping it perpetually enmeshed",
            "maintaining the security zone in southern Lebanon",
        ],
    },
    "source-daniel-davis-postol-patriot-missile-capabilities-2026-06-23.md": {
        "titles": [
            "Show Open — Interceptor Fundamentals",
            "Graham Clip — Hezbollah Escalation Policy",
            "Warsaw Brief — Skepticism and Data",
            "Gulf War — Scud Video Evidence",
            "Raytheon — Integrity Exchange",
            "Iran Theater — Radar Detonation Data",
            "Tomahawk — Russia Intercept Ability",
        ],
        "anchors": [
            "when you use Hezbollah to attack Israel, I think the new policy will",
            "lot of skepticism and hostility quite honestly from the audience",
            "spiraling uh Scud. So, this is a a very interesting video",
            "everything that people say about your integrity is demonstrated",
            "detonation of the uh of the incoming Iranian ballistic missile warhead",
            "tomahawk cruise missiles. Does Russia have the ability",
        ],
    },
    "source-mario-nawfal-weichert-tucker-mtg-abandon-republican-party-maga-falling-apart-2026-06-23.md": {
        "titles": [
            "Show Open — MAGA Fracture",
            "Hormuz Green Route — Blockade",
            "Oil Restart — Months Timeline",
            "Netanyahu — Act Alone Frame",
            "Military Industry — US Dependence",
            "West Bank — Human Rights",
            "Tucker MTG — GOP Exit",
        ],
        "anchors": [
            "administration and they use that green route down there",
            "weeks, probably closer to months before any of those oil production",
            "to act alone against this nuclear threat against Iran",
            "having a totally independent military industry",
            "rights conditions in the West Bank and Gaza",
            "Tucker and Marjorie Taylor",
        ],
    },
    "source-mercouris-putin-warns-russian-army-war-with-west-coming-russia-leads-west-in-arms-output-us-iran-talks-stuck-2026-06-23.md": {
        "titles": [
            "Show Open — Cadets Meeting",
            "Putin Speech — War With West",
            "Historic Lands — Left Bank Ukraine",
            "Lavrov — Diplomacy Failed",
            "Europe Aggression — Storm Shadow",
            "Belarus — Lukashenko Alliance",
            "Hezbollah — Lebanon MOU Link",
            "US Iran Talks — Stuck",
            "Close — Platform Reminder",
        ],
        "anchors": [
            "meeting between Putin and military cadets",
            "All this territory used to be referred to as Left Bank Ukraine",
            "preparing for war with us and are increasing their military",
            "Lavrov, in which he has said that all the diplomatic initiatives",
            "Storm Shadow missile if that was indeed what it was",
            "nothing was agreed substantively about anything",
            "Hezbollah for its part is insisting that it will go on fighting",
            "Zelenskyy's ultimatum to Belarus remains in effect",
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
