"""Tests for schema cross-object invariants."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

def test_resolved_event_requires_outcome(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import prediction_lib
    import schema_invariants

    data_dir = tmp_path / "statecraft" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "event-registry.json").write_text(
        json.dumps(
            {
                "bad_event": {
                    "question": "Test?",
                    "resolution_criteria": "criteria",
                    "status": "resolved",
                    "outcome": None,
                }
            }
        ),
        encoding="utf-8",
    )
    pred_dir = tmp_path / "statecraft" / "notes" / "predictions"
    pred_dir.mkdir(parents=True)

    monkeypatch.setattr(prediction_lib, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(prediction_lib, "EVENT_REGISTRY_PATH", data_dir / "event-registry.json")
    monkeypatch.setattr(prediction_lib, "PREDICTIONS_DIR", pred_dir)
    monkeypatch.setattr(schema_invariants, "REPO_ROOT", tmp_path)

    issues = schema_invariants.run_prediction_invariants(events_path=data_dir / "event-registry.json")
    assert any("resolved event requires outcome" in line for line in issues)

def test_prediction_status_must_match_event(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import prediction_lib
    import schema_invariants

    data_dir = tmp_path / "statecraft" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "event-registry.json").write_text(
        json.dumps(
            {
                "evt": {
                    "question": "Test?",
                    "resolution_criteria": "criteria",
                    "status": "resolved",
                    "outcome": "yes",
                }
            }
        ),
        encoding="utf-8",
    )
    pred_dir = tmp_path / "statecraft" / "notes" / "predictions"
    pred_dir.mkdir(parents=True)
    (pred_dir / "note.md").write_text(
        textwrap.dedent(
            """\
            ---
            note_type: prediction
            event_id: evt
            speaker: freeman
            date_made: 2025-01-01
            stance: yes
            source: source-archive/statecraft/2025-01-01/example.md
            status: pending
            ---
            """
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(prediction_lib, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(prediction_lib, "EVENT_REGISTRY_PATH", data_dir / "event-registry.json")
    monkeypatch.setattr(prediction_lib, "PREDICTIONS_DIR", pred_dir)
    monkeypatch.setattr(schema_invariants, "REPO_ROOT", tmp_path)

    issues = schema_invariants.run_prediction_invariants(events_path=data_dir / "event-registry.json")
    assert any("inconsistent with event" in line for line in issues)
