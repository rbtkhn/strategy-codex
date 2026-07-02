"""Unit tests for youtube_transcripts (no network)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from youtube_transcripts.hashing import compute_content_hash, normalize_for_hash, strip_transcript_header
from youtube_transcripts.index_rows import load_index_videos, normalize_upload_date
from youtube_transcripts.quality import compute_quality, tier_from_parts

def test_normalize_for_hash_stable() -> None:
    assert normalize_for_hash("  hello   world  ") == "hello world"

def test_strip_transcript_header() -> None:
    raw = "# line1\n# line2\n\nbody here"
    assert strip_transcript_header(raw) == "body here"

def test_content_hash_stable() -> None:
    h1 = compute_content_hash("abc", "hello", "1.0.0")
    h2 = compute_content_hash("abc", "hello", "1.0.0")
    assert h1 == h2
    assert len(h1) == 64

def test_compute_quality_bounds() -> None:
    q = compute_quality("x" * 500, 120.0, "tier1_api", 100.0)
    assert 0.0 <= q <= 1.0

def test_tier_from_parts() -> None:
    assert tier_from_parts("ytdlp", "manual") == "tier2_manual"
    assert tier_from_parts("ytdlp", "auto") == "tier2_auto"

def test_discovery_extract_video_id() -> None:
    from youtube_transcripts.discovery import extract_video_id

    assert extract_video_id("dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

def test_retry_call_succeeds_first_try() -> None:
    from youtube_transcripts.retry import retry_call

    n = {"c": 0}

    def ok() -> int:
        n["c"] += 1
        return 42

    assert retry_call(ok, max_attempts=3) == 42
    assert n["c"] == 1

def test_normalize_upload_date_variants() -> None:
    assert normalize_upload_date("20260503") == "2026-05-03"
    assert normalize_upload_date("2026-05-03") == "2026-05-03"
    assert normalize_upload_date("2026-05-03T12:34:56Z") == "2026-05-03"
    assert normalize_upload_date("") is None

def test_load_index_videos_normalizes_rows(tmp_path: Path) -> None:
    index_path = tmp_path / "index.json"
    index_path.write_text(
        """
{
  "videos": [
    {
      "video_id": "abc123",
      "title": "Example title",
      "upload_date": "20260503",
      "url": "https://www.youtube.com/watch?v=abc123",
      "status": "listed_only",
      "duration_seconds": "321"
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )
    videos = load_index_videos(index_path)
    assert len(videos) == 1
    assert videos[0]["video_id"] == "abc123"
    assert videos[0]["upload_date"] == "2026-05-03"
    assert videos[0]["status"] == "listed_only"
    assert videos[0]["duration_seconds"] == "321"
