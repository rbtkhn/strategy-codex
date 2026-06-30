#!/usr/bin/env python3
"""Manual ASR spot-fix + source-section — 2026-06-27 Dialogue Works Ray McGovern interview."""
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
    "source-dialogue-works-ray-mcgovern-iran-missiles-force-us-retreat-bases-moving-west-escape-attacks-2026-06-27.md"
)

HOST = "Nima Alkhorshid"
GUEST = "Ray McGovern"

MANUAL_ASR: tuple[tuple[str, str], ...] = (
    ("sirk area", "Sirik area"),
    ("Baharin", "Bahrain"),
    ("Strait of form", "Strait of Hormuz"),
    ("straight of HUS", "Strait of Hormuz"),
    ("Shakesoms", "Sheikhdoms"),
    ("Ebola", "Hezbollah"),
    ("Gata", "Qatar"),
    ("jcular", "jocular"),
    ("Nemo these", "Nima these"),
    ("Thank you Nema", "Thank you Nima"),
    ("bridal he puts the res", "bridle he puts the reins"),
    ("irassable unpredictable", "irreversible unpredictable"),
    ("General Danu Porstar", "General Michael Caine"),
    ("Two hours later, Dier was fired", "Two hours later, Caine was fired"),
    ("Lavro.", "Lavrov."),
    ("says Lavo,", "says Lavrov,"),
    ("Puchin.", "Putin."),
    (" chaired by Puchin.", " chaired by Putin."),
    ("Latia", "Latvia"),
    ("Latafia", "Latvia"),
    ("Latafians", "Latvians"),
    ("Latians", "Latvians"),
    (" in Ria,", " in Riga,"),
    ("places in Ria,", "places in Riga,"),
    ("Dimmitri Trinan", "Dmitry Trenin"),
    ("Dimmitri Trenan", "Dmitry Trenin"),
    ("Mir asked him", "Mearsheimer asked him"),
    ("a kadag.", "Karaganov."),
    ("Karagandov", "Karaganov"),
    ("Mizf the former president", "Medvedev the former president"),
    ("Belusf", "Belousov"),
    ("with coffin", "Witkoff"),
    ("Atlantas", "Latvians"),
    ("Mosedc", "Mossadegh"),
    ("Musc uh man", "Mossadegh uh man"),
    ("Moses in Iran", "Mossadegh in Iran"),
    ("slovak thing", "SAVAK thing"),
    ("Lanningrad", "Leningrad"),
    ("Lennengrad", "Leningrad"),
    ("Langard", "Leningrad"),
    ("little Vita", "little Viktor"),
    ("Vichi again", "Viktor again"),
    ("Vich is over", "Viktor is over"),
    ("Hex Seth", "Hegseth"),
    ("JD Vant.", "JD Vance."),
    ("hypersight", "hypersonic"),
    ("formos", "Hormuz"),
)

MANUAL_ASR_SPOT_FIX = (
    "2026-06-28 — Sirik; Bahrain; Hormuz; Sheikhdoms; Hezbollah; Qatar; "
    "Lavrov; Putin; Latvia/Latvians/Riga; Dmitry Trenin; Karaganov; "
    "Belousov; Witkoff; Mossadegh; SAVAK; Leningrad; Viktor; Caine; Hegseth; "
    "tentative: Nima/Nema host ASR"
)

SECTION_TITLES = [
    "Show Open — Hormuz Escalation And IRGC Hotline Denial",
    "Forked Tongue — Rubio Bahrain And Fifth Fleet Aftermath",
    "Strait Control — MOU Fiction And Catbird Seat",
    "Oman Fee — Bloomberg GCC Division And Rubio Route",
    "Lebanon Arc — Resistance Fly And Israel Made Us Do It",
    "MOU Shield — Hegseth Filter And Midterm Pressure",
    "Bases West — Wall Street Journal Rear-Area Shift",
    "Outlast Game — Map Myopia Wilkerson And Caine Firing",
    "MOU Lebanon — Withdrawal Clause And Government Fixture",
    "Palestine Solidarity — Moral Issue And Hamas Model",
    "Israeli Agenda — GCC Propaganda And Society Shift",
    "Joe Kent — Rubio Admission And Mossadegh 1953",
    "Ukraine Circus — Drone Pin Pricks And Rutte Puppet",
    "Putin Judgment — Latvia Bases And NATO Escalation Ladder",
    "Starlink Response — Drones And Kremlin Sergeants",
    "Anchorage Dead — Lavrov Ushakov Versus Rubio Bahrain",
    "Close — Putin Brother Siege And Judiciousness",
]

SECTION_ANCHORS = [
    "Nima these are really good questions.",
    "Yeah. My understanding is that Iran has doesn't feel that they're in some sort of rush",
    "what's what's left of what's left of that place.",
    "Yeah. The question is Rey, is the United States using the MOU to somehow reduce the burden",
    "Well, the reality is it would make it even a greater and more accessible target.",
    "Well that's an easy one.",
    "text is forcing Israel to withdraw from Lebanon. Basically,",
    "I think for Iran, Rey, the case of Palestine and the case of Lebanon is a moral issue.",
    "Yeah. Yeah. My understanding is this, that Iran is not going to back down, Ry.",
    "Yeah. And as I quoted Secretary of State Rubio, uh, Israel started it and, uh,",
    "one of the other fronts that is important right now is the case of Ukraine",
    "Is Latvia a member of NATO?",
    "do we have five more minutes or so?",
    "Rubio in Bahrain yesterday says Anchorage is dead.",
    "Before wrapping up, my understanding of Russia, as you mentioned, I think there's so much",
    "June 22nd was the Nazi invasion.",
]

RESECTION_NOTE = (
    " · source-section re-section pass 2026-06-28 "
    f"({len(SECTION_TITLES)} sections; Hormuz–Lebanon–Ukraine–Putin close arc)"
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
