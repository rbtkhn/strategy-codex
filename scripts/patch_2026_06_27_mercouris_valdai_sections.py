#!/usr/bin/env python3
"""source-section batch — 2026-06-27 Mercouris solo Valdai / Le Monde / Lavrov MoU monologue."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    find_anchor_pos,
    insert_sections,
    mark_sectioned_frontmatter,
    reflow_section_paragraphs,
    split_transcript_document,
    write_paragraph_reflow_capture,
)

DAY = ROOT / "source-archive/statecraft/2026-06-27"

CAPTURE = "source-alexander-mercouris-putin-lukashenko-rebuff-zelensky-meet-in-valdai-french-msm-admits-kiev-troops-losing-mou-unravels-2026-06-27.md"

SECTION_TITLES = [
    "Show Open — Saturday Date And Belarus Threats",
    "Putin Lukashenko — Union State And Regional Security",
    "Valdai Meeting — Symbolism And December Attack",
    "Washington Mood — Bessent Minerals And European Aid",
    "Donbass Front — Le Monde Exhaustion And Logistics Campaign",
    "Drone War — Deep Strikes And Russian Adaptation",
    "Lavrov Anchorage — Iran MoU And Diplomatic Bad Faith",
    "Nabiullina — Key Rate Cut And Inflation Paradox",
    "Monetary Overkill — Overshoot Cycle And Putin Loyalty",
    "Iran Gulf — Hormuz Lebanon And China Pivot",
    "Britain — Project Ukraine And Zelensky Curse",
    "Close — Subscribe And Platform Sign-Off",
]

SECTION_ANCHORS = [
    "And sure enough, a meeting has indeed now taken place.",
    "The most interesting thing however about this meeting between Lukashenko and Putin",
    "Incidentally, we've been getting more and more leaks from the United States",
    "Meanwhile, the war goes on and I'm not going to discuss in huge detail",
    "So anyway, that I think is the overall situation on the front lines. Now, Ukrainian drone attacks on Russia continue.",
    "Now I want to return to something that the Russian foreign minister Sergey Lavrov said",
    "Now, at this point, I would like to say something about the current situation in the Russian economy",
    "Now, there is much to be said for Nabiullina.",
    "In the meantime, the situation between Iran and the United States remains",
    "Now, I'm going to finish this program by returning to a discussion of the situation in Britain.",
    "Anyway, that's all I'm going to say about it on this program. Let me remind you again to tick the like button",
]


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


def validate_capture(path: Path) -> list[str]:
    errors: list[str] = []
    doc = path.read_text(encoding="utf-8")
    try:
        _, _, body = flat_body_from_doc(doc)
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


def write_resectioned_capture(path: Path) -> None:
    doc = path.read_text(encoding="utf-8")
    head, marker, body = flat_body_from_doc(doc)
    head = mark_sectioned_frontmatter(head, section_count=len(SECTION_TITLES))
    body = insert_sections(body.strip(), SECTION_TITLES, SECTION_ANCHORS)
    body = reflow_section_paragraphs(body)
    path.write_text(head + marker + body, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--reflow-only",
        action="store_true",
        help="Paragraph reflow on existing section map only (no re-section).",
    )
    args = parser.parse_args()

    path = DAY / CAPTURE
    if not path.is_file():
        print(f"missing {path}")
        return 1
    if args.reflow_only:
        if args.dry_run:
            print(f"OK {CAPTURE} (reflow-only dry run)")
            return 0
        write_paragraph_reflow_capture(path)
        print(f"OK {CAPTURE} (paragraph reflow)")
        return 0
    errs = validate_capture(path)
    if errs:
        print(f"FAIL {CAPTURE}:")
        for e in errs:
            print(f"  - {e}")
        return 1
    print(f"OK {CAPTURE} ({len(SECTION_TITLES)} sections)")
    if not args.dry_run:
        write_resectioned_capture(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
