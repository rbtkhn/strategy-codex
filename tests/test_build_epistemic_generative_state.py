"""Tests for ENGM artifact builder."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_build_epistemic_generative_state_cli() -> None:
    proc = subprocess.run(
        ["python3", "scripts/build_epistemic_generative_state.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_check_epistemic_generative_state_advisory() -> None:
    subprocess.run(
        ["python3", "scripts/build_epistemic_generative_state.py"],
        cwd=REPO_ROOT,
        check=True,
    )
    proc = subprocess.run(
        ["python3", "scripts/check_epistemic_generative_state.py", "--advisory"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
