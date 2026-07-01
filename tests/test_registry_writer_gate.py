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

from prediction.registry_writer import (  # noqa: E402
    RegistryGateError,
    append_changelog,
    compile_registry,
    load_registry,
    validate_registry_gate,
    validate_upsert_gate,
)
from prediction_lib import load_event_registry  # noqa: E402


def test_current_registry_passes_compile_gate() -> None:
    errors = validate_registry_gate(load_event_registry())
    assert not errors, errors


def test_compile_registry_succeeds() -> None:
    compiled = compile_registry(write=False)
    assert compiled


def test_missing_falsifier_blocked_on_upsert() -> None:
    registry = load_event_registry()
    with tempfile.TemporaryDirectory() as tmp:
        reg_path = Path(tmp) / "event-registry.json"
        log_path = Path(tmp) / "changelog.jsonl"
        reg_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
        try:
            append_changelog(
                "upsert_event",
                {
                    "event_id": "gate_test_no_falsifier",
                    "event": {
                        "question": "Will test event without falsifier happen?",
                        "resolution_criteria": "Operator resolves.",
                        "status": "open",
                    },
                },
                path=log_path,
            )
        except RegistryGateError as exc:
            assert any("missing falsifier" in e for e in exc.errors)
        else:
            raise AssertionError("expected RegistryGateError for missing falsifier")


def test_fingerprint_collision_blocked_on_upsert() -> None:
    registry = load_event_registry()
    donor_id = "gaza_ceasefire_holds_2025"
    donor = dict(registry[donor_id])
    with tempfile.TemporaryDirectory() as tmp:
        reg_path = Path(tmp) / "event-registry.json"
        log_path = Path(tmp) / "changelog.jsonl"
        reg_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
        errors = validate_upsert_gate("duplicate_gaza_clone", donor, registry)
        assert errors
        assert any("collision" in e or "duplicate" in e for e in errors)
