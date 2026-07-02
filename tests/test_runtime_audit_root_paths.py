"""Runtime/export audit writers use the repo-root profile contract."""

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

import export_runtime_bundle as erb  # noqa: E402
import harness_events as he  # noqa: E402

@pytest.fixture
def work_root() -> Path:
    base = REPO_ROOT / ".test-tmp" / "runtime-audit-root-paths"
    root = base / uuid.uuid4().hex
    root.mkdir(parents=True)
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)

def test_harness_event_appends_under_operator_events(work_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import repo_io

    monkeypatch.setattr(he, "REPO_ROOT", work_root)
    monkeypatch.setattr(repo_io, "REPO_ROOT", work_root)
    monkeypatch.setattr(repo_io, "OPERATOR_EVENTS_DIR", work_root / "runtime" / "operator-events")

    he.append_harness_event("strategy-codex", "unit", "root_write", path=str(work_root))

    path = work_root / "runtime" / "operator-events" / "harness-events.jsonl"
    assert path.is_file()
    assert not (work_root / "platform/users" / "strategy-codex").exists()
    row = json.loads(path.read_text(encoding="utf-8").strip())
    assert row["fork_id"] == "strategy-codex"
    assert row["harness_id"] == "unit"

def test_runtime_bundle_defaults_to_root_bundle_dir(work_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(erb, "REPO_ROOT", work_root)

    assert erb._profile_dir("strategy-codex") == work_root
    assert erb._default_output_dir("strategy-codex") == work_root / "runtime/bundle"
    assert not (work_root / "platform/users" / "strategy-codex").exists()
