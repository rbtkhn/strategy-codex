"""Tests for epistemic plugin conflict resolver."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.plugins.conflict_resolver import merge_object  # noqa: E402

def _core_obj() -> dict:
    return {
        "trajectory_signals": {"directional": 0.7, "volatility": 0.1, "drift": 0.05},
        "regime": {"label": "fragmentation", "confidence": 0.65},
    }

def test_merge_preserves_core_label_and_directional() -> None:
    outputs = [
        {
            "plugin_name": "p1",
            "confidence": 0.2,
            "modifications": {
                "signals": {"narrative_coherence_score": 0.4},
                "regime_adjustments": {"confidence_delta": -0.1},
                "annotations": {"voice_profile": "structural_realist"},
            },
        }
    ]
    merged = merge_object(_core_obj(), outputs)
    assert merged["regime"]["label"] == "fragmentation"
    assert merged["trajectory_signals"]["directional"] == 0.7
    assert merged["trajectory_signals"]["narrative_coherence_score"] == 0.4
    assert merged["annotations"]["voice_profile"] == "structural_realist"
    assert merged["regime"]["core_confidence"] == 0.65

def test_merge_confidence_bounded() -> None:
    outputs = [
        {
            "plugin_name": "p1",
            "confidence": 1.0,
            "modifications": {
                "signals": {},
                "regime_adjustments": {"confidence_delta": 0.5},
                "annotations": {},
            },
        }
    ]
    merged = merge_object(_core_obj(), outputs)
    assert 0.0 <= merged["regime"]["confidence"] <= 1.0
