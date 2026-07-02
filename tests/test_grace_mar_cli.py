from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

def test_help_lists_gate_commands() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "grace_mar.cli", "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "gate board" in proc.stderr
    assert "gate merge" in proc.stderr

def test_unknown_command_exits_two() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "grace_mar.cli", "not-a-command"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "Unknown command" in proc.stderr

def test_gate_diff_requires_candidate_id() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "grace_mar.cli", "gate", "diff"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "CANDIDATE" in proc.stderr
