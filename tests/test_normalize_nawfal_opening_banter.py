"""Tests for Mario Nawfal opening banter normalization."""

from __future__ import annotations

from pathlib import Path

from scripts.normalize_nawfal_opening_banter import (
    EDITORIAL_DROPOUT_TRIM_NOTE,
    EDITORIAL_ORPHAN_TRIM_NOTE,
    EDITORIAL_PRODUCTION_TRIM_NOTE,
    EDITORIAL_TRIM_NOTE,
    normalize_text,
    trim_guest_dropout_block,
    trim_orphan_opening_fragment,
    trim_production_audio_block,
    trim_transcript_body,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def _wrap_capture(guest: str, transcript_body: str) -> str:
    return f"""---
ingest_date: 2026-05-31
pub_date: 2026-05-31
kind: transcript
show: Mario Nawfal
host: Mario Nawfal
guest: {guest}
title: "Test capture"
source_url: "https://www.youtube.com/watch?v=test"
editorial_note: Light cleanup only.
---

# Test capture

## Transcript

{transcript_body}
"""


def test_diesen_fixture_trims_schedule_banter():
    body = (
        "Hey man. >> Hi. How are you? >> Good. Glenn, you? >> Yeah. I can't complain. >> Long time.\n\n"
        ">> welcome back to reality. Well, the reality that we're dealing with now is um [sighs] "
        "there's a few things happening. Even though people think it's been all quiet.\n\n"
        ">> Yeah. No. Well, that's an interesting development because when they went into this ceasefire."
    )
    new_body, changed, removed, prefix, _, _, _ = trim_transcript_body(body, "Glenn Diesen", False)
    assert changed
    assert removed >= 1 or prefix
    assert "two weeks" not in new_body.lower()
    assert "welcome back to reality" not in new_body.lower()
    assert "interesting development" in new_body


def test_aguilar_fixture_unchanged():
    body = (
        "Hey, Colonel. Hello, Mario. How are you? >> Good. Um, so the obviously you're up to speed "
        "with what happened. Iran threatened Israel not to strike Beirut."
    )
    new_body, changed, _, _, _, _, _ = trim_transcript_body(body, "Lt. Col. Anthony Aguilar", False)
    assert not changed
    assert new_body == body


def test_aguilar_orphan_fragment_trim():
    body = (
        ">> Um, I I heard the last thing, but I also >> I'll read it out quick. "
        "It's a quick one. I'll read it very quickly. US Navy Central Command has warned mariners and airmen "
        "that Sentcom will be conducting military operations in the straight of Hamuz. "
        ">> Yes, this is an outcome."
    )
    new_paragraphs, changed = trim_orphan_opening_fragment([body])
    assert changed
    joined = "\n\n".join(new_paragraphs)
    assert "heard the last thing" not in joined.lower()
    assert "US Navy Central Command" in joined
    assert ">> Yes, this is an outcome" in joined


def test_orphan_second_pass_on_trimmed_file():
    text = _wrap_capture(
        "Lt. Col. Anthony Aguilar",
        ">> Um, I I heard the last thing, but I also >> I'll read it out quick. "
        "It's a quick one. I'll read it very quickly. US Navy Central Command has warned mariners. "
        ">> Yes, this is an outcome.",
    )
    path = Path(
        "source-archive/statecraft/2026-05-29/source-nawfal-anthony-aguilar-breaking-trump-orders-military-action-2026-05-29.md"
    )
    base = text.replace(
        "editorial_note: Light cleanup only.",
        "editorial_note: Light cleanup only.\nopening_trim_applied: true\nopening_tier: heavy-banter",
    )
    changed, new_text, file_change = normalize_text(path, base, include_side_quests=False)
    assert changed
    assert file_change is not None
    assert file_change.orphan_trimmed
    assert "orphan_trim_applied: true" in new_text
    assert EDITORIAL_ORPHAN_TRIM_NOTE in new_text
    assert "heard the last thing" not in new_text.split("## Transcript", 1)[1].lower()


def test_johnson_guest_dropout_trim():
    body = (
        "ISRAEL ASKS TRUMP TO ESCALATE - YouTube\n\nTranscripts:\n"
        "through the National Defense Authorization Act to integrate the American and Israeli military. "
        "Charlie Kirk and TPUSA. I think uh Lisa Larry's internet just cut out or the video just cut out "
        "if you could quickly check it in the studio and then while waiting for Larry to join "
        "before we go through the news recap I'll jump into the news recap now with\n"
        "Larry. Did you hear the part I talked about TPUSA? >> Yeah. So, the Charlie Kirk there's "
        "circumstantial evidence."
    )
    new_paragraphs, changed = trim_guest_dropout_block([body], "Larry Johnson")
    assert changed
    joined = "\n\n".join(new_paragraphs)
    assert "lisa" not in joined.lower()
    assert "internet just cut out" not in joined.lower()
    assert "Larry. Did you hear" in joined
    assert "circumstantial archive/placeholders/evidence" in joined


def test_kent_opening_no_guest_dropout_trim():
    body = (
        "So, I want to bring this up first before we go into what's happening in Iran. "
        "Lisa, if you can show that tweet again. Um, you may be wondering two things."
    )
    new_paragraphs, changed = trim_guest_dropout_block([body], "Joe Kent")
    assert not changed


def test_barnes_production_block_trim():
    body = (
        ">> Yeah, glad to be here. >> So, um, one thing along the, uh, by the way, Lisa, Robert's volume is a bit low. "
        "Just a heads up.\n\n"
        ">> I think so. I'll have the producer because I can't hear myself. Um, just to make sure it's at the same level.\n\n"
        "Uh, good to have you, man. Yeah. So, a lot of people are talking on whether we're going to have a deal or not. "
        "Politically, is a resumption of war even possible?"
    )
    new_paragraphs, changed = trim_production_audio_block(body.split("\n\n"))
    assert changed
    joined = "\n\n".join(new_paragraphs)
    assert "lisa" not in joined.lower()
    assert "producer" not in joined.lower()
    assert "a lot of people are talking" in joined.lower()
    assert "resumption of war" in joined.lower()


def test_aguilar_opening_keeps_lisa_when_substantive_first():
    body = (
        "Uh, Colonel, how are you? >> I'm doing well. How are you, Mario? >> Good. Um, I'm hoping you can help me make sense of this. "
        "Did you see the announcement that came in from US Navy Central Command? Just came in. I'm going to get the a uh Lisa to fix your audio."
    )
    new_paragraphs, changed = trim_production_audio_block([body])
    assert not changed


def test_production_second_pass_on_trimmed_file():
    text = _wrap_capture(
        "Robert Barnes",
        ">> Yeah, glad to be here. >> So, um, by the way, Lisa, Robert's volume is a bit low.\n\n"
        "Uh, good to have you, man. Yeah. So, a lot of people are talking on whether we're going to have a deal or not. "
        ">> Not in Trump's mind, no.",
    )
    path = Path(
        "source-archive/statecraft/2026-05-31/source-nawfal-barnes-breaking-u-s-to-merge-military-with-israel-2026-05-31.md"
    )
    base = text.replace(
        "editorial_note: Light cleanup only.",
        "editorial_note: Light cleanup only.\nopening_trim_applied: true\nopening_tier: heavy-banter",
    )
    changed, new_text, file_change = normalize_text(path, base, include_side_quests=False)
    assert changed
    assert file_change is not None
    assert file_change.production_trimmed
    assert "production_trim_applied: true" in new_text
    assert EDITORIAL_PRODUCTION_TRIM_NOTE in new_text
    assert "lisa" not in new_text.split("## Transcript", 1)[1].lower()


def test_macgregor_fixture_unchanged():
    body = (
        "So, cuz Trump is praising the Islamic Republic, saying he wants to meet uh the supreme leader. "
        "At the same time, what seems to what looks like it's happening is that the US is trying to sneak "
        "ships through the Strait of Hormuz."
    )
    new_body, changed, _, _, _, _, _ = trim_transcript_body(body, "Douglas Macgregor", False)
    assert not changed
    assert "Strait of Hormuz" in new_body


def test_normalize_text_updates_metadata_on_apply_shape():
    text = _wrap_capture(
        "Glenn Diesen",
        "Hey man. >> Hi. How are you?\n\nWell, the reality that we're dealing with now is Iran controls Hormuz.",
    )
    path = Path("source-archive/statecraft/2026-05-31/source-nawfal-diesen-test.md")
    changed, new_text, file_change = normalize_text(path, text, include_side_quests=False)
    assert changed
    assert file_change is not None
    assert file_change.intro_removed
    assert file_change.opening_tier in {"heavy-banter", "host-monologue", "clean"}
    assert "opening_tier:" in new_text
    assert "opening_trim_applied: true" in new_text
    assert EDITORIAL_TRIM_NOTE in new_text
    assert "Hey man" not in new_text.split("## Transcript", 1)[1]


def test_reapply_on_trimmed_file_is_noop():
    text = _wrap_capture(
        "Glenn Diesen",
        "Hey man. >> Hi. How are you?\n\nWell, the reality that we're dealing with now is Iran controls Hormuz.",
    )
    path = Path("source-archive/statecraft/2026-05-31/source-nawfal-diesen-test.md")
    _, trimmed_text, first_change = normalize_text(path, text, include_side_quests=False)
    assert first_change is not None
    assert first_change.intro_removed

    changed, new_text, second_change = normalize_text(
        path, trimmed_text, include_side_quests=False
    )
    assert not changed
    assert second_change is not None
    assert second_change.opening_tier == "heavy-banter"
    assert "opening_trim_applied: true" in new_text
    assert "opening_tier: heavy-banter" in new_text


def test_tag_only_sets_opening_tier_without_trim():
    text = _wrap_capture(
        "Douglas Macgregor",
        "So, cuz Trump is praising the Islamic Republic. Iran controls the Strait of Hormuz.",
    )
    path = Path("source-archive/statecraft/2026-06-06/source-nawfal-macgregor-test.md")
    changed, new_text, file_change = normalize_text(
        path, text, include_side_quests=False, tag_only=True
    )
    assert changed
    assert file_change is not None
    assert not file_change.intro_removed
    assert "opening_tier:" in new_text
    assert "Strait of Hormuz" in new_text
