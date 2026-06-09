"""Tests for cross-family caption/paste wrapper normalization."""

from __future__ import annotations

from pathlib import Path

from scripts.normalize_caption_wrapper_residue import (
    EDITORIAL_NOTE,
    decode_html_entities,
    normalize_text,
    strip_caption_header,
    strip_transcripts_prefix,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_decode_html_entities():
    body = "&gt;&gt; Thank you. &amp; welcome &quot;here&quot;."
    decoded, changed = decode_html_entities(body)
    assert changed
    assert decoded == '>> Thank you. & welcome "here".'


def test_strip_caption_header():
    body = "Kind: captions\nLanguage: en\nWhen you're negotiating with Iran"
    stripped, changed = strip_caption_header(body)
    assert changed
    assert stripped.startswith("When you're negotiating")


def test_strip_transcripts_prefix():
    body = "Transcripts:\nOh, really? >> Yeah."
    stripped, changed = strip_transcripts_prefix(body)
    assert changed
    assert stripped.startswith("Oh, really?")


def test_normalize_fixture_metadata():
    body = (
        "Kind: captions\nLanguage: en\n"
        "&gt;&gt; Hello there. &amp; welcome."
    )
    capture = f"""---
kind: transcript
show: Daniel Davis Deep Dive
host: Daniel Davis
guest: Test Guest
---

## Transcript

{body}
"""
    changed, new_text, change = normalize_text(
        REPO_ROOT / "source-archive/statecraft/2026-05-13/source-daniel-davis-deep-dive-test.md",
        capture,
    )
    assert changed
    assert change is not None
    assert change.entities_decoded
    assert change.caption_header_stripped
    assert "&gt;&gt;" not in new_text
    assert "Kind: captions" not in new_text
    assert "caption_wrapper_normalize_applied: true" in new_text
    assert EDITORIAL_NOTE in new_text
    assert change.wrapper_tier == "caption-metadata"
