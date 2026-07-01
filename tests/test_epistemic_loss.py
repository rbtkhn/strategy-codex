"""Tests for PR2 epistemic calibration loss."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.epistemic_loss import (  # noqa: E402
    DEFAULT_WEIGHTS,
    brier_score,
    build_calibration_payload,
    compute_aggregate_loss,
    entropy_misalignment,
    outcome_to_label,
    prediction_error,
    regime_shift_delay,
    shannon_entropy,
)


def test_outcome_to_label() -> None:
    assert outcome_to_label("yes") == 1.0
    assert outcome_to_label("no") == 0.0
    assert outcome_to_label(None) is None


def test_prediction_error_and_brier() -> None:
    assert prediction_error(0.7, 1.0) == 0.3
    assert brier_score(0.7, 1.0) == 0.09


def test_shannon_entropy_bounds() -> None:
    uniform = shannon_entropy([0.33, 0.33, 0.34])
    peaked = shannon_entropy([1.0, 0.0, 0.0])
    assert 0.0 <= uniform <= 1.0
    assert peaked < uniform


def test_entropy_misalignment_non_negative() -> None:
    block = entropy_misalignment(
        engm_event={
            "voice_projections": {
                "freeman": {
                    "sensor_weight": 1.0,
                    "observation_probs": {
                        "affirm_escalation": 0.8,
                        "affirm_deescalation": 0.1,
                        "withhold": 0.1,
                    },
                }
            }
        },
        timeline_event={
            "latest_by_speaker": {
                "freeman": {"stance": "uncertain"},
            }
        },
        y_pred=0.8,
        y_true=0.0,
    )
    assert block["value"] >= 0.0
    assert block["overconfidence_penalty"] == 0.05


def test_regime_shift_delay_normalized() -> None:
    block = regime_shift_delay(
        timeline_event={
            "shifts": {
                "freeman": [
                    {
                        "type": "stance_shift",
                        "to_date": "2026-04-28",
                    }
                ]
            }
        },
        signal_block={"regime_shift_detected": False},
        regime={"global_signals": {"regime_shift_detected": False}},
        eval_date="2026-06-29",
    )
    assert block["shift_count"] == 1
    assert 0.0 <= block["value"] <= 1.0


def test_aggregate_loss_in_unit_interval() -> None:
    event_blocks = {
        "resolved": {
            "included_in_brier": True,
            "prediction_error": 0.4,
            "brier_score": 0.16,
            "entropy_misalignment": 0.1,
        },
        "open": {
            "included_in_brier": False,
            "entropy_misalignment": 0.2,
        },
    }
    aggregate = compute_aggregate_loss(event_blocks=event_blocks, weights=DEFAULT_WEIGHTS)
    assert 0.0 <= aggregate["total_loss"] <= 1.0
    assert aggregate["components"]["prediction_error"]["event_count"] == 1


def test_build_calibration_payload_resolved_only_brier() -> None:
    payload = build_calibration_payload(
        registry={
            "resolved_yes": {
                "status": "resolved",
                "outcome": "yes",
            },
            "open_event": {
                "status": "open",
                "outcome": None,
            },
        },
        engm={
            "events": {
                "resolved_yes": {"event_probability": 0.6},
                "open_event": {"event_probability": 0.5},
            }
        },
        timeline={"events": {}},
        signals={"events": {}},
        regime={"global_signals": {}},
        eval_date="2026-06-29",
    )
    assert payload["interpretation"] == "calibration_metric"
    assert payload["_meta"]["calibration_source"] == "heuristic_v1"
    assert payload["_meta"]["calibration_scope"]["brier_eligible"] == 1
    assert payload["events"]["resolved_yes"]["included_in_brier"] is True
    assert payload["events"]["open_event"]["included_in_brier"] is False
    assert "brier_score" not in payload["events"]["open_event"]


def test_build_calibration_payload_on_live_registry() -> None:
    from prediction_lib import load_event_registry  # noqa: E402

    payload = build_calibration_payload(
        registry=load_event_registry(),
        engm={"events": {}},
        timeline={"events": {}},
        signals={"events": {}},
        regime={"global_signals": {}},
        eval_date="2026-06-29",
    )
    assert payload["_meta"]["calibration_scope"]["resolved_event_count"] >= 3
