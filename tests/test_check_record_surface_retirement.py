"""Tests for scripts/check_record_surface_retirement.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_record_surface_retirement_passes() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/check_record_surface_retirement.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
