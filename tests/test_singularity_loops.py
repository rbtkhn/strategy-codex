"""Tests for singularity loop registry pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_loop_registry as build_registry  # noqa: E402
import check_loop_registry as check_registry  # noqa: E402
import singularity_loop_lib as lib  # noqa: E402
from singularity_loop_invariants import run_singularity_loop_invariants  # noqa: E402


def test_build_registry_shape() -> None:
    payload = lib.build_registry_payload()
    assert len(payload["loops"]) == 5
    ids = {row["id"] for row in payload["loops"]}
    assert ids == {
        "innermost-loop-capture",
        "moonshots-synthesis-watch",
        "singularity-monthly-synthesis",
        "spine-health-check",
        "work-cici-daily-ops",
    }


def test_registry_and_check_pass_on_repo() -> None:
    assert build_registry.check_artifact(output_path=lib.DEFAULT_REGISTRY_OUTPUT) == 0
    assert check_registry.run_check() == 0


def test_duplicate_id_fails_invariants() -> None:
    rows = [
        {"id": "a", "source_file": "one.yaml", "dependencies": []},
        {"id": "a", "source_file": "two.yaml", "dependencies": []},
    ]
    issues = run_singularity_loop_invariants(rows)
    assert any("duplicate loop id" in line for line in issues)


def test_missing_dependency_fails_invariants() -> None:
    rows = [{"id": "a", "source_file": "one.yaml", "dependencies": [{"loop_id": "missing"}]}]
    issues = run_singularity_loop_invariants(rows)
    assert any("unknown dependency" in line for line in issues)


def test_build_registry_fails_on_bad_yaml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    loops_dir = tmp_path / "singularity" / "loops" / "research"
    loops_dir.mkdir(parents=True)
    (loops_dir / "bad.yaml").write_text(
        "loop:\n  id: bad-loop\n  category: research\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(lib, "LOOPS_DIR", tmp_path / "singularity" / "loops")

    with pytest.raises(ValueError):
        lib.build_registry_payload(loops_dir=tmp_path / "singularity" / "loops")


def test_refresh_and_brief_lists_attention() -> None:
    brief = lib.refresh_and_brief(source="tests/test_singularity_loops.py")
    assert brief is not None
    assert "attention:" in brief
    assert "innermost-loop-capture" in brief


def test_check_detects_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    out = tmp_path / "loop-registry.json"
    out.write_text(json.dumps({"loops": []}) + "\n", encoding="utf-8")
    monkeypatch.setattr(build_registry, "REPO_ROOT", tmp_path)
    assert build_registry.check_artifact(output_path=out) == 1
