#!/usr/bin/env python3
"""source-section batch — Apr 2026 Redacted × Pape guest capture (outline pinned).

Status: OUTLINE ONLY — do not run until operator approves section map.
Verify anchors: python scripts/patch_2026_04_20_redacted_pape_sections.py --check-anchors

Ship note: legacy capture lacks `## Transcript`; `--apply` inserts that marker after the H1
title block (preserves `Host:` / `Professor Robert Pape:` speaker labels).
"""
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

REL = (
    "source-archive/statecraft/2026-04-20/"
    "source-pape-collapse-ahead-of-schedule-2026-04-20.md"
)

SPEC = {
    "titles": [
        "Show Open — Redacted Welcome and Ahead-of-Schedule Update",
        "Three Stages — Shortages Window and Contraction by May 31",
        "China Quagmire Logic — June Factory Tour and Beijing No-Lose View",
        "China Energy Stockpile — Solar-Nuclear Mix and Decade of Tariff Prep",
        "US Energy Grade — Lugar Legacy, Tanker Armada, and Five-Year Plan Gap",
        "Forty-Eight-Hour Clock — Zero-Sum Power, Lebanon Truce, and Debt Load",
        "Pocketbook Return — Working-Class Gas Pain and Targeted Relief Ask",
        "May 31 Cascade — Three-Trajectory Discipline and Erie Pennsylvania",
        "Close — Consequences Over Conspiracy and Escalation Trap Plug",
    ],
    "anchors": [
        "three stages",
        "Is this really about China",
        "stockpiling its oil",
        "letter grade",
        "next 48 hours",
        "We're back with Professor Pape",
        "next 60 days",
        "purposeful devaluation of the U.S. dollar",
    ],
    "note": (
        "Redacted host-labeled interview (Clayton / Natali Morris); no `## Transcript` yet. "
        "Load-bearing Hormuz shortage arc — pair with Apr 12 Escalation Trap Substack post. "
        "Ad-break stub at line ~60 preserved inside §7 pocketbook block."
    ),
}

TRANSCRIPT_MARKER = "## Transcript\n"

def extract_flat_body(doc: str) -> str:
    if TRANSCRIPT_MARKER in doc:
        return doc.split(TRANSCRIPT_MARKER, 1)[1]
    parts = doc.split("---", 2)
    if len(parts) < 3:
        raise ValueError("missing frontmatter")
    tail = parts[2].lstrip("\n")
    if not tail.startswith("#"):
        raise ValueError("expected H1 after frontmatter")
    blank = tail.find("\n\n")
    if blank == -1:
        raise ValueError("no body after H1")
    return tail[blank + 2 :]

def normalize_for_section_ship(doc: str) -> tuple[str, str, str]:
    if TRANSCRIPT_MARKER in doc:
        return split_transcript_document(doc)
    parts = doc.split("---", 2)
    if len(parts) < 3:
        raise ValueError("missing frontmatter")
    tail = parts[2].lstrip("\n")
    blank = tail.find("\n\n")
    if blank == -1:
        raise ValueError("no body after H1")
    title_block = tail[:blank]
    body = tail[blank + 2 :]
    head = f"---{parts[1]}---\n\n{title_block}\n\n{TRANSCRIPT_MARKER}"
    return head, TRANSCRIPT_MARKER, body

def check_spec(path: Path, spec: dict) -> bool:
    doc = path.read_text(encoding="utf-8")
    flat = " ".join(extract_flat_body(doc).split())
    pos = 0
    ok = True
    print(f"=== {path.name} ({len(spec['titles'])} sections) ===")
    for i, anchor in enumerate(spec["anchors"], start=1):
        try:
            pos = find_anchor_pos(flat, anchor, pos) + len(anchor)
            print(f"  anchor {i} -> section {i + 1}: {spec['titles'][i]}")
        except ValueError as exc:
            ok = False
            print(f"  {i}. FAIL — {exc}")
    print(f"  -> {spec['titles'][-1]} (EOF)")
    if spec.get("note"):
        print(f"  note: {spec['note']}")
    print()
    return ok

def apply_spec(path: Path, spec: dict) -> None:
    doc = path.read_text(encoding="utf-8")
    head, marker, body = normalize_for_section_ship(doc)
    path.write_text(f"{head}{body}", encoding="utf-8", newline="\n")
    write_sectioned_capture(
        path,
        spec["titles"],
        spec["anchors"],
        reject_if_sectioned=False,
        body_marker=marker,
    )

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write sectioned capture (operator-approved ship only)",
    )
    parser.add_argument(
        "--check-anchors",
        action="store_true",
        help="Verify all anchors resolve; no file writes",
    )
    args = parser.parse_args()

    path = ROOT / REL
    if args.check_anchors or not args.apply:
        ok = check_spec(path, SPEC)
        if not args.apply:
            print("OUTLINE ONLY — pass --apply after operator approval to ship.")
        return 0 if ok else 1

    apply_spec(path, SPEC)
    print(f"sectioned {REL}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
