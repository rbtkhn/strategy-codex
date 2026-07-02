"""Tests for epistemic plugin runner."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.plugins.runner import build_enriched_payload, run_plugins_on_object  # noqa: E402

def _minimal_bundle() -> dict:
    core_obj = {
        "voice": "freeman",
        "timestamp": "2025-01-14",
        "capture_map_event_id": "evt_a",
        "primary_event_id": "evt_a",
        "event_distribution": [{"event_id": "evt_a", "weight": 1.0}],
        "trajectory_signals": {"directional": 0.75, "volatility": 0.0, "drift": 0.0},
        "regime": {"label": "stabilization", "confidence": 0.7},
        "alignment_entropy": 0.5,
        "interpretation": "unified_epistemic_state",
        "claim": "test claim",
    }
    return {
        "epistemic_state": {
            "_meta": {
                "object_count": 1,
                "epistemic_source": "heuristic_v1",
            },
            "interpretation": "epistemic_state",
            "objects": [core_obj],
        }
    }

def test_run_plugins_isolated_per_object() -> None:
    core_obj = _minimal_bundle()["epistemic_state"]["objects"][0]
    results, merged = run_plugins_on_object(core_obj)
    assert len(results) >= 2
    names = {r["plugin_name"] for r in results}
    assert "mearsheimer_adapter_v0" in names
    assert "narrative_coherence_signal_v0" in names
    assert "voice_profile" in merged.get("annotations", {})

def test_build_enriched_payload_shape() -> None:
    payload = build_enriched_payload(_minimal_bundle(), registry={})
    assert payload["interpretation"] == "epistemic_enriched"
    assert len(payload["objects"]) == 1
    block = payload["objects"][0]
    assert "core" in block and "plugin_results" in block and "merged" in block
    assert payload["_meta"]["plugin_influence_cap"] == 0.3
    assert "evaluation" in payload
