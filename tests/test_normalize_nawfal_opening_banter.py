"""Tests for Mario Nawfal opening banter normalization."""

from __future__ import annotations

from pathlib import Path

from scripts.normalize_nawfal_opening_banter import (
    EDITORIAL_TRIM_NOTE,
    normalize_text,
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
    new_body, changed, removed, prefix = trim_transcript_body(body, "Glenn Diesen", False)
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
    new_body, changed, _, _ = trim_transcript_body(body, "Lt. Col. Anthony Aguilar", False)
    assert not changed
    assert new_body == body


def test_macgregor_fixture_unchanged():
    body = (
        "So, cuz Trump is praising the Islamic Republic, saying he wants to meet uh the supreme leader. "
        "At the same time, what seems to what looks like it's happening is that the US is trying to sneak "
        "ships through the Strait of Hormuz."
    )
    new_body, changed, _, _ = trim_transcript_body(body, "Douglas Macgregor", False)
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
