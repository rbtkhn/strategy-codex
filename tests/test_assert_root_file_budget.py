from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_root_file_budget_manifest_valid():
    proc = subprocess.run(
        [sys.executable, "scripts/assert_root_file_budget.py", "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert '"root_file_count"' in proc.stdout

def test_root_file_budget_warn_mode_allows_over_budget():
    proc = subprocess.run(
        [sys.executable, "scripts/assert_root_file_budget.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "Over budget by:" in proc.stdout or "over_budget_by" in proc.stdout

def test_root_file_budget_strict_passes_at_target():
    proc = subprocess.run(
        [sys.executable, "scripts/assert_root_file_budget.py", "--strict"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "within limits" in proc.stdout or "Over budget by: 0" in proc.stdout
