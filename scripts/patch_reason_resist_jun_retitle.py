#!/usr/bin/env python3
"""Thematic retitle — Reason to Resist Jun 13 / Jun 18 bootstrap slug sections."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import write_slug_retitle_capture  # noqa: E402

ARCHIVE = ROOT / "source-archive/statecraft"

CAPTURES: dict[str, list[tuple[str, str]]] = {
    "2026-06-13/source-lascaris-helmer-how-will-russia-restore-deterrence-2026-06-13.md": [
        ("Show Open — Introduction", "Show Open — Helmer Deterrence and Russian Street"),
        (
            "Segment 2 — Disloyal To President Putin's Leadership",
            "Russian Street Dissent — Propaganda and Delagin Critics",
        ),
        (
            "Segment 3 — Then What We Have Is",
            "Election Repression — Nabiullina and Youth Internet",
        ),
        (
            "Segment 4 — Has Uh Allowed Various Supporters",
            "Nabiullina Sick Leave — Budget Deficit Fight",
        ),
        (
            "Segment 5 — Cover For A Faction A",
            "SMO vs War — Dmitriev Anchorage Line",
        ),
        (
            "Segment 6 — The Ruling Party In The",
            "Duma Elections — Vote Fraud and Communists",
        ),
        (
            "Segment 7 — A Festering Corpse Ever Since",
            "Yeltsin Fraud — Foreign Ministry Systemic Strikes",
        ),
        (
            "Segment 8 — In Which Drones Were Being",
            "Putin Repudiates Lavrov — Drone MOD List",
        ),
        (
            "Segment 9 — Immune From Attack Which They",
            "Strategic Rear Asymmetry — Karaganov Inevitable",
        ),
        (
            "Segment 10 — Negative For The For The",
            "Anchorage Fix — No NATO Strike Yet",
        ),
    ],
    "2026-06-18/source-lascaris-henningsen-war-on-iran-far-from-over-2026-06-18.md": [
        ("Show Open — Introduction", "Show Open — Lebanon Ceasefire Violations"),
        (
            "Segment 2 — Within The Straight Of Hormu",
            "Trump Hormuz Reality — G7 Oil Tanker Rhetoric",
        ),
        (
            "Segment 3 — They're Smart Sir You Shouldn't",
            "Ballistic Missiles — GCC Parallel Track",
        ),
        (
            "Segment 4 — It For A Month We",
            "Soleimani Hit — US Drove the Bus",
        ),
        (
            "Segment 5 — Literally Uh Bullet Points To",
            "Tail Wags Dog — IPAC and Symbiotic Empire",
        ),
        (
            "Segment 6 — Imperialism But Over Time The",
            "Israeli Lobby Cabinet — Safe Seats Drained",
        ),
        (
            "Segment 7 — Why Would You Do That",
            "MOU Lebanon Integrity — Ambiguous Language",
        ),
        (
            "Segment 8 — Thing Is I'll Start With",
            "Iran Not Duped — Agreement-Incapable US",
        ),
        (
            "Segment 9 — The Paper It's Written On",
            "MOU Roadmap — Hezbollah Terror Label",
        ),
        (
            "Segment 10 — Such Control Over The Government",
            "Beirut Veto — Lebanese Army Disarmed",
        ),
        (
            "Segment 11 — To Withstand That Pressure I",
            "Horowitz Apoplexy — Deal Will Be Sabotaged",
        ),
    ],
}

def main() -> int:
    failed = 0
    for rel, slug_headings in CAPTURES.items():
        path = ARCHIVE / rel
        if not path.is_file():
            print(f"missing {path}")
            failed += 1
            continue
        try:
            write_slug_retitle_capture(path, slug_headings)
        except ValueError as exc:
            print(f"FAIL {rel}: {exc}")
            failed += 1
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
