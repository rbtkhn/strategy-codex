#!/usr/bin/env python3
"""Section-balance pass — Reason to Resist May 24 / May 26 (split overweight rails)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    detect_body_marker,
    find_anchor_pos,
    insert_sections,
    mark_sectioned_frontmatter,
    split_transcript_document,
)

ARCHIVE = ROOT / "source-archive/statecraft"

CAPTURES: dict[str, dict] = {
    "2026-05-18/source-lascaris-russian-strikes-europe-nato-members-inevitable-2026-05-18.md": {
        "titles": [
            "Show Open — NATO Strike Prediction",
            "Moscow Drone Barrage — Escalation Pattern",
            "Air Defense Limits — Lebanon and Israel Comparison",
            "Russian MOD List — European Drone Suppliers",
            "EU Militarization — 5% GDP and War by 2030",
            "Domestic Pressure — Casualties Economy Levada",
            "Karaganov Clip — Escalation Ladder Diesen Interview",
            "Morality and History — Provocation Narrative",
            "Capitulation or Catastrophe — Two Ways This War Ends",
            "Iran Contrast — No NATO Strikes Yet",
            "Closing — Inevitable Strikes and Call to Act",
        ],
        "anchors": [
            "over the weekend, ukraine launched its largest drone attack",
            "today, france's paper of record, le monde",
            "now, uh 1 month ago russia's government published a list",
            "almost all of europe's nato members",
            "now, on top of this, russia's government is coming under increasing pressure",
            "in addition, uh and this is uh equally troubling",
            "um and i want to talk a little bit about two other things",
            "do you really want to risk the future of all that you hold dear",
            "and that is the war in iran",
            "and finally, a personal reflection",
        ],
    },
    "2026-05-24/source-lascaris-helmer-russia-retaliates-student-dormitory-strike-2026-05-24.md": {
        "titles": [
            "Show Open — Helmer Welcome",
            "Starobilsk Toll — Bila Tserkva and Oreshnik Setup",
            "Helmer Opening Analysis — Oreshnik and Targets",
            "Election-Period Terrorism — Why Starobilsk",
            "Dimitri Strategic Rear — NATO Immunity Argument",
            "Putin Quotes — Neo-Nazism vs Street Read",
            "Putin Battlefield Claims — Helmer Fact-Check",
            "Dmitriev Bribery — Trump Fix Is In",
            "Evidence Debate — Bribes and Strategic Rear",
            "Lefkada Drone — Kostyukov Faction Gap",
            "Lefkada Escalation — Drone Control Room Debate",
            "Kostyukov Lavrov — Military Means Consensus",
            "Rubio Sweden — Negotiated Settlement Quote",
            "GRU Military Means — Beijing Putin-Xi Shift",
            "NATO Strike Candidates — Helmer No Article 5",
            "Patrushev Lefkada — Greece Warning and Outro",
        ],
        "anchors": [
            "unfortunately, the the death toll is now over 20",
            "what is your overall reaction to these developments?",
            "let's go to the question of why the ukrainians did that",
            "um it is becoming increasingly clear that uh as you as you just pointed out",
            "well, i think you very clearly, dmitri, expressed the common sense",
            "let's go to the next point. i'm speaking in in order",
            "but here's what president putin says. it's the cost we",
            "what is the purpose of kirill dmitriev",
            "well, my first question is i'm not just in your",
            "we're talking no longer about pinpricks",
            "professionals like admiral kostyukov, the head of gru",
            "he said in sweden at the end of uh the nato meeting there",
            "well, the gru, the general staff, the security council think differently",
            "now, i i just want to clarify one thing",
            "but you raise another point that dimitri in in our mentioning",
        ],
    },
    "2026-05-26/source-lascaris-trump-sabotages-peace-talks-gaza-flotilla-2026-05-26.md": {
        "titles": [
            "Show Open — Iran Ceasefire Charade",
            "USCENTCOM Strike — Bandar Abbas",
            "Iranian MFA — Ceasefire Violation",
            "Tabnak Casualties — FARS MQ-9",
            "Araghchi Qatar — Assets and Sabotage",
            "Lebanon Yellow Line — Israeli Expansion",
            "Oil Market — Guardian Point of No Return",
            "Matilda Malle — Interception and Boarding",
            "Matilda Malle — Warship to Connection Lost",
            "Ihab Layf — Perseverance Timeline",
            "Ihab Layf — Prison Ship Detail",
            "Ihab Layf — Torture and Consular Gap",
            "Carney-Herzog Readout — Host Frame",
            "Close — Sanctions and Palestinian Centrality",
        ],
        "anchors": [
            "last night, within a few hours of me making this argument",
            "the iranian foreign ministry subsequently confirmed",
            "in iran, the news website tabnak",
            "all of this happened while iran's foreign minister abbas araghchi",
            "now, if all of this wasn't bad enough, the terrorist israeli military announced",
            "today, predictably, the price of brent crude shot back up",
            "now with that uh let's turn to our guests",
            "oh, it was so when you jump on the warship",
            "the second flotilla passenger we spoke with is ihab layf",
            "so let's uh get into some more detail about this horror show",
            "um, now we've all seen this uh outrageous footage of ben-gvir",
            "i would like to show you a readout issued by the office of the prime minister",
            "the last thing i want to ask you, ihab",
        ],
    },
}

def flatten_sectioned_body(body: str) -> str:
    chunks = re.split(r"^### .+$", body, flags=re.M)
    return "\n\n".join(c.strip() for c in chunks if c.strip())

def validate_flat(flat: str, spec: dict) -> list[str]:
    errors: list[str] = []
    titles = spec["titles"]
    anchors = spec["anchors"]
    if len(titles) != len(anchors) + 1:
        errors.append(
            f"title/anchor count mismatch: {len(titles)} titles, {len(anchors)} anchors"
        )
    cursor = 0
    for anchor in anchors:
        try:
            pos = find_anchor_pos(flat, anchor, cursor)
            cursor = pos + 1
        except ValueError as exc:
            errors.append(str(exc))
    return errors

def balance_capture(path: Path, spec: dict, *, dry_run: bool = False) -> None:
    doc = path.read_text(encoding="utf-8")
    head, marker, body = split_transcript_document(doc)
    flat = flatten_sectioned_body(body)
    errs = validate_flat(flat, spec)
    if errs:
        raise ValueError(f"{path.name}: " + "; ".join(errs))

    if dry_run:
        print(f"OK {path.relative_to(ARCHIVE)} ({len(spec['titles'])} sections)")
        return

    head = mark_sectioned_frontmatter(head, section_count=len(spec["titles"]))
    if "section-balance pass" not in head:
        head = re.sub(
            r'^(editorial_note: "?)(.*?)("?\s*)$',
            r'\1\2 · section-balance pass 2026-06-26.\3',
            head,
            count=1,
            flags=re.M,
        )

    new_body = insert_sections(flat, spec["titles"], spec["anchors"])
    path.write_text(f"{head}{marker}\n\n{new_body}\n", encoding="utf-8", newline="\n")
    print(
        f"wrote {path} ({len(new_body.split()):,} words, {len(spec['titles'])} sections)"
    )

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    failed = 0
    for rel, spec in CAPTURES.items():
        path = ARCHIVE / rel
        if not path.is_file():
            print(f"missing {path}")
            failed += 1
            continue
        try:
            balance_capture(path, spec, dry_run=args.dry_run)
        except ValueError as exc:
            print(f"FAIL {rel}: {exc}")
            failed += 1
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
