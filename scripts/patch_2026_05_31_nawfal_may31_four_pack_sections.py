#!/usr/bin/env python3
"""source-section batch — May 31, 2026 Nawfal four-pack (Diesen + Barnes + Johnson + Weichert).

Status: merged maps — Diesen §8–§9; Weichert §7–§8 + §9–§10 (9§ parity).
Verify anchors: python scripts/patch_2026_05_31_nawfal_may31_four_pack_sections.py --check-anchors
Apply all:       python scripts/patch_2026_05_31_nawfal_may31_four_pack_sections.py --apply
Apply one:       python scripts/patch_2026_05_31_nawfal_may31_four_pack_sections.py --apply --only diesen
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    find_anchor_pos,
    normalize_for_anchor,
    write_sectioned_capture,
)

CAPTURES: dict[str, dict] = {
    "diesen": {
        "rel": (
            "source-archive/statecraft/2026-05-31/"
            "source-mario-nawfal-diesen-breaking-iran-collects-tolls-from-28-ships-in-past-24-hours-2026-05-31.md"
        ),
        "titles": [
            "Hormuz Toll Corridor — Quiet Kinetic Front and $50M-Day Revenue",
            "Ceasefire Status Quo — Blockade vs Toll Booth and Oman Cooperation",
            "Negotiation Sticking Points — Frozen Assets, $300B Reconstruction, Trump Hardening",
            "Iran Won the War — Strategic Defeat Frame and Non-Binding MOU Skepticism",
            "China Objective — Long-Horizon Regime Pressure vs Band-Aid Ceasefire",
            "Post-Deal Region — Stronger Iran, Israeli Panic, Clean Break vs Scale-Back",
            "Greater Israel — Lebanon Territory Snatch vs Hezbollah Security Competition",
            "Gaza-to-Istanbul Stack — Brutality, Ethnostate Logic, Genocide Politics, Dehumanization Flags",
            "Parliament Hormuz Law — Sovereignty Off Table and US Primacy Collapse Close",
        ],
        "anchors": [
            "Yeah. No. Well, that's an interesting development because when they went into this ceasefire",
            "on the Iranian side, there still they said there's been some progress in the negotiations",
            "Yeah. One of my guests said it's the worst strategic defeat since Vietnam War",
            "But Iran strategically is extremely important for the US when it comes back to China",
            "Yeah, that's an excellent question because I think the entire world will be different",
            "Do you believe greater Israel project is actual policy in Israel or it's just a minority",
            "when you look at the atrocities that happen in Gaza, I actually have a doctor coming on",
            "Um, according to me News, the Iranian news outlet, a member of the Iranian",
        ],
        "note": "Nine sections (merged §8–§9). Pair §1–§2 + §9 with MR/BP Hormuz toll arc.",
    },
    "barnes": {
        "rel": (
            "source-archive/statecraft/2026-05-31/"
            "source-mario-nawfal-barnes-breaking-u-s-to-merge-military-with-israel-2026-05-31.md"
        ),
        "titles": [
            "Deal vs Resumption — Trump/Hegseth Leverage vs Rational Actors",
            "Declaring Victory — MAGA Base vs Independent Voter Who Knows US Lost",
            "Blockade Post — Behind-the-Scenes Deal and Iranian Skepticism",
            "Last-Minute Redictation — Action-Dependent Iran and Self-Sabotage Pattern",
            "Walter Reed Cognitive Test — Behavioral Dementia vs Perfect MoCA Score",
            "NDAA Military Merge — Authority vs Tech Access and Nuclear Theft History",
            "Mossad Embedded — Dual Roles in CIA, Pentagon, and State Department",
            "Buried NDAA Provision — Josh Paul, Massie Whistleblower, Surveillance Kill Switch",
            "Espionage Stack — Pollard, Maxwell/Tower, Decades of Misappropriated Secrets",
            "Presidents Who Pushed Back — Reagan Lebanon Holocaust, Kennedy Nuclear Inspection",
            "APAC Machine — Money, Media, Book-Deal Laundering, Salem/TPUSA, Israel as Center Story",
        ],
        "anchors": [
            "Uh I don't agree with the latter. I mean I know they are whispering that to Trump",
            "deal. Well, I knew from behind the scenes that the deal was there to be made",
            "He keeps convincing himself that he can redictate the terms at the last minute",
            "Other people think it's because he's in the pocket of Israel or he's intimidated by Israel",
            "Have you gone through this? >> Yes, it's steeply problematic",
            "Can you can you can you tell me more about them? So effectively what it is is you'll be sitting across",
            "So, US and Israeli military ties ties are poised to become more deeply entrenched",
            "Can you go back to what is what we know about the Jonathan Pollard story",
            "Which president, which American president stood up to Israel the most?",
            "Those members of Congress, a few million dollars, you know, 2 million there",
        ],
        "note": "Eleven sections. Pair §6–§8 with MR Aguilar May 31 §224 stack.",
    },
    "johnson": {
        "rel": (
            "source-archive/statecraft/2026-05-31/"
            "source-mario-nawfal-larry-johnson-israel-asks-trump-to-escalate-2026-05-31.md"
        ),
        "titles": [
            "Charlie Kirk Thread — TPUSA Break, August Pressure, Operational Doubts",
            "Trump Under Duress — Joe Kent Warning and Missing Assassination Badge",
            "Lobbying Landscape — APAC Dominance, MIC, NDAA Access Lock-In",
            "Lebanon Escalation Ask — Beirut Expansion, Iran Red Line, Hormuz Toll + Parliament Law",
            "Lebanon Trap — WAP Overextension vs Conri Axis-Weakened Since Oct 7 Counter",
            "Nuclear Shadow — Pakistan/North Korea Transfer and Regional Escalation Ladder",
            "Trump Tougher Terms — Diesel Dependency, Global-South Iran, Zelensky Patriot Plea",
            "Arsenal Reality — Belarus Unlikely, NYT Dark Transits, CNN Robotics Skepticism",
            "Israel Does What It Wants — Lebanon Leash Facade and Sunday Close",
        ],
        "anchors": [
            "I think I told you that before. Joe Kent said to me, that really caught me by surprise",
            "Which lobbying group do you think that has the most influence in the US uh the US government?",
            "well talking about Israel there is the main focus what's happening in Iran right now",
            "Um, yeah, this is the update that came in from MTV, Lebanese news outlets",
            "Do you think that's a possibility? Um, it's possible, but I I I think the under the old prohibition of Kami",
            "well yeah I mean he's he's asking for actually the surrender of Iran and Iran's not going to surrender",
            "A question. >> Go ahead. >> Um, I've heard talk about um, Bellarus potentially joining the war",
            "Do you think he'll approve their request to expand operations in Lebanon or he keep them on leash",
        ],
        "note": "Nine sections. Pair §4 with Diesen §9; §7 with Weichert Tomahawk/Zelensky lane.",
    },
    "weichert": {
        "rel": (
            "source-archive/statecraft/2026-05-31/"
            "source-mario-nawfal-weichert-iran-us-rearming-for-war-2026-05-31.md"
        ),
        "titles": [
            "Mixed Signals Open — MOU Amendments, Lebanese Latani Crossing, Iran Red Line",
            "Rearm Not Deal — Strategic Positioning, Hormuz as Iranian River",
            "Toll Economics — Rubio UN Clip, Recession/Depression Risk, 60-Day MOU Window",
            "Arsenal Bone Dry — Cannibalized Stockpiles, Indopac/Europe/Yukon Diversion",
            "Ryan McBath Debate — Tomahawk One-Third Burn, Supply-Chain Bottlenecks",
            "NDAA §224 — Defense-Industrial Merge, Israel Backdoor Aid, §1222 Subterranean",
            "Gaza MOU + Parliament Law — 60-Day Trap, Hormuz Sovereignty, Lebanon Expansion Ask",
            "621-Mile Seam — Zangehoor Corridor, Putin Endgame, CNN Bases, Crassus Analogy",
            "Lieberman Hormuz Indifference — UAE Retaliation Option, IDF Overextension, Demining Close",
        ],
        "anchors": [
            "That's right. And that's the tell, Mario. There is no deal that this deal is is all just vamping",
            "There you go. There you go. So this whole thing is what this is is Trump is I think trying to manipulate the oil markets",
            "So, um I know why do you think there won't be a deal? >> Because there's no stasis here.",
            "You saw Zelensky's pleased about this today. He uh yeah, >> he gave an interview to Face the Nation",
            "What it's actually doing is merging the US and Israeli defense industrial base and tech sectors together",
            "What does an MOU mean? Look at someone used the example of Gaza",
            "By the way, 621 miles now is all that separates the Iranian front from the Ukrainian front",
            "debating Avdor um Leeman, I think the former national security adviser to um Netanyahu",
        ],
        "note": "Nine sections (merged §7–§8 and §9–§10). Pair §5–§6 with Barnes §6–§8; §7 with Diesen §9 / Johnson §4.",
    },
}

TRANSCRIPT_MARKER = "## Transcript\n"
LEGACY_SPLIT = "---\n\n"

def extract_flat_body(doc: str) -> str:
    if TRANSCRIPT_MARKER in doc:
        return doc.split(TRANSCRIPT_MARKER, 1)[1]
    if LEGACY_SPLIT in doc:
        return doc.split(LEGACY_SPLIT, 1)[1]
    raise ValueError("no transcript body (expected ## Transcript or legacy --- split)")

def flatten_sectioned_body(body: str) -> str:
    body = body.strip()
    if "### " not in body:
        return body
    while True:
        new = re.sub(r"^### [^\n]+\n+", "", body)
        new = re.sub(r"\n+### [^\n]+\n+", "\n\n", new)
        if new == body:
            break
        body = new
    return body.strip()

def ensure_flat_transcript(path: Path) -> None:
    doc = path.read_text(encoding="utf-8")
    if TRANSCRIPT_MARKER not in doc:
        return
    head, body = doc.split(TRANSCRIPT_MARKER, 1)
    flat = flatten_sectioned_body(body)
    if flat == body.strip():
        return
    path.write_text(f"{head}{TRANSCRIPT_MARKER}\n\n{flat}\n", encoding="utf-8", newline="\n")

def check_spec(path: Path, spec: dict) -> bool:
    doc = path.read_text(encoding="utf-8")
    body = flatten_sectioned_body(extract_flat_body(doc).strip())
    pos = 0
    ok = True
    print(f"=== {path.name} ({len(spec['titles'])} sections) ===")
    for i, anchor in enumerate(spec["anchors"], start=1):
        try:
            pos = find_anchor_pos(body, anchor, pos) + len(normalize_for_anchor(anchor))
            print(f"  anchor {i} -> section {i + 1}: {spec['titles'][i]}")
        except ValueError as exc:
            ok = False
            print(f"  {i}. FAIL — {exc}")
    print(f"  -> {spec['titles'][-1]} (EOF)")
    if spec.get("note"):
        print(f"  note: {spec['note']}")
    print()
    return ok

def apply_spec(path: Path, spec: dict) -> None:
    ensure_flat_transcript(path)
    write_sectioned_capture(
        path,
        spec["titles"],
        spec["anchors"],
        reject_if_sectioned=False,
    )

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write sectioned captures (operator-approved ship only)",
    )
    parser.add_argument(
        "--check-anchors",
        action="store_true",
        help="Verify all anchors resolve; no file writes",
    )
    parser.add_argument(
        "--only",
        choices=sorted(CAPTURES),
        help="Limit to one capture key (diesen|barnes|johnson|weichert)",
    )
    args = parser.parse_args()

    keys = [args.only] if args.only else list(CAPTURES)
    ok_all = True
    for key in keys:
        spec = CAPTURES[key]
        path = ROOT / spec["rel"]
        if not path.is_file():
            print(f"MISSING {spec['rel']}", file=sys.stderr)
            ok_all = False
            continue
        if args.apply:
            apply_spec(path, spec)
            print(f"sectioned {spec['rel']}")
        else:
            ok_all = check_spec(path, spec) and ok_all

    if not args.apply:
        print("Pass --apply after operator approval to ship.")
    return 0 if ok_all else 1

if __name__ == "__main__":
    raise SystemExit(main())
