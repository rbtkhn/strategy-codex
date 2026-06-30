#!/usr/bin/env python3
"""Source-section ship — 2026-06-28 Alexander Mercouris solo Russia Hits Back / FSB / Putin."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    prepare_section_patch_body,
    validate_section_anchors,
    write_sectioned_capture,
)

DAY = ROOT / "source-archive/statecraft/2026-06-28"

CAPTURE = (
    "source-alexander-mercouris-russia-hits-back-kills-kiev-intel-chief-"
    "putin-west-kiev-strikes-destabilisation-failed-2026-06-28.md"
)

SECTION_TITLES = [
    "Show Open — Sunday Date And FSB Fakrif Claim",
    "Dirty War — Russian Counter Assassination Escalation",
    "FSB Networks — Agent Policy Change In Ukraine",
    "Putin United Russia — Western Destabilisation Strategy",
    "Putin Speech — Normalcy War And Terror Frame",
    "Mercouris Visit — Calm Mood And FSB Message Link",
    "Front Lines — Konstantinovka Kramatorsk Pokrovsk",
    "Russian Strikes — Railways Drones And Mig 29 Theory",
    "Hardliner Pressure — Reuters And Donbass Victory",
    "EU Drone Doubts — Oil Exports And Retaliation Risk",
    "Persian Gulf — MOU Fragility And Iran Demands",
    "Close — Platforms And Subscribe",
]

SECTION_ANCHORS = [
    "Well, on this occasion with the announcement by the FSB",
    "Now there is something else to say which is comes from information",
    (
        "Well, even as the FSB has been conveying these messages, the Russian President "
        "Vladimir Putin has now spoken to the annual Congress of the United Russia Party"
    ),
    "In other words, that as much as anything else, the war now has become a war",
    "Now, of course, Putin would say that and perhaps privately he is more concerned",
    "Now, in the meantime, the war itself continues in the same way that it did previously",
    "All the best observers of the war confirm this",
    (
        "Now, I'm going to finish this runup about Ukrainian news by discussing some "
        "information that's now circulating in parts of the Western media"
    ),
    "Now I am relieved to hear this but I would say that actually the situation is worse",
    "Anyway, let me now turn to the situation in the Persian Gulf",
    "Anyway, this is where I'm going to finish today's program",
]

RESECTION_NOTE = (
    " · source-section pass 2026-06-29 (12 sections; FSB dirty war/Putin/Donbass/Gulf arc)"
)

def validate_capture(path: Path) -> list[str]:
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = prepare_section_patch_body(doc, manual_asr=())
    except ValueError as exc:
        return [str(exc)]
    return validate_section_anchors(body, SECTION_TITLES, SECTION_ANCHORS)

def write_capture(path: Path) -> None:
    write_sectioned_capture(
        path,
        SECTION_TITLES,
        SECTION_ANCHORS,
        reject_if_sectioned=False,
    )
    doc = path.read_text(encoding="utf-8")
    if "source-section pass" not in doc:
        doc = doc.replace(
            "· source-clean pass 2026-06-29.",
            f"· source-clean pass 2026-06-29.{RESECTION_NOTE}",
        )
        doc = doc.replace(
            "not human-verified verbatim; verify before quotation.\"",
            f"not human-verified verbatim; verify before quotation.{RESECTION_NOTE}\"",
        )
        path.write_text(doc, encoding="utf-8")

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

    print(f"OK {CAPTURE} ({len(SECTION_TITLES)} sections)")
    if not args.dry_run:
        write_capture(path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
