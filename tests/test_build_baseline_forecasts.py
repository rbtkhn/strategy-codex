"""Tests for PR5 baseline forecast build/check CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_build_baseline_forecasts_cli() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/build_baseline_forecasts.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    out = REPO_ROOT / "runtime" / "artifacts" / "baseline-forecast-metrics.json"
    assert out.is_file()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["interpretation"] == "baseline_evaluation"
    assert "persistence" in payload["baselines"]


def test_check_baseline_forecasts_advisory() -> None:
    subprocess.run(
        [sys.executable, "scripts/build_baseline_forecasts.py"],
        cwd=REPO_ROOT,
        check=True,
    )
    proc = subprocess.run(
        [sys.executable, "scripts/check_baseline_forecasts.py", "--advisory"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "baseline forecast metrics valid" in proc.stdout
