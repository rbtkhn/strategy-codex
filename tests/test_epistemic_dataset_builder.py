"""Tests for PR4 epistemic dataset builder."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.epistemic_dataset_builder import (  # noqa: E402
    DEFAULT_SPLIT_DATE,
    build_dataset_payload,
    build_dataset_row,
    build_latent_features,
    build_voice_observations,
    temporal_split,
)


def test_build_voice_observations() -> None:
    event = {"question": "Will China capitulate to tariff pressure?"}
    timeline = {
        "entries": [
            {"date": "2025-04-22", "speaker": "freeman", "stance": "no"},
        ]
    }
    obs = build_voice_observations(event, timeline, anchor_date="2025-04-22")
    assert len(obs) == 1
    assert obs[0]["voice"] == "freeman"
    assert "freeman:no" in obs[0]["claim"]


def test_build_latent_features_dims() -> None:
    features = build_latent_features(
        engm_event={"event_probability": 0.56},
        engm_latent={"Z": [0.1, 0.2, 0.3, 0.4], "dimensions": ["a", "b", "c", "d"]},
        signal_vector=[0.35, 1.0, 0.4, 0.0, 0.0],
    )
    assert len(features["Z"]) == 4
    assert len(features["signal_vector"]) == 5
    assert features["inference_source"] == "heuristic_v1"


def test_outcome_censoring() -> None:
    row_before = build_dataset_row(
        "gaza_test",
        {
            "question": "q",
            "falsifier": "x",
            "status": "resolved",
            "outcome": "no",
            "resolved_date": "2025-10-10",
        },
        timeline_event={
            "entries": [
                {"date": "2025-01-21", "speaker": "freeman", "stance": "no"},
                {"date": "2025-10-10", "speaker": "freeman", "stance": "no"},
            ]
        },
        signal_block={"confidence": 0.35, "cross_voice_alignment": 1.0, "drift_vector": [0.1]},
        semantic_block={},
        engm_event={"event_probability": 0.5},
        engm_latent={"Z": [0.1, 0.2, 0.3, 0.4]},
        anchor_date="2025-01-21",
        anchor_index=0,
        split_date=DEFAULT_SPLIT_DATE,
    )
    assert row_before["outcome"] is None
    assert row_before["outcome_censored"] is True

    row_after = build_dataset_row(
        "gaza_test",
        {
            "question": "q",
            "falsifier": "x",
            "status": "resolved",
            "outcome": "no",
            "resolved_date": "2025-10-10",
        },
        timeline_event={
            "entries": [
                {"date": "2025-01-21", "speaker": "freeman", "stance": "no"},
                {"date": "2025-10-10", "speaker": "freeman", "stance": "no"},
            ]
        },
        signal_block={"confidence": 0.35, "cross_voice_alignment": 1.0, "drift_vector": [0.1]},
        semantic_block={},
        engm_event={"event_probability": 0.5},
        engm_latent={"Z": [0.1, 0.2, 0.3, 0.4]},
        anchor_date="2025-10-10",
        anchor_index=1,
        split_date=DEFAULT_SPLIT_DATE,
    )
    assert row_after["outcome"] == "no"
    assert row_after["outcome_censored"] is False


def test_temporal_split() -> None:
    rows = [
        {"anchor_date": "2025-06-01", "split": "train"},
        {"anchor_date": "2026-02-01", "split": "test"},
    ]
    train, test = temporal_split(rows, split_date="2026-01-01")
    assert len(train) == 1
    assert len(test) == 1


def test_build_dataset_payload_interpretation() -> None:
    payload = build_dataset_payload(
        registry={
            "ev1": {"falsifier": "test", "question": "Will X happen?"},
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
        engm={
            "latent_state": {"Z": [0.1, 0.2, 0.3, 0.4], "dimensions": ["a", "b", "c", "d"]},
            "events": {"ev1": {"event_probability": 0.5}},
        },
        split_date="2026-01-01",
    )
    assert payload["interpretation"] == "ml_ready_dataset"
    assert payload["_meta"]["dataset_source"] == "heuristic_v1"
    assert len(payload["train"]) + len(payload["test"]) == 1
    row = payload["train"][0]
    assert row["interpretation"] == "epistemic_dataset_row"
    assert "task_labels" in row
    assert "regime_shift" in row["task_labels"]


def test_build_dataset_payload_on_live_registry() -> None:
    payload = build_dataset_payload(
        timeline={"events": {}},
        signals={"events": {}},
        semantic_scores={"events": {}},
        engm={"latent_state": {"Z": [0, 0, 0, 0]}, "events": {}},
    )
    assert payload["_meta"]["dataset_scope"]["row_count"] >= 0
