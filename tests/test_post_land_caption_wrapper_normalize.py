"""Tests for caption wrapper post-land hook."""

from __future__ import annotations

from pathlib import Path

from scripts.post_land_caption_wrapper_normalize import post_land_caption_wrapper_normalize

def test_skip_non_transcript(tmp_path):
    path = tmp_path / "source-archive" / "statecraft" / "2026-05-13" / "source-notes-test.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nkind: article\n---\n\n## Notes\n\nSummary only.\n", encoding="utf-8")
    result = post_land_caption_wrapper_normalize(path)
    assert result.status == "skipped-not-transcript"

def test_apply_transcripts_prefix(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "scripts.post_land_caption_wrapper_normalize.ARCHIVE_ROOT",
        tmp_path / "source-archive" / "statecraft",
    )
    path = tmp_path / "source-archive" / "statecraft" / "2026-06-02" / "source-nawfal-test-2026-06-02.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
kind: transcript
show: Mario Nawfal
host: Mario Nawfal
guest: Test Guest
---

## Transcript

Transcripts:
Oh, really? >> Yeah. Well, um, as as you were saying.
""",
        encoding="utf-8",
    )
    result = post_land_caption_wrapper_normalize(path)
    assert result.status == "applied"
    assert "transcripts_prefix" in result.flags
    saved = path.read_text(encoding="utf-8")
    assert "Transcripts:" not in saved
    assert "Oh, really?" in saved
