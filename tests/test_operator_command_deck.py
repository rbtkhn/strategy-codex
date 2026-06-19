"""Tests for scripts/operator_command_deck.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import statecraft_intake_queue as intake_queue  # noqa: E402
from operator_report_utils import Finding  # noqa: E402
from operator_command_deck import (  # noqa: E402
    build_deck_context,
    build_json_payload,
    build_markdown,
    load_git_summary,
    main,
    rank_next_actions,
)

FIXTURE_ROUTER = """\
## Router Index

| Transaction object | Crisis object | Use when | Primary lanes | Settlement spine | Entropy signal | Recursive utility |
| --- | --- | --- | --- | --- | --- | --- |
| [Hormuz Compact](../transactions/hormuz-transit-sanctions-relief-compact/) | Chokepoint transit insurance sanctions | Hormuz shipping sanctions | America, Iran | x | x | x |
"""

GATE_FIXTURE = """\
# Recursion Gate (fixture)

### CANDIDATE-9999 (Fixture pending)
```yaml
status: pending
summary: fixture pending candidate for deck test
mind_category: knowledge
```
"""


def _write_archive(path: Path) -> None:
    day = path.stem[-10:]
    path.write_text(
        "\n".join(
            [
                "---",
                f"pub_date: '{day}'",
                "kind: transcript",
                "source_form: interview",
                "thread: marandi",
                "threads:",
                "  - marandi",
                "---",
                "# Body",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _setup_fixture_repo(tmp_path: Path, day: str, *, desync: bool = False) -> dict[str, Path]:
    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    slug = f"source-deck-test-{day}.md"
    source = day_dir / slug
    _write_archive(source)

    daily_dir = tmp_path / "statecraft" / "daily"
    daily_dir.mkdir(parents=True)
    daily_path = daily_dir / f"{day}.md"
    if desync:
        daily_path.write_text(
            f"# State Synthesis — {day}\n\nArchive checkpoint: **0**\n",
            encoding="utf-8",
        )
    else:
        daily_path.write_text(
            "\n".join(
                [
                    f"# State Synthesis — {day}",
                    "",
                    "## Executive Read",
                    "",
                    "Dominant object — **Hormuz chokepoint transit insurance sanctions relief**.",
                    "",
                    "Archive checkpoint: **1** source-bearing captures.",
                    f"- [Deck test](../../source-archive/statecraft/{day}/{slug})",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    sheets_dir = tmp_path / "statecraft" / "sheets"
    sheets_dir.mkdir(parents=True)
    (sheets_dir / "transaction-router.md").write_text(FIXTURE_ROUTER, encoding="utf-8")

    queue_root = tmp_path / "runtime" / "artifacts" / "statecraft-intake-queue"
    monkeypatch_queue = queue_root
    queue_day = queue_root / day
    queue_day.mkdir(parents=True)
    sidecar_path = queue_day / f"{slug[:-3]}.v1.json"
    sidecar_path.write_text(
        json.dumps(
            {
                "schema_version": "statecraft-intake-sidecar.v1",
                "source_path": f"source-archive/statecraft/{day}/{slug}",
                "synthesis_status": "queued",
                "transaction_candidate": True,
                "regions": ["Persia"],
                "non_canonical": True,
            }
        ),
        encoding="utf-8",
    )

    (tmp_path / "skills").mkdir(parents=True, exist_ok=True)
    (tmp_path / "skills" / "skill-candidates.md").write_text(
        "\n".join(
            [
                "# Skill candidates",
                "",
                "## Log",
                "",
                "| Date | Working name | Trigger | Pointer |",
                "|------|--------------|---------|---------|",
                "| 2026-06-01 | test-skill-draft | when testing | this thread |",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {
        "source": source,
        "daily_path": daily_path,
        "queue_root": monkeypatch_queue,
    }


@pytest.fixture()
def deck_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    day = "2026-06-27"
    paths = _setup_fixture_repo(tmp_path, day)
    monkeypatch.setattr(intake_queue, "QUEUE_ROOT", paths["queue_root"])
    monkeypatch.setattr("statecraft_war_room.QUEUE_ROOT", paths["queue_root"])
    return tmp_path, day, paths


def test_generates_deck_with_authority_header(deck_env) -> None:
    repo_root, day, _paths = deck_env
    ctx = build_deck_context(repo_root, include_git=False)
    actions = rank_next_actions(ctx, max_actions=5)
    md = build_markdown(ctx, actions, generated_at="2099-01-01 00:00 UTC")
    assert "Mode: runtime / derived" in md
    assert "Authority: advisory only" in md
    assert "## 2. Recommended Next Actions" in md
    assert actions


def test_blocking_surgeon_outranks_intake(deck_env, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root, _day, _paths = deck_env

    blocking = Finding(
        severity="blocking",
        category="broken_link",
        message="missing SSOT link",
        file="docs/x.md",
    )

    def fake_findings(*_a, **_k):
        return [blocking], {}

    monkeypatch.setattr("operator_command_deck.build_findings", fake_findings)
    ctx = build_deck_context(repo_root, include_git=False)
    actions = rank_next_actions(ctx, max_actions=5)
    assert actions
    assert actions[0].category == "repo_surgeon"
    assert actions[0].priority == 1


def test_desync_promotes_intake_action(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    day = "2026-06-28"
    paths = _setup_fixture_repo(tmp_path, day, desync=True)
    monkeypatch.setattr(intake_queue, "QUEUE_ROOT", paths["queue_root"])
    monkeypatch.setattr("statecraft_war_room.QUEUE_ROOT", paths["queue_root"])
    ctx = build_deck_context(tmp_path, include_git=False)
    assert ctx.war_room.sync_status == "desync"
    actions = rank_next_actions(ctx, max_actions=5)
    intake_actions = [a for a in actions if a.category == "intake"]
    assert intake_actions
    assert intake_actions[0].priority <= 3


def test_does_not_mutate_ssot_files(deck_env, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root, day, paths = deck_env
    gate_path = repo_root / "recursion-gate.md"
    gate_path.write_text(GATE_FIXTURE, encoding="utf-8")
    gate_before = gate_path.read_text(encoding="utf-8")
    source_before = paths["source"].read_text(encoding="utf-8")
    daily_before = paths["daily_path"].read_text(encoding="utf-8")

    out = repo_root / "runtime" / "artifacts" / "operator-command-deck" / "latest.md"
    json_out = repo_root / "runtime" / "artifacts" / "operator-command-deck" / "latest.json"
    monkeypatch.setattr("operator_command_deck.REPO_ROOT", repo_root)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "operator_command_deck.py",
            "--out",
            str(out),
            "--json-out",
            str(json_out),
            "--no-git",
        ],
    )
    assert main() == 0
    assert gate_path.read_text(encoding="utf-8") == gate_before
    assert paths["source"].read_text(encoding="utf-8") == source_before
    assert paths["daily_path"].read_text(encoding="utf-8") == daily_before


def test_json_schema_fields(deck_env) -> None:
    repo_root, _day, _paths = deck_env
    ctx = build_deck_context(repo_root, include_git=False)
    actions = rank_next_actions(ctx, max_actions=5)
    payload = build_json_payload(ctx, actions, generated_at="2099-01-01 00:00 UTC")
    for key in (
        "generated_at",
        "authority",
        "posture",
        "next_actions",
        "surgeon_summary",
        "war_room_summary",
        "git_summary",
        "budget_summary",
        "backlog_summary",
        "gate_summary",
    ):
        assert key in payload
    assert payload["gate_summary"] is None


def test_include_gate_off_by_default(deck_env) -> None:
    repo_root, _day, _paths = deck_env
    ctx = build_deck_context(repo_root, include_git=False, include_gate=False)
    assert ctx.gate_summary is None
    md = build_markdown(ctx, [], generated_at="2099-01-01 00:00 UTC")
    assert "Gate Watch" not in md


def test_include_gate_surfaces_pending(deck_env) -> None:
    repo_root, _day, _paths = deck_env
    gate_path = repo_root / "recursion-gate.md"
    gate_path.write_text(GATE_FIXTURE, encoding="utf-8")
    ctx = build_deck_context(repo_root, include_git=False, include_gate=True)
    assert ctx.gate_summary is not None
    assert ctx.gate_summary.get("pending_count", 0) >= 1
    md = build_markdown(ctx, rank_next_actions(ctx), generated_at="2099-01-01 00:00 UTC")
    assert "Gate Watch" in md


def test_no_git_when_flagged(deck_env) -> None:
    repo_root, _day, _paths = deck_env
    summary = load_git_summary(repo_root, enabled=False)
    assert summary.get("enabled") is False
    ctx = build_deck_context(repo_root, include_git=False)
    assert ctx.git_summary.get("enabled") is False


def test_handles_missing_budget_receipt(deck_env) -> None:
    repo_root, _day, _paths = deck_env
    ctx = build_deck_context(repo_root, include_git=False)
    assert ctx.budget_summary.get("stale") is True
    actions = rank_next_actions(ctx, max_actions=5)
    budget_actions = [a for a in actions if a.category == "context_budget"]
    assert budget_actions
