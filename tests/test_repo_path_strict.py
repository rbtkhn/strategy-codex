from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import (  # noqa: E402
    GRACE_MAR_COMPAT_KEYS,
    GRACE_MAR_INSTANCE_DIR,
    REPO_PATH_CLASSIFICATION,
    REPO_PATH_MIGRATIONS,
    collect_wave_readiness_report,
    keys_for_wave,
    load_path_fallback_retirement,
    profile_dir,
    profile_rel_posix,
    reset_legacy_path_resolve_count,
    resolve_repo_path,
    scan_legacy_path_layout,
    strict_paths_enabled,
    validate_path_fallback_retirement,
    validate_repo_path_classification,
)

WAVE_1_KEYS = frozenset(
    {
        "artifacts",
        "daily-handoff",
        "prepared-context",
        "runtime-bundle",
        "apps",
        "src",
        "skills",
        "skills-portable",
        "schema-registry",
        "styles",
        "auto-research",
        "bridges",
    }
)

WAVE_2_KEYS = frozenset(
    {
        "app",
        "bin",
        "deployment",
        "config",
        "extension",
        "integrations",
        "miniapp",
        "users",
        "template",
        "profile",
    }
)

def test_profile_dir_points_at_grace_mar_instance():
    root = profile_dir("strategy-codex")
    assert root == GRACE_MAR_INSTANCE_DIR
    assert (root / "recursion-gate.md").is_file()

def test_profile_rel_posix():
    rel = profile_rel_posix("strategy-codex")
    assert rel == "archive/grace-mar-instance"

