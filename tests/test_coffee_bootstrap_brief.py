"""Tests for first-command coffee bootstrap helpers."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from assess_session_load import _compute_option_weights, _pick_recommendation
from coffee_bootstrap_brief import format_coffee_bootstrap_brief, format_coffee_recent_rhythm


def _write_events(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    return path


def test_recent_rhythm_prefers_coffee_close_and_omits_dates(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** — coffee_close (strategy-codex) ok=true picked=B outcome=partial readiness=execution_ready artifacts=scripts/a.py,tests/test_a.py loops=materialization-stub,next-action next=run-tests
- **2026-05-01 11:00 UTC** — coffee_close (strategy-codex) ok=true picked=C outcome=blocked readiness=blocked artifacts=docs/x.md loops=materialization-stub next=repair-fetch
- **2026-05-01 12:00 UTC** — coffee_close (strategy-codex) ok=true picked=conductor outcome=done readiness=ship_ready conductor=kleiber conductor_state=closed artifacts=commit:abc1234 loops=materialization-stub next=push
""",
    )

    text = format_coffee_recent_rhythm(
        "strategy-codex",
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )

    assert "Recent rhythm:" in text
    assert "readiness ship_ready" in text
    assert "commit:abc1234" in text
    assert "materialization-stub x2" in text
    assert "kleiber is closed" in text
    assert "2026-" not in text
    assert "UTC" not in text


def test_recent_rhythm_falls_back_to_recent_cadence_without_close(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 09:00 UTC** — coffee (strategy-codex) ok=true mode=work-start
- **2026-05-01 10:00 UTC** — dream (strategy-codex) ok=true
""",
    )

    text = format_coffee_recent_rhythm(
        "strategy-codex",
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )

    assert "coffee work-start -> dream pass" in text
    assert "No coffee_close receipt yet" in text


def test_bootstrap_brief_formats_recommendation_without_conductor_hub_line() -> None:
    text = format_coffee_bootstrap_brief(
        {
            "start_state": "load=light; branches=0; memory=ok",
            "recent_rhythm": "Recent rhythm:\n- Last close picked A: done, readiness ship_ready.",
            "artifact_anchors": ["commit:abc1234"],
            "conductor_continuity": {
                "conductor": "kleiber",
                "state": "closed",
                "source": "coffee_close",
            },
            "recommended_hub": "A",
            "recommended_label": "Steward",
            "reason": "last coffee close is ship_ready - Steward can review and ship",
        }
    )

    assert "Coffee Bootstrap Brief" in text
    assert "Recommended hub: A. Steward" in text
    assert "Conductor continuity: kleiber closed" in text
    assert "E. Conductor" not in text


def test_recommendation_uses_coffee_close_readiness() -> None:
    base_weights = _compute_option_weights("light", None, 0)

    rec, reason = _pick_recommendation(
        "light",
        base_weights,
        [],
        {"last_close": {"readiness": "ship_ready", "artifacts": ["commit:abc1234"]}},
    )
    assert (rec, reason) == (
        "A",
        "last coffee close is ship_ready - Steward can review and ship",
    )

    rec, reason = _pick_recommendation(
        "light",
        base_weights,
        [],
        {"last_close": {"readiness": "execution_ready", "artifacts": ["scripts/x.py"]}},
    )
    assert rec == "B"
    assert "code/test artifacts" in reason

    rec, reason = _pick_recommendation(
        "light",
        base_weights,
        [],
        {"last_close": {"readiness": "orientation", "artifacts": ["docs/x.md"]}},
    )
    assert rec == "C"
    assert "orientation-only" in reason

    rec, reason = _pick_recommendation(
        "light",
        base_weights,
        [],
        {"last_close": {"readiness": "blocked", "artifacts": ["scripts/x.py"]}},
    )
    assert rec == "B"
    assert "blocked on code/test artifacts" in reason


def test_operator_coffee_exposes_first_command_mode() -> None:
    src = (REPO_ROOT / "scripts" / "operator_coffee.py").read_text(encoding="utf-8")

    assert '"first-command"' in src
    assert "--first-command" in src
    assert "Coffee Bootstrap Brief" in src
    assert "append_cadence_event(" in src
    assert "mode=args.mode" in src
