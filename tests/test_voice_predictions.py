"""Tests for voice-agnostic prediction record infrastructure."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from voice_prediction_pilot import get_voice_config, list_voice_speakers  # noqa: E402


def test_voice_registry_lists_freeman_and_mercouris() -> None:
    speakers = list_voice_speakers()
    assert "freeman" in speakers
    assert "mercouris" in speakers


def test_freeman_config_paths() -> None:
    cfg = get_voice_config("freeman")
    assert cfg.speaker == "freeman"
    assert cfg.public_map_path.name == "freeman-prediction-public-map.json"
    assert cfg.predictions_md_path.name == "freeman-predictions.md"
    assert len(cfg.pilot_event_order) == 7


def test_mercouris_config_paths() -> None:
    cfg = get_voice_config("mercouris")
    assert cfg.speaker == "mercouris"
    assert cfg.public_map_path.name == "mercouris-prediction-public-map.json"
    assert len(cfg.pilot_event_order) == 2


def test_build_voice_predictions_freeman_check() -> None:
    proc = subprocess.run(
        ["python3", "scripts/build_voice_predictions.py", "--speaker", "freeman", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_bootstrap_voice_capture_map_freeman_check() -> None:
    proc = subprocess.run(
        [
            "python3",
            "scripts/bootstrap_voice_capture_map.py",
            "--speaker",
            "freeman",
            "--check",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_bootstrap_voice_capture_map_mercouris_check() -> None:
    proc = subprocess.run(
        [
            "python3",
            "scripts/bootstrap_voice_capture_map.py",
            "--speaker",
            "mercouris",
            "--check",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_build_and_check_mercouris_predictions() -> None:
    build = subprocess.run(
        ["python3", "scripts/build_voice_predictions.py", "--speaker", "mercouris"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stderr or build.stdout
    drift = subprocess.run(
        [
            "python3",
            "scripts/build_voice_predictions.py",
            "--speaker",
            "mercouris",
            "--check",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert drift.returncode == 0, drift.stderr or drift.stdout
    shape = subprocess.run(
        ["python3", "scripts/check_voice_predictions.py", "--speaker", "mercouris"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert shape.returncode == 0, shape.stderr or shape.stdout
