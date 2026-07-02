"""Smoke tests for fork-language audit (strategy-codex operator routing)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

def test_audit_fork_language_strict_exits_zero():
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "audit_fork_language.py"),
            "--strict",
            "--errors-only",
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr

def test_validate_grace_mar_stub_redirects():
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "validate_grace_mar_stub_redirects.py")],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
