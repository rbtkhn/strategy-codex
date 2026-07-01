"""Tests for build_multivoice_extraction.py drift gate."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.run_multivoice_extraction import run_mvel  # noqa: E402


def test_run_mvel_status_ok() -> None:
    status = run_mvel(semantic_scores={}, disagreement={})
    assert status["status"] == "ok"
    assert status["trajectory_count"] >= 0


def test_build_multivoice_extraction_check() -> None:
    build = subprocess.run(
        [sys.executable, "scripts/build_multivoice_extraction.py"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stderr

    check = subprocess.run(
        [sys.executable, "scripts/build_multivoice_extraction.py", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert check.returncode == 0, check.stderr

    dataset = REPO / "runtime" / "artifacts" / "multivoice-extracted-dataset.json"
    payload = json.loads(dataset.read_text(encoding="utf-8"))
    assert payload.get("interpretation") == "multivoice_extraction"
