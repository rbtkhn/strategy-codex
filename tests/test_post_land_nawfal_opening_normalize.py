"""Tests for Nawfal post-land intake hook."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.post_land_nawfal_opening_normalize import post_land_nawfal_opening_normalize

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = REPO_ROOT / "source-archive" / "statecraft" / "2026-05-31"


def _write_capture(path: Path, guest: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
ingest_date: 2026-05-31
pub_date: 2026-05-31
kind: transcript
show: Mario Nawfal
host: Mario Nawfal
guest: {guest}
title: "Test capture"
source_url: "https://www.youtube.com/watch?v=test"
---

# Test

## Transcript

{body}
""",
        encoding="utf-8",
    )


def test_skips_non_nawfal_capture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    archive = tmp_path / "source-archive" / "statecraft" / "2026-05-31"
    path = archive / "source-mercouris-test.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
ingest_date: 2026-05-31
pub_date: 2026-05-31
kind: transcript
show: The Duran
host: Alexander Mercouris
guest: Guest Name
title: "Test capture"
source_url: "https://www.youtube.com/watch?v=test"
---

# Test

## Transcript

So, the situation in Ukraine continues to develop.
""",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    import scripts.post_land_nawfal_opening_normalize as hook

    monkeypatch.setattr(hook, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(hook, "ARCHIVE_ROOT", archive.parent)

    result = post_land_nawfal_opening_normalize(path)
    assert result.status == "skipped-not-nawfal"
    assert not result.applied


def test_applies_nawfal_trim_on_land(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    archive = tmp_path / "source-archive" / "statecraft" / "2026-05-31"
    path = archive / "source-nawfal-diesen-test.md"
    _write_capture(
        path,
        "Glenn Diesen",
        "Hey man. >> Hi. How are you?\n\nWell, the reality that we're dealing with now is Iran controls Hormuz.",
    )
    monkeypatch.chdir(tmp_path)
    import scripts.post_land_nawfal_opening_normalize as hook

    monkeypatch.setattr(hook, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(hook, "ARCHIVE_ROOT", archive.parent)

    result = post_land_nawfal_opening_normalize(path)
    assert result.status == "applied"
    assert result.applied
    assert "intro" in result.flags or "prefix" in result.flags
    saved = path.read_text(encoding="utf-8")
    assert "opening_trim_applied: true" in saved
    assert "Hey man" not in saved.split("## Transcript", 1)[1]


def test_dry_run_does_not_write(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    archive = tmp_path / "source-archive" / "statecraft" / "2026-05-31"
    path = archive / "source-nawfal-diesen-dry-run.md"
    original = (
        "Hey man. >> Hi.\n\nWell, the reality that we're dealing with now is Iran controls Hormuz."
    )
    _write_capture(path, "Glenn Diesen", original)
    monkeypatch.chdir(tmp_path)
    import scripts.post_land_nawfal_opening_normalize as hook

    monkeypatch.setattr(hook, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(hook, "ARCHIVE_ROOT", archive.parent)

    result = post_land_nawfal_opening_normalize(path, dry_run=True)
    assert result.status == "dry-run"
    assert not result.applied
    assert "Hey man" in path.read_text(encoding="utf-8")
