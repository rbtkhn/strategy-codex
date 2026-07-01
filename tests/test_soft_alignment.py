"""Tests for episystem soft_alignment (SAL)."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.soft_alignment import (  # noqa: E402
    CAPTURE_MAP_PRIOR,
    entropy_nats,
    soft_align,
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


def test_soft_align_multi_event_mass() -> None:
    dist, entropy = soft_align(
        "alpha capitulation and beta tariff overlap",
        capture_event_id="evt_a",
        terms_index=_terms_index(),
        registry=_registry(),
    )
    assert len(dist) >= 2
    assert abs(sum(float(d["weight"]) for d in dist) - 1.0) < 0.001
    assert entropy >= 0.0


def test_soft_align_capture_prior_only() -> None:
    dist, entropy = soft_align(
        "unrelated claim text",
        capture_event_id="evt_a",
        terms_index=_terms_index(),
        registry=_registry(),
    )
    assert dist[0]["event_id"] == "evt_a"
    assert dist[0]["weight"] == 1.0
    assert entropy == 0.0


def test_capture_map_prior_constant() -> None:
    assert CAPTURE_MAP_PRIOR == 0.55


def test_entropy_nats_uniform() -> None:
    ent = entropy_nats([0.5, 0.5])
    assert ent > 0.6
