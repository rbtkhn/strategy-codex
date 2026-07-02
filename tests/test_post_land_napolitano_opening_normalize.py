"""Tests for Napolitano post-land intake hook."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.post_land_napolitano_opening_normalize import post_land_napolitano_opening_normalize

REPO_ROOT = Path(__file__).resolve().parent.parent

def _write_capture(path: Path, guest: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
ingest_date: 2026-05-29
pub_date: 2026-05-29
kind: transcript
show: Judging Freedom
host: Judge Andrew Napolitano
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

def test_skips_non_napolitano_capture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    archive = tmp_path / "source-archive" / "statecraft" / "2026-05-29"
    path = archive / "source-nawfal-test.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
ingest_date: 2026-05-29
pub_date: 2026-05-29
kind: transcript
show: Mario Nawfal
host: Mario Nawfal
guest: Guest Name
title: "Test capture"
source_url: "https://www.youtube.com/watch?v=test"
---

# Test

## Transcript

Hey man. Iran controls Hormuz.
""",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    import scripts.post_land_napolitano_opening_normalize as hook

    monkeypatch.setattr(hook, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(hook, "ARCHIVE_ROOT", archive.parent)

    result = post_land_napolitano_opening_normalize(path)
    assert result.status == "skipped-not-napolitano"
    assert not result.applied

def test_applies_napolitano_trim_on_land(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    archive = tmp_path / "source-archive" / "statecraft" / "2026-05-29"
    path = archive / "source-napolitano-sachs-test.md"
    _write_capture(
        path,
        "Jeffrey Sachs",
        "Undeclared wars are commonplace. What if Jefferson was right?\n\n"
        "Hi everyone, Judge Andrew Napolitano here for Judging Freedom. Today is Friday. "
        "Professor Jeffrey Sachs will be with us in just a moment. But first, this. "
        "Call my friends at Lear Capital today.\n\n"
        "Professor Sachs, good day to you, my friend. Why is Israel at war?",
    )
    monkeypatch.chdir(tmp_path)
    import scripts.post_land_napolitano_opening_normalize as hook

    monkeypatch.setattr(hook, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(hook, "ARCHIVE_ROOT", archive.parent)

    result = post_land_napolitano_opening_normalize(path)
    assert result.status == "applied"
    assert result.applied
    assert "cold_open" in result.flags or "sponsor" in result.flags
    saved = path.read_text(encoding="utf-8")
    assert "napolitano_cold_open_trim_applied: true" in saved or "napolitano_sponsor_trim_applied: true" in saved
    transcript = saved.split("## Transcript", 1)[1]
    assert "Undeclared wars" not in transcript
    assert "Lear Capital" not in transcript
    assert "Professor Sachs, good day" in transcript

def test_dry_run_does_not_write(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    archive = tmp_path / "source-archive" / "statecraft" / "2026-05-29"
    path = archive / "source-napolitano-sachs-dry-run.md"
    original = (
        "Undeclared wars are commonplace.\n\n"
        "Hi everyone, Judge Andrew Napolitano here for Judging Freedom. Today is Friday. "
        "Professor Jeffrey Sachs, good day to you."
    )
    _write_capture(path, "Jeffrey Sachs", original)
    monkeypatch.chdir(tmp_path)
    import scripts.post_land_napolitano_opening_normalize as hook

    monkeypatch.setattr(hook, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(hook, "ARCHIVE_ROOT", archive.parent)

    result = post_land_napolitano_opening_normalize(path, dry_run=True)
    assert result.status == "dry-run"
    assert not result.applied
    assert "Undeclared wars" in path.read_text(encoding="utf-8")

def test_collect_batch_paths_by_day(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    archive = tmp_path / "source-archive" / "statecraft"
    day = archive / "2026-06-16"
    _write_capture(day / "source-napolitano-a.md", "Guest A", "Hi everyone, Judge Andrew Napolitano here.")
    _write_capture(day / "source-napolitano-b.md", "Guest B", "Hi everyone, Judge Andrew Napolitano here.")
    monkeypatch.chdir(tmp_path)
    import scripts.post_land_napolitano_opening_normalize as hook

    monkeypatch.setattr(hook, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(hook, "ARCHIVE_ROOT", archive)

    paths = hook.collect_batch_paths(day="2026-06-16")
    assert len(paths) == 2
    assert all("source-napolitano-" in p.name for p in paths)

def test_run_batch_streams_summary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    archive = tmp_path / "source-archive" / "statecraft" / "2026-06-16"
    path = archive / "source-napolitano-clean.md"
    _write_capture(
        path,
        "Jeffrey Sachs",
        "Hi everyone, Judge Andrew Napolitano here for Judging Freedom. Today is Friday. "
        "Professor Jeffrey Sachs, good day to you.",
    )
    monkeypatch.chdir(tmp_path)
    import scripts.post_land_napolitano_opening_normalize as hook

    monkeypatch.setattr(hook, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(hook, "ARCHIVE_ROOT", archive.parent)

    _, summary = hook.run_batch([path], dry_run=True, stream=True)
    out = capsys.readouterr().out
    assert "source-napolitano-clean.md" in out
    assert summary.scanned == 1
    assert summary.no_op + summary.would_change == 1
