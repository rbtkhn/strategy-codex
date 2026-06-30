"""Tests for Freeman prediction record — colocated JSON + public markdown."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
JSON_PATH = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.json"
MD_PATH = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.md"
CAPTURE_MAP = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-capture-map.json"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_freeman_predictions as checker  # noqa: E402


def test_freeman_capture_map_exists() -> None:
    assert CAPTURE_MAP.is_file()
    data = json.loads(CAPTURE_MAP.read_text(encoding="utf-8"))
    assert len(data["rows"]) == 36


def test_freeman_predictions_json_exists() -> None:
    assert JSON_PATH.is_file()
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["speaker"] == "freeman"
    assert len(data["events"]) == 7
    assert data["_meta"].get("schema") == "freeman-predictions-v2"


def test_freeman_events_have_anchor_excerpts() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    for event in data["events"]:
        assert str(event.get("anchor_excerpt") or "").strip()
        cite = event.get("anchor_citation") or {}
        assert cite.get("title")
        assert "youtube_url" in cite


def test_freeman_appearances_have_excerpts() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    for event in data["events"]:
        for app in event["appearances"]:
            assert str(app.get("public_excerpt") or "").strip()
            assert str(app.get("public_excerpt_short") or "").strip()
            assert "youtube_url" in (app.get("citation") or {})


def test_freeman_predictions_markdown_public_structure() -> None:
    text = MD_PATH.read_text(encoding="utf-8")
    for needle in (
        "# Chas Freeman Prediction Record",
        "## At a Glance",
        "## Method",
        "<details>",
        "<summary>Source trail</summary>",
        "— Chas Freeman,",
    ):
        assert needle in text


def test_freeman_predictions_builder_check() -> None:
    proc = subprocess.run(
        ["python3", "scripts/build_freeman_predictions.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_freeman_predictions_shape_checker() -> None:
    issues, _ = checker.run_check(json_path=JSON_PATH, md_path=MD_PATH)
    assert not issues
