"""Tests for signal prediction tasks artifact builder."""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_build_signal_prediction_tasks_cli() -> None:
    proc = subprocess.run(
        ["python3", "scripts/build_signal_prediction_tasks.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_check_signal_prediction_tasks_advisory() -> None:
    subprocess.run(
        ["python3", "scripts/build_signal_prediction_tasks.py"],
        cwd=REPO_ROOT,
        check=True,
    )
    proc = subprocess.run(
        ["python3", "scripts/check_signal_prediction_tasks.py", "--advisory"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
