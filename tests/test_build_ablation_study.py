"""Tests for PR6 ablation study build/check CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_build_ablation_study_cli() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/build_ablation_study.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    out = REPO_ROOT / "runtime" / "artifacts" / "ablation-study.json"
    assert out.is_file()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["interpretation"] == "ablation_evaluation"
    assert "full" in payload["variants"]
    assert isinstance(payload["drops"], list)


def test_check_ablation_study_advisory() -> None:
    subprocess.run(
        [sys.executable, "scripts/build_ablation_study.py"],
        cwd=REPO_ROOT,
        check=True,
    )
    proc = subprocess.run(
        [sys.executable, "scripts/check_ablation_study.py", "--advisory"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "ablation study valid" in proc.stdout
