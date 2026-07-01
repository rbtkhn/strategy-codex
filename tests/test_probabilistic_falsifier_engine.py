"""Tests for Phase 3.5 probabilistic falsifier inference engine."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from registry_pipeline.contracts import (  # noqa: E402
    HIGH_ENTROPY_THRESHOLD,
    falsifier_key_for_fingerprint,
    predictive_fingerprint,
    validate_falsifier_model,
)
from registry_pipeline.probabilistic_falsifier_engine import (  # noqa: E402
    enrich_event_falsifiers,
    infer_falsifier_model,
    run_inference,
)


def test_iran_template_selected_for_macgregor_style_event() -> None:
    event_id = "iran_airpower_escalation_2026"
    event = {
        "question": "Will Iran airpower deter US escalation?",
        "tags": ["macgregor-seed", "iran"],
    }
    model = infer_falsifier_model(event_id, event)
    assert not validate_falsifier_model(model)
    ids = {m["id"] for m in model["failure_modes"]}
    assert any("escalation" in i or "withdrawal" in i or "capitulation" in i for i in ids)
    assert abs(sum(m["probability"] for m in model["failure_modes"]) - 1.0) < 0.02
    assert model["inference_source"] == "heuristic_v1"


def test_enrich_event_adds_model_when_falsifier_missing() -> None:
    event_id = "test_infer_gap"
    event = {"question": "Will NATO expand exposure in Ukraine?"}
    enriched, inferences = enrich_event_falsifiers(event_id, event)
    assert enriched.get("falsifier_model")
    assert not validate_falsifier_model(enriched["falsifier_model"])
    assert inferences
    assert inferences[0]["event_id"] == event_id


def test_explicit_string_falsifier_not_replaced() -> None:
    event_id = "explicit_falsifier_row"
    event = {
        "question": "Will test hold?",
        "falsifier": "Operator observes decisive counter-evidence.",
    }
    enriched, inferences = enrich_event_falsifiers(event_id, event)
    assert enriched["falsifier"] == event["falsifier"]
    assert "falsifier_model" not in enriched
    assert not inferences


def test_fallback_template_has_high_entropy() -> None:
    model = infer_falsifier_model("opaque_claim_xyz", {"question": "Something vague happens."})
    assert float(model["entropy"]) >= HIGH_ENTROPY_THRESHOLD - 0.05


def test_fingerprint_ignores_probability_weight_tweaks() -> None:
    base = {
        "question": "Will Iran capitulate under airpower pressure?",
        "falsifier_model": infer_falsifier_model("iran_test_fp", {"question": "Iran airpower", "tags": ["iran"]}),
    }
    tweaked = dict(base)
    modes = [dict(m) for m in base["falsifier_model"]["failure_modes"]]
    modes[0]["probability"] = 0.5
    modes[1]["probability"] = 0.3
    modes[2]["probability"] = 0.2
    tweaked["falsifier_model"] = dict(base["falsifier_model"])
    tweaked["falsifier_model"]["failure_modes"] = modes
    assert falsifier_key_for_fingerprint(base) == falsifier_key_for_fingerprint(tweaked)
    assert predictive_fingerprint("iran_test_fp", base) == predictive_fingerprint("iran_test_fp", tweaked)


def test_run_inference_report_shape() -> None:
    registry = {
        "a": {"question": "Iran strike?", "tags": ["iran"]},
        "b": {"question": "Will hold?", "falsifier": "Fails on wire."},
    }
    report = run_inference(registry)
    assert report["inferred_count"] >= 1
    assert "inferences" in report
