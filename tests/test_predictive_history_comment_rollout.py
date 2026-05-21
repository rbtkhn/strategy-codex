from __future__ import annotations

from pathlib import Path

from grace_mar.predictive_history_comment_rollout import (
    build_queue_rows,
    render_markdown_summary,
    render_telegram_summary,
)


def test_build_queue_rows_resolves_phase_one_and_phase_two(tmp_path: Path) -> None:
    rows = build_queue_rows(queue_path=tmp_path / "queue.json")

    phase1 = next(row for row in rows if row["source_id"] == "gt-16" and row["phase"] == 1)
    assert phase1["status"] == "ready"
    assert phase1["target_url"].startswith("https://github.com/rbtkhn/ph-civ/tree/main/")
    assert "ChatGPT, Claude, or Grok" in phase1["comment_draft"]
    assert "ph-civ" in phase1["comment_draft"]

    phase2 = next(row for row in rows if row["source_id"] == "gt-16" and row["phase"] == 2)
    assert phase2["status"] == "ready"
    assert phase2["target_url"].endswith("corpus/media-packs/gt-16.md")
    assert "ph-mus exhibit link" in phase2["comment_draft"]
    assert "ChatGPT, Claude, or Grok" in phase2["comment_draft"]


def test_build_queue_rows_parks_missing_phase_two_routes(tmp_path: Path) -> None:
    rows = build_queue_rows(queue_path=tmp_path / "queue.json")

    parked = next(row for row in rows if row["source_id"] == "gt-01" and row["phase"] == 2)
    assert parked["status"] == "parked"
    assert "ph-mus route" in parked["park_reason"]
    assert parked["comment_draft"] == ""


def test_render_summaries(tmp_path: Path) -> None:
    rows = build_queue_rows(queue_path=tmp_path / "queue.json")
    markdown = render_markdown_summary(rows)
    telegram = render_telegram_summary(rows)

    assert "# Predictive History two-phase comment rollout" in markdown
    assert "Phase 1 ready" in markdown
    assert "Phase 2 parked" in markdown
    assert "Predictive History two-phase rollout update" in telegram
    assert "Phase 1 uses the chapter-folder doorway comment" in telegram
