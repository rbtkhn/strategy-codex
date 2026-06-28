#!/usr/bin/env python3
"""Manual ASR spot-fix + source-section — 2026-06-27 Dialogue Works Larry Johnson Sirik interview."""
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
    insert_sections,
    mark_sectioned_frontmatter,
    reflow_section_paragraphs,
    split_transcript_document,
)

DAY = ROOT / "source-archive/statecraft/2026-06-27"

CAPTURE = (
    "source-dialogue-works-larry-johnson-us-bombs-iran-near-sirik-tehran-counterstrike-us-bases-regional-war-2026-06-27.md"
)

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
    ">> how >> take out all the air tankers of Ben Gurion for starter",
    ">> Here is no reports, Larry. It seems that two Bandar Lengeh",
    ">> Larry, do you do you think that Europe as as right now what's going on?",
    "What's so amazing to me that MOU is a failed sort of contract between Iran and the United States.",
]

RESECTION_NOTE = (
    " · source-section re-section pass 2026-06-28 "
    f"({len(SECTION_TITLES)} sections; §10 MOU sliver merged §9; §21 tanker block split incl. Europe/NATO)"
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
    note = f" · interview speaker-label pass 2026-06-28 ({turns} turns; Nima/Larry >> markers)"
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
    if "manual_asr_spot_fix:" not in head and asr_subs:
        head = patch_manual_asr_frontmatter(head, subs=asr_subs)
    head = mark_sectioned_frontmatter(head, section_count=len(SECTION_TITLES))
    head = append_resection_note(head)
    body = insert_sections(body, SECTION_TITLES, SECTION_ANCHORS)
    body, turns_labeled = apply_interview_turn_speaker_labels(
        body,
        host="Nima Alkhorshid",
        guest="Larry Johnson",
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
