"""Tests for Phase 4.5 signal extraction engine."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.signal_extraction_engine import (  # noqa: E402
    build_regime_summary,
    classify_signal,
    cross_voice_alignment,
    effective_falsifier_model,
    extract_event_signal,
    extract_signals,
)
from prediction_lib import load_event_registry  # noqa: E402


def test_effective_model_uses_inferred_view_for_string_falsifier() -> None:
    event_id = "iran_airpower_test"
    event = {
        "question": "Will Iran airpower deter US escalation?",
        "falsifier": "Wire-grade explicit falsifier.",
        "tags": ["iran"],
    }
    model, source = effective_falsifier_model(event_id, event)
    assert source == "inferred_view"
    assert model.get("failure_modes")


def test_extract_signals_on_live_registry() -> None:
    events = load_event_registry()
    timeline = {"events": {}}
    disagreement = {"events": {}}
    semantic = {"events": {}}
    signals = extract_signals(events, timeline=timeline, disagreement=disagreement, semantic_scores=semantic)
    assert len(signals) >= 14
    sample = next(iter(signals.values()))
    assert sample["signal_type"]
    assert sample["distribution_source"] in {"persisted", "inferred_view"}


def test_freeman_only_stable_signal() -> None:
    event_id = "china_tariff_capitulation_2025"
    event = {
        "question": "Will China capitulate?",
        "falsifier": "China accepts major demands without retaliation.",
    }
    timeline_event = {
        "entries": [
            {"date": "2025-04-04", "speaker": "freeman", "stance": "no"},
            {"date": "2026-03-17", "speaker": "freeman", "stance": "no"},
        ],
        "latest_by_speaker": {"freeman": {"stance": "no"}},
    }
    signal = extract_event_signal(
        event_id,
        event,
        timeline_event=timeline_event,
        disagreement_event=None,
        semantic_block={"entropy_score": 0.0, "falsifier_confidence": "high"},
    )
    assert signal["cross_voice_alignment"] == 1.0
    assert signal["signal_type"] in {"directional", "saturation", "convergence"}


def test_macgregor_high_entropy_down_weights_alignment() -> None:
    event_id = "macgregor_stress"
    event = {"question": "Opaque claim?", "tags": ["macgregor-seed"]}
    model, _ = effective_falsifier_model(event_id, event)
    timeline_event = {
        "latest_by_speaker": {
            "freeman": {"stance": "no"},
            "macgregor": {"stance": "yes"},
        }
    }
    low_entropy = cross_voice_alignment(
        event_id,
        event,
        model,
        timeline_event,
        semantic_block={"entropy_score": 0.0},
    )
    high_entropy = cross_voice_alignment(
        event_id,
        event,
        model,
        timeline_event,
        semantic_block={"entropy_score": 0.9},
    )
    assert high_entropy <= low_entropy


def test_regime_shift_classification() -> None:
    signal_type, confidence, regime = classify_signal(
        drift=[0.02, 0.2, 0.03],
        alignment=0.5,
        entropy_score=0.4,
        gini_norm=0.1,
        stance_variance=0.0,
        entropy_series=[0.7, 0.71, 0.72],
    )
    assert signal_type == "regime_shift"
    assert regime is True
    assert confidence > 0


def test_build_regime_summary_shape() -> None:
    summary = build_regime_summary(
        {
            "iran_x": {
                "cross_voice_alignment": 0.4,
                "drift_vector": [0.3, 0.5],
                "regime_shift_detected": True,
                "distribution_source": "inferred_view",
            }
        },
        {"iran_x": {"question": "Iran escalation?"}},
    )
    assert summary["global_signals"]["regime_shift_detected"] is True
    assert summary["global_signals"]["voice_alignment"] == "moderate"
