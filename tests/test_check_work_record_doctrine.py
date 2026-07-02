"""Tests for deprecated WORK/Record banner guard."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check_work_record_doctrine.py"

def test_doctrine_check_passes_on_repo() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "[ok] work/record doctrine banner check passed" in proc.stdout

def test_banner_line_detected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_work_record_doctrine", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    bad = tmp_path / "statecraft" / "notes" / "README.md"
    bad.parent.mkdir(parents=True)
    bad.write_text("WORK" + " only; not Record.\n", encoding="utf-8")

    monkeypatch.setattr(mod, "REPO_ROOT", tmp_path)

    issues = mod.scan_file(bad)
    assert issues
