"""Tests for structured MCP memory routing and briefing helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "platform/src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from grace_mar import structured_memory  # noqa: E402

def test_route_capture_explicit_hint_wins() -> None:
    route = structured_memory.route_capture_surface("ignored text", surface_hint="decisions")
    assert route.surface_key == "decisions"
    assert route.legacy_surface_key == "governed_state"
    assert route.reason == "explicit surface hint"

def test_route_capture_accepts_legacy_hint_aliases() -> None:
    route = structured_memory.route_capture_surface("ignored text", surface_hint="prepared_context")
    assert route.surface_key == "thinking"
    assert route.legacy_surface_key == "prepared_context"

def test_route_capture_heuristic_prefers_goals() -> None:
    route = structured_memory.route_capture_surface(
        "Our north star is to finish the migration and keep the objective visible."
    )
    assert route.surface_key == "north_star"
    assert route.legacy_surface_key == "governed_state"
    assert route.reason.startswith("heuristic keyword match")

def test_route_capture_defaults_to_thinking() -> None:
    route = structured_memory.route_capture_surface("A vague note without obvious signals.")
    assert route.surface_key == "thinking"
    assert route.legacy_surface_key == "prepared_context"

def test_build_capture_record_uses_title_and_compatibility() -> None:
    record = structured_memory.build_capture_record(
        "We decided to keep the user-facing API stable.",
        surface_hint=None,
        user_id="grace-mar",
        session_id="SES-20260507-001",
        source_tool="capture_decision",
    )
    assert record["surface_key"] == "decisions"
    assert record["legacy_surface_key"] == "governed_state"
    assert record["session_id"] == "SES-20260507-001"
    assert record["title"]
    assert record["body"].startswith("We decided")

def test_build_tool_payload_accepts_capture_observation() -> None:
    payload = structured_memory.build_tool_payload(
        "capture_observation",
        user_id="grace-mar",
        session_id="SES-20260507-001",
        text="A runtime observation worth keeping.",
        metadata={"source": "rg"},
    )
    assert payload["tool"] == "capture_observation"
    assert payload["surface_key"] == "thinking"
    assert payload["legacy_surface_key"] == "prepared_context"
    assert payload["session_id"] == "SES-20260507-001"

def test_build_session_event_maps_legacy_surface() -> None:
    event = structured_memory.build_session_event(
        "prompt_submit",
        user_id="grace-mar",
        session_id="SES-20260507-001",
        text="Prompt submitted for review.",
        payload={"prompt_id": "P-1"},
        source_tool="bridge",
    )
    assert event["surface_key"] == "session_events"
    assert event["legacy_surface_key"] == "prepared_context"
    assert event["event_type"] == "prompt_submit"
    assert event["payload"] == {"prompt_id": "P-1"}

def test_get_briefing_renders_sections() -> None:
    brief = structured_memory.get_briefing(
        {
            "north_star": [{"title": "Goal", "body": "Finish the memory bridge."}],
            "active_projects": [{"body": "Wire the session lifecycle hooks."}],
            "decisions": [{"body": "Keep the old path compatible."}],
            "brags": [{"body": "Shipped the first scaffold."}],
            "thinking": [{"body": "Need a clean routing contract."}],
            "session_events": [{"body": "session_start at 09:00Z"}],
        },
        session_manifest={
            "session_id": "SES-20260507-001",
            "fork_id": "grace-mar",
            "started_at": "2026-05-07T09:00:00Z",
            "ended_at": "",
        },
    )
    assert "# Briefing" in brief
    assert "## Session" in brief
    assert "## North Star" in brief
    assert "## Active Projects" in brief
    assert "## Decisions" in brief
    assert "## Brags" in brief
    assert "## Thinking" in brief
    assert "## Session Events" in brief
    assert "north_star / active_projects / decisions -> governed_state" in brief

def test_standup_is_compact() -> None:
    standup = structured_memory.standup(
        {"thinking": [{"body": "Keep the wedge small."}]},
        session_manifest={"session_id": "SES-20260507-002"},
    )
    assert "# Standup" in standup
    assert "## Next Step" in standup
    assert "Compact" not in standup

def test_start_and_wrap_use_fork_lifecycle(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[str, tuple, dict]] = []
    repo_root = REPO_ROOT / ".structured-memory-test"

    def fake_begin(repo_root: Path, fork_id: str, *, channel: str = "operator") -> dict[str, str]:
        calls.append(("begin", (repo_root, fork_id), {"channel": channel}))
        return {"session_id": "SES-20260507-003"}

    def fake_end(
        repo_root: Path,
        fork_id: str,
        session_id: str,
        *,
        drift_score_after: float | None = None,
        git_commit: str = "",
    ) -> dict[str, str]:
        calls.append(
            (
                "end",
                (repo_root, fork_id, session_id),
                {"drift_score_after": drift_score_after, "git_commit": git_commit},
            )
        )
        return {"session_id": session_id, "git_commit": git_commit}

    monkeypatch.setattr(structured_memory.fork_lifecycle, "begin_session", fake_begin)
    monkeypatch.setattr(structured_memory.fork_lifecycle, "end_session", fake_end)

    started = structured_memory.start_session(repo_root, "grace-mar", channel="bridge")
    wrapped = structured_memory.wrap_up(
        repo_root,
        "grace-mar",
        "SES-20260507-003",
        drift_score_after=0.25,
        git_commit="abc123",
    )

    assert started["session_id"] == "SES-20260507-003"
    assert wrapped["git_commit"] == "abc123"
    assert calls[0][0] == "begin"
    assert calls[0][2]["channel"] == "bridge"
    assert calls[1][0] == "end"
    assert calls[1][2]["git_commit"] == "abc123"
