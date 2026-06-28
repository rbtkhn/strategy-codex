#!/usr/bin/env python3
"""Manual ASR spot-fix + source-section — 2026-06-27 Dialogue Works Ray McGovern interview."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    apply_interview_turn_speaker_labels,
    find_anchor_pos,
    inject_section_open_turn_markers,
    insert_sections,
    mark_sectioned_frontmatter,
    reflow_section_paragraphs,
    restore_turn_markers_from_speaker_labels,
    split_transcript_document,
)

DAY = ROOT / "source-archive/statecraft/2026-06-27"

CAPTURE = (
    "source-dialogue-works-ray-mcgovern-iran-missiles-force-us-retreat-bases-moving-west-escape-attacks-2026-06-27.md"
)

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


def flatten_sectioned_body(body: str) -> str:
    chunks: list[str] = []
    current: list[str] = []
    for line in body.splitlines():
        if line.startswith("### "):
            if current:
                chunks.append("\n".join(current).strip())
                current = []
            continue
        current.append(line)
    if current:
        chunks.append("\n".join(current).strip())
    return "\n\n".join(chunks)


def flat_body_from_doc(doc: str) -> tuple[str, str, str]:
    head, marker, body = split_transcript_document(doc)
    if body.lstrip().startswith("### "):
        body = flatten_sectioned_body(body)
    return head, marker, body


def apply_manual_asr(text: str) -> tuple[str, int]:
    count = 0
    for old, new in MANUAL_ASR:
        if old in text:
            text = text.replace(old, new)
            count += 1
    return text, count


def patch_manual_asr_frontmatter(head: str, *, subs: int) -> str:
    today = "2026-06-28"
    note_tail = f" · manual ASR spot-fix {today}"
    if "manual_asr_spot_fix:" not in head:
        head = head.replace(
            "\n---\n",
            f'\nmanual_asr_spot_fix: "{MANUAL_ASR_SPOT_FIX}"\n---\n',
            1,
        )
    if re.search(r"^source_note:", head, flags=re.M):
        if note_tail.strip() not in head:
            head = re.sub(
                r'^(source_note: ")(.*?)(")\s*$',
                rf"\1\2{note_tail}\3",
                head,
                count=1,
                flags=re.M,
            )
    receipt = f"Manual ASR spot-fix {today} ({subs} substitution groups); AI-assisted source-clean"
    if re.search(r"^editorial_note:", head, flags=re.M):
        head = re.sub(
            r'^editorial_note: ".*?"\s*$',
            f'editorial_note: "{receipt} · not human-verified verbatim; verify before quotation."',
            head,
            count=1,
            flags=re.M,
        )
    return head


def append_resection_note(head: str) -> str:
    if re.search(r"^editorial_note:", head, flags=re.M):
        head = re.sub(
            r" · source-section re-section pass 2026-06-28 \([^)]+\)",
            "",
            head,
        )
        if RESECTION_NOTE not in head:
            head = re.sub(
                r'^(editorial_note: ")(.*?)("\s*$)',
                rf"\1\2{RESECTION_NOTE}\3",
                head,
                count=1,
                flags=re.M,
            )
    return head


def prepare_body(doc: str) -> tuple[str, str, str]:
    head, marker, body = flat_body_from_doc(doc)
    body, _ = apply_manual_asr(body.strip())
    if "**Ray McGovern:**" in body:
        body = restore_turn_markers_from_speaker_labels(
            body,
            host="Nima Alkhorshid",
            guest="Ray McGovern",
        )
    return head, marker, body


def validate_capture(path: Path) -> list[str]:
    errors: list[str] = []
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_body(doc)
    except ValueError as exc:
        return [str(exc)]
    if len(SECTION_TITLES) != len(SECTION_ANCHORS) + 1:
        errors.append(
            f"title/anchor count mismatch: {len(SECTION_TITLES)} titles, {len(SECTION_ANCHORS)} anchors"
        )
    cursor = 0
    for anchor in SECTION_ANCHORS:
        try:
            pos = find_anchor_pos(body, anchor, cursor)
            cursor = pos + 1
        except ValueError as exc:
            errors.append(str(exc))
    return errors


def append_speaker_label_note(head: str, *, turns: int) -> str:
    note = f" · interview speaker-label pass 2026-06-28 ({turns} turns; Nima/Ray >> markers)"
    if note in head:
        return head
    if re.search(r"^editorial_note:", head, flags=re.M):
        return re.sub(
            r'^(editorial_note: ")(.*?)("\s*$)',
            rf"\1\2{note}\3",
            head,
            count=1,
            flags=re.M,
        )
    return head


def write_capture(path: Path) -> int:
    doc = path.read_text(encoding="utf-8")
    head, marker, body = flat_body_from_doc(doc)
    body, asr_subs = apply_manual_asr(body.strip())
    if "**Ray McGovern:**" in body:
        body = restore_turn_markers_from_speaker_labels(
            body,
            host="Nima Alkhorshid",
            guest="Ray McGovern",
        )
    if "manual_asr_spot_fix:" not in head and asr_subs:
        head = patch_manual_asr_frontmatter(head, subs=asr_subs)
    head = mark_sectioned_frontmatter(head, section_count=len(SECTION_TITLES))
    head = append_resection_note(head)
    body = insert_sections(body, SECTION_TITLES, SECTION_ANCHORS)
    body = inject_section_open_turn_markers(body)
    if "**Ray McGovern:**" in body or "**Nima Alkhorshid:**" in body:
        body = restore_turn_markers_from_speaker_labels(
            body,
            host="Nima Alkhorshid",
            guest="Ray McGovern",
        )
        body = inject_section_open_turn_markers(body)
    body, turns_labeled = apply_interview_turn_speaker_labels(
        body,
        host="Nima Alkhorshid",
        guest="Ray McGovern",
    )
    if turns_labeled:
        head = append_speaker_label_note(head, turns=turns_labeled)
    body = reflow_section_paragraphs(body)
    path.write_text(head + marker + body, encoding="utf-8")
    return asr_subs


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
