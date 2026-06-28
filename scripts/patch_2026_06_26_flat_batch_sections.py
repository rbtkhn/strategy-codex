#!/usr/bin/env python3
"""source-section batch — 2026-06-26 flat captures (8 remaining after MOU cluster)."""
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
    "source-alexander-mercouris-zelensky-threatens-belarus-kharkov-kiev-lavrov-rubio-bury-anchorage-2026-06-26.md": {
        "titles": [
            "Show Open — Ever Lovely and Rubio Bahrain",
            "Anchorage Denial — Rubio Agreement Wording",
            "Lavrov Skepticism — Diplomatic Outreach Resentment",
            "Zelensky Winter — Energy Grid Pressure",
            "Russian Polling — VTsIOM Trust Ratings",
            "Battlefield — Fab Bombs and Air Defense",
            "Denmark Policy — Military Service Exemption",
            "China Iran — Strategic Partnership Friction",
            "Hormuz Close — China's Economic Interest",
        ],
        "anchors": [
            "I am going to discuss certain comments made by the US Secretary of State Marco Rubio",
            "When my counterpart Marco Rubio says there were only proposals by no but no agreement in Alaska",
            "At a fundamental level, as a professional diplomat in charge of the Russian foreign minister min ministry",
            "that the damage done to the energy system by the Russian strikes last autumn and mid- winter",
            "We have, by the way, had another opinion poll on trust ratings in Russia",
            "it is a long time since I saw any reports of any Russian aircraft shot down",
            "a recent policy announcement by the Danish government",
            "China's backing to Iran over the course of the current conflict has been perhaps rather less",
        ],
    },
    "source-daniel-davis-robert-barnes-iran-deal-miscalculations-2026-06-26.md": {
        "titles": [
            "Show Open — MOU Headwinds and Lebanon Point One",
            "Netanyahu Box — BB Files and Election Clock",
            "Israel Lobby Bills — MSAD CIA Merge Fight",
            "NYC Primary — Anti-Israel Not Anti-Semitic",
            "Hamas Funding — BB Files and Qatar",
            "Peace Deal Cowards — Vance Architect vs Saboteurs",
            "Historical Analog — Kennedy and Admin Saboteurs",
            "Herbert Hoover — Economic Precipice Fear",
            "Republican Reform — Midterm Blue Wave Question",
            "1776 Law Center — Convention and Legal Strategy",
            "Judicial Branch — Duopoly Remedy and Close",
        ],
        "anchors": [
            "one of the biggest headwinds is is number one on the list of the memorandum",
            "the documentary the BB files and others",
            "merging MSAD with the CIA and the intelligence apparatus",
            "No, it was anti-Israel because that was the most Jewish district in America",
            "the BB files is it detailed what I think you may have talked about this with Tucker",
            "They don't want to be blamed for the peace deal that ends the war",
            "historical analog to this where someone was trying to get through an important piece",
            "And the comparison to Herbert Hoover clearly got to got to him",
            "can the Republican party be reformed or is it too late?",
            "the 1776 Law Center convention which we have right there",
        ],
    },
    "source-daniel-davis-seyed-marandi-will-us-collapse-global-economy-2026-06-26.md": {
        "titles": [
            "Show Open — Trump Nice Iran and Champagne",
            "MOU Reality — IAEA Sites and Lebanon Leverage",
            "Rubio Religious Lunatics — Governance and Narrative",
            "Trust History — JCPOA and Negotiation Impossibility",
            "MOU Funds — Vance Dishonesty and Walkout",
            "Netanyahu Mistake — Hormuz Leverage Grows",
            "Asset Release — Trickle Regulation and Reciprocal",
            "Day 61 MOU Text — Toll Fantasy Rubio Clip",
            "Day 61 Fees — Rubio vs Iranian Position",
            "Proxy Support — Rubio and Baghaei Lines",
            "Warsaw Analogy — Proxy Blame Game",
            "Islamic Outreach — Western Press Blackout",
            "US Defeat Register — Regional Realignment",
            "Netanyahu Lebanon — Hormuz Closure Consequence",
            "Forecast — Israeli Policy and Escalation Risk",
        ],
        "anchors": [
            "I what I can say though is that from from what I'm learned from the recent nego",
            "You used to call them religious theocratic lunatics",
            "No, it becomes almost impossible because if we go and look at the history",
            "Now it appears that some relief of energy sanctions has happened",
            "If Iran did not control the Strait of Hormuz, the United States would not carry out",
            "What if the the United States keeps that condition that you have to buy American stuff",
            "Well, that certainly has been the way it has been so far",
            "Let's suppose that we went crazy for and lost our minds completely",
            'And the Iranians say, "No, there there are going to be fees on day 61.',
            "Secretary Rubio saying uh a couple of comments here.",
            "like a thousand people are slaughtered and I'm in Warsaw",
            "didn't get a lot of press here in the West at all",
            "the United States has been seen as being defeated on the battlefield",
            "slaughtered hundreds of people in minutes, in order to wreck it. And that's what caused the the Strait of Hormuz",
        ],
    },
    "source-dialogue-works-chas-freeman-collapse-israel-agenda-2026-06-26.md": {
        "titles": [
            "Show Open — Beth Yahoun and Geneva Round Two",
            "Hormuz IMO Route — Tanker Attack Counter",
            "Syria Lebanon Hold — MOU Article 1 Challenge",
            "Busher Inspections — IAEA Partial Access",
            "August 21 Clock — MOU 60-Day Window",
            "War Mongers — Senate Israel Support",
            "Israeli Aggression — Three Issue Stack",
            "Military Approach Fails — October 7 Lesson",
            "Israel Cliff — Party System Exhaustion",
            "NATO Rutte — Vance Israel Pressure",
        ],
        "anchors": [
            "let me start with what has happened last night again",
            "Iran successfully uh countered that with an attack on a tanker",
            "This is a direct challenge to the agreement between the United States and Iran.",
            "There are inspections going on at Busher at the request of the Russians",
            "August 21st that is the end of the 60-day period",
            "very strongly supportive of Israel.",
            "all three of these issues arise because of Israeli aggression or genocide.",
            "what was October 7th about?",
            "where is Israel's got to save itself?",
        ],
    },
    "source-judging-freedom-johnson-mcgovern-intel-roundtable-weekly-wrap-26-june-2026-06-26.md": {
        "titles": [
            "Show Open — Hormuz Status Roundtable",
            "Fuel Buffer — Diesel and Aviation Crisis",
            "Asset Recall — McGovern Huge Moment",
            "Syria Hezbollah — Trump al-Shara Idea",
            "CIA Propaganda — Iran Regime Change Line",
            "Hexath Promotion — Political Generals",
            "UN Security Architecture — Five-Year Deal",
            "Scott Ritter Drones — Russia Factory Strikes Close",
        ],
        "anchors": [
            "What is the status of the straight of Hormuz",
            "if anything happens like a hurricane that takes out a refinery",
            "as McGovern as Ray McGovern would say that's huge",
            "empowering uh Syrian president al-Shara to actually go into southern Lebanon",
            "CIA funded propaganda outfit that was based uh in in the Netherlands",
            "You get promoted by the by the Hexaths of this world.",
            "the UN security council will approve so they don't have to do this five years from now",
        ],
    },
    "source-judging-freedom-macgregor-judgment-day-trump-war-lost-2026-06-26.md": {
        "titles": [
            "Show Open — Hormuz Insurance and IRGC Resurrection",
            "Land Power — Cold War Germany Lesson",
            "Hill Hatred — Iran Defeated Us Narrative",
            "Israeli Agents — Bomb Your Way to Success",
            "Syria Hezbollah — Trump Disappointed Israel",
            "Manipulated Trump — Erdogan Wedge Fantasy",
            "Insurance Either-Or — London Won't Play",
            "Hazardous Choice — Israel Lobby Ruthless",
            "Ukraine Analogy — 500 More Tanks Close",
        ],
        "anchors": [
            "Colonel Douglas McGregor joins us now",
            "one of the reasons we maintained a force on the ground in Germany of 275,000 troops",
            "The hatred of the of the Iranians in particular is at an all-time high",
            "the Israelis and their agents in the United States wanted him to continue to bomb",
            "involving Syria in this mess, is Syria really going to side with the Israelis",
            "hopelessly manipulated he really is by his Israeli friends",
            "insured for millions of dollars won't accidentally be caught up in the violence",
            "that sounds great in theory, but in practice that's very hazardous for him",
        ],
    },
    "source-mario-nawfal-daniel-davis-us-boots-lebanon-israel-recognition-mou-2026-06-26.md": {
        "titles": [
            "Show Open — US Boots Remove Resistance",
            "Netanyahu No Withdrawal — Graduation Speech",
            "MOU Negotiable — IDF Withdrawal Contingencies",
            "Surrender Rhetoric — IRGC Pivot",
            "Pilot Zones — Security Zone Language",
            "Khamenei Weak Support — Internal MOU Battle",
            "Downrange Sources — No Boots Possibility",
            "America First Vance — Boots Appetite Question",
            "Trump Capability — Get Out Position",
        ],
        "anchors": [
            "based on what you just read that's I don't know how else you could interpret",
            "they're not going to withdraw from anywhere, especially not in southern Lebanon",
            "this is just what we're negotiating",
            "The IRGC has to surrender or face certain death",
            "Israel and Lebanon agreed to two areas adjacent to the blue line",
            "when he said he bought off on the MOU",
            "nobody but nobody has talked about any of this as even being a theoretical possibility",
            "America first as opposed to possibly being Israel first",
        ],
    },
    "source-mario-nawfal-macgregor-israel-furious-trump-turkey-syria-lebanon-2026-06-26.md": {
        "titles": [
            "Show Open — Turkey F-35 and Israel Statement",
            "Iran Strong — China Russia Allies",
            "Erdogan Interests — Ottoman Geography",
            "Khan Engines — Take Money and Run",
            "Square the Circle — Israel Induce US Back",
            "Nothing Left to Bomb — War Continues",
            "Americans Want Out — Washington vs Public",
            "Hill Support — Pull Support Leverage",
            "Ukraine Losses — Conflict Horizon Close",
        ],
        "anchors": [
            "Trump has been praising Erdogan",
            "Iran is strong. It's more powerful today militarily",
            "Northern Iraq is viewed as a Turkish area",
            "I would just take the money and run if I were Mr. Erdogan",
            "how do you how do you square this particular circle? You can't.",
            "there is nothing left to bomb then like I understand",
            "But that's what Americans inside the United States want.",
            "we're going to pull our support from you.",
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
