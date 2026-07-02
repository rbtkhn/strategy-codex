from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from scripts.build_work_pass_ledger import (
    build_work_pass_ledger,
    collect_recent_work_pass_closes,
    render_work_pass_ledger_markdown,
)

def test_collect_recent_work_pass_closes_extended_row(tmp_path: Path) -> None:
    events = tmp_path / "cadence.md"
    events.write_text(
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:05 UTC** — coffee_close (strategy-codex) ok=true picked=D outcome=partial readiness=execution_ready object_ref=docs/a.md falsify=stay-narrow verdict=shaped
""",
        encoding="utf-8",
    )
    rows = collect_recent_work_pass_closes(
        "strategy-codex",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 2, 0, 0, tzinfo=timezone.utc),
    )
    assert rows[0]["kind"] == "coffee_close"
    assert rows[0]["object_ref"] == "docs/a.md"
    assert rows[0]["legacy"] is False

def test_render_work_pass_ledger_markdown_title() -> None:
    md = render_work_pass_ledger_markdown(
        {
            "user_id": "strategy-codex",
            "days": 7,
            "generated_at": "2026-06-19T12:00:00+00:00",
            "work_pass_close_count": 1,
            "legacy_outcome_count": 0,
            "audit": {
                "explicit_pick_count": 0,
                "explicit_outcome_count": 0,
                "inferred_outcome_count": 0,
                "explicit_picks_by_conductor": {},
                "explicit_outcomes_by_conductor": {},
                "inferred_outcomes_by_conductor": {},
                "coffee_close_closes_by_conductor": {},
                "open_picks": [],
                "evidence_richness": {"notebook_ref": 0, "falsify": 0},
                "closure": {"open_pick_count": 0, "closure_rate": "n/a"},
            },
            "active_arc": None,
            "recent_closes": [],
            "friction_candidates": [],
        }
    )
    assert md.startswith("# Work-pass ledger")
    assert "coffee_close" in md

def test_build_conductor_shim_reexports_work_pass() -> None:
    from scripts import build_conductor_ledger as shim

    assert shim.build_conductor_ledger is shim.build_work_pass_ledger
    assert shim.collect_recent_conductor_closes is shim.collect_recent_work_pass_closes
