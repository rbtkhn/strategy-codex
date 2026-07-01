"""Tests for epistemic plugin base contract."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.plugins.base import (  # noqa: E402
    MAX_PLUGIN_INFLUENCE,
    detect_input_mutation,
    normalize_plugin_weights,
    validate_plugin_output,
)


def test_validate_plugin_output_ok() -> None:
    output = {
        "plugin_name": "test_plugin",
        "modifications": {
            "signals": {"extra": 0.5},
            "regime_adjustments": {"confidence_delta": -0.01},
            "annotations": {"note": "ok"},
        },
        "confidence": 0.2,
    }
    assert validate_plugin_output(output) == []


def test_validate_rejects_signal_overwrite() -> None:
    output = {
        "plugin_name": "bad",
        "modifications": {
            "signals": {"directional": 0.99},
            "regime_adjustments": {},
            "annotations": {},
        },
        "confidence": 0.1,
    }
    issues = validate_plugin_output(output)
    assert any("directional" in i for i in issues)


def test_validate_rejects_regime_label() -> None:
    output = {
        "plugin_name": "bad",
        "modifications": {
            "signals": {},
            "regime_adjustments": {"label": "escalation"},
            "annotations": {},
        },
        "confidence": 0.1,
    }
    issues = validate_plugin_output(output)
    assert any("label" in i for i in issues)


def test_normalize_plugin_weights_caps_at_max() -> None:
    outputs = [{"confidence": 0.5}, {"confidence": 0.5}, {"confidence": 0.5}]
    weights = normalize_plugin_weights(outputs)
    assert abs(sum(weights) - MAX_PLUGIN_INFLUENCE) < 1e-6


def test_detect_input_mutation() -> None:
    before = {"a": 1}
    after = {"a": 2}
    assert detect_input_mutation(before, after) is True
