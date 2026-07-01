"""Tests for PR3 signal prediction tasks."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.signal_prediction_tasks import (  # noqa: E402
    DEFAULT_HORIZON_DAYS,
    SIGNAL_VECTOR_DIMENSIONS,
    build_signal_vector,
    build_task_payload,
    derive_delta_label,
    derive_regime_shift_label,
    predict_convergence,
    predict_delta,
    predict_regime_shift,
)


def test_build_signal_vector_bounds() -> None:
    vec = build_signal_vector(
        {
            "confidence": 0.35,
            "cross_voice_alignment": 0.8,
            "drift_vector": [0.1, 0.2, 0.3],
            "regime_shift_detected": True,
        },
        {"entropy_score": 0.5},
    )
    assert len(vec) == len(SIGNAL_VECTOR_DIMENSIONS)
    assert all(0.0 <= v <= 1.0 or v == 1.0 for v in vec)
    assert vec[3] == 1.0


def test_derive_regime_shift_label() -> None:
    timeline = {
        "shifts": {
            "freeman": [{"to_date": "2026-04-28", "type": "stance_shift"}],
        }
    }
    assert derive_regime_shift_label(timeline_event=timeline, anchor_date="2026-04-01") == "shift"
    assert derive_regime_shift_label(timeline_event=timeline, anchor_date="2026-05-01") == "no_shift"


def test_derive_delta_label_fixture() -> None:
    event = {"question": "test", "falsifier": "x"}
    timeline = {
        "entries": [
            {"date": "2025-01-01", "speaker": "freeman", "stance": "no"},
            {"date": "2025-02-15", "speaker": "freeman", "stance": "yes"},
        ]
    }
    label = derive_delta_label(
        "test_event",
        event,
        timeline_event=timeline,
        semantic_block={},
        anchor_date="2025-01-01",
        anchor_index=0,
        horizon_days=30,
    )
    assert label["future_outcome"] in {"up", "down", "flat"}
    assert "delta" in label


def test_predict_regime_shift_heuristic() -> None:
    pred = predict_regime_shift(
        "x",
        signal_vector=[0.35, 1.0, 0.4, 1.0, 0.0],
        signal_block={"drift_vector": [0.2, 0.5]},
    )
    assert pred["predicted_outcome"] == "shift"


def test_predict_delta_heuristic() -> None:
    pred = predict_delta(
        "x",
        signal_vector=[0.35, 1.0, 0.4, 0.0, 0.0],
        p_t=0.5,
        signal_block={"drift_vector": [0.1, 0.2]},
    )
    assert pred["predicted_outcome"] == "up"


def test_predict_convergence_heuristic() -> None:
    pred = predict_convergence(
        signal_vector=[0.35, 0.8, 0.4, 0.0, 0.0],
        voice_states={"freeman": "no", "mercouris": "no"},
    )
    assert pred["predicted_outcome"] == "converged"


def test_build_task_payload_interpretation() -> None:
    payload = build_task_payload(
        registry={
            "ev1": {
                "falsifier": "test falsifier",
                "question": "q",
            }
        },
        timeline={
            "events": {
                "ev1": {
                    "entries": [
                        {"date": "2025-01-01", "speaker": "freeman", "stance": "no"},
                        {"date": "2025-02-01", "speaker": "freeman", "stance": "no"},
                    ]
                }
            }
        },
        signals={"events": {"ev1": {"confidence": 0.35, "cross_voice_alignment": 1.0, "drift_vector": [0.1]}}},
        semantic_scores={"events": {"ev1": {"entropy_score": 0.0}}},
        horizon_days=DEFAULT_HORIZON_DAYS,
    )
    assert payload["interpretation"] == "supervised_task_space"
    assert payload["_meta"]["task_source"] == "heuristic_v1"
    for example in payload["examples"]:
        assert example["interpretation"] == "supervised_task_example"


def test_build_task_payload_on_live_registry() -> None:
    payload = build_task_payload(
        timeline={"events": {}},
        signals={"events": {}},
        semantic_scores={"events": {}},
    )
    assert payload["_meta"]["task_scope"]["example_count"] >= 0
