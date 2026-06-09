"""Tests for Judging Freedom / Napolitano opening scaffold normalization."""

from __future__ import annotations

from pathlib import Path

from scripts.normalize_napolitano_opening_scaffold import (
    EDITORIAL_COLD_OPEN_NOTE,
    EDITORIAL_CLOSE_NOTE,
    EDITORIAL_SPONSOR_NOTE,
    normalize_text,
    trim_close_promo_block,
    trim_cold_open_block,
    trim_sponsor_block,
    trim_transcript_body,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def _wrap_capture(guest: str, transcript_body: str, extra_meta: str = "") -> str:
    return f"""---
ingest_date: 2026-05-29
pub_date: 2026-05-29
kind: transcript
show: Judging Freedom
host: Judge Andrew Napolitano
guest: {guest}
title: "Test capture"
source_url: "https://www.youtube.com/watch?v=test"
editorial_note: Operator-pasted transcript body.
{extra_meta}---

# Test capture

## Transcript

{transcript_body}
"""


def test_cold_open_and_sponsor_trim():
    body = (
        "Undeclared wars are commonplace. What if Jefferson was right? "
        "Freedom's greatest hour of danger is now.\n\n"
        "Hi everyone, Judge Andrew Napolitano here for Judging Freedom. Today is Friday, May 30th, 2026. "
        "Professor Jeffrey Sachs will be with us in just a moment. Why is Israel at war, but first this. "
        "Call my friends at Lear Capital to find out. Call 8005114620 or go to leerjudgenap.com today.\n\n"
        "Professor Sachs, good day to you, my friend, and thank you very much for double duty this week. "
        "Before we get to Israel, you recently published an open letter."
    )
    new_body, changed, change = trim_transcript_body(
        body, "Jeffrey Sachs", allow_cold_open=True, allow_sponsor=True, allow_close=False
    )
    assert changed
    assert change.cold_open_trimmed
    assert change.sponsor_trimmed
    assert "Undeclared wars" not in new_body
    assert "Lear Capital" not in new_body
    assert "Professor Sachs, good day" in new_body


def test_already_trimmed_host_tease_unchanged():
    body = (
        "Hi everyone, Judge Andrew Napolitano here for Judging Freedom. Today is Monday, April 20th, 2026. "
        "Professor Jeffrey Sachs will be with us in just a moment. Is the war over?\n\n"
        "Professor Sachs, welcome here, my dear friend. I want to take a break from Iran."
    )
    new_body, changed, _ = trim_transcript_body(
        body, "Jeffrey Sachs", allow_cold_open=True, allow_sponsor=True, allow_close=False
    )
    assert not changed
    assert new_body == body


def test_close_promo_trim():
    paragraphs = [
        "Professor Sachs, thank you very much.",
        "Thank you. Have a nice evening.",
        ">> Thank you. >> Thank you. And coming up later today at 4:00 this afternoon, "
        "Scott Ritter. Judge Napolitano for Judging Freedom. Heat. Heat.",
    ]
    new_paragraphs, changed = trim_close_promo_block(paragraphs)
    assert changed
    joined = "\n\n".join(new_paragraphs)
    assert "coming up later today" not in joined.lower()
    assert not joined.rstrip().endswith("And")
    assert "Have a nice evening" in joined


def test_close_promo_trim_schedule_block():
    paragraphs = [
        "Professor Sachs, thank you very much.",
        "Thank you. Have a nice evening.",
        "Coming up tomorrow, Wednesday at 8 in the morning, Dr. Gilbert Doctorow. "
        "At 3:00 in the afternoon, Phil Giraldi, Judge Napolitano for Judging Freedom. [Music]",
    ]
    new_paragraphs, changed = trim_close_promo_block(paragraphs)
    assert changed
    joined = "\n\n".join(new_paragraphs)
    assert "Coming up tomorrow" not in joined
    assert "Judge Napolitano for Judging Freedom" not in joined
    assert "Have a nice evening" in joined


def test_normalize_text_sets_receipt_fields():
    body = (
        "Undeclared wars are commonplace.\n\n"
        "Hi everyone, Judge Andrew Napolitano here for Judging Freedom. Today is Friday. "
        "Professor Jeffrey Sachs will be with us in just a moment. But first, this. "
        "Call my friends at Lear Capital today.\n\n"
        "Professor Sachs, good day to you, my friend. Why is Israel at war?"
    )
    text = _wrap_capture("Jeffrey Sachs", body)
    path = Path("source-archive/statecraft/2026-05-29/source-napolitano-sachs-test-2026-05-29.md")
    changed, new_text, file_change = normalize_text(path, text)
    assert changed
    assert file_change is not None
    assert file_change.cold_open_trimmed
    assert file_change.sponsor_trimmed
    assert "napolitano_cold_open_trim_applied: true" in new_text
    assert "napolitano_sponsor_trim_applied: true" in new_text
    assert EDITORIAL_COLD_OPEN_NOTE in new_text
    assert EDITORIAL_SPONSOR_NOTE in new_text
    assert "Undeclared wars" not in new_text
    assert "Lear Capital" not in new_text


def test_cold_open_only_before_host_intro():
    body = (
        "Undeclared wars are commonplace. Freedom's greatest hour of danger is now.\n\n"
        "Hi everyone, Judge Andrew Napolitano here for Judging Freedom. Today is Monday."
    )
    trimmed, changed = trim_cold_open_block(body)
    assert changed
    assert trimmed.startswith("Hi everyone")


def test_sponsor_and_guest_in_one_paragraph():
    paragraph = (
        "Hi everyone, Judge Andrew Napolitano here for Judging Freedom. Today is Friday. "
        "Professor Jeffrey Sachs will be with us in just a moment. Why is Israel at war, but first this. "
        "That's why I want to tell you about my Patriot Supply. "
        "So go to preparewiththeadjudge.com right now. "
        ">> Professor Sachs, good day to you, my friend. Before we get to Israel."
    )
    new_paragraphs, changed = trim_sponsor_block([paragraph], "Jeffrey Sachs")
    assert changed
    joined = "\n\n".join(new_paragraphs)
    assert "Patriot Supply" not in joined
    assert "preparewiththeadjudge" not in joined
    assert "Professor Sachs, good day" in joined
    assert "Why is Israel at war" in joined


def test_sponsor_paragraph_removed():
    paragraphs = [
        "Hi everyone, Judge Andrew Napolitano here for Judging Freedom. Today is Tuesday, December 2nd, 2025. "
        "Professor Jeffrey Sachs will be with us in just a minute on what new wars is Donald Trump planning. "
        "But first, this history tells us every market eventually falls.",
        "Call my friends at Lear Capital to find out. Call 8005114620 or go to leerjudgenap.com today.",
        "Professor Sachs, welcome here my dear friend and thank you for accommodating my schedule.",
    ]
    new_paragraphs, changed = trim_sponsor_block(paragraphs, "Jeffrey Sachs")
    assert changed
    joined = "\n\n".join(new_paragraphs)
    assert "Lear Capital" not in joined
    assert "Professor Sachs, welcome" in joined
    assert "what new wars is Donald Trump planning" in joined
