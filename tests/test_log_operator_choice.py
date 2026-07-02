"""Tests for scripts/log_operator_choice.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import log_operator_choice as loc  # noqa: E402
import repo_io  # noqa: E402

@pytest.fixture
def user_profile(tmp_path, monkeypatch):
    user_dir = tmp_path / "platform/users" / "test-user"
    user_dir.mkdir(parents=True)
    monkeypatch.setattr(repo_io, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(repo_io, "profile_dir", lambda uid: user_dir)
    return user_dir

def test_append_work_choice_creates_block(user_profile):
    p = loc.append_work_choice(
        "test-user",
        context="WORK",
        picked="A",
        tags="~15m",
        note="gate pass",
    )
    assert p.is_file()
    text = p.read_text(encoding="utf-8")
    assert "[WORK-choice]" in text
    assert "context: WORK" in text
    assert "picked: A" in text
    assert "tags: ~15m" in text
    assert "gate pass" in text

def test_append_second_choice_preserves_first(user_profile):
    loc.append_work_choice("test-user", context="DAILY", picked="1", tags="", note="")
    loc.append_work_choice("test-user", context="WORK", picked="B", tags="", note="")
    text = (user_profile / "session-transcript.md").read_text(encoding="utf-8")
    assert text.count("### [WORK-choice]") == 2

def test_append_coffee_context(user_profile):
    loc.append_work_choice("test-user", context="COFFEE", picked="E", tags="steward=gate", note="")
    text = (user_profile / "session-transcript.md").read_text(encoding="utf-8")
    assert "context: COFFEE" in text
    assert "picked: E" in text
