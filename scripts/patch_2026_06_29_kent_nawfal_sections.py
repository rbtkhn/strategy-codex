#!/usr/bin/env python3
"""Source-section ship — 2026-06-29 Mario Nawfal × Joe Kent oligarchs interview."""
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

DAY = ROOT / "source-archive/statecraft/2026-06-29"
CAPTURE = "source-mario-nawfal-kent-israel-oligarchs-hijacked-us-government-2026-06-29.md"
HOST = "Mario Nawfal"
GUEST = "Joe Kent"

SPEC = {
    "titles": [
        "Show Open — Negotiations Qatar And Walk Away Frame",
        "Lebanon Referee — CENTCOM Vs MOU And Israel Stasis",
        "War Resumption — SenCom Options And Trump Messaging",
        "Kazakhstan Tungsten — NYT Deal And Business In Politics",
        "Oligarchy — Dark Money And Mamdani Backlash",
        "Butler Deep State — Assassination Threads And Kent Silva",
        "Pack Money — Congress PACS And Immunity Dossiers",
        "Surveillance And Legal — Gaetz Fabrication And Weaponized Courts",
        "Populist Coalition — Tucker Tulsi Massie Third Party",
        "Brad Cooper Lebanon — Empire Exit And Iraq Lessons",
        "NCTC Hezbollah — Shia Threat And Dehumanization Trap",
        "Root Causes — Soleimani Taliban And Israel Blowback",
        "Close — War Machine Clip And Sign Off",
    ],
    "anchors": [
        ">> You made a good point from us advocating for Trump walking away to now uh CENTCOM commander going to Lebanon to make sure a deal that the US just signed up to gets implemented.",
        ">> Do you worry that we could see a resumption of the war?",
        ">> I want to Lisa, can you show that image I just sent you?",
        "Do you think um the US would you call the I know it's a democracy but do you think it's also an oligarchy?",
        ">> Yeah. You were talking about how Trump was different and then something happened",
        "Um have you witnessed any of that yourself? You seem to be a straight shooter.",
        ">> Do you think you're being spied on now?",
        "What's your plan now? What are you planning to do?",
        "Show this image. Please, Lisa, if you show these images now of of uh Brad Cooper",
        "as you you were the director of the national uh the NCC the national counterterroris center.",
        "one of the key mistakes that we've made here by going to war with Iran and taking this much more aggressive stance against Iran",
        ">> Um let me get that clip. Uh kill terrorist is Brad Pit playing in a movie.",
    ],
    "note": (
        " · source-section pass 2026-06-29 (13 sections; NCTC/root-causes split)"
    ),
    "manual_asr": (
        ("straight of Hmuz", "Strait of Hormuz"),
        ("straight of Hamuz", "Strait of Hormuz"),
        ("straits of horror moves", "Strait of Hormuz"),
        ("straight support moves", "Strait of Hormuz"),
        ("straightfor.", "Strait of Hormuz."),
        (" he has aou ", " he has a MOU "),
        (" we got anou ", " we got a MOU "),
        ("sentcom", "CENTCOM"),
        ("SenCom", "CENTCOM"),
        ("Caner Fitzgerald", "Cantor Fitzgerald"),
        ("NDA section 224", "NDAA section 224"),
        ("Kasum Somani", "Qasem Soleimani"),
        ("Abuani Muandas", "Abu Mahdi al-Muhandis"),
        ("Marger Taylor Green", "Marjorie Taylor Greene"),
        ("Matt Gates", "Matt Gaetz"),
        ("Musha Kame", "Khamenei"),
        ("Mushta Kame", "Khamenei"),
        ("Zad Gerard", "Ziad Jarrah"),
    ),
}

def validate_capture(path: Path) -> list[str]:
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_section_patch_body(
            doc,
            manual_asr=SPEC["manual_asr"],
            interview_host=HOST,
            interview_guest=GUEST,
        )
    except ValueError as exc:
        return [str(exc)]
    return validate_section_anchors(body, SPEC["titles"], SPEC["anchors"])

def write_capture(path: Path) -> int:
    return write_interview_section_patch_capture(
        path,
        SPEC["titles"],
        SPEC["anchors"],
        manual_asr=SPEC["manual_asr"],
        manual_asr_spot_fix="",
        resection_note=SPEC["note"],
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
    print(f"OK {CAPTURE} ({len(SPEC['titles'])} sections, anchors validated)")
    if args.dry_run:
        return 0
    words = write_capture(path)
    print(f"wrote {CAPTURE} ({words} words, {len(SPEC['titles'])} sections)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
