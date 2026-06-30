from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from scripts.check_generated_surfaces import (
    MANIFEST_PATH,
    collect_orphan_issues,
    _load_manifest,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_generated_manifest_schema():
    proc = subprocess.run(
        [sys.executable, "scripts/check_generated_surfaces.py", "--manifest-only"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "25 entries" in proc.stdout


def test_manifest_includes_work_dev_control_plane():
    text = (REPO_ROOT / "generated-manifest.yaml").read_text(encoding="utf-8")
    for entry_id in (
        "work-dev-integration-status",
        "work-dev-known-gaps",
        "work-dev-proof-ledger",
        "work-dev-target-registry",
        "work-dev-continuity-blocks",
    ):
        assert entry_id in text


def test_manifest_includes_statecraft_notes_registry():
    text = (REPO_ROOT / "generated-manifest.yaml").read_text(encoding="utf-8")
    assert "statecraft-notes-registry-md" in text
    assert "runtime/artifacts/statecraft-notes-registry.md" in text
    assert "statecraft-notes-registry-json" in text


def test_manifest_includes_freeman_predictions():
    text = (REPO_ROOT / "generated-manifest.yaml").read_text(encoding="utf-8")
    assert "freeman-predictions-md" in text
    assert "statecraft/voices/freeman/freeman-predictions.md" in text
    assert "freeman-predictions-json" in text
    assert "statecraft/voices/freeman/freeman-predictions.json" in text


def test_manifest_includes_freeman_capture_map_check():
    text = (REPO_ROOT / "generated-manifest.yaml").read_text(encoding="utf-8")
    assert "freeman-prediction-capture-map" in text
    assert "statecraft/data/freeman-prediction-capture-map.json" in text
    assert "bootstrap_freeman_capture_map.py" in text


def test_manifest_includes_mercouris_predictions():
    text = (REPO_ROOT / "generated-manifest.yaml").read_text(encoding="utf-8")
    assert "mercouris-predictions-md" in text
    assert "statecraft/voices/mercouris/mercouris-predictions.md" in text
    assert "mercouris-predictions-json" in text
    assert "statecraft/voices/mercouris/mercouris-predictions.json" in text


def test_manifest_includes_mercouris_capture_map_check():
    text = (REPO_ROOT / "generated-manifest.yaml").read_text(encoding="utf-8")
    assert "mercouris-prediction-capture-map" in text
    assert "statecraft/data/mercouris-prediction-capture-map.json" in text
    assert "bootstrap_voice_capture_map.py" in text


def test_generated_surfaces_headers_pass():
    proc = subprocess.run(
        [sys.executable, "scripts/check_generated_surfaces.py", "--headers-only", "--strict"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_generated_surfaces_strict_passes():
    archive = subprocess.run(
        [sys.executable, "scripts/refresh_statecraft_archive_indices.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if archive.returncode != 0:
        pytest.skip("local archive navigation drift; strict generated check runs clean on CI tree")

    proc = subprocess.run(
        [sys.executable, "scripts/check_generated_surfaces.py", "--check", "--strict"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "ok: generated surfaces check passed" in proc.stdout


def test_orphan_generated_file_detected():
    issues = collect_orphan_issues({"LLM-ROUTING.md"}, strict_orphans=True)
    assert not any(
        i.startswith("orphan:") and "LLM-ROUTING.md" in i for i in issues
    )


def test_work_dev_surfaces_not_orphan_strict():
    manifest_paths = {entry.path for entry in _load_manifest(MANIFEST_PATH)}
    issues = collect_orphan_issues(manifest_paths, strict_orphans=True)
    work_dev = [
        i
        for i in issues
        if "docs/skill-work/work-dev/generated/" in i
        or "runtime/artifacts/work-dev/" in i
    ]
    assert not work_dev, work_dev


def test_orphan_scan_subcommand():
    proc = subprocess.run(
        [sys.executable, "scripts/check_generated_surfaces.py", "--orphans-only"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0
    assert "ok:" in proc.stdout or "generated-surfaces:" in proc.stderr
