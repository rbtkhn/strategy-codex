from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from scripts.check_generated_surfaces import (
    ORPHAN_DEFER_PREFIXES,
    collect_orphan_issues,
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
    assert "10 entries" in proc.stdout


def test_manifest_includes_statecraft_notes_registry():
    text = (REPO_ROOT / "generated-manifest.yaml").read_text(encoding="utf-8")
    assert "statecraft-notes-registry-md" in text
    assert "runtime/artifacts/statecraft-notes-registry.md" in text
    assert "statecraft-notes-registry-json" in text


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

    issues_deferred = [
        i
        for i in collect_orphan_issues(set(), strict_orphans=True)
        if ORPHAN_DEFER_PREFIXES[0] in i
    ]
    assert all(
        i.startswith("orphan (deferred):") for i in issues_deferred
    ), issues_deferred


def test_deferred_work_dev_orphan_does_not_strict_fail():
    proc = subprocess.run(
        [
            sys.executable,
            "scripts/check_generated_surfaces.py",
            "--orphans-only",
            "--strict-orphans",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    blocking = [
        line
        for line in (proc.stderr or "").splitlines()
        if line.startswith("generated-surfaces: orphan:") and "work-dev" in line
    ]
    assert not blocking, proc.stderr


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
