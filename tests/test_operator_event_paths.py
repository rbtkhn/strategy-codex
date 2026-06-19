"""Tests for operator ledger and dream handoff path resolvers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from repo_io import (  # noqa: E402
    LAST_DREAM_BASENAME,
    last_dream_write_path,
    operator_ledger_write_path,
    profile_dir,
    resolve_last_dream_path,
    resolve_ledger_path,
)


@pytest.fixture
def isolated_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    import repo_io

    monkeypatch.setattr(repo_io, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(repo_io, "OPERATOR_EVENTS_DIR", tmp_path / "runtime" / "operator-events")
    monkeypatch.setattr(repo_io, "DEFAULT_USERS_DIR", tmp_path / "platform/users")
    return tmp_path


def test_resolve_ledger_prefers_operator_events(isolated_root: Path) -> None:
    root = profile_dir("strategy-codex")
    legacy = root / "pipeline-events.jsonl"
    legacy.write_text('{"event":"staged"}\n', encoding="utf-8")
    new_dir = isolated_root / "runtime" / "operator-events"
    new_dir.mkdir(parents=True)
    new = new_dir / "pipeline-events.jsonl"
    new.write_text('{"event":"applied"}\n', encoding="utf-8")
    assert resolve_ledger_path("strategy-codex", "pipeline-events.jsonl") == new


def test_resolve_ledger_fallback_root(isolated_root: Path) -> None:
    root = profile_dir("strategy-codex")
    legacy = root / "merge-receipts.jsonl"
    legacy.write_text('{"merged_at":"2026-01-01"}\n', encoding="utf-8")
    assert resolve_ledger_path("strategy-codex", "merge-receipts.jsonl") == legacy


def test_operator_ledger_write_path_creates_dir(isolated_root: Path) -> None:
    p = operator_ledger_write_path("strategy-codex", "cadence-learning-events.jsonl")
    assert p.parent.is_dir()
    assert p == isolated_root / "runtime" / "operator-events" / "cadence-learning-events.jsonl"


def test_last_dream_prefers_daily_handoff(isolated_root: Path) -> None:
    root = profile_dir("strategy-codex")
    handoff = root / "runtime/daily-handoff" / LAST_DREAM_BASENAME
    handoff.parent.mkdir(parents=True)
    handoff.write_text(json.dumps({"ok": True}), encoding="utf-8")
    root_legacy = root / LAST_DREAM_BASENAME
    root_legacy.write_text(json.dumps({"ok": False}), encoding="utf-8")
    assert resolve_last_dream_path("strategy-codex") == handoff


def test_last_dream_write_path(isolated_root: Path) -> None:
    p = last_dream_write_path("strategy-codex")
    assert p == isolated_root / "runtime/daily-handoff" / LAST_DREAM_BASENAME
    assert p.parent.is_dir()
