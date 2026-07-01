"""Tests for PR6 ablation study."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.ablation_study import (  # noqa: E402
    AblationFlags,
    VARIANTS,
    compute_drops,
    neutralize_disagreement_payload,
    neutralize_signals_payload,
    rebuild_membrane,
    score_variant,
)


def _mini_inputs() -> dict:
    registry = {
        "evt_a": {
            "question": "Will event A happen?",
            "falsifier": "Observable falsifier A",
            "status": "resolved",
            "outcome": "no",
            "resolved_date": "2025-06-01",
            "start_date": "2025-01-01",
        },
        "evt_b": {
            "question": "Will event B happen?",
            "falsifier": "Observable falsifier B",
            "status": "open",
        },
    }
    timeline = {
        "events": {
            "evt_a": {
                "entries": [
                    {"date": "2025-01-10", "speaker": "freeman", "stance": "no"},
                    {"date": "2025-06-01", "speaker": "freeman", "stance": "no"},
                ],
                "shifts": {"freeman": [{"to_date": "2025-06-01", "from_stance": "no", "to_stance": "no"}]},
            },
            "evt_b": {
                "entries": [
                    {"date": "2025-01-10", "speaker": "freeman", "stance": "yes"},
                    {"date": "2025-02-01", "speaker": "mercouris", "stance": "no"},
                ]
            },
        }
    }
    signals = {
        "events": {
            "evt_a": {
                "confidence": 0.8,
                "cross_voice_alignment": 0.9,
                "drift_vector": [0.4, 0.45],
                "regime_shift_detected": False,
            },
            "evt_b": {
                "confidence": 0.7,
                "cross_voice_alignment": 0.5,
                "drift_vector": [0.5, 0.55],
                "regime_shift_detected": True,
            },
        }
    }
    disagreement = {
        "events": {
            "evt_a": {
                "latest_voice_level": {"disagreement_score_normalized": 0.1},
            },
            "evt_b": {
                "latest_voice_level": {"disagreement_score_normalized": 0.6},
            },
        }
    }
    semantic = {"events": {"evt_a": {"entropy_score": 0.2}, "evt_b": {"entropy_score": 0.3}}}
    regime = {"global_signals": {"regime_shift_detected": False}}
    return {
        "registry": registry,
        "timeline": timeline,
        "signals": signals,
        "disagreement": disagreement,
        "semantic_scores": semantic,
        "regime": regime,
    }


def test_neutralize_signals_changes_confidence() -> None:
    payload = neutralize_signals_payload({"events": {"x": {"confidence": 0.9}}})
    assert payload["events"]["x"]["confidence"] == 0.5


def test_neutralize_disagreement_zeros_gini() -> None:
    payload = neutralize_disagreement_payload(
        {"events": {"x": {"latest_voice_level": {"disagreement_score_normalized": 0.8}}}}
    )
    assert payload["events"]["x"]["latest_voice_level"]["disagreement_score_normalized"] == 0.0


def test_rebuild_membrane_signal_ablation_differs_from_full() -> None:
    inputs = _mini_inputs()
    full = rebuild_membrane(AblationFlags(), split_date="2026-01-01", **inputs)
    ablated = rebuild_membrane(
        AblationFlags(signal_extraction=False),
        split_date="2026-01-01",
        **inputs,
    )
    full_prob = full["engm"]["events"]["evt_a"]["event_probability"]
    ablated_prob = ablated["engm"]["events"]["evt_a"]["event_probability"]
    assert full_prob != ablated_prob


def test_score_variant_has_core_and_structural() -> None:
    inputs = _mini_inputs()
    membrane = rebuild_membrane(AblationFlags(), split_date="2026-01-01", **inputs)
    scored = score_variant(membrane, timeline=inputs["timeline"], regime=inputs["regime"], split_date="2026-01-01")
    assert "core" in scored
    assert "structural" in scored
    assert "brier" in scored["core"]


def test_compute_drops_null_when_low_n() -> None:
    variants = {
        "full": {"core": {"brier": 0.2, "n_probability": 0}},
        "no_signal_extraction": {"core": {"brier": 0.1, "n_probability": 0}},
    }
    drops = compute_drops(variants, reference="full")
    assert drops[0]["performance_drop"] is None
    assert drops[0]["note"] == "low_n"


def test_compute_drops_positive_when_variant_worse() -> None:
    variants = {
        "full": {"core": {"brier": 0.1, "n_probability": 2}},
        "no_signal_extraction": {"core": {"brier": 0.3, "n_probability": 2}},
    }
    drops = compute_drops(
        variants,
        reference="full",
    )
    signal_drop = next(d for d in drops if d["variant"] == "no_signal_extraction")
    assert signal_drop["performance_drop"] == 0.2


def test_variants_count() -> None:
    assert len(VARIANTS) == 5
    assert "full" in VARIANTS
    assert "no_disagreement_graph" in VARIANTS
