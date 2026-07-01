"""Tests for PR1 epistemic generative model."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.epistemic_generative_model import (  # noqa: E402
    OBSERVATION_CLASSES,
    PROB_CEILING,
    PROB_EPSILON,
    build_engm_payload,
    decode_event_probability,
    infer_latent_state,
    project_voice,
    sensor_weight_for_voice,
    softmax,
)
from prediction_lib import load_event_registry  # noqa: E402


def test_softmax_sums_to_one() -> None:
    probs = softmax([1.0, 2.0, 0.5])
    assert abs(sum(probs) - 1.0) < 0.001


def test_infer_latent_state_bounds() -> None:
    latent = infer_latent_state(
        registry=load_event_registry(),
        signals={"a": {"drift_vector": [0.4, 0.5], "regime_shift_detected": False}},
        regime={"global_signals": {"geopolitical_escalation": "stable", "voice_alignment": "high"}},
    )
    assert len(latent["Z"]) == 4
    assert all(0.0 <= v <= 1.0 for v in latent["Z"])
    assert latent["inference_source"] == "heuristic_v1"


def test_voice_projections_differ() -> None:
    z = [0.5, 0.5, 0.5, 0.5]
    freeman = project_voice(z, "freeman")
    macgregor = project_voice(z, "macgregor")
    assert freeman["observation_probs"] != macgregor["observation_probs"]
    assert freeman["dominant_class"] in OBSERVATION_CLASSES


def test_macgregor_sensor_down_weight() -> None:
    low = sensor_weight_for_voice("macgregor", semantic_events={})
    high = sensor_weight_for_voice(
        "macgregor",
        semantic_events={"x": {"entropy_score": 0.9}, "y": {"entropy_score": 0.91}},
    )
    assert high < low


def test_event_probability_clamped() -> None:
    prob = decode_event_probability(
        "iran_test",
        {"question": "Iran escalation?"},
        [0.9, 0.1, 0.2, 0.95],
        signal_block={"confidence": 0.99},
        timeline_event={"latest_by_speaker": {"a": {"stance": "yes"}, "b": {"stance": "no"}}},
    )
    assert PROB_EPSILON <= prob <= PROB_CEILING


def test_build_engm_payload_on_live_registry() -> None:
    payload = build_engm_payload(
        registry=load_event_registry(),
        timeline={"events": {}},
        signals={"events": {}},
        regime={"global_signals": {"geopolitical_escalation": "stable", "voice_alignment": "moderate"}},
        semantic_scores={"events": {}},
    )
    assert payload["latent_state"]["Z"]
    assert len(payload["events"]) >= 14
    sample = next(iter(payload["events"].values()))
    assert sample["interpretation"] == "probabilistic_projection"
    assert "voice_projections" in sample
