"""Tests for scripts/operator_dashboard.py."""

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
from operator_dashboard import (  # noqa: E402
    DashboardRunConfig,
    build_umbrella_json,
    build_umbrella_markdown,
    load_child_payloads,
    main,
    run_all,
)
from operator_report_utils import Finding  # noqa: E402

FIXTURE_ROUTER = """\
## Router Index

| Transaction object | Crisis object | Use when | Primary lanes | Settlement spine | Entropy signal | Recursive utility |
| --- | --- | --- | --- | --- | --- | --- |
| [Hormuz Compact](../transactions/hormuz-transit-sanctions-relief-compact/) | Chokepoint transit insurance sanctions | Hormuz shipping sanctions | America, Iran | x | x | x |
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


def _setup_fixture_repo(tmp_path: Path, day: str) -> dict[str, Path]:
    (tmp_path / "docs").mkdir(parents=True)
    (tmp_path / "docs" / "ok.md").write_text("# OK\n", encoding="utf-8")

    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    slug = f"source-umbrella-test-{day}.md"
    source = day_dir / slug
    _write_archive(source)

    daily_dir = tmp_path / "statecraft" / "daily"
    daily_dir.mkdir(parents=True)
    daily_path = daily_dir / f"{day}.md"
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
                f"- [Umbrella test](../../source-archive/statecraft/{day}/{slug})",
                "",
            ]
        ),
        encoding="utf-8",
    )

    sheets_dir = tmp_path / "statecraft" / "sheets"
    sheets_dir.mkdir(parents=True)
    (sheets_dir / "transaction-router.md").write_text(FIXTURE_ROUTER, encoding="utf-8")

    queue_root = tmp_path / "runtime" / "artifacts" / "statecraft-intake-queue"
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
        "# Skill candidates\n\n## Log\n\n| Date | Working name | Trigger | Pointer |\n",
        encoding="utf-8",
    )

    return {"source": source, "daily_path": daily_path, "queue_root": queue_root}


@pytest.fixture()
def umbrella_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    day = "2026-06-28"
    paths = _setup_fixture_repo(tmp_path, day)
    monkeypatch.setattr(intake_queue, "QUEUE_ROOT", paths["queue_root"])
    monkeypatch.setattr("statecraft_war_room.QUEUE_ROOT", paths["queue_root"])
    monkeypatch.setattr("operator_dashboard.REPO_ROOT", tmp_path)
    return tmp_path, paths


def _artifact_paths(repo_root: Path) -> dict[str, Path]:
    base = repo_root / "runtime" / "artifacts"
    return {
        "surgeon_md": base / "repo-surgeon" / "latest.md",
        "surgeon_json": base / "repo-surgeon" / "latest.json",
        "war_room_md": base / "statecraft-war-room" / "latest.md",
        "war_room_json": base / "statecraft-war-room" / "latest.json",
        "deck_md": base / "operator-command-deck" / "latest.md",
        "deck_json": base / "operator-command-deck" / "latest.json",
        "umbrella_md": base / "operator-dashboard" / "latest.md",
        "umbrella_json": base / "operator-dashboard" / "latest.json",
    }


def test_run_all_writes_four_buckets(umbrella_env) -> None:
    repo_root, _paths = umbrella_env
    paths = _artifact_paths(repo_root)
    config = DashboardRunConfig(
        out=paths["umbrella_md"],
        json_out=paths["umbrella_json"],
        no_git=True,
    )
    result = run_all(repo_root, config)
    assert result.exit_code == 0
    for key in paths:
        assert paths[key].is_file(), key


def test_compose_only_builds_umbrella(umbrella_env) -> None:
    repo_root, _paths = umbrella_env
    paths = _artifact_paths(repo_root)
    surgeon_payload = {"status": "yellow", "blocking_count": 0, "warning_count": 1}
    war_room_payload = {
        "sync_status": "ok",
        "active_objects": [{"name": "Hormuz"}],
        "latest_archive_day": "2026-06-28",
    }
    deck_payload = {
        "posture": {
            "git_clean": True,
            "budget_stale": True,
            "surgeon_status": "yellow",
            "war_room_sync_status": "ok",
        },
        "next_actions": [
            {
                "priority": 1,
                "category": "context_budget",
                "action": "Refresh context budget",
                "source_path": "runtime/prepared-context/last-budget-builds.json",
            }
        ],
    }
    for key in ("surgeon_json", "war_room_json", "deck_json"):
        path = paths[key]
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"surgeon_json": surgeon_payload, "war_room_json": war_room_payload, "deck_json": deck_payload}[key]
        path.write_text(json.dumps(payload), encoding="utf-8")

    config = DashboardRunConfig(
        out=paths["umbrella_md"],
        json_out=paths["umbrella_json"],
        compose_only=True,
    )
    result = run_all(repo_root, config)
    assert result.exit_code == 0
    md = paths["umbrella_md"].read_text(encoding="utf-8")
    assert "Mode: runtime / derived" in md
    assert "Top Next Actions" in md
    assert "Refresh context budget" in md
    assert "runtime/artifacts/repo-surgeon/latest.md" in md


def test_umbrella_markdown_and_json_fields(umbrella_env) -> None:
    repo_root, _paths = umbrella_env
    config = DashboardRunConfig(no_git=True)
    surgeon = {"status": "green", "blocking_count": 0, "warning_count": 0}
    war_room = {"sync_status": "ok", "active_objects": [], "latest_archive_day": "2026-06-28"}
    deck = {
        "posture": {
            "git_clean": False,
            "budget_stale": False,
            "surgeon_status": "green",
            "war_room_sync_status": "ok",
        },
        "next_actions": [
            {
                "priority": 2,
                "category": "statecraft_intake",
                "action": "Promote queued intake",
                "source_path": "docs/statecraft-intake-queue.md",
            }
        ],
    }
    md = build_umbrella_markdown(
        surgeon,
        war_room,
        deck,
        generated_at="2099-01-01 00:00 UTC",
        repo_root=repo_root,
        config=config,
    )
    payload = build_umbrella_json(
        surgeon,
        war_room,
        deck,
        generated_at="2099-01-01 00:00 UTC",
        repo_root=repo_root,
        config=config,
    )
    assert "Authority: advisory only" in md
    assert "Promote queued intake" in md
    assert payload["authority"] == "runtime_derived"
    assert payload["next_actions"]
    assert "surgeon_md" in payload["child_paths"]


def test_fail_on_blocking_propagates_exit_code(umbrella_env, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root, _paths = umbrella_env
    paths = _artifact_paths(repo_root)

    blocking = Finding(
        severity="blocking",
        category="broken_link",
        message="missing SSOT link",
        file="docs/x.md",
    )

    def fake_surgeon(*_a, **kwargs):
        payload = {"status": "red", "blocking_count": 1, "warning_count": 0}
        out = kwargs.get("out") or kwargs.get("json_out")
        if out and str(out).endswith(".json"):
            path = out if out.is_absolute() else (repo_root / out)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload), encoding="utf-8")
        elif out:
            path = out if out.is_absolute() else (repo_root / out)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# surgeon\n", encoding="utf-8")
        if kwargs.get("fail_on_blocking"):
            return 1, payload
        return 0, payload

    monkeypatch.setattr("operator_dashboard.generate_surgeon_report", fake_surgeon)

    config = DashboardRunConfig(
        out=paths["umbrella_md"],
        json_out=paths["umbrella_json"],
        fail_on_blocking=True,
        no_git=True,
    )
    result = run_all(repo_root, config)
    assert result.exit_code == 1


def test_main_compose_only_cli(umbrella_env, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root, _paths = umbrella_env
    paths = _artifact_paths(repo_root)
    for name, payload in (
        ("surgeon_json", {"status": "green", "blocking_count": 0}),
        ("war_room_json", {"sync_status": "ok", "active_objects": []}),
        ("deck_json", {"next_actions": [], "posture": {"git_clean": True, "budget_stale": False}}),
    ):
        path = paths[name]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "operator_dashboard.py",
            "--compose-only",
            "--out",
            str(paths["umbrella_md"]),
            "--json-out",
            str(paths["umbrella_json"]),
        ],
    )
    assert main() == 0
    assert paths["umbrella_md"].is_file()


def test_load_child_payloads_missing_raises(umbrella_env) -> None:
    repo_root, _paths = umbrella_env
    config = DashboardRunConfig(
        compose_only=True,
        surgeon_json_out=Path("runtime/artifacts/repo-surgeon/missing.json"),
        war_room_json_out=Path("runtime/artifacts/statecraft-war-room/missing.json"),
        deck_json_out=Path("runtime/artifacts/operator-command-deck/missing.json"),
    )
    with pytest.raises(FileNotFoundError):
        load_child_payloads(repo_root, config)
