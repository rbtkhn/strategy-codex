"""Tests for check_agent_turn_discipline.py."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def discipline_mod():
    path = REPO_ROOT / "scripts" / "check_agent_turn_discipline.py"
    name = "check_agent_turn_discipline"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )


def _assistant(*tool_blocks: dict) -> dict:
    content = [{"type": "text", "text": "working"}]
    for block in tool_blocks:
        content.append({"type": "tool_use", **block})
    return {"role": "assistant", "message": {"content": content}}


def test_clean_single_shell(discipline_mod, tmp_path: Path):
    p = tmp_path / "clean.jsonl"
    _write_jsonl(
        p,
        [
            _assistant({"name": "Shell", "input": {"command": "git status"}}),
        ],
    )
    report = discipline_mod.scan_transcript(p, last_turns=10)
    assert report.hard_count == 0


def test_parallel_shell(discipline_mod, tmp_path: Path):
    p = tmp_path / "parallel_shell.jsonl"
    _write_jsonl(
        p,
        [
            _assistant(
                {"name": "Shell", "input": {"command": "git status"}},
                {"name": "Shell", "input": {"command": "git diff"}},
            ),
        ],
    )
    report = discipline_mod.scan_transcript(p)
    assert any(v.rule_id == "parallel_shell" for v in report.violations)


def test_parallel_strreplace(discipline_mod, tmp_path: Path):
    p = tmp_path / "parallel_strreplace.jsonl"
    _write_jsonl(
        p,
        [
            _assistant(
                {"name": "StrReplace", "input": {"path": "a.md", "old_string": "x", "new_string": "y"}},
                {"name": "StrReplace", "input": {"path": "b.md", "old_string": "x", "new_string": "y"}},
            ),
        ],
    )
    report = discipline_mod.scan_transcript(p)
    assert any(v.rule_id == "parallel_strreplace" for v in report.violations)


def test_read_write_same_path(discipline_mod, tmp_path: Path):
    target = str(tmp_path / "foo.md")
    p = tmp_path / "rw.jsonl"
    _write_jsonl(
        p,
        [
            _assistant(
                {"name": "Read", "input": {"path": target}},
                {"name": "StrReplace", "input": {"path": target, "old_string": "a", "new_string": "b"}},
            ),
        ],
    )
    report = discipline_mod.scan_transcript(p)
    assert any(v.rule_id == "read_write_same_path" for v in report.violations)


def test_format_markdown_no_violations(discipline_mod, tmp_path: Path):
    p = tmp_path / "ok.jsonl"
    _write_jsonl(p, [_assistant({"name": "Read", "input": {"path": "x.md"}})])
    report = discipline_mod.scan_transcript(p)
    md = "\n".join(discipline_mod.format_markdown_lines(report))
    assert "## Agent turn discipline" in md
    assert "No parallel Shell" in md


def test_last_turns_window(discipline_mod, tmp_path: Path):
    p = tmp_path / "window.jsonl"
    rows = [_assistant({"name": "Read", "input": {"path": f"{i}.md"}}) for i in range(5)]
    rows.append(
        _assistant(
            {"name": "Shell", "input": {"command": "a"}},
            {"name": "Shell", "input": {"command": "b"}},
        )
    )
    _write_jsonl(p, rows)
    report = discipline_mod.scan_transcript(p, last_turns=1)
    assert report.assistant_turns_scanned == 1
    assert report.hard_count == 1
