"""Tests for registry_writer semantic gatekeeper."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from registry_pipeline.registry_writer import (  # noqa: E402
    RegistryGateError,
    append_changelog,
    compile_registry,
    validate_registry_gate,
    validate_upsert_gate,
)
from prediction_lib import load_event_registry  # noqa: E402


def test_current_registry_passes_compile_gate() -> None:
    errors, warnings = validate_registry_gate(load_event_registry())
    assert not errors, errors


def test_compile_registry_succeeds() -> None:
    compiled = compile_registry(write=False)
    assert compiled


def test_missing_falsifier_inferred_on_upsert() -> None:
    registry = load_event_registry()
    event = {
        "question": "Will Iran airpower deter escalation?",
        "tags": ["iran", "macgregor-seed"],
        "resolution_criteria": "Operator resolves.",
        "status": "open",
    }
    errors, _ = validate_upsert_gate("gate_test_inferred_falsifier", event, registry)
    assert not errors, errors
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "changelog.jsonl"
        append_changelog(
            "upsert_event",
            {"event_id": "gate_test_inferred_falsifier", "event": event},
            path=log_path,
        )
        assert log_path.is_file()


def test_invalid_falsifier_model_blocked_on_upsert() -> None:
    registry = load_event_registry()
    bad_event = {
        "question": "Bad model row?",
        "falsifier_model": {"failure_modes": [{"id": "only_one", "condition": "x", "probability": 1.0}]},
        "resolution_criteria": "Operator resolves.",
        "status": "open",
    }
    errors, _ = validate_upsert_gate("gate_test_bad_model", bad_event, registry, run_infer=False)
    assert errors
    assert any("falsifier_model" in e for e in errors)


def test_inferred_model_only_passes_compile_gate() -> None:
    event_id = "compile_infer_only"
    event = {
        "question": "Will Ukraine reach stalemate by 2027?",
        "tags": ["ukraine"],
        "resolution_criteria": "Operator resolves.",
        "status": "open",
    }
    from registry_pipeline.probabilistic_falsifier_engine import enrich_event_falsifiers

    enriched, _ = enrich_event_falsifiers(event_id, event)
    errors, _ = validate_registry_gate({event_id: enriched})
    assert not errors, errors


def test_fingerprint_collision_blocked_on_upsert() -> None:
    registry = load_event_registry()
    donor_id = "gaza_ceasefire_holds_2025"
    donor = dict(registry[donor_id])
    errors, _ = validate_upsert_gate("duplicate_gaza_clone", donor, registry, run_infer=False)
    assert errors
    assert any("collision" in e or "duplicate" in e for e in errors)
