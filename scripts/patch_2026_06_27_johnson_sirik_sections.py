#!/usr/bin/env python3
"""Manual ASR spot-fix + source-section — 2026-06-27 Dialogue Works Larry Johnson Sirik interview."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    prepare_section_patch_body,
    validate_section_anchors,
    write_interview_section_patch_capture,
)

DAY = ROOT / "source-archive/statecraft/2026-06-27"

CAPTURE = (
    "source-dialogue-works-larry-johnson-us-bombs-iran-near-sirik-tehran-counterstrike-us-bases-regional-war-2026-06-27.md"
)

HOST = "Nima Alkhorshid"
GUEST = "Larry Johnson"

MANUAL_ASR: tuple[tuple[str, str], ...] = (
    ("the band Langia band co", "Bandar Lengeh and two"),
    ("coming out of Alud uh not aloud, out of Jordan", "coming out of Al Udeid — no, not Al Udeid — out of Jordan"),
    ("trade for Moses", "trade for Hormuz"),
    ("trade of Heros", "Strait of Hormuz"),
    ("trade of form", "Strait of Hormuz"),
    ("state of her", "Strait of Hormuz"),
    ("pass through this rad without permission", "pass through this route without permission"),
    ("with with poses government", "with Pezeshkian government"),
    ("discussion last night with Sulle Man the because", "discussion last night with Suleiman because"),
    ("Today I talk with David Pine.", "Today I talk with David Pyne."),
    ("Bengurian", "Ben Gurion"),
    ("band Langia", "Bandar Lengeh"),
    ("Nabatia", "Nabatieh"),
    ("Mafik Alti", "Muwaffaq Salti"),
    ("Sandcom", "CENTCOM"),
    ("Sentcom", "CENTCOM"),
    ("Aluded", "Al Udeid"),
    ("Alouded", "Al Udeid"),
    ("alouded", "Al Udeid"),
    (" counter to the uhou and", " counter to the MOU and"),
    ("Surk area", "Sirik area"),
    ("Rian's Iran's", "Iran's"),
    ("Bill Mah.", "Bill Maher."),
    ("Bill Marsh.", "Bill Maher."),
)

MANUAL_ASR_SPOT_FIX = (
    "2026-06-28 — Sirik; CENTCOM; Al Udeid; Ben Gurion; Bandar Lengeh; Nabatieh; "
    "Muwaffaq Salti; MOU/uhou; Marandi (prior pass); tentative: Pezeshkian; "
    "David Pyne; Suleiman"
)

SECTION_TITLES = [
    "Show Open — Sirik Strikes And Hormuz Context",
    "Military Theater — Last Night Vs Tonight Escalation",
    "Bahrain Trigger — Fifth Fleet And Aviation Fuel",
    "No Hotline — IRGC Confirmed Escalation By Monday",
    "Strike Origins — Jordan Kuwait Bahrain And UAE Logic",
    "Rubio GCC — UKMTO Routes And MOU Terms",
    "US Breaking MOU — Trump GCC Condemnation",
    "Lebanon Complicates — MOU First Clause Violation",
    "Assembly Of Experts — 62 Of 86 And MOU Breakdown",
    "Hormuz Toll Debate — Sanctions Skepticism",
    "Ben Gurion Puzzle — Tehran Inflation Split",
    "David Pyne — Modest Response Alternative",
    "F-35 Depletion — MOU Outcomes And Lebanon",
    "Lebanon Loophole — Sovereignty And Israel Agreement",
    "MOU Loophole — Nabatieh Strikes Yellow Line",
    "Fuel Attrition — Aviation Crisis Two Weeks",
    "Lebanon Horror — US Role And Erdogan Talk",
    "Greater Israel — Iranian Internal Split",
    "Israel Overstretch — Gaza West Bank Four Fronts",
    "Retaliation Map — Drones Al Udeid CAOC And Project Freedom",
    "VLCC Interdiction — Japan Pressure Escalatory Cycle",
    "Legalistic Retaliation — Jordan Kuwait UAE Rules",
    "JASSM Bandar Lengeh — Strike Route Over UAE",
    "Europe NATO — CENTCOM British Involvement",
    "Close — Europe Ukraine Congress Trump Rubio",
]

SECTION_ANCHORS = [
    "I mean, let's just last night's attacks were what I call military political theater.",
    "Well, you know, the US is not responding um because of the ship.",
    "the communication line that JD Vance was talking about it there is no communication Larry",
    ">> I I think I think they're probably coming out of",
    ">> The whole I think it's it's the outcome of the Marco Rubio's visit",
    ">> Look they stopped the the United States has been breaking the MOU almost every day.",
    ">> I don't know if Larry the case of Lebanon is complicating the whole thing.",
    ">> Well, the assembly the assembly of experts issued that, right?",
    ">> Yeah. You see the flag of Hezbollah in the crowd",
    ">> Their argument is this Larry. Those people who are not agreeing with these negotiations.",
    "You know, I really, for the life of me, I don't know why Iran hasn't taken out",
    "Today I talk with David Pyne.",
    ">> Yes. No, that's true. And you understand that if the United States starts",
    ">> Well, if if the government of Lebanon is not asking Iran for help",
    ">> Yeah. My the reason that I said why do they need to say in MOU because",
    "everything if they try to run air strikes, tomahawk missiles, cruise missiles into the interior of Iran",
    ">> But I mean, look, um, but what's going on in Lebanon is horrible.",
    "The concept on the part of Iranian is that we have to make Lebanon the graveyard",
    ">> Yeah. The Iranian media is just reporting on the damage that was done so far.",
    ">> But you mean they're going to Iran's going to hit the oil tankers that are floating.",
    "take out all the air tankers of Ben Gurion for starter",
    ">> Here is no reports, Larry. It seems that two Bandar Lengeh",
    ">> Larry, do you do you think that Europe as as right now what's going on?",
    "What's so amazing to me that MOU is a failed sort of contract between Iran and the United States.",
]

RESECTION_NOTE = (
    " · source-section re-section pass 2026-06-28 "
    f"({len(SECTION_TITLES)} sections; §10 MOU sliver merged §9; §21 tanker block split incl. Europe/NATO)"
)

def validate_capture(path: Path) -> list[str]:
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_section_patch_body(
            doc,
            manual_asr=MANUAL_ASR,
            interview_host=HOST,
            interview_guest=GUEST,
        )
    except ValueError as exc:
        return [str(exc)]
    return validate_section_anchors(body, SECTION_TITLES, SECTION_ANCHORS)

def write_capture(path: Path) -> int:
    return write_interview_section_patch_capture(
        path,
        SECTION_TITLES,
        SECTION_ANCHORS,
        manual_asr=MANUAL_ASR,
        manual_asr_spot_fix=MANUAL_ASR_SPOT_FIX,
        resection_note=RESECTION_NOTE,
        interview_host=HOST,
        interview_guest=GUEST,
    )

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = DAY / CAPTURE
    if not path.is_file():
        print(f"missing {path}")
        return 1
    errs = validate_capture(path)
    if errs:
        print(f"FAIL {CAPTURE}:")
        for e in errs:
            print(f"  - {e}")
        return 1
    print(f"OK {CAPTURE} ({len(SECTION_TITLES)} sections, anchors validated)")
    if not args.dry_run:
        subs = write_capture(path)
        print(f"wrote {CAPTURE} (manual_asr_groups={subs})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
