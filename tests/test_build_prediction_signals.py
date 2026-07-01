"""Tests for prediction signals artifact builder."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_build_prediction_signals_cli() -> None:
    proc = subprocess.run(
        ["python3", "scripts/build_prediction_signals.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_check_prediction_signals_advisory() -> None:
    subprocess.run(
        ["python3", "scripts/build_prediction_signals.py"],
        cwd=REPO_ROOT,
        check=True,
    )
    subprocess.run(
        ["python3", "scripts/build_prediction_regime_summary.py"],
        cwd=REPO_ROOT,
        check=True,
    )
    proc = subprocess.run(
        ["python3", "scripts/check_prediction_signals.py", "--advisory"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
