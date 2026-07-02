from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "validate_speaker_memory_benchmark_family.py"

def load_module():
    spec = importlib.util.spec_from_file_location("validate_speaker_memory_benchmark_family", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def test_live_repo_shape_passes_structural_checks_except_known_subprocesses() -> None:
    mod = load_module()

    def fake_runner(argv: list[str], cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(argv, 0, stdout="ok", stderr="")

    result = mod.run_all_checks(command_runner=fake_runner)

    assert result["checks"][0]["ok"] is True
    assert result["checks"][1]["ok"] is True
    assert result["checks"][2]["ok"] is True
    assert result["checks"][5]["ok"] is True

def test_fixture_completeness_fails_when_required_file_missing(tmp_path: Path) -> None:
    mod = load_module()
    fixtures = tmp_path / "fixtures"
    fixture = fixtures / "sm-1-speaker-object-repair"
    fixture.mkdir(parents=True)
    for name in ("metadata.json", "prompt.md", "source-pack.md", "rubric.md"):
        (fixture / name).write_text("x", encoding="utf-8")

    check, fixture_ids = mod.check_fixture_completeness(fixtures)

    assert fixture_ids == ["sm-1-speaker-object-repair"]
    assert check.ok is False
    assert "expected-output-shape.md" in check.detail

def test_registry_consistency_fails_when_scorer_default_target_missing(tmp_path: Path) -> None:
    mod = load_module()
    fixtures = tmp_path / "fixtures"
    fixture = fixtures / "sm-9-example"
    fixture.mkdir(parents=True)
    (fixture / "metadata.json").write_text(
        json.dumps({"benchmark_id": "sm-9-example"}),
        encoding="utf-8",
    )

    class FakeScorer:
        DEFAULT_TARGETS = {}

    check, _ = mod.check_registry_consistency(FakeScorer, fixtures)

    assert check.ok is False
    assert "missing scorer default targets" in check.detail

def test_scorer_smoke_fails_when_weak_sample_passes(tmp_path: Path) -> None:
    mod = load_module()

    class FakeScorer:
        def build_score(self, run_dir: Path) -> dict:
            return {"closeout": "Held"}

    check = mod.check_scorer_smoke(FakeScorer(), ["sm-1-speaker-object-repair"])

    assert check.ok is False
    assert "expected Broke, got Held" in check.detail

def test_speaker_object_baseline_failure_propagates() -> None:
    mod = load_module()

    def fake_runner(argv: list[str], cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(argv, 1, stdout="", stderr="speaker validator failed")

    check = mod.check_speaker_object_baseline(fake_runner)

    assert check.ok is False
    assert check.detail == "speaker validator failed"

def test_portable_skill_verify_failure_propagates() -> None:
    mod = load_module()

    def fake_runner(argv: list[str], cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(argv, 1, stdout="", stderr="portable skill verify failed")

    check = mod.check_portable_skill_verify(fake_runner)

    assert check.ok is False
    assert check.detail == "portable skill verify failed"
