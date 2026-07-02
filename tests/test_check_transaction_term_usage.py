"""Tests for transaction terminology guard."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check_transaction_term_usage.py"

def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

def test_canonical_note_term_law_matches_complexity_budget():
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_transaction_term_usage", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    budget = (REPO_ROOT / "docs" / "complexity-budget.md").read_text(encoding="utf-8")
    assert mod.CANONICAL_NOTE_TERM_LAW.replace("\n", " ") in budget.replace("\n", " ")

def test_warn_mode_exits_zero_even_with_violations_before_doctrine_fix() -> None:
    """Warn mode must not fail CI during transition; strict catches regressions."""
    proc = _run("--warn")
    assert proc.returncode == 0

def test_strict_passes_after_doctrine_retirement() -> None:
    proc = _run("--strict", "--skills-strict")
    assert proc.returncode == 0, proc.stderr

def test_script_importable() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_transaction_term_usage", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "DISALLOWED_PATTERNS")
    assert len(mod.TIER1_DOCS) >= 20
