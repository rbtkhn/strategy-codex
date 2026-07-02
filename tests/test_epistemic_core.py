"""Tests for episystem epistemic_core."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.epistemic_core import (  # noqa: E402
    classify_regime,
    compute_signal,
    infer_probabilities,
    partition_claims,
    process_claim,
)

def _registry() -> dict:
    return {
        "evt_a": {"question": "Will A happen?", "falsifier": "falsifier a", "status": "open"},
        "evt_b": {"question": "Will B happen?", "falsifier": "falsifier b", "status": "open"},
    }

def _terms_index() -> dict:
    return {
        "evt_a": ["alpha", "capitulation"],
        "evt_b": ["beta", "tariff"],
    }

def test_classify_regime_escalation() -> None:
    regime = classify_regime(
        {"directional": 0.72, "volatility": 0.2, "drift": 0.15},
        [{"event_id": "evt_a", "weight": 1.0}],
        0.5,
    )
    assert regime["label"] == "escalation"

def test_classify_regime_fragmentation() -> None:
    regime = classify_regime(
        {"directional": 0.4, "volatility": 0.3, "drift": 0.02},
        [{"event_id": "evt_a", "weight": 0.5}, {"event_id": "evt_b", "weight": 0.5}],
        1.5,
    )
    assert regime["label"] == "fragmentation"

def test_macgregor_volatility_dampening() -> None:
    trajectories = [
        {
            "event_id": "evt_a",
            "voice": "macgregor",
            "trajectory": [
                {"timestamp": "2025-01-01", "probability": 0.2, "stance": "no"},
                {"timestamp": "2025-06-01", "probability": 0.8, "stance": "yes"},
            ],
        }
    ]
    projections = [
        {
            "event_id": "evt_a",
            "weight": 1.0,
            "probability": 0.8,
            "stance": "yes",
            "confidence": 0.7,
        }
    ]
    high_ent = compute_signal(
        projections,
        trajectories=trajectories,
        voice="macgregor",
        primary_event_id="evt_a",
        semantic_entropy=0.9,
    )
    low_ent = compute_signal(
        projections,
        trajectories=trajectories,
        voice="macgregor",
        primary_event_id="evt_a",
        semantic_entropy=0.0,
    )
    assert high_ent["volatility"] <= low_ent["volatility"]
    assert high_ent["volatility"] < low_ent["volatility"]

def test_partition_claims_matched() -> None:
    claims = [{"voice": "freeman", "event_id": "evt_a", "claim": "alpha"}]
    matched, unmatched, audit = partition_claims(claims, _registry())
    assert len(matched) == 1
    assert len(unmatched) == 0
    assert audit["stats"]["matched_count"] == 1

def test_process_claim_includes_capture_map_event_id() -> None:
    claims = infer_probabilities(
        [
            {
                "voice": "freeman",
                "event_id": "evt_a",
                "capture_map_event_id": "evt_a",
                "claim": "alpha capitulation likely",
                "stance": "yes",
                "timestamp": "2025-01-01",
                "capture": "source-archive/statecraft/2025-01-01/source-a.md",
            }
        ]
    )
    trajectories = [
        {
            "event_id": "evt_a",
            "voice": "freeman",
            "trajectory": [
                {
                    "timestamp": "2025-01-01",
                    "probability": 0.75,
                    "stance": "yes",
                    "confidence": 0.7,
                }
            ],
        }
    ]
    obj = process_claim(
        claims[0],
        capture_map_event_id="evt_a",
        trajectories=trajectories,
        terms_index=_terms_index(),
        registry=_registry(),
        semantic_scores={},
    )
    assert obj["capture_map_event_id"] == "evt_a"
    assert obj["interpretation"] == "unified_epistemic_state"
    assert "event_distribution" in obj
