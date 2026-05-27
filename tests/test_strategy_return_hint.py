"""Tests for the read-only explicit Strategy return hint."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import strategy_return_hint as srh  # noqa: E402


def test_live_accumulator_text_prefers_append_marker() -> None:
    text = """# Daily strategy inbox

Header policy with stale examples.

_(Append below this line during the day.)_

- live line
"""
    assert srh.live_accumulator_text(text) == "- live line"


def test_build_strategy_return_hint_buckets_and_recommendation(tmp_path: Path) -> None:
    repo = tmp_path
    inbox = repo / "codex" / "daily-strategy-inbox.md"
    raw_root = repo / "codex" / "years" / "2026" / "raw-input"
    status = repo / "codex" / "STATUS.md"
    days = repo / "codex" / "years" / "2026" / "chapters" / "2026-04" / "days.md"
    inbox.parent.mkdir(parents=True)
    raw_root.mkdir(parents=True)
    status.parent.mkdir(parents=True, exist_ok=True)
    days.parent.mkdir(parents=True)

    inbox.write_text(
        """# Inbox

_(Append below this line during the day.)_

- batch-analysis | theme | tension-first cluster
- X | cold: claim | https://example.substack.com/p/unmatched | verify:pending-primary
- open loop: revisit Hormuz falsifier
""",
        encoding="utf-8",
    )
    status.write_text("| **Active chapter** | `2026-04` |\n", encoding="utf-8")
    days.write_text("# days\n", encoding="utf-8")

    hint = srh.build_strategy_return_hint(repo, inbox_path=inbox, raw_root=raw_root, status_path=status)

    assert hint.ready == 1
    assert hint.verify == 1
    assert hint.carry == 1
    assert hint.raw_input_gap == 1
    assert hint.active_chapter == "2026-04"
    assert hint.active_days_path == "codex/years/2026/chapters/2026-04/days.md"
    assert hint.suggested_move.startswith("source hygiene first")
    assert hint.raw_input_gap_urls == ("https://example.substack.com/p/unmatched",)


def test_raw_input_gap_matches_source_url_slug(tmp_path: Path) -> None:
    raw_root = tmp_path / "raw"
    raw_file = raw_root / "2026-05-09" / "source.md"
    raw_file.parent.mkdir(parents=True)
    raw_file.write_text(
        """---
source_url: https://example.substack.com/p/robot-labor-shock
---
body
""",
        encoding="utf-8",
    )
    live = "- source | https://example.substack.com/p/robot-labor-shock?utm_source=test"

    assert srh.raw_input_gap_count(live, raw_root) == 0


def test_accumulator_drift_days_tracks_behind_and_future() -> None:
    assert srh.accumulator_drift_days(None) is None
    assert srh.accumulator_drift_days("2026-05-09", today=srh.date(2026, 5, 9)) == 0
    assert srh.accumulator_drift_days("2026-05-08", today=srh.date(2026, 5, 9)) == 1
    assert srh.accumulator_drift_days("2026-05-10", today=srh.date(2026, 5, 9)) == -1


def test_raw_input_gap_ignores_tbd_and_nearby_raw_pointer(tmp_path: Path) -> None:
    live = "\n".join(
        [
            "- YT | cold: placeholder | https://www.youtube.com/watch?v=TBD-davis-hormuz",
            "- YT | cold: pointed | [provenance/2026-04-29/source.md](provenance/2026-04-29/source.md) | https://www.youtube.com/watch?v=abc123",
        ]
    )

    assert srh.raw_input_gap_count(live, tmp_path / "missing-raw") == 0


def test_suggested_move_priority() -> None:
    assert srh.suggested_c_move(raw_input_gap=1, verify=9, ready=9).startswith("source hygiene")
    assert srh.suggested_c_move(raw_input_gap=0, verify=1, ready=9).startswith("verify seam")
    assert srh.suggested_c_move(raw_input_gap=0, verify=0, ready=1).startswith("compose-read")
    assert srh.suggested_c_move(raw_input_gap=0, verify=0, ready=0).startswith("light daily-brief")
