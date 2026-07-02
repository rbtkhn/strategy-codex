"""Canonical Record path helpers (repo_io)."""

import os
import shutil
import sys
import uuid
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from repo_io import (  # noqa: E402
    CANONICAL_EVIDENCE_BASENAME,
    CANONICAL_RECORD_FILES_REQUIRED,
    assert_canonical_record_layout,
    missing_canonical_record_files,
    profile_dir,
)

@pytest.fixture
def work_root():
    base = REPO / ".test-tmp" / "record-paths"
    root = base / uuid.uuid4().hex
    root.mkdir(parents=True)
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)

def test_constants_match_documented_triple():
    assert CANONICAL_RECORD_FILES_REQUIRED == (
        "self.md",
        "self-knowledge.md",
        CANONICAL_EVIDENCE_BASENAME,
        "recursion-gate.md",
    )

def test_grace_mar_instance_has_required_files():
    mid = missing_canonical_record_files("grace-mar")
    assert mid == [], f"missing: {mid}"

def test_assert_passes_for_grace_mar():
    assert_canonical_record_layout("grace-mar", context="test")

def test_assert_skipped_when_env_set(monkeypatch):
    monkeypatch.setenv("GRACE_MAR_SKIP_PATH_CHECK", "1")
    # fake user with no dir — should not raise
    assert_canonical_record_layout("nonexistent-user-xyz-12345", context="test")

def test_profile_dir_uses_repo_root_for_any_profile_id():
    assert profile_dir("__no_such_fork_dir__") == REPO

def test_assert_uses_repo_root_for_any_profile_id(monkeypatch):
    monkeypatch.delenv("GRACE_MAR_SKIP_PATH_CHECK", raising=False)
    assert_canonical_record_layout("__no_such_fork_dir__", context="test")

def test_assert_raises_when_required_file_missing(monkeypatch, work_root):
    monkeypatch.delenv("GRACE_MAR_SKIP_PATH_CHECK", raising=False)
    (work_root / "self.md").write_text("x", encoding="utf-8")
    (work_root / "self-knowledge.md").write_text("x", encoding="utf-8")
    (work_root / CANONICAL_EVIDENCE_BASENAME).write_text("x", encoding="utf-8")
    # recursion-gate.md missing

    import repo_io as ri

    monkeypatch.setattr(ri, "REPO_ROOT", work_root)

    with pytest.raises(RuntimeError, match="recursion-gate"):
        ri.assert_canonical_record_layout("tmpfork")
