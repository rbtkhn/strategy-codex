"""Tests for scripts/transcript_section_curation.py."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    detect_body_marker,
    insert_sections,
    mark_sectioned_frontmatter,
    normalize_for_anchor,
    split_transcript_document,
)


def test_insert_sections_splits_on_anchors_and_last_runs_to_eof():
    body = "Open line. First anchor section one. Second anchor section two tail."
    out = insert_sections(
        body,
        ["Open", "One", "Two"],
        ["first anchor", "second anchor"],
    )
    assert out.startswith("### Open\n\nOpen line.")
    assert "### One\n\nFirst anchor section one." in out
    assert "### Two\n\nSecond anchor section two tail." in out


def test_insert_sections_applies_asr_cleanup_before_split():
    body = "Start. Professor Dieng speaks. Next anchor part."
    out = insert_sections(
        body,
        ["A", "B"],
        ["next anchor"],
        asr_cleanup_fn=lambda t: t.replace("Professor Dieng", "Professor Jiang"),
    )
    assert "Professor Jiang speaks" in out
    assert "Professor Dieng" not in out


def test_normalize_for_anchor_unicode_punctuation():
    assert normalize_for_anchor("Let's — go") == "let's - go"


def test_detect_body_marker_statecraft_transcript():
    doc = "---\ntitle: x\n---\n\n## Transcript\n\nHello."
    assert detect_body_marker(doc) == "## Transcript\n"


def test_split_transcript_document():
    doc = "---\n---\n\n## Transcript\n\nBody here."
    head, marker, body = split_transcript_document(doc)
    assert marker == "## Transcript\n"
    assert body.strip() == "Body here."


def test_mark_sectioned_frontmatter_adds_curation_field():
    head = "---\ntitle: test\nsource_note: \"landed\"\n---\n\n"
    out = mark_sectioned_frontmatter(head, section_count=3)
    assert "transcript_curation: curated_sectioned" in out
    assert "source-section pass" in out
    assert "(3 sections)" in out
