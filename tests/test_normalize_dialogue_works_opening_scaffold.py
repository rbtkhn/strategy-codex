"""Tests for Dialogue Works / Nima Alkhorshid opening scaffold normalization."""

from __future__ import annotations

from pathlib import Path

from scripts.normalize_dialogue_works_opening_scaffold import (
    EDITORIAL_MID_NOTE,
    normalize_text,
    trim_book_substack_interrupt,
    trim_close_substack_block,
    trim_mid_substack_before_question,
    trim_transcript_body,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

def _wrap_capture(transcript_body: str, *, solo: bool = False, extra_meta: str = "") -> str:
    guest_line = "guest: Alastair Crooke" if not solo else "guest_people: []"
    form = "source_form: solo" if solo else "source_form: interview"
    return f"""---
ingest_date: 2026-05-13
pub_date: 2026-05-13
kind: transcript
{form}
show: Dialogue Works
host: Nima Alkhorshid
{guest_line}
channel_slug: dialogue-works
title: "Test capture"
source_url: "https://www.youtube.com/watch?v=test"
{extra_meta}---

# Test capture

## Transcript

{transcript_body}
"""

def test_mid_substack_trim_before_question():
    body = (
        "Hi everybody. Today is Wednesday, May 13, 2026 and our dear friend Alistister Krook is here with us. "
        "Welcome back, Alistister. >> Thank you. Always a pleasure, Nemo. Thank you. "
        ">> It's a great pleasure, Alistister, to have you on. And please go right below Alistair's name, "
        "he you can find conflicts forum.substack.com. If you go there and subscribe to this Substack account, "
        "he's going to give you deep analysis. And Alistister, let me start with what's going on right now. "
        "Moments ago, we've learned that Donald Trump has arrived in China."
    )
    new_body, changed = trim_mid_substack_before_question(body)
    assert changed
    assert "substack.com" not in new_body.lower()
    assert "let me start with what's going on right now" in new_body
    assert "Welcome back, Alistister" in new_body

def test_book_interrupt_trim():
    body = (
        "Hi everybody. Today's Friday, June 5th, 2026 and our dear friend Alistister Krook is here with us. "
        "Welcome back, Alistister. >> Thank you very much. "
        ">> And I want to start with what has happened between Israel and Lebanon. Israel announced an attack. "
        "What is the axis of resistance? We know that you wrote a book in 2009. "
        "And the other one is the article on your Substack about Iran takes its chance with war. "
        ">> Uh well there was there has been a significant shift in Israeli thinking."
    )
    new_body, changed = trim_book_substack_interrupt(body)
    assert changed
    assert "axis of resistance" not in new_body
    assert "significant shift in Israeli thinking" in new_body
    assert "I want to start with what has happened between Israel and Lebanon" in new_body

def test_solo_timezone_preamble_unchanged():
    body = (
        "Hi everybody. Today here in Brazil is Monday and because it's 12:15 a.m. "
        "but in the east coast of the United States is 11:15. Then I want to start with what has happened today. "
        "This is today here in Brazil is June 8th, 2026 but still in the east coast is June 7, 2026."
    )
    meta = {"source_form": "solo", "guest": ""}
    new_body, changed, _ = trim_transcript_body(
        body,
        meta,
        allow_mid=True,
        allow_interrupt=True,
        allow_close=True,
        allow_noise=True,
    )
    assert not changed
    assert new_body == body

def test_close_substack_trim():
    paragraphs = [
        "Patrick, that is interesting analysis on the lobby.",
        ">> Thank you so much, Patrick, for being with us today. >> Great pleasure. "
        "Please go uh before wrapping up, please go to 21st Century Wire and Patrick Henningsson.substack.com. "
        "Thank you so much, Patrick. My pleasure. Thanks, Nema.",
    ]
    new_paragraphs, changed = trim_close_substack_block(paragraphs)
    assert changed
    joined = "\n\n".join(new_paragraphs)
    assert "21st Century Wire" not in joined
    assert "interesting analysis on the lobby" in joined

def test_normalize_crooke_fixture_metadata():
    body = (
        "Hi everybody. Today is Wednesday, May 13, 2026 and our dear friend Alistister Krook is here with us. "
        "Welcome back, Alistister. >> Thank you. "
        "And please go right below to conflicts forum.substack.com and subscribe. "
        "And Alistister, let me start with what's going on right now. Moments ago Trump arrived."
    )
    capture = _wrap_capture(body)
    changed, new_text, change = normalize_text(
        REPO_ROOT / "source-archive/statecraft/2026-05-13/source-alkorshid-crooke-test.md",
        capture,
    )
    assert changed
    assert change is not None
    assert change.mid_substack_trimmed
    assert "dialogue_works_substack_trim_applied: true" in new_text
    assert EDITORIAL_MID_NOTE in new_text
    assert change.opening_tier == "host-tease"
