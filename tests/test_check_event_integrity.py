"""Tests for event integrity checker."""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check_event_integrity.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_event_integrity_passes_on_repo() -> None:
    proc = _run()
    assert proc.returncode == 0
    assert "[ok] event integrity valid" in proc.stdout


def test_unknown_event_id_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_event_integrity", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)

    data_dir = tmp_path / "statecraft" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "event-registry.json").write_text(
        json.dumps(
            {
                "known_event": {
                    "question": "Test?",
                    "resolution_criteria": "Test criteria",
                    "status": "open",
                    "outcome": None,
                }
            }
        ),
        encoding="utf-8",
    )

    pred_dir = tmp_path / "statecraft" / "notes" / "predictions"
    pred_dir.mkdir(parents=True)
    (pred_dir / "bad-note.md").write_text(
        textwrap.dedent(
            """\
            ---
            note_type: prediction
            event_id: missing_event
            speaker: mercouris
            date_made: 2025-01-01
            stance: no
            source: source-archive/statecraft/2025-01-01/example.md
            ---
            """
        ),
        encoding="utf-8",
    )

    import prediction_lib

    monkeypatch.setattr(prediction_lib, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(prediction_lib, "EVENT_REGISTRY_PATH", data_dir / "event-registry.json")
    monkeypatch.setattr(prediction_lib, "PREDICTIONS_DIR", pred_dir)
    monkeypatch.setattr(mod, "EVENT_REGISTRY_PATH", data_dir / "event-registry.json")

    assert mod.run_check(registry_path=data_dir / "event-registry.json") == 1
