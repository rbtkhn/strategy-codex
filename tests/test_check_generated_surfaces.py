from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_generated_manifest_schema():
    proc = subprocess.run(
        [sys.executable, "scripts/check_generated_surfaces.py", "--manifest-only"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_generated_surfaces_headers_pass():
    proc = subprocess.run(
        [sys.executable, "scripts/check_generated_surfaces.py", "--headers-only", "--strict"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_generated_surfaces_orchestrator_runs_drift_check():
    """Drift failures are warn-mode until Sprint 9; ensure orchestrator executes."""
    proc = subprocess.run(
        [sys.executable, "scripts/check_generated_surfaces.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert proc.returncode in (0, 1)
    assert "generated surfaces check passed" in proc.stdout or "generated-surfaces:" in proc.stderr
