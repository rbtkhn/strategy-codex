from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from scripts.build_conductor_ledger import (
    build_conductor_ledger,
    collect_friction_candidates,
    collect_recent_conductor_closes,
    render_conductor_ledger_markdown,
)


def test_collect_recent_conductor_closes_includes_outcomes_and_closed_coffee_closes(
    tmp_path: Path,
) -> None:
    events = tmp_path / "cadence.md"
    events.write_text(
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** — coffee_pick (strategy-codex) ok=true picked=conductor conductor=kleiber
- **2026-05-01 10:05 UTC** — coffee_conductor_outcome (strategy-codex) ok=true verdict=watch conductor=kleiber notebook_ref=docs/a.md falsify=stay-narrow
- **2026-05-01 11:00 UTC** — coffee_pick (strategy-codex) ok=true picked=conductor conductor=karajan
- **2026-05-01 11:10 UTC** — coffee_close (strategy-codex) ok=true picked=conductor outcome=done readiness=ship_ready conductor=karajan conductor_state=closed artifacts=commit:abc1234 loops=arc next=push
""",
        encoding="utf-8",
    )
    rows = collect_recent_conductor_closes(
        "strategy-codex",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 2, 0, 0, tzinfo=timezone.utc),
    )
    assert rows[0]["kind"] == "coffee_conductor_outcome"
    assert rows[1]["kind"] == "coffee_close"
    assert rows[1]["conductor"] == "karajan"


def test_collect_friction_candidates_skips_template_placeholders(tmp_path: Path) -> None:
    notebook = tmp_path / "journal"
    notebook.mkdir()
    (notebook / "day.md").write_text(
        """### Conductor close
- **Friction / rule candidate (optional):** Conductor worked once options named concrete batch outcomes.
""",
        encoding="utf-8",
    )
    (notebook / "template.md").write_text(
        """- **Friction / rule candidate (optional):** <what failed; home = skill-write | conductor | strategy-template | none; future check = would this rule have prevented today's drag?>
""",
        encoding="utf-8",
    )
    rows = collect_friction_candidates(search_roots=(notebook,), max_items=4)
    assert len(rows) == 1
    assert rows[0]["path"].endswith("journal/day.md")


def test_build_and_render_conductor_ledger_reports_active_arc_and_shortcut(
    tmp_path: Path,
) -> None:
    events = tmp_path / "cadence.md"
    events.write_text(
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** — coffee_pick (strategy-codex) ok=true picked=conductor conductor=karajan focus=month-arc
- **2026-05-01 10:05 UTC** — coffee_conductor_outcome (strategy-codex) ok=true verdict=watch conductor=karajan notebook_ref=docs/a.md falsify=stay-narrow
- **2026-05-02 10:00 UTC** — coffee_pick (strategy-codex) ok=true picked=conductor conductor=karajan
- **2026-05-02 10:05 UTC** — coffee_conductor_outcome (strategy-codex) ok=true verdict=hold conductor=karajan notebook_ref=docs/b.md falsify=keep-shape
""",
        encoding="utf-8",
    )
    payload = build_conductor_ledger(
        "strategy-codex",
        days=7,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
        events_path=events,
        max_friction=0,
    )
    assert payload["active_arc"] is not None
    assert payload["active_arc"]["conductor"] == "karajan"
    assert payload["compiled_shortcut_offer"] == "karajan-review"

    markdown = render_conductor_ledger_markdown(payload)
    assert "# Conductor Ledger" in markdown
    assert "Compiled shortcut offer: `karajan-review`" in markdown
    assert "Outcome lines with `falsify=`: `2`" in markdown
