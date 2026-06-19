from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from cadence_learning import (  # noqa: E402
    build_pattern_watch,
    load_learning_events,
    log_coffee_choice_start,
    log_coffee_resolution_from_close,
    log_dream_stage,
)


def test_dream_stage_and_coffee_resolution_round_trip(tmp_path: Path) -> None:
    ledger = tmp_path / "cadence-learning-events.jsonl"
    handoff = {
        "generated_at": "2026-06-02T06:00:00Z",
        "learning_action_recommendation": "confirm",
        "learning_action_reason": "recent outcome receipts point toward follow-through",
        "carry_forward_object": "stage-commit-bootstrap-drift-fix",
        "carry_forward_test": "Is the prior judgment still live enough to follow through cleanly?",
        "confidence_class": "medium",
        "bias_strength": "soft",
        "tomorrow_inherits": "Tomorrow inherits (hint): **Confirm** ...",
    }
    log_dream_stage("strategy-codex", handoff=handoff, ledger_path=ledger)
    log_coffee_choice_start(
        "strategy-codex",
        coffee_id="2026-06-02T08:00:00Z",
        load_result={
            "recommended_action": "confirm",
            "recommendation_reason": "validated follow-through pressure",
            "recommendation_source": "assess_session_load",
            "downstream_hint": "Confirm - last close is ship_ready and still lines up with current work",
        },
        ledger_path=ledger,
    )
    log_coffee_resolution_from_close(
        "strategy-codex",
        picked="A",
        outcome="done",
        readiness="ship_ready",
        artifacts=["scripts/example.py"],
        loops=[],
        next_slug="stage-commit",
        ledger_path=ledger,
    )

    events = load_learning_events("strategy-codex", ledger_path=ledger)
    assert [row["event_type"] for row in events] == ["dream_stage", "coffee_choice", "coffee_resolution"]
    resolution = events[-1]
    assert resolution["actual_learning_action"] == "confirm"
    assert resolution["dream_match_class"] == "confirmed"
    assert resolution["hindsight_class"] == "validated"


def test_coffee_resolution_carries_extended_close_fields(tmp_path: Path) -> None:
    ledger = tmp_path / "cadence-learning-events.jsonl"
    log_dream_stage(
        "strategy-codex",
        handoff={"generated_at": "2026-06-02T06:00:00Z", "learning_action_recommendation": "reframe"},
        ledger_path=ledger,
    )
    log_coffee_choice_start(
        "strategy-codex",
        coffee_id="2026-06-02T08:00:00Z",
        load_result={
            "recommended_action": "reframe",
            "recommendation_reason": "narrow object",
            "recommendation_source": "assess_session_load",
            "downstream_hint": "",
        },
        ledger_path=ledger,
    )
    log_coffee_resolution_from_close(
        "strategy-codex",
        picked="D",
        outcome="partial",
        readiness="execution_ready",
        object_ref="statecraft/daily/2026-06-17.md",
        falsify="pseudo-gate-J16",
        verdict="shaped",
        attention="one object only",
        ledger_path=ledger,
    )
    resolution = load_learning_events("strategy-codex", ledger_path=ledger)[-1]
    assert resolution["object_ref"] == "statecraft/daily/2026-06-17.md"
    assert resolution["falsify"] == "pseudo-gate-J16"
    assert resolution["verdict"] == "shaped"
    assert resolution["attention"] == "one object only"


def test_pattern_watch_detects_repeated_premature_confirm(tmp_path: Path) -> None:
    ledger = tmp_path / "cadence-learning-events.jsonl"
    for idx in range(2):
        log_dream_stage(
            "strategy-codex",
            handoff={
                "generated_at": f"2026-06-02T0{idx}:00:00Z",
                "learning_action_recommendation": "confirm",
            },
            ledger_path=ledger,
        )
        log_coffee_choice_start(
            "strategy-codex",
            coffee_id=f"2026-06-02T1{idx}:00:00Z",
            load_result={"recommended_action": "confirm", "recommendation_reason": "x", "recommendation_source": "assess", "downstream_hint": ""},
            ledger_path=ledger,
        )
        log_coffee_resolution_from_close(
            "strategy-codex",
            picked="A",
            outcome="partial",
            readiness="orientation",
            artifacts=[],
            loops=[],
            next_slug="next",
            ledger_path=ledger,
        )

    pattern = build_pattern_watch("strategy-codex", ledger_path=ledger)
    assert pattern is not None
    assert pattern["recommended_action"] == "test"