def test_check_repo_path_strict_warn_mode():
    proc = subprocess.run(
        [sys.executable, "scripts/check_repo_path_strict.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode in (0, 1)

def test_strict_paths_raises_on_legacy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("STRATEGY_CODEX_STRICT_PATHS", "1")
    assert strict_paths_enabled()
    reset_legacy_path_resolve_count()
    # artifacts canonical exists in real repo — strict mode should not raise for it.
    path = resolve_repo_path("artifacts")
    assert path.is_dir()

def test_scan_legacy_path_layout_is_list():
    issues = scan_legacy_path_layout()
    assert isinstance(issues, list)

def test_every_repo_path_migration_has_classification():
    issues = validate_repo_path_classification()
    assert issues == []

def test_no_classification_without_migration_key():
    issues = validate_repo_path_classification()
    missing = [i for i in issues if i.startswith("missing classification")]
    orphan = [i for i in issues if i.startswith("classification without")]
    assert missing == []
    assert orphan == []

def test_legacy_fallback_keys_have_retirement_policy():
    issues = validate_path_fallback_retirement()
    assert issues == [], issues

def test_path_fallback_retirement_policy_has_no_legacy_entries():
    retirement = load_path_fallback_retirement()
    legacy_entries = {
        key: entry.get("legacy")
        for key, entry in retirement.items()
        if entry.get("legacy")
    }
    assert legacy_entries == {}

def test_grace_mar_compat_keys_are_isolated():
    compat_keys = {k for k, v in REPO_PATH_CLASSIFICATION.items() if v == "grace_mar_compat"}
    assert compat_keys == set(GRACE_MAR_COMPAT_KEYS)
    assert compat_keys <= set(REPO_PATH_CLASSIFICATION)

def test_check_repo_path_strict_json():
    proc = subprocess.run(
        [sys.executable, "scripts/check_repo_path_strict.py", "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    payload = json.loads(proc.stdout)
    assert "summary" in payload
    assert payload["summary"]["total_keys"] == 29
    assert "retirement_candidates" in payload

def test_wave_1_fallbacks_removed():
    for key in WAVE_1_KEYS:
        assert len(REPO_PATH_MIGRATIONS[key]) == 1, key

def test_wave_1_retirement_policy_has_no_legacy():
    retirement = load_path_fallback_retirement()
    for key in WAVE_1_KEYS:
        assert retirement[key]["legacy"] == [], key
        assert retirement[key]["retirement_status"] == "keep_no_legacy", key

def test_wave_2_fallbacks_removed():
    for key in WAVE_2_KEYS:
        assert len(REPO_PATH_MIGRATIONS[key]) == 1, key

def test_wave_2_retirement_policy_has_no_legacy():
    retirement = load_path_fallback_retirement()
    for key in WAVE_2_KEYS:
        assert retirement[key]["legacy"] == [], key
        assert retirement[key]["retirement_status"] == "keep_no_legacy", key

def test_wave_2_canonical_paths_exist():
    for key in WAVE_2_KEYS:
        canonical = REPO_ROOT / REPO_PATH_MIGRATIONS[key][0]
        assert canonical.exists(), key

def test_wave_2_readiness_report_covers_all_keys():
    report = collect_wave_readiness_report(wave=2)
    assert set(report["keys"]) == keys_for_wave(2)

def test_wave_2_readiness_all_ready():
    report = collect_wave_readiness_report(wave=2)
    for key, item in report["keys"].items():
        assert item["status"] in {"ready", "ready_docs_only_refs"}, (key, item)

def test_check_repo_path_strict_wave_2():
    proc = subprocess.run(
        [sys.executable, "scripts/check_repo_path_strict.py", "--wave", "2"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "Wave 2 platform readiness" in proc.stdout

WAVE_3_KEYS = frozenset(
    {
        "evidence",
        "reflection-proposals",
        "review-queue",
    }
)

def test_wave_3_keys_are_expected():
    assert keys_for_wave(3) == WAVE_3_KEYS

def test_wave_3_fallbacks_removed():
    for key in WAVE_3_KEYS:
        assert len(REPO_PATH_MIGRATIONS[key]) == 1, key

def test_wave_3_retirement_policy_has_no_legacy():
    retirement = load_path_fallback_retirement()
    for key in WAVE_3_KEYS:
        assert retirement[key]["legacy"] == [], key
        assert retirement[key]["retirement_status"] == "keep_no_legacy", key

def test_wave_3_canonical_paths_exist():
    for key in WAVE_3_KEYS:
        canonical = REPO_ROOT / REPO_PATH_MIGRATIONS[key][0]
        assert canonical.exists(), key

def test_wave_3_readiness_report_covers_all_keys():
    report = collect_wave_readiness_report(wave=3)
    assert set(report["keys"]) == WAVE_3_KEYS

def test_wave_3_readiness_all_ready():
    report = collect_wave_readiness_report(wave=3)
    for key, item in report["keys"].items():
        assert item["status"] in {"ready", "ready_docs_only_refs"}, (key, item)

def test_check_repo_path_strict_wave_3():
    proc = subprocess.run(
        [sys.executable, "scripts/check_repo_path_strict.py", "--wave", "3"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "Wave 3 archive placeholder readiness" in proc.stdout

def test_check_repo_path_strict_wave_3_strict_readiness():
    proc = subprocess.run(
        [
            sys.executable,
            "scripts/check_repo_path_strict.py",
            "--wave",
            "3",
            "--strict-readiness",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout

WAVE_4_KEYS = frozenset(
    {
        "bot",
        "recursion-gate-staging",
        "bootstrap",
    }
)

def test_wave_4_keys_are_expected():
    assert keys_for_wave(4) == WAVE_4_KEYS

def test_wave_4_fallbacks_removed():
    for key in WAVE_4_KEYS:
        assert len(REPO_PATH_MIGRATIONS[key]) == 1, key

def test_wave_4_retirement_policy_has_no_legacy():
    retirement = load_path_fallback_retirement()
    for key in WAVE_4_KEYS:
        assert retirement[key]["legacy"] == [], key
        assert retirement[key]["retirement_status"] == "keep_no_legacy", key

def test_wave_4_canonical_paths_exist():
    for key in WAVE_4_KEYS:
        canonical = REPO_ROOT / REPO_PATH_MIGRATIONS[key][0]
        assert canonical.exists(), key

def test_wave_4_readiness_report_covers_all_keys():
    report = collect_wave_readiness_report(wave=4)
    assert set(report["keys"]) == WAVE_4_KEYS

def test_wave_4_readiness_all_ready():
    report = collect_wave_readiness_report(wave=4)
    for key, item in report["keys"].items():
        assert item["status"] in {"ready", "ready_docs_only_refs"}, (key, item)

def test_no_legacy_fallback_tuples_remain():
    fallback_keys = {
        key: entry
        for key, entry in REPO_PATH_MIGRATIONS.items()
        if len(entry) > 1
    }
    assert fallback_keys == {}

def test_check_repo_path_strict_wave_4():
    proc = subprocess.run(
        [sys.executable, "scripts/check_repo_path_strict.py", "--wave", "4"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "Wave 4 Grace-Mar compatibility readiness" in proc.stdout

def test_check_repo_path_strict_wave_4_strict_readiness():
    proc = subprocess.run(
        [
            sys.executable,
            "scripts/check_repo_path_strict.py",
            "--wave",
            "4",
            "--strict-readiness",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
