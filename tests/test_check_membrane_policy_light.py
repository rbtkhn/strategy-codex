"""Tests for scripts/check_membrane_policy_light.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKER = REPO_ROOT / "scripts" / "check_membrane_policy_light.py"


def _load_mod():
    name = "check_membrane_policy_light_test_mod"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, CHECKER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_runtime_artifacts_with_canonical_phrase_flagged() -> None:
    mod = _load_mod()
    phrase = mod._line_claims_runtime_as_authoritative(
        "See runtime/artifacts/skill-cards/foo.json as canonical truth.\n"
    )
    assert phrase == "canonical"


def test_runtime_artifacts_with_negation_not_flagged() -> None:
    mod = _load_mod()
    phrase = mod._line_claims_runtime_as_authoritative(
        "runtime/artifacts/README.md — do not replace canonical skill files.\n"
    )
    assert phrase is None


def test_runtime_artifacts_without_authority_phrase_ok() -> None:
    mod = _load_mod()
    phrase = mod._line_claims_runtime_as_authoritative(
        "Rebuild from runtime/artifacts/skill-cards/foo.json when stale.\n"
    )
    assert phrase is None


def test_complement_allowed_examples_path() -> None:
    mod = _load_mod()
    assert mod._complement_rel_allowed("examples/foo.json")
    assert mod._complement_rel_allowed("README.md")
    assert not mod._complement_rel_allowed("stray/foo.json")


def test_complement_paths_flags_stray_file(tmp_path: Path, monkeypatch) -> None:
    mod = _load_mod()
    complements = tmp_path / "runtime" / "runtime-complements"
    complements.mkdir(parents=True)
    (complements / "README.md").write_text("# ok", encoding="utf-8")
    (complements / "stray").mkdir()
    (complements / "stray" / "leak.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(mod, "COMPLEMENTS_ROOT", complements)
    errors = mod.check_complement_paths()
    assert len(errors) == 1
    assert "stray/leak.json" in errors[0]


def test_repo_membrane_policy_light_passes() -> None:
    mod = _load_mod()
    errors = mod.run_checks()
    assert not errors, "\n".join(errors)
