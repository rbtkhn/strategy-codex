"""Tests for Agent Handoff Queue validator."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check_agent_handoff_queue.py"


def run_checker(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def _write_item(queue_root: Path, status_dir: str, filename: str, body: str) -> Path:
    dest_dir = queue_root / status_dir
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / filename
    path.write_text(body, encoding="utf-8")
    return path


MINIMAL_TODO = """---
id: ahq-20260630-999
title: Minimal todo
status: agent_todo
owner: codex
requester: operator
created_at: 2026-06-30T12:00:00Z
membrane_class: instrumental_work
context:
  - AGENTS.md
definition_of_done:
  - done
receipt_required: true
---

# Minimal
"""


def test_queue_checker_runs_on_repo_samples():
    proc = run_checker()
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_queue_checker_strict_runs_on_repo_samples():
    proc = run_checker("--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_queue_checker_json_runs():
    proc = run_checker("--json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "ok"
    assert payload["items"] >= 2
    assert "errors" in payload
    assert "warnings" in payload


def test_missing_core_field_fails(tmp_path: Path):
    body = MINIMAL_TODO.replace("owner: codex\n", "")
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "agent-todo", "ahq-20260630-999-minimal.md", body)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT))
    assert proc.returncode != 0
    assert "owner" in proc.stderr


def test_invalid_status_fails(tmp_path: Path):
    body = MINIMAL_TODO.replace("status: agent_todo", "status: bogus")
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "agent-todo", "ahq-20260630-999-minimal.md", body)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT))
    assert proc.returncode != 0
    assert "invalid status" in proc.stderr


def test_directory_status_mismatch_fails(tmp_path: Path):
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "agent-done", "ahq-20260630-999-minimal.md", MINIMAL_TODO)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT))
    assert proc.returncode != 0
    assert "must live under" in proc.stderr


def test_agent_done_without_receipt_fails(tmp_path: Path):
    body = MINIMAL_TODO.replace("status: agent_todo", "status: agent_done")
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "agent-done", "ahq-20260630-999-minimal.md", body)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT))
    assert proc.returncode != 0
    assert "receipt" in proc.stderr


def test_needs_input_without_blocking_question_fails(tmp_path: Path):
    body = MINIMAL_TODO.replace("status: agent_todo", "status: needs_input")
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "needs-input", "ahq-20260630-999-minimal.md", body)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT))
    assert proc.returncode != 0
    assert "blocking_question" in proc.stderr


def test_gate_required_without_gate_fails(tmp_path: Path):
    body = MINIMAL_TODO.replace("status: agent_todo", "status: gate_required")
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "gate-required", "ahq-20260630-999-minimal.md", body)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT))
    assert proc.returncode != 0
    assert "gate" in proc.stderr


def test_void_without_void_reason_fails(tmp_path: Path):
    body = MINIMAL_TODO.replace("status: agent_todo", "status: void")
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "void", "ahq-20260630-999-minimal.md", body)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT))
    assert proc.returncode != 0
    assert "void_reason" in proc.stderr


def test_id_filename_mismatch_fails(tmp_path: Path):
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "agent-todo", "wrong-name.md", MINIMAL_TODO)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT))
    assert proc.returncode != 0
    assert "filename must start with id" in proc.stderr


def test_empty_status_block_fails(tmp_path: Path):
    body = MINIMAL_TODO.replace(
        "status: agent_todo",
        "status: needs_input\nblocking_question: {}",
    )
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "needs-input", "ahq-20260630-999-minimal.md", body)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT))
    assert proc.returncode != 0
    assert "blocking_question" in proc.stderr


def test_recommended_fields_warn_default_passes(tmp_path: Path):
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "agent-todo", "ahq-20260630-999-minimal.md", MINIMAL_TODO)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT))
    assert proc.returncode == 0
    assert "warning:" in proc.stderr
    assert "allowed_actions" in proc.stderr


def test_glance_shows_open_section():
    proc = run_checker("--glance")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Agent handoff queue (open)" in proc.stdout


def test_recommended_fields_fail_strict(tmp_path: Path):
    queue_root = tmp_path / "queue"
    _write_item(queue_root, "agent-todo", "ahq-20260630-999-minimal.md", MINIMAL_TODO)
    proc = run_checker("--queue-root", str(queue_root), "--repo-root", str(REPO_ROOT), "--strict")
    assert proc.returncode != 0
    assert "allowed_actions" in proc.stderr
