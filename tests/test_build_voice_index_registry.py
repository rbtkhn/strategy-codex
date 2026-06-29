#!/usr/bin/env python3
"""Tests for voice index registry generator."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_voice_index_registry as reg_cli  # noqa: E402
import voice_index_registry_core as core  # noqa: E402


def test_validate_yaml_code_exclusion_parity_passes_with_seed() -> None:
    registry = core.load_voice_index_registry_yaml()
    findings = core.validate_yaml_code_exclusion_parity(registry)
    assert any(f.code == "exception_registry" and f.level == "pass" for f in findings)


def test_validate_yaml_code_exclusion_parity_fails_when_missing() -> None:
    registry = {"schema_version": "1.0", "voices": {"pape": {"exclusions": ["ok"]}}}
    findings = core.validate_yaml_code_exclusion_parity(registry)
    assert any(f.level == "fail" and f.code == "exception_registry" for f in findings)


def test_build_voice_index_registry_check_missing_artifacts(tmp_path: Path, monkeypatch) -> None:
    md = tmp_path / "voice-index-parity.md"
    js = tmp_path / "voice-index-parity.json"
    monkeypatch.setattr(reg_cli, "REPO_ROOT", tmp_path)
    assert reg_cli.check_artifacts(md_path=md, json_path=js, archive_root=tmp_path / "arch") == 1


def test_render_registry_json_shape() -> None:
    row = core.VoiceRegistryRow(
        voice="sample",
        primary_index="statecraft/voices/sample/sample-index.md",
        listed_in_voices_router=True,
        builder="scripts/build_sample_index.py",
        audit_command="python scripts/audit_statecraft_archive_index.py --shelf-index sample",
        eligible_captures=1,
        indexed_captures=1,
        parity="pass",
        broken_links=0,
    )
    summary = core.build_summary([row])
    payload = json.loads(core.render_registry_json([row], summary))
    assert payload["summary"]["voices_discovered"] == 1
    assert payload["voices"][0]["voice"] == "sample"
