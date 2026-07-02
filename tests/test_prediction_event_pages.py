"""Tests for cross-voice prediction event pages (Phase 6 MVP)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
EVENTS_DIR = REPO_ROOT / "statecraft" / "predictions" / "events"
MATRIX_PATH = REPO_ROOT / "statecraft" / "predictions" / "cross-voice-matrix.md"
FREEMAN_JSON = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.json"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_prediction_event_pages import build_outputs  # noqa: E402
from prediction_lib import load_event_registry  # noqa: E402

def test_freeman_event_page_exists_and_has_freeman_row() -> None:
    page = EVENTS_DIR / "gaza_ceasefire_holds_2025.md"
    assert page.is_file()
    text = page.read_text(encoding="utf-8")
    assert "freeman" in text
    assert "GENERATED FILE" in text

def test_cross_voice_matrix_lists_freeman_and_second_voice() -> None:
    assert MATRIX_PATH.is_file()
    text = MATRIX_PATH.read_text(encoding="utf-8")
    assert "freeman" in text
    assert "mercouris" in text or "macgregor" in text

def test_matrix_uses_only_registry_event_ids() -> None:
    registry = load_event_registry()
    pages, _ = build_outputs(
        registry_path=REPO_ROOT / "statecraft" / "data" / "event-registry.json",
        timeline_path=REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json",
        disagreement_path=REPO_ROOT / "runtime" / "artifacts" / "prediction-disagreement.json",
    )
    for event_id in pages:
        assert event_id in registry

def test_build_prediction_event_pages_check_passes() -> None:
    proc = subprocess.run(
        ["python3", "scripts/build_prediction_event_pages.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout

def test_freeman_shelf_json_companion_valid() -> None:
    data = json.loads(FREEMAN_JSON.read_text(encoding="utf-8"))
    assert data["speaker"] == "freeman"
    for event in data["events"]:
        assert event["event_id"] in load_event_registry()
