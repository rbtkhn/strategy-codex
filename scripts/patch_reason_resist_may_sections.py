#!/usr/bin/env python3
"""source-section pass for Reason to Resist May 2026 captures (host-only channel shelf)."""
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
            "Starobilsk Dormitory — Friday Attack",
            "Bila Tserkva Response — Putin Order",
            "Helmer Opening Analysis — Oreshnik and Targets",
            "Election-Period Terrorism — Why Starobilsk",
            "Dimitri Strategic Rear — NATO Immunity Argument",
            "Putin Quotes vs Street — Dmitriev Bribery",
            "Rubio Sweden — Negotiated Settlement Only",
            "Beijing Putin-Xi — Military Means Shift",
            "NATO Strike Candidates — Helmer No Article 5",
        ],
        "anchors": [
            "unfortunately, the the death toll is now over 20",
            "hours after the strike, uh, the russian president ordered",
            "what is your overall reaction to these developments?",
            "let's go to the question of why the ukrainians did that",
            "um it is becoming increasingly clear that uh as you as you just pointed out",
            "well, i think you very clearly, dmitri, expressed the common sense",
            "he said in Sweden at the end of uh the NATO meeting there",
            "now, i i just want to clarify one thing",
            "the i that i i have no source in general staff",
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
            "Gaza Flotilla — Matilda Malle Shot in Custody",
            "Ihab Layf — Prison Ship Torture",
            "Carney-Herzog Readout — No Consequences",
            "Close — Palestinian Centrality",
        ],
        "anchors": [
            "last night, within a few hours of me making this argument",
            "the iranian foreign ministry subsequently confirmed",
            "in iran, the news website tabnak",
            "all of this happened while iran's foreign minister abbas araghchi",
            "now, if all of this wasn't bad enough, the terrorist israeli military announced",
            "today, predictably, the price of brent crude shot back up",
            "now with that uh let's turn to our guests",
            "the first participant we spoke with is matilda malle",
            "the second flotilla passenger we spoke with is ihab layf",
            "i would like to show you a readout issued by the office of the prime minister",
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
        errors.append(
            f"title/anchor count mismatch: {len(titles)} titles, {len(anchors)} anchors"
        )
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
    args = parser.parse_args()

    failed = 0
    for rel, spec in CAPTURES.items():
        path = ROOT / "source-archive/statecraft" / rel
        if not path.is_file():
            print(f"missing {path}")
            failed += 1
            continue
        errs = validate_capture(path, spec)
        if errs:
            print(f"FAIL {rel}:")
            for e in errs:
                print(f"  - {e}")
            failed += 1
            continue
        if args.dry_run:
            print(f"OK {rel} ({len(spec['titles'])} sections)")
            continue
        write_sectioned_capture(path, spec["titles"], spec["anchors"])

    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
