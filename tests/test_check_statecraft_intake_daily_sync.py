"""Tests for scripts/check_statecraft_intake_daily_sync.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

@pytest.fixture()
def sync_mod():
    path = REPO_ROOT / "scripts" / "check_statecraft_intake_daily_sync.py"
    spec = importlib.util.spec_from_file_location("check_statecraft_intake_daily_sync", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod

def test_parse_daily_checkpoint_and_slugs(sync_mod):
    text = """
Archive checkpoint: **14** source-bearing captures.
- [Sachs](../../source-archive/statecraft/2026-06-08/source-judging-freedom-sachs-is-trump-losing-it-2026-06-08.md)
- [Crooke](../../source-archive/statecraft/2026-06-08/source-judging-freedom-crooke-ceasefire-for-all-or-ceasefire-for-no-one-2026-06-08.md)
"""
    assert sync_mod._parse_daily_checkpoint(text) == 14
    slugs = sync_mod._parse_daily_source_slugs(text, "2026-06-08")
    assert "source-judging-freedom-sachs-is-trump-losing-it-2026-06-08.md" in slugs
    assert len(slugs) == 2

def test_desync_when_daily_missing_archive_slug(sync_mod, tmp_path: Path):
    day = "2026-06-08"
    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    (day_dir / "source-alpha-test-2026-06-08.md").write_text("---\nkind: transcript\n---\n", encoding="utf-8")
    (day_dir / "source-beta-test-2026-06-08.md").write_text("---\nkind: transcript\n---\n", encoding="utf-8")

    daily_dir = tmp_path / "statecraft" / "daily"
    daily_dir.mkdir(parents=True)
    daily_path = daily_dir / f"{day}.md"
    daily_path.write_text(
        "\n".join(
            [
                "Archive checkpoint: **2** source-bearing captures.",
                f"- [Alpha](../../source-archive/statecraft/{day}/source-alpha-test-2026-06-08.md)",
            ]
        ),
        encoding="utf-8",
    )

    report = sync_mod.build_sync_report(day, root=archive_root, daily_dir=daily_dir)
    assert report.status == "desync"
    assert report.archive_count == 2
    assert report.daily_checkpoint_count == 2
    assert report.archive_only == ("source-beta-test-2026-06-08.md",)
    assert report.exit_code == 1

def test_ok_when_lists_align(sync_mod, tmp_path: Path):
    day = "2026-06-08"
    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    slug = "source-alpha-test-2026-06-08.md"
    (day_dir / slug).write_text("---\nkind: transcript\n---\n", encoding="utf-8")

    daily_dir = tmp_path / "statecraft" / "daily"
    daily_dir.mkdir(parents=True)
    (daily_dir / f"{day}.md").write_text(
        "\n".join(
            [
                "Archive checkpoint: **1** source-bearing captures.",
                f"- [Alpha](../../source-archive/statecraft/{day}/{slug})",
            ]
        ),
        encoding="utf-8",
    )

    report = sync_mod.build_sync_report(day, root=archive_root, daily_dir=daily_dir)
    assert report.status == "ok"
    assert report.exit_code == 0

def test_no_daily_is_ok(sync_mod, tmp_path: Path):
    day = "2026-06-09"
    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    (day_dir / "source-only-2026-06-09.md").write_text("---\nkind: transcript\n---\n", encoding="utf-8")

    daily_dir = tmp_path / "statecraft" / "daily"
    daily_dir.mkdir(parents=True)

    report = sync_mod.build_sync_report(day, root=archive_root, daily_dir=daily_dir)
    assert report.status == "no_daily"
    assert report.exit_code == 0

def test_live_june_08_ok_after_sachs_wire_in(sync_mod):
    report = sync_mod.build_sync_report("2026-06-08")
    assert report.status == "ok", sync_mod.format_human(report)
    assert "DESYNC" not in sync_mod.format_human(report).upper()

def test_resolve_latest_captured_day_picks_newest_with_sources(sync_mod, tmp_path: Path):
    archive_root = tmp_path / "source-archive" / "statecraft"
    for day in ("2026-06-07", "2026-06-08"):
        day_dir = archive_root / day
        day_dir.mkdir(parents=True)
        (day_dir / f"source-sample-{day}.md").write_text("---\nkind: transcript\n---\n", encoding="utf-8")
    empty_dir = archive_root / "2026-06-09"
    empty_dir.mkdir(parents=True)
    (empty_dir / "README.md").write_text("# empty\n", encoding="utf-8")

    assert sync_mod.resolve_latest_captured_day(root=archive_root) == "2026-06-08"

def test_resolve_latest_captured_day_none_when_empty(sync_mod, tmp_path: Path):
    archive_root = tmp_path / "source-archive" / "statecraft"
    archive_root.mkdir(parents=True)
    assert sync_mod.resolve_latest_captured_day(root=archive_root) is None

def test_batch_audit_mixed_ok_and_desync(sync_mod, tmp_path: Path):
    archive_root = tmp_path / "source-archive" / "statecraft"
    daily_dir = tmp_path / "statecraft" / "daily"
    daily_dir.mkdir(parents=True)

    for day, slug in (("2026-06-07", "source-a-2026-06-07.md"), ("2026-06-08", "source-b-2026-06-08.md")):
        day_dir = archive_root / day
        day_dir.mkdir(parents=True)
        (day_dir / slug).write_text("---\nkind: transcript\n---\n", encoding="utf-8")

    (daily_dir / "2026-06-07.md").write_text(
        "Archive checkpoint: **1**\n"
        "- [A](../../source-archive/statecraft/2026-06-07/source-a-2026-06-07.md)\n",
        encoding="utf-8",
    )
    (daily_dir / "2026-06-08.md").write_text(
        "Archive checkpoint: **1**\n",
        encoding="utf-8",
    )

    reports = sync_mod.build_batch_reports(root=archive_root, daily_dir=daily_dir)
    assert len(reports) == 2
    assert reports[0].status == "ok"
    assert reports[1].status == "desync"
    assert sync_mod.batch_exit_code(reports) == 1
    human = sync_mod.format_batch_human(reports)
    assert "desync: 1" in human
    assert "2026-06-08" in human
