"""Tests for Singularity action cards and loop run receipts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import append_singularity_loop_run as append_run  # noqa: E402
import check_singularity_loop_runs as check_runs  # noqa: E402
import validate_all_schemas as validate_schemas  # noqa: E402
from singularity_loop_lib import load_registry  # noqa: E402


@pytest.fixture
def registry_path() -> Path:
    return REPO_ROOT / "runtime" / "artifacts" / "loop-registry.json"


def test_append_writes_valid_jsonl(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    out = tmp_path / "runs.jsonl"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "append_singularity_loop_run.py",
            "--loop-id",
            "grace-gems-marketplace-ops",
            "--status",
            "planned",
            "--action-card",
            "singularity/action-cards/grace-gems-marketplace-ops/2026-07-01.md",
            "--output",
            str(out),
        ],
    )
    assert append_run.main() == 0
    line = out.read_text(encoding="utf-8").strip()
    row = json.loads(line)
    assert row["loop_id"] == "grace-gems-marketplace-ops"
    assert row["status"] == "planned"
    assert row["action_card"].endswith("2026-07-01.md")
    assert "timestamp" in row


def test_check_missing_file_exits_zero(tmp_path: Path) -> None:
    missing = tmp_path / "missing.jsonl"
    assert check_runs.run_check(runs_path=missing, registry_path=REPO_ROOT / "runtime/artifacts/loop-registry.json") == 0


def test_check_empty_file_exits_zero(tmp_path: Path, registry_path: Path) -> None:
    empty = tmp_path / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    assert check_runs.run_check(runs_path=empty, registry_path=registry_path) == 0


def test_check_known_loop_id(tmp_path: Path, registry_path: Path) -> None:
    runs = tmp_path / "runs.jsonl"
    runs.write_text(
        json.dumps(
            {
                "timestamp": "2026-07-01T12:00:00+00:00",
                "loop_id": "mountain-homestead-ops",
                "status": "planned",
                "action_card": "singularity/action-cards/mountain-homestead-ops/2026-07-01.md",
                "next_loop_ids": [],
                "source": "test",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    assert check_runs.run_check(runs_path=runs, registry_path=registry_path) == 0


def test_check_unknown_loop_id_fails(tmp_path: Path, registry_path: Path) -> None:
    runs = tmp_path / "runs.jsonl"
    runs.write_text(
        json.dumps(
            {
                "loop_id": "not-a-real-loop-id",
                "status": "planned",
                "action_card": "x.md",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    assert check_runs.run_check(runs_path=runs, registry_path=registry_path) == 1


def test_check_unknown_next_loop_id_fails(tmp_path: Path, registry_path: Path) -> None:
    runs = tmp_path / "runs.jsonl"
    runs.write_text(
        json.dumps(
            {
                "loop_id": "mountain-homestead-ops",
                "status": "planned",
                "action_card": "x.md",
                "next_loop_ids": ["not-a-real-loop-id"],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    assert check_runs.run_check(runs_path=runs, registry_path=registry_path) == 1


def test_done_without_proof_warns_not_fails(
    tmp_path: Path, registry_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    runs = tmp_path / "runs.jsonl"
    runs.write_text(
        json.dumps(
            {
                "loop_id": "mountain-homestead-ops",
                "status": "done",
                "action_card": "x.md",
                "next_loop_ids": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    assert check_runs.run_check(runs_path=runs, registry_path=registry_path) == 0
    captured = capsys.readouterr()
    assert "[warn]" in captured.out or "[warn]" in captured.err


def test_example_action_card_frontmatter_validates() -> None:
    card = REPO_ROOT / "singularity/action-cards/grace-gems-margin-policy-review/2026-07-01.md"
    registry = validate_schemas.load_registry()
    entry = registry["schemas"]["singularity_action_card"]
    lines, failed = validate_schemas.validate_entry("singularity_action_card", entry)
    assert not failed, "\n".join(lines)
    assert any("grace-gems-margin-policy-review/2026-07-01.md" in line for line in lines)


def test_registry_has_twenty_five_loops() -> None:
    registry = load_registry()
    assert len(registry.get("loops") or []) == 25
