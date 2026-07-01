"""Tests for epistemic calibration loss artifact builder."""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EVAL_DATE = "2026-06-29"


def test_build_epistemic_calibration_loss_cli() -> None:
    subprocess.run(
        ["python3", "scripts/build_epistemic_generative_state.py"],
        cwd=REPO_ROOT,
        check=True,
    )
    proc = subprocess.run(
        [
            "python3",
            "scripts/build_epistemic_calibration_loss.py",
            "--eval-date",
            EVAL_DATE,
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_check_epistemic_calibration_loss_advisory() -> None:
    subprocess.run(
        [
            "python3",
            "scripts/build_epistemic_calibration_loss.py",
            "--eval-date",
            EVAL_DATE,
        ],
        cwd=REPO_ROOT,
        check=True,
    )
    proc = subprocess.run(
        ["python3", "scripts/check_epistemic_calibration_loss.py", "--advisory"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
