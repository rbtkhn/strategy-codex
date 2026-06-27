#!/usr/bin/env python3
"""source-section batch — Apr 2026 Breaking Points × Pape guest capture (outline pinned).

Status: OUTLINE ONLY — do not run until operator approves section map.
Verify anchors: python scripts/patch_2026_04_29_breaking_points_pape_sections.py --check-anchors

Ship note: legacy capture lacks `## Transcript`; `--apply` inserts that marker before the
speaker block (preserves **Ryan Grim:** / **Professor Robert Pape:** labels).
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
    "source-archive/statecraft/2026-04-29/"
    "source-pape-grim-nuclear-iran-inevitable-2026-04-29.md"
)

SPEC = {
    "titles": [
        "Show Open — Breaking Points Welcome and Escalation Trap Frame",
        "UAE OPEC Exit — US Lost Control and Fourth Center Fragmentation",
        "Oil Price Trajectory — Shortages Stage and Misery Index Forecast",
        "Strait Negotiations — Rubio Toll Definition and Ten-Point Walkthrough",
        "Nuclear Sequencing — Grim Pushback and Global Spillover Beyond Hormuz",
        "JCPOA Origins — Obama-Putin Trade and Russia Coalition Impossibility Today",
        "Close — Escalation Trap Plug and Breaking Points Outro",
    ],
    "anchors": [
        "Let's just start with the OPEC news",
        "Brent crude prices were at",
        "fluent Trumpese",
        "slight difference of view here",
        "in 2015, as you know, Russia was part of the Iran nuclear deal",
        "always a pleasure. Thank you.",
    ],
    "note": (
        "Operator-paste interview with speaker labels; no ASR clean required. "
        "Ship inserts `## Transcript` after intro block if missing."
    ),
}

TRANSCRIPT_MARKER = "## Transcript\n"
LEGACY_SPLIT = "---\n\n"


def extract_flat_body(doc: str) -> str:
    if TRANSCRIPT_MARKER in doc:
        return doc.split(TRANSCRIPT_MARKER, 1)[1]
    if LEGACY_SPLIT in doc:
        return doc.split(LEGACY_SPLIT, 1)[1]
    raise ValueError("no transcript body (expected ## Transcript or legacy --- split)")


def normalize_for_section_ship(doc: str) -> tuple[str, str, str]:
    """Return head, marker, body; insert ## Transcript when legacy shape."""
    if TRANSCRIPT_MARKER in doc:
        head, marker, body = split_transcript_document(doc)
        return head, marker, body
    if LEGACY_SPLIT not in doc:
        raise ValueError("missing legacy --- split for transcript body")
    head, body = doc.split(LEGACY_SPLIT, 1)
    head = head.rstrip() + "\n\n" + TRANSCRIPT_MARKER
    return head, TRANSCRIPT_MARKER, body.lstrip("\n")


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
