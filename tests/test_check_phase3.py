"""Tests for Phase 3 check_phase3 CI gates."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_phase3 import check_orphan_events  # noqa: E402
from registry_pipeline.falsifier_validator import validate_falsifiers, validate_trajectory_v4  # noqa: E402
from prediction_lib import load_event_registry  # noqa: E402


def test_trajectory_v4_passes_on_migrated_registry() -> None:
    events = load_event_registry()
    assert not validate_trajectory_v4(events)


def test_no_orphan_enrolled_events() -> None:
    events = load_event_registry()
    assert not check_orphan_events(events)


def test_invalid_falsifier_model_is_error_tier() -> None:
    events = {
        "bad_model": {
            "question": "Bad?",
            "falsifier_model": {
                "failure_modes": [{"id": "solo", "condition": "x", "probability": 1.0}],
                "inference_source": "heuristic_v1",
            },
        }
    }
    errors, warnings, _ = validate_falsifiers(events, strict=True)
    assert errors
    assert not warnings


def test_high_entropy_inferred_model_warns_not_errors() -> None:
    from registry_pipeline.probabilistic_falsifier_engine import enrich_event_falsifiers

    event_id = "high_entropy_stub"
    enriched, _ = enrich_event_falsifiers(event_id, {"question": "Opaque claim with no tags."})
    errors, warnings, high_entropy = validate_falsifiers({event_id: enriched}, strict=True)
    assert not errors, errors
    assert event_id in high_entropy or warnings


def test_check_phase3_cli_passes() -> None:
    proc = subprocess.run(
        ["python3", "scripts/check_phase3.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
