"""Integration compute-ledger append helper."""

from __future__ import annotations

import json
import shutil
import sys
import uuid
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from emit_compute_ledger import append_integration_ledger  # noqa: E402


@pytest.fixture
def work_root() -> Path:
    base = REPO_ROOT / ".test-tmp" / "compute-ledger"
    root = base / uuid.uuid4().hex
    root.mkdir(parents=True)
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _ledger_path(root: Path) -> Path:
    return root / "compute-ledger.jsonl"


def test_append_integration_ledger_writes_line(work_root: Path) -> None:
    append_integration_ledger(
        "u1",
        operation="test_op",
        runtime="test_rt",
        success=True,
        wall_ms=10,
        bytes_processed=100,
        source_artifact_count=2,
        repo_root=work_root,
    )
    p = _ledger_path(work_root)
    assert p.is_file()
    assert not (work_root / "platform/users" / "u1").exists()
    line = p.read_text(encoding="utf-8").strip().splitlines()[-1]
    o = json.loads(line)
    assert o["operation"] == "test_op"
    assert o["bucket"] == "integration"
    assert o["success"] is True


def test_append_integration_ledger_task_fields(work_root: Path) -> None:
    append_integration_ledger(
        "u1",
        operation="export_with_task",
        runtime="openclaw",
        success=True,
        wall_ms=42,
        task_id="TASK-001",
        task_type="export",
        outcome_confidence=0.95,
        repo_root=work_root,
    )
    p = _ledger_path(work_root)
    line = p.read_text(encoding="utf-8").strip().splitlines()[-1]
    o = json.loads(line)
    assert o["task_id"] == "TASK-001"
    assert o["task_type"] == "export"
    assert o["outcome_confidence"] == 0.95
    assert o["operation"] == "export_with_task"


def test_append_integration_ledger_task_fields_omitted(work_root: Path) -> None:
    append_integration_ledger(
        "u1",
        operation="no_task",
        runtime="cli",
        success=True,
        wall_ms=1,
        repo_root=work_root,
    )
    p = _ledger_path(work_root)
    line = p.read_text(encoding="utf-8").strip().splitlines()[-1]
    o = json.loads(line)
    assert "task_id" not in o
    assert "task_type" not in o
    assert "outcome_confidence" not in o


def test_append_integration_ledger_outcome_confidence_clamped(work_root: Path) -> None:
    append_integration_ledger(
        "u1",
        operation="clamp_test",
        runtime="cli",
        success=True,
        wall_ms=1,
        outcome_confidence=1.5,
        repo_root=work_root,
    )
    p = _ledger_path(work_root)
    line = p.read_text(encoding="utf-8").strip().splitlines()[-1]
    o = json.loads(line)
    assert o["outcome_confidence"] == 1.0


def test_append_integration_ledger_env_tokens(work_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GRACE_MAR_INTEGRATION_PROMPT_TOKENS", "100")
    monkeypatch.setenv("GRACE_MAR_INTEGRATION_COMPLETION_TOKENS", "50")
    monkeypatch.setenv("GRACE_MAR_INTEGRATION_MODEL", "test-model")
    append_integration_ledger(
        "u1",
        operation="with_tokens",
        runtime="openclaw",
        success=True,
        wall_ms=1,
        repo_root=work_root,
    )
    p = _ledger_path(work_root)
    line = p.read_text(encoding="utf-8").strip().splitlines()[-1]
    o = json.loads(line)
    assert o["prompt_tokens"] == 100
    assert o["completion_tokens"] == 50
    assert o["total_tokens"] == 150
    assert o["model"] == "test-model"
    assert o["token_accounting"] == "env"
