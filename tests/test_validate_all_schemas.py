"""Tests for unified schema validation."""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_all_schemas.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_validate_all_schemas_prediction_scope_passes() -> None:
    proc = _run("--scope", "prediction")
    assert proc.returncode == 0
    assert "[ok] validate_all_schemas passed" in proc.stdout


def test_missing_prediction_status_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("validate_all_schemas", VALIDATOR)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)

    pred_dir = tmp_path / "statecraft" / "notes" / "predictions"
    pred_dir.mkdir(parents=True)
    (pred_dir / "bad.md").write_text(
        textwrap.dedent(
            """\
            ---
            note_type: prediction
            event_id: known_event
            speaker: freeman
            date_made: 2025-01-01
            stance: no
            source: source-archive/statecraft/2025-01-01/example.md
            ---
            """
        ),
        encoding="utf-8",
    )

    data_dir = tmp_path / "statecraft" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "event-registry.json").write_text(
        json.dumps(
            {
                "known_event": {
                    "question": "Test?",
                    "resolution_criteria": "criteria",
                    "status": "open",
                    "outcome": None,
                }
            }
        ),
        encoding="utf-8",
    )

    registry = tmp_path / "schemas" / "registry.yaml"
    registry.parent.mkdir(parents=True)
    registry.write_text(
        textwrap.dedent(
            """\
            version: 1
            schemas:
              prediction:
                path: schemas/statecraft/prediction.schema.json
                applies_to: statecraft/notes/predictions/*.md
                format: markdown_frontmatter
                scope: prediction
              event_registry:
                path: schemas/statecraft/event.schema.json
                applies_to: statecraft/data/event-registry.json
                format: json_object_map
                scope: prediction
            """
        ),
        encoding="utf-8",
    )

    schema_src = REPO_ROOT / "schemas" / "statecraft"
    schema_dst = tmp_path / "schemas" / "statecraft"
    schema_dst.mkdir(parents=True)
    for name in ("prediction.schema.json", "event.schema.json"):
        (schema_dst / name).write_text((schema_src / name).read_text(encoding="utf-8"), encoding="utf-8")

    monkeypatch.setattr(mod, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY_PATH", registry)

    import prediction_lib
    import schema_invariants

    monkeypatch.setattr(prediction_lib, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(prediction_lib, "EVENT_REGISTRY_PATH", data_dir / "event-registry.json")
    monkeypatch.setattr(prediction_lib, "PREDICTIONS_DIR", pred_dir)
    monkeypatch.setattr(schema_invariants, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(schema_invariants, "EVENT_REGISTRY_PATH", data_dir / "event-registry.json")

    assert mod.run_validation(scope="prediction", include_invariants=False) == 1
