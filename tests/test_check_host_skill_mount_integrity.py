from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


scrub = _load_module("scrub_skill_mojibake", SCRIPTS / "scrub_skill_mojibake.py")
integrity = _load_module(
    "check_host_skill_mount_integrity", SCRIPTS / "check_host_skill_mount_integrity.py"
)


def test_marker_count_detects_triple_encoded_em_dash() -> None:
    sample = "pipeline \u00c3\u0192\u00c6\u2019\u00c3\u00a2\u00e2\u0082\u00ac\u00e2\u0080\u009d not recall"
    assert scrub.marker_count(sample) > 0
    fixed = scrub.fix_mojibake(sample)
    assert scrub.marker_count(fixed) == 0
    assert "—" in fixed or "pipeline" in fixed


def test_live_skills_have_no_mojibake_markers() -> None:
    skills_dir = REPO_ROOT / ".cursor" / "skills"
    offenders = []
    for skill_file in sorted(skills_dir.glob("*/SKILL.md")):
        text = skill_file.read_text(encoding="utf-8")
        if scrub.marker_count(text):
            offenders.append(skill_file.parent.name)
    assert offenders == []


def test_collect_encoding_issues_clean_skill(tmp_path: Path) -> None:
    skill_dir = tmp_path / "demo-skill"
    skill_dir.mkdir()
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(
        "---\nname: demo-skill\ndescription: clean\n---\n\n# Demo\n",
        encoding="utf-8",
    )
    assert integrity.collect_encoding_issues(skill_file) == []


def test_collect_encoding_issues_flags_mojibake(tmp_path: Path) -> None:
    skill_dir = tmp_path / "bad-skill"
    skill_dir.mkdir()
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(
        "---\nname: bad-skill\ndescription: broken\n---\n\nBroken \u00c3\u0192\u00c2\u00a2 text\n",
        encoding="utf-8",
    )
    issues = integrity.collect_encoding_issues(skill_file)
    assert any(issue.kind == "encoding-mojibake" for issue in issues)
