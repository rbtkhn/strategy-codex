#!/usr/bin/env python3
"""source-section batch for 2026-06-25 statecraft intakes."""
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
    "source-dialogue-works-larry-johnson-us-directly-calling-iran-vance-switzerland-bombshell-2026-06-25.md": {
        "titles": [
            "Show Open — June 25 Welcome",
            "Rutte NATO — Iran Complicity Claim",
            "Trump Europe — Passive Landing Rights",
            "Hormuz MarineTraffic — Outbound Only",
            "Oil Economics — Heavy Crude and Aviation",
            "Rutte White House — Trump Brand Salesman",
            "Foundation of Lies — Europe and Iran",
            "BRICS New Delhi — Yuan and SIPs",
            "Pakistan Munir — SEO and Gulf Architecture",
            "Vance Channel — Switzerland Military Line",
            "Oman Hormuz — Mechanism Friction",
            "Netanyahu Lebanon — Offramp and Insanity",
            "Turkey NATO — Ukraine Second Front",
            "Close — See You Tomorrow",
        ],
        "anchors": [
            "response from the spokesperson of Iranian foreign ministry",
            "Trump got into a nasty back and forth with Maloney",
            "there's a website called marinetra.com",
            "20% of the supply was shut down",
            "You stay here. I go over to these boards",
            "built on a foundation of lies one lie after another",
            "India hosted the 16 BRICS National Security Advisors",
            "Pakistan is a full member of the SEO Larry",
            "JD Vance told unheard",
            "process of new the new mechanism is you is happening",
            "Benjamin Net said that we have we removed",
            "The next NATO summit is going to be in Turkey",
            "We're going to talk tomorrow",
        ],
    },
    "source-judging-freedom-blumenthal-israel-in-panic-2026-06-25.md": {
        "titles": [
            "Show Open — Is Israel in Panic",
            "Quinnipiac Poll — US Support Too High",
            "Netanyahu Perception — Successor Bench",
            "Zionism Structure — Colonial Dream Failed",
            "Hezbollah FPV — Southern Lebanon Front",
            "NYC Primaries — AIPAC Defeats",
            "Randy Fine — Republican Fissures and Vance",
            "Close — Colombia Teaser",
        ],
        "anchors": [
            "Israel's in panic over a new Quinnipiac poll",
            "Well, if you if you want to know how he's perceived",
            "Well, I've been saying that I think Netanyahu",
            "What kind of shape is Hezbollah in today?",
            "How do you I'm switching gears, Max",
            "Here is um the prince of the American Zionists",
            "I know you want to talk about the Colombia presidential",
        ],
    },
    "source-mercouris-lukashenko-no-to-zelensky-belarus-stands-with-russia-russian-troops-enter-sumy-eu-no-to-kiev-entry-2026-06-25.md": {
        "titles": [
            "Show Open — Zelensky Belarus Threats",
            "Attack Called Off — Putin Lukashenko Track",
            "Russian Security Council — Neighbors and Stability",
            "Lukashenko Minsk — War Would Change Drastically",
            "Lavrov and Medvedev — Negotiations Stop",
            "Marat Kulgin — Donbass Fortified Line",
            "Sumy Breakthrough — Narrative Versus Reality",
            "EU Membership — Ukraine Bargaining Chip",
            "Voronezh Strike — Dirty Dagger Missile",
            "Persian Gulf — MOU as Minsk Agreement",
            "Close — Platform Reminder",
        ],
        "anchors": [
            "it appears however as of today that this idea of an attack on Belarus has been called off",
            "We have two questions today.",
            "Zelensky's representatives were here at this very spot",
            "Meanwhile, other Russian officials have been speaking",
            "Marat Hulin whom I have consistently considered the best reporter",
            "Now there's been reports from Sumy over the course of this morning",
            "Apparently, at the last EU Council meeting",
            "A few days ago, there was a attack, a strike on Verones",
            "Now, I do want to say a little bit more about the situation in the Persian Gulf",
            "Anyway, this is where I'm going to finish today's program",
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
