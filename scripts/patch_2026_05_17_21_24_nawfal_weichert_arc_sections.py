#!/usr/bin/env python3
"""source-section batch — May 17 / 21 / 24 Weichert rearm arc (pre–May 31).

Verify: python scripts/patch_2026_05_17_21_24_nawfal_weichert_arc_sections.py --check-anchors
Apply:  python scripts/patch_2026_05_17_21_24_nawfal_weichert_arc_sections.py --apply
Apply one: python scripts/patch_2026_05_17_21_24_nawfal_weichert_arc_sections.py --apply --only may21
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
    "may17": {
        "rel": (
            "source-archive/statecraft/2026-05-17/"
            "source-mario-nawfal-weichert-russia-ukraine-escalating-iran-war-restarting-2026-05-17.md"
        ),
        "titles": [
            "WWIII Gray Zone Open — Ukraine Barrage, Gulf Live Hits, Three-Front Link",
            "Iran Restart Frame — Energy Infra, Island Landing, Trump Id Kinetic",
            "Karaganov Link — Ukraine-Iran Same War, Putin Decisive Window",
            "Tactical Nuclear Revision — NATO Infrastructure, Hudson Collapse Strategy",
            "Russia Unchained — Last Legs Ukraine, NATO Deploy Halt, Turkish Bloc",
            "Taiwan Article 5 — Trump Freeze Signal, Bilateral Abandonment Read",
            "NSC Resume Combat — TACO Trap, Baked-In Shock, Hormuz Toll Booth",
            "Gulf Pragmatic Iran — UAE Chain Break, MBS War Miscalculation",
            "China Desperation Close — Xi Wins, Mad King, Multipolar Speed-Up",
        ],
        "anchors": [
            "Yeah, so basically, with the Middle East front",
            "Do you think they will strike? How would it look like?",
            "No, I completely agree with that and actually Sergey Karaganov",
            "Yeah, well, yeah, Karaganov is one of those voices",
            "Well, there's nothing really at this point other than fear",
            "No, I I and I and I think the reason I say no, look at what Trump said about Taiwan",
            "It just came in now. CNN, Trump with met with his national security team",
            "Well, in my opinion Israel is more damaged than they're letting on",
        ],
        "note": "Nine sections (8 anchors). §3–§4 pair May 31 Weichert §8 corridor · §7 with May 21 Hormuz toll arc.",
    },
    "may21": {
        "rel": (
            "source-archive/statecraft/2026-05-21/"
            "source-mario-nawfal-weichert-trump-miscalculated-iran-war-2026-05-21.md"
        ),
        "titles": [
            "Gulf Zero Influence — Consultancy Slow-Walk, Regional Tragedy Open",
            "Gulf Stopped Strike — Trump Thanks Trio, WH Rubio/Hegseth vs Kushner Split",
            "Hormuz Toll Booth — DIB Reconstitution, Israel Still Decider, Gallipoli Repeat",
            "Trump-Netanyahu Cycle — Adelson June 2024, Massie/AARP Boomer Block",
            "Al Arabiya Capitulation — Strategic Defeat Frame, Sanctions Easing Nothing Left",
            "Putin-Xi 40 vs Trump Punt — Sino-Russian Order, China Iran Exploit Fear",
            "First Island Chain Lost — A2/AD Overmatch, Taiwan Freeze Ripple, Rare Earth Processing",
            "Gulf Weak Link — WWI Red-Line Ladder, Iran Rational Escalation",
            "Enriched Uranium Walk-Away — Lebanon Not US Concern, Pape Escalation Trap Close",
        ],
        "anchors": [
            "Where to start, man? Where do we start?",
            "And then we get a report today that Trump and Netanyahu had a big fight",
            "Apparently, the US airstrikes on the defense industrial base of Iran were not as effective",
            "What do you think of the Massie election?",
            "That would be literally Trump capitulating",
            "whereas the meeting with the Americans, it sounded like there was a lot of punting going on",
            "In my view, and I and I'm not happy about it, but in my view, the US has lost the first island chain",
            "I have a I just got like this kind of chill that people in the 1910s",
        ],
        "note": "Nine sections (8 anchors). §3 pairs May 31 Weichert §2–§3 · §9 pairs May 24 MOU collapse bench.",
    },
    "may24": {
        "rel": (
            "source-archive/statecraft/2026-05-24/"
            "source-mario-nawfal-weichert-trump-iran-deal-collapsing-2026-05-24.md"
        ),
        "titles": [
            "MOU Cancel Open — Tasnim, Netanyahu Lebanon Freedom-of-Action Sticking Point",
            "Hajj Pause Theory — Fake Deal Appearance, Trump Slow-Walk, July 4 Shock",
            "Stalemate Frame — Walk Away Better, David Pine ORBAT Lie",
            "UNCLOS Persistent Objector — 30-Day Fee Finesse, Montreux Precedent",
            "Lindsey Graham Shift — Lose Little vs Big, Israel Married Cause",
            "Netanyahu Shrink + Pulse — Nuclear-Only Frame, Taj Mahal Casino",
            "Legal Trap + Sinwar — Abraham Accords Dead, Fars Promotional Pulse",
            "Decapitation + Samson — Russia Miniaturization 2023, Natanz Desert One",
            "Patch Fuse + Axios Abraham — UAE Finlandization, Merkava Massacre Doctrine",
            "Trump Junior Partner — CNN No Deal Today, Frozen Conflict Close",
        ],
        "anchors": [
            "Yeah. Israeli Channel 13 is saying that uh Netanyahu is trying to influence the Lebanon aspect",
            "Um in my opinion, what you've seen with this so-called deal has been",
            "None of that is on the table",
            "I mean, this is a this is a perfect precedent. The Montreux Convention",
            "Let me read Lindsey Graham's post",
            "Spot the difference. I'm actually going to put two statements that Netanyahu has made",
            "Netanyahu is not in a position to ever make peace",
            "authorize an Israeli strike against Iran, a decapitation strike",
            "According to Axios, Trump told Arab and Muslim leaders on Saturday",
        ],
        "note": "Ten sections. §1–§4 bookend May 31 Weichert §1–§3 MOU/Hormuz · §8 pairs May 31 §7 parliament/Gaza arc.",
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
            if i < len(spec["titles"]):
                print(f"  anchor {i} -> section {i + 1}: {spec['titles'][i]}")
            else:
                print(f"  anchor {i} -> (extra anchor; expected {len(spec['titles'])} titles)")
        except ValueError as exc:
            ok = False
            title = spec["titles"][i] if i < len(spec["titles"]) else spec["titles"][-1]
            print(f"  {i}. FAIL — {exc} (expected §{i + 1}: {title})")
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
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--check-anchors", action="store_true")
    parser.add_argument("--only", choices=list(CAPTURES))
    args = parser.parse_args()

    if not args.apply and not args.check_anchors:
        args.check_anchors = True

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
