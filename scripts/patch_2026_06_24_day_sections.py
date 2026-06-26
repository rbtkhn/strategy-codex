#!/usr/bin/env python3
"""source-section batch for 2026-06-24 statecraft interview intakes."""
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

DAY = ROOT / "source-archive/statecraft/2026-06-24"

CAPTURES: dict[str, dict] = {
    "source-napolitano-diesen-europe-preparing-war-2026-06-24.md": {
        "titles": [
            "Show Open — Europe and War",
            "Putin Warning — West Preparing for War",
            "Storm Shadow — NATO Already at War",
            "Russophobia — Root of Bellicosity",
            "Ukraine Infrastructure — Putin and Retaliation",
            "SMO Endgame — Diplomatic and Military Paths",
            "Manpower — Drones, Troops, and Casualties",
            "Merz — German Militarization",
            "Iran MOU — Memorandum of Understanding",
            "Close — Thanks and Farewell",
        ],
        "anchors": [
            "Professor Diesen, welcome",
            "You know, you mentioned the Storm Shadow",
            "What is the root, the cause of this bellicosity",
            "One of the things that President Putin complained",
            "What is the prospect for a conclusion",
            "can you capture and control territory by drones",
            "Our uh friend and colleague Colonel McGregor",
            "I'd like to pick your brain before we leave on the other topic",
            "Professor Diesen, thank you very much",
        ],
    },
    "source-napolitano-marandi-iran-stands-firm-negotiations-2026-06-24.md": {
        "titles": [
            "Show Open — Negotiations and Tehran",
            "Life in Tehran — Oil and the Economy",
            "Hormuz Control — Who Holds the Strait",
            "Rubio — International Waters Claim",
            "US Navy — War Planning Failures",
            "Lebanon — MOU and Israeli Occupation",
            "Switzerland — Missiles and IAEA",
            "Netanyahu — Lebanon Security Zone",
            "War Risk — Gaza, Ashura, and Patience",
            "Close — Farewell",
        ],
        "anchors": [
            "Professor Miranda, welcome",
            "who is in control of the straight of hormuz",
            "Here's uh Secretary of State Rubio",
            "Is the US Navy out of the picture",
            "What will Iran do if the Israelis refuse to leave Lebanon",
            "Talk to us uh about the uh negotiations in Switzerland",
            "the latest from Netanyahu",
            "Do you foresee Iran using military force against the Israelis",
            "Thank you, Professor Miranda",
        ],
    },
    "source-napolitano-mate-iran-deal-pause-not-peace-2026-06-24.md": {
        "titles": [
            "Show Open — Goldman Primary Defeat",
            "Poetica — Coffee Shop and Civil Rights Probe",
            "NY Primaries — Mamdani and Anti-Apac Wave",
            "Iran MOU — Lebanon and Trump Leverage",
            "Netanyahu — Pakistan Mediator Warning",
            "Performative Pause — Syria and Hezbollah",
            "Morandi Warning — Israeli Navy and Missiles",
            "Reflecting Pool — Domestic Politics Humor",
            "Close — Farewell",
        ],
        "anchors": [
            "Aaron Mate, my dear friend",
            "This is what the coffee shop uh posted",
            "let's go to the memorandum of understanding",
            "In response to that, here's what the prime minister of Pakistan",
            "Professor Muhammad Morandi who was on with us earlier",
            "Trump's big idea is get Syria to go fight",
            "Before we go, just for a little bit of humor",
            "Thank you, Aaron",
        ],
    },
    "source-glenn-diesen-max-blumenthal-iran-deal-divides-us-triggers-panic-israel-2026-06-24.md": {
        "titles": [
            "Open — MOU and US-Israel Relationship",
            "Domestic Politics — Defeat and Trump Spin",
            "IAEA — Scientists and a Different MOU",
            "Vance — Restrainers and Israel Panic",
            "Military Defeat — Kaine and Hormuz",
            "Lebanon — Sabotage Lever and Apac",
            "Tucker — GOP Exit and Third Party",
            "Desperation — False Flags and Nuclear Israel",
            "Close — Greyzone Link",
        ],
        "anchors": [
            "So, I was wondering if you could speak to some of the domestic politics",
            "Donald Trump is declaring that there will be IAEA inspectors",
            "So, Donald Trump has to has to do this",
            "where does that place Israel at this point",
            "Lebanon will be the main lever",
            "Tucker Carlson declared, I think yesterday",
            "pay-for-play anti-semitism attacks",
            "United Against a Nuclear Israel campaign",
        ],
    },
    "source-moral-resistance-parsi-israel-refuse-leave-lebanon-will-iran-respond-2026-06-24.md": {
        "titles": [
            "Open — Deal Progress and Israel Impediment",
            "Negotiations — Working Groups and Signals",
            "Lebanon — Conflicting Processes",
            "Israel Won't Leave — Incremental Escalation",
            "US Pressure — Channel 13 and Vance",
            "Iran Response — Counter-Escalation Options",
            "Gaza vs Lebanon — Strategic Split",
            "Regional Security — Umbrella and Abraham Accords",
        ],
        "anchors": [
            "So treat um what's going on with the negotiations",
            "why would the Americans be playing both sides",
            "So how do you deal with that entire issue",
            "Channel 13 reported two days ago",
            "won't that break the deal down",
            "You just mentioned Gaza",
            "new security umbrella that has been created",
        ],
    },
    "source-nawfal-parsi-israel-will-not-withdraw-lebanon-2026-06-24.md": {
        "titles": [
            "Open — Lebanon Withdrawal Reports",
            "Israeli Rhetoric — Bennett and Ben-Gvir",
            "Channel 13 — IDF Restrictions",
            "Kicking and Screaming — Donors and Influence",
            "Journalist IDF Claims — Fact vs Accusation",
            "Gaza Uninhabitable — Greater Israel Objective",
            "Palestine — Iran Win and Arab Coalition",
            "Gulf Bases — Phased US Withdrawal",
            "Meta Censorship — Francesca and Apac Backlash",
        ],
        "anchors": [
            "What do you make of the developments in Lebanon",
            "I do want to reference the channel 13 report",
            "Can you elaborate what that kicking and screaming is",
            "Have you looked into this the u the so the claims by Israel",
            "Do you think um you're in in the belief that Israel did what they did in Gaza",
            "now that Iran won this war do you think",
            "withdrawal of foreign military forces from the region",
            "Hillary Newer, not sure if you know him",
        ],
    },
    "source-daniel-davis-larry-johnson-iran-deal-trump-making-it-up-2026-06-24.md": {
        "titles": [
            "Open — Trump Oil Gusher Claims",
            "Tanker Math — Mines and Insurance Crisis",
            "Shut-in Oil — Restart Timeline",
            "Rubio — Lebanon vs MOU Ceasefire",
            "Hezbollah Stopped — Iran Strike Frame",
            "Tucker Eight Calls — Pre-War Warnings",
            "Five Iranian Wins — Surrender Spin vs Reality",
            "Russia Ukraine — Putin Cadets Warning",
        ],
        "anchors": [
            "go to marine.com",
            "shut in oil getting turned back on",
            "Secretary of State Marco Rubio",
            "Hezbollah stopped firing",
            "talked to President Trump eight times",
            "full-on surrender document for the Iranian side",
            "Vladimir Putin a couple of days ago address some cadets",
        ],
    },
    "source-dialogue-works-johnson-israel-next-war-preparing-bomb-yemen-2026-06-24.md": {
        "titles": [
            "Open — Gaza UN Report and Yemen Prep",
            "Yemen Operations — Channel 14 Prep",
            "Pakistan — Regional Security Architecture",
            "Lebanon Talks — No Progress",
            "Rubio — UAE and Kuwait Visit",
            "Rutte — EU Flights and Italy Denial",
            "Hungary — Orban and EU Politics",
            "Close — Farewell",
        ],
        "anchors": [
            "14-year-old kid boy was killed",
            "Channel 14 in Israel reported",
            "Iranian president going to Pakistan",
            "Axis reported today there was a meeting",
            "What is the mission of Rubio going to UAE",
            "Did you hear Mark Route Larry today",
            "Orban",
        ],
    },
    "source-daniel-davis-alastair-crooke-iran-deal-who-dictating-terms-2026-06-24.md": {
        "titles": [
            "Open — MOU Framework Not Agreement",
            "Iranian Ten Points — Who Dictates Terms",
            "Trump Hormuz — True Social Claims",
            "Frozen Funds — Farmers and Leverage",
            "Peak Leverage — China Oil and IRGC",
            "Lebanon — Hezbollah Withdrawal",
            "Russia Ukraine — Escalation Risk",
            "Europe — Long-Range Missiles and Ian Proud",
        ],
        "anchors": [
            "the Iranian 10 points",
            "true social that President Trump",
            "they will only buy food from American farmers",
            "peak leverage doesn't come till",
            "Lebanon. There's a reason why that was required",
            "Russia Ukraine war",
            "Ian Proud",
        ],
    },
    "source-weichert-carlson-jd-vance-warning-israel-israel-firsters-iran-growing-strength-2026-06-24.md": {
        "titles": [
            "Monologue — Lebanon Casualties and Betrayal",
            "Monologue — Iran War Justification and Lebanon",
            "Monologue — Defeat and Getting Out",
            "Interview — Weichert on Durable Peace",
            "Hormuz — Sixty-Day Clock and Reserves",
            "Israel Wild Card — Submarines and Apac Politics",
            "Close — Farewell",
        ],
        "anchors": [
            "Over 4,000 Lebanese",
            "Israel cajjol convinced threatened",
            "he announces we're getting out",
            "So, you said at the outset",
            "the 60 days is what we have",
            "Tom Cotton is the driving force",
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
