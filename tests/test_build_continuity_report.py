"""Tests for build_continuity_report.py."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

from build_continuity_report import build_report, format_md  # noqa: E402

ARTIFACT_JSON = REPO / "runtime" / "artifacts" / "continuity-report.json"
ARTIFACT_MD = REPO / "runtime" / "artifacts" / "continuity-report.md"

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
    assert "Prediction rows" in md

def test_build_continuity_report_json_is_non_mutating():
    json_mtime = ARTIFACT_JSON.stat().st_mtime if ARTIFACT_JSON.is_file() else None
    md_mtime = ARTIFACT_MD.stat().st_mtime if ARTIFACT_MD.is_file() else None
    time.sleep(0.05)

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
    assert "prediction_row_count" in data
    assert "open_prediction_count" not in data

    if json_mtime is not None:
        assert ARTIFACT_JSON.stat().st_mtime == json_mtime
    if md_mtime is not None:
        assert ARTIFACT_MD.stat().st_mtime == md_mtime

def test_build_continuity_report_write_creates_artifacts():
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "build_continuity_report.py"),
            "--write",
            "--json",
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["continuity_root"] == "continuity"
    assert ARTIFACT_JSON.is_file()
    assert ARTIFACT_MD.is_file()
    written = json.loads(ARTIFACT_JSON.read_text(encoding="utf-8"))
    assert written["prediction_row_count"] == data["prediction_row_count"]

def test_build_continuity_report_default_prints_markdown():
    json_mtime = ARTIFACT_JSON.stat().st_mtime if ARTIFACT_JSON.is_file() else None
    time.sleep(0.05)

    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "build_continuity_report.py")],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stderr
    assert "Continuity report" in proc.stdout
    assert "derived" in proc.stdout.lower()
    assert proc.stdout.strip()
    if json_mtime is not None:
        assert ARTIFACT_JSON.stat().st_mtime == json_mtime
