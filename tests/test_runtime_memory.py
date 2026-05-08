"""Tests for runtime-only memory payload builders."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from grace_mar.runtime import runtime_memory  # noqa: E402


def test_runtime_use_cases_list_the_expected_workflow_surfaces() -> None:
    names = [case["name"] for case in runtime_memory.RUNTIME_USE_CASES]
    assert names == [
        "session_start_briefing",
        "post_tool_context_capture",
        "decision_capture",
        "retrieval_miss_logging",
        "wrap_up_handoff",
    ]


def test_session_start_brief_reads_continuity_files(monkeypatch) -> None:
    contents = {
        (REPO_ROOT / "session-log.md").resolve(): "session log\nline 2\n",
        (REPO_ROOT / "recursion-gate.md").resolve(): "gate\nentry\n",
        (REPO_ROOT / "self-evidence.md").resolve(): "evidence\nentry\n",
        (REPO_ROOT / "docs/skill-work/work-dev/workspace.md").resolve(): "workspace\n",
        (REPO_ROOT / "docs/skill-work/work-dev/session-continuity-contract.md").resolve(): "continuity\n",
    }

    def fake_read_text(path: Path) -> str:
        return contents.get(path.resolve(), "")

    monkeypatch.setattr(runtime_memory, "_read_text", fake_read_text)

    brief = runtime_memory.build_session_start_brief(REPO_ROOT, instance_id="grace-mar", lane="work-dev", session_id="SES-1")

    assert brief["kind"] == "session_start_brief"
    assert brief["instance_id"] == "grace-mar"
    assert "# Runtime Session Brief" in brief["markdown"]
    assert "session-log.md" in brief["markdown"]
    assert "recursion-gate.md" in brief["markdown"]
    assert "self-evidence.md" in brief["markdown"]
    assert "workspace.md" in brief["markdown"]
    assert "session-continuity-contract.md" in brief["markdown"]


def test_get_briefing_renders_sections() -> None:
    brief = runtime_memory.get_briefing(
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


def test_standup_omits_session_events() -> None:
    standup = runtime_memory.standup(
        {
            "thinking": [{"body": "Keep the wedge small."}],
            "session_events": [{"body": "session_start at 09:00Z"}],
        },
        session_manifest={"session_id": "SES-20260507-002"},
    )

    assert "# Standup" in standup
    assert "## Thinking" in standup
    assert "## Session Events" not in standup


def test_capture_observation_has_fingerprint_and_session() -> None:
    obs = runtime_memory.capture_observation(
        "The search found the missing transcript.",
        instance_id="grace-mar",
        session_id="SES-20260507-001",
        lane="work-dev",
        metadata={"tool": "rg"},
        related_record_path="docs/runtime/memory-retrieval.md",
    )
    assert obs["instance_id"] == "grace-mar"
    assert obs["source"] == "observation"
    assert obs["session_id"] == "SES-20260507-001"
    assert obs["lane"] == "work-dev"
    assert obs["metadata"] == {"tool": "rg"}
    assert len(obs["fingerprint"]) == 64


def test_capture_tool_use_has_fingerprint_and_session() -> None:
    obs = runtime_memory.capture_tool_use(
        "The search found the missing transcript.",
        instance_id="grace-mar",
        session_id="SES-20260507-001",
        lane="work-dev",
        metadata={"tool": "rg"},
        related_record_path="docs/runtime/memory-retrieval.md",
    )
    assert obs["instance_id"] == "grace-mar"
    assert obs["source"] == "tool_use"
    assert obs["session_id"] == "SES-20260507-001"
    assert obs["lane"] == "work-dev"
    assert obs["metadata"] == {"tool": "rg"}
    assert len(obs["fingerprint"]) == 64


def test_capture_decision_and_brag_route_separately() -> None:
    decision = runtime_memory.capture_decision(
        "Use runtime-only Supabase memory.",
        instance_id="grace-mar",
        session_id="SES-20260507-002",
        lane="work-dev",
    )
    brag = runtime_memory.capture_brag(
        "Shipped the bridge scaffold.",
        instance_id="grace-mar",
        session_id="SES-20260507-002",
        lane="work-dev",
    )

    assert decision["source"] == "decision"
    assert decision["observation_type"] == "decision"
    assert brag["source"] == "brag"
    assert brag["observation_type"] == "brag"


def test_retrieval_miss_record_contains_context() -> None:
    miss = runtime_memory.log_retrieval_miss(
        "structured memory use cases",
        instance_id="grace-mar",
        surface="prepared_context",
        failure_class="scope_mismatch",
        session_id="SES-20260507-003",
        lane_or_context="work-dev",
        expected_target="docs/runtime/runtime-memory.md",
        notes="Search started in the bridge docs instead of the runtime docs.",
        related_paths=["docs/runtime-vs-record.md"],
        suggested_improvement="point the query at runtime docs first",
    )

    assert miss["instance_id"] == "grace-mar"
    assert miss["retrieval_surface"] == "prepared_context"
    assert miss["failure_class"] == "scope_mismatch"
    assert miss["related_paths"] == ["docs/runtime-vs-record.md"]
    assert miss["suggested_improvement"] == "point the query at runtime docs first"


def test_wrap_up_and_sync_receipt_shapes() -> None:
    wrap = runtime_memory.wrap_up(
        instance_id="grace-mar",
        session_id="SES-20260507-004",
        lane="work-dev",
        summary="Closed the runtime-memory wedge.",
        open_loops=["Push docs"],
        next_entrypoint="docs/runtime/runtime-memory.md",
    )
    legacy_wrap = runtime_memory.build_wrap_up_session(
        instance_id="grace-mar",
        session_id="SES-20260507-004",
        lane="work-dev",
        summary="Closed the runtime-memory wedge.",
        open_loops=["Push docs"],
        next_entrypoint="docs/runtime/runtime-memory.md",
    )
    receipt = runtime_memory.build_sync_receipt(
        "abc123",
        instance_id="grace-mar",
        surfaces=["self.md", "self-archive.md"],
        notes="Git merge propagated to runtime cache",
    )

    assert wrap["status"] == "ended"
    assert wrap["open_loops"] == ["Push docs"]
    assert legacy_wrap["summary"] == wrap["summary"]
    assert receipt["git_commit_sha"] == "abc123"
    assert receipt["surfaces"] == ["self.md", "self-archive.md"]
