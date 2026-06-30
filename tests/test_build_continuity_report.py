"""Tests for build_continuity_report.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

from build_continuity_report import build_report, format_md  # noqa: E402


def test_build_report_shape():
    report = build_report(REPO)
    assert report.continuity_root == "continuity"
    assert report.authority.startswith("derived")
    assert report.generated


def test_format_md_marks_derived():
    report = build_report(REPO)
    md = format_md(report)
    assert "derived" in md.lower()
    assert "not SSOT" in md or "Authority" in md


def test_build_continuity_report_writes_artifacts(tmp_path, monkeypatch):
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "build_continuity_report.py"), "--json"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["continuity_root"] == "continuity"
    assert (REPO / "runtime" / "artifacts" / "continuity-report.json").is_file()
