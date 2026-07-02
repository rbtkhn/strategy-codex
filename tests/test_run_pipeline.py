"""Tests for episystem run_pipeline."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.run_pipeline import build_artifacts, check_artifacts  # noqa: E402

def test_build_artifacts_shape() -> None:
    bundle = build_artifacts(include_multivoice=True)
    assert "epistemic_state" in bundle
    assert "signals" in bundle
    assert "regimes" in bundle
    assert bundle["epistemic_state"]["interpretation"] == "epistemic_state"
    assert bundle["signals"]["interpretation"] == "epistemic_signals"
    assert bundle["regimes"]["interpretation"] == "epistemic_regimes"
    assert len(bundle["epistemic_state"]["objects"]) > 0

def test_run_pipeline_check_cli() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/prediction/run_pipeline.py", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr

def test_check_artifacts_in_process() -> None:
    assert check_artifacts() == 0

def test_with_plugins_writes_enriched() -> None:
    from prediction.run_pipeline import build_artifacts

    bundle = build_artifacts(with_plugins=True)
    assert "epistemic_enriched" in bundle
    assert bundle["epistemic_enriched"]["interpretation"] == "epistemic_enriched"

def test_core_check_unchanged_without_plugins_flag() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/prediction/run_pipeline.py", "--check-enriched"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
