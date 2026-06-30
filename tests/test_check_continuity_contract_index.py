"""Tests for continuity contract index checker."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

from check_continuity_contract_index import check_contract_index  # noqa: E402


def test_contract_index_passes_on_repo():
    report = check_contract_index(REPO)
    assert report.errors == [], report.errors


def test_contract_index_fails_missing_owner(tmp_path: Path):
    root = tmp_path / "continuity"
    root.mkdir()
    (root / "README.md").write_text("# r\n", encoding="utf-8")
    report = check_contract_index(tmp_path)
    assert report.missing_owners


def test_contract_index_cli():
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "check_continuity_contract_index.py")],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stderr
