"""Tests for prediction registry and metrics pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_prediction_metrics as check_metrics  # noqa: E402
import check_prediction_registry as check_registry  # noqa: E402
import prediction_lib as lib  # noqa: E402

def test_build_registry_fixture_shape() -> None:
    payload = lib.build_registry_payload()
    assert len(payload["predictions"]) == 3
    speakers = {row["speaker"] for row in payload["predictions"]}
    assert speakers == {"mercouris", "ritter"}

def test_metrics_open_event_accuracy_null() -> None:
    registry = lib.build_registry_payload()
    events = lib.load_event_registry()
    metrics = lib.build_metrics_payload(registry, events)
    for bucket in metrics["voices"].values():
        assert bucket["accuracy"] is None
        assert bucket["scorable"] == 0

def test_registry_and_metrics_checks_pass_on_repo() -> None:
    assert check_registry.run_check() == 0
    assert check_metrics.run_check() == 0

def test_registry_fails_on_unknown_event(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    data_dir = tmp_path / "statecraft" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "event-registry.json").write_text(
        json.dumps(
            {
                "known_event": {
                    "question": "Q?",
                    "resolution_criteria": "Criteria",
                    "status": "open",
                    "outcome": None,
                }
            }
        ),
        encoding="utf-8",
    )
    pred_dir = tmp_path / "statecraft" / "notes" / "predictions"
    pred_dir.mkdir(parents=True)
    (pred_dir / "bad.md").write_text(
        """---
note_type: prediction
event_id: missing
speaker: mercouris
date_made: 2025-01-01
stance: no
source: source-archive/statecraft/2025-01-01/example.md
---
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(lib, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(lib, "EVENT_REGISTRY_PATH", data_dir / "event-registry.json")
    monkeypatch.setattr(lib, "PREDICTIONS_DIR", pred_dir)

    with pytest.raises(ValueError, match="unknown event_id"):
        lib.build_registry_payload()
