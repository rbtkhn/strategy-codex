"""Tests for Dialogue Works post-land opening normalize hook."""

from __future__ import annotations

from pathlib import Path

from scripts.post_land_dialogue_works_opening_normalize import (
    post_land_dialogue_works_opening_normalize,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = REPO_ROOT / "source-archive" / "statecraft" / "2026-05-13"


def _write_capture(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
show: Dialogue Works
host: Nima Alkhorshid
guest: Test Guest
channel_slug: dialogue-works
---

## Transcript

{body}
""",
        encoding="utf-8",
    )


def test_skip_non_dialogue_works(tmp_path):
    path = tmp_path / "source-archive" / "statecraft" / "2026-05-13" / "source-napolitano-test.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nshow: Judging Freedom\n---\n\n## Transcript\n\nHi everyone.\n", encoding="utf-8")
    result = post_land_dialogue_works_opening_normalize(path)
    assert result.status == "skipped-not-dialogue-works"


def test_apply_mid_trim(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "scripts.post_land_dialogue_works_opening_normalize.ARCHIVE_ROOT",
        tmp_path / "source-archive" / "statecraft",
    )
    path = tmp_path / "source-archive" / "statecraft" / "2026-05-13" / "source-alkorshid-test-guest-2026-05-13.md"
    _write_capture(
        path,
        "Hi everybody. Today is May 13, 2026. Welcome back. "
        "And please go right below to test.substack.com for more. "
        "And let me start with what happened today in the region.",
    )
    result = post_land_dialogue_works_opening_normalize(path)
    assert result.status == "applied"
    assert "mid_substack" in result.flags
    saved = path.read_text(encoding="utf-8")
    assert "substack.com" not in saved.lower()
