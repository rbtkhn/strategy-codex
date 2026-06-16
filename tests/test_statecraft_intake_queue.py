"""Tests for scripts/statecraft_intake_queue.py."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def queue_mod():
    path = REPO_ROOT / "scripts" / "statecraft_intake_queue.py"
    spec = importlib.util.spec_from_file_location("statecraft_intake_queue", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _write_archive(path: Path, *, source_form: str = "interview") -> None:
    path.write_text(
        "\n".join(
            [
                "---",
                f"pub_date: '{path.stem[-10:]}'",
                f"kind: transcript",
                f"source_form: {source_form}",
                "thread: marandi",
                "threads:",
                "  - marandi",
                "host_people:",
                "  - Glenn Diesen",
                "guest_people:",
                "  - Seyed M. Marandi",
                "source_url: https://example.com/watch",
                "---",
                "# Body",
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_new_status_without_daily_or_sidecar(queue_mod, tmp_path: Path, monkeypatch):
    day = "2026-06-20"
    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    source = day_dir / f"source-alpha-test-{day}.md"
    _write_archive(source)

    daily_dir = tmp_path / "statecraft" / "daily"
    daily_dir.mkdir(parents=True)
    (daily_dir / f"{day}.md").write_text("Archive checkpoint: **0**\n", encoding="utf-8")

    queue_root = tmp_path / "artifacts" / "statecraft-intake-queue"
    monkeypatch.setattr(queue_mod, "QUEUE_ROOT", queue_root)

    rows, _ = queue_mod.build_queue_report(
        day, root=archive_root, daily_dir=daily_dir, allow_desync=True
    )
    assert len(rows) == 1
    assert rows[0].synthesis_status == "new"
    assert rows[0].in_daily is False


def test_daily_status_when_linked(queue_mod, tmp_path: Path, monkeypatch):
    day = "2026-06-21"
    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    slug = f"source-beta-test-{day}.md"
    _write_archive(day_dir / slug)

    daily_dir = tmp_path / "statecraft" / "daily"
    daily_dir.mkdir(parents=True)
    daily_path = daily_dir / f"{day}.md"
    daily_path.write_text(
        "\n".join(
            [
                "Archive checkpoint: **1** source-bearing captures.",
                f"- [Beta](../../source-archive/statecraft/{day}/{slug})",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(queue_mod, "QUEUE_ROOT", tmp_path / "artifacts" / "statecraft-intake-queue")

    rows, _ = queue_mod.build_queue_report(
        day, root=archive_root, daily_dir=daily_dir, allow_desync=True
    )
    assert rows[0].synthesis_status == "daily"
    assert rows[0].in_daily is True


def test_emit_sidecars_writes_valid_json(queue_mod, tmp_path: Path, monkeypatch):
    day = "2026-06-22"
    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    slug = f"source-gamma-test-{day}.md"
    _write_archive(day_dir / slug)

    queue_root = tmp_path / "artifacts" / "statecraft-intake-queue"
    monkeypatch.setattr(queue_mod, "QUEUE_ROOT", queue_root)

    row = queue_mod.SourceQueueRow(
        source_stem=slug[:-3],
        source_path=f"source-archive/statecraft/{day}/{slug}",
        synthesis_status="new",
        threads=("marandi",),
        actors=("Glenn Diesen", "Seyed M. Marandi"),
        source_url="https://example.com/watch",
        reasoning="source_form=interview",
        heuristic_score=4,
        sidecar_path=None,
        in_daily=False,
    )
    written = queue_mod.emit_sidecars(day, [row])
    assert len(written) == 1
    sidecar = json.loads((queue_root / day / f"{slug[:-3]}.v1.json").read_text(encoding="utf-8"))
    assert sidecar["schema_version"] == "statecraft-intake-sidecar.v1"
    assert sidecar["synthesis_status"] == "queued"
    assert sidecar["non_canonical"] is True


def test_write_digest_lists_new_sources(queue_mod):
    day = "2026-06-23"
    rows = [
        queue_mod.SourceQueueRow(
            source_stem=f"source-delta-test-{day}",
            source_path=f"source-archive/statecraft/{day}/source-delta-test-{day}.md",
            synthesis_status="new",
            threads=("diesen",),
            actors=("Glenn Diesen",),
            source_url=None,
            reasoning="source_form=solo",
            heuristic_score=1,
            sidecar_path=None,
            in_daily=False,
        )
    ]
    digest = queue_mod.format_digest(day, rows, top_n=5)
    assert "Statecraft Intake Digest" in digest
    assert "source-delta-test" in digest
    assert "## Hold / watch" in digest


def test_emit_sidecars_does_not_modify_archive(queue_mod, tmp_path: Path, monkeypatch):
    day = "2026-06-24"
    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    source = day_dir / f"source-epsilon-test-{day}.md"
    original = "---\nkind: transcript\n---\n# Body\n"
    source.write_text(original, encoding="utf-8")

    monkeypatch.setattr(queue_mod, "QUEUE_ROOT", tmp_path / "artifacts" / "statecraft-intake-queue")
    row = queue_mod.SourceQueueRow(
        source_stem=source.stem,
        source_path=str(source),
        synthesis_status="new",
        threads=(),
        actors=(),
        source_url=None,
        reasoning="v0",
        heuristic_score=0,
        sidecar_path=None,
        in_daily=False,
    )
    queue_mod.emit_sidecars(day, [row])
    assert source.read_text(encoding="utf-8") == original
