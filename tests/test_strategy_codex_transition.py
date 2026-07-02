"""Regression checks for strategy-codex naming migration."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "validate_strategy_codex_transition.py"

def test_strategy_codex_transition_validator() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=REPO,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "validate_strategy_codex_transition: OK" in result.stderr
