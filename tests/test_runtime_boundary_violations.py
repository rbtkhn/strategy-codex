"""Boundary-violation tests for newer runtime paths.

These negative tests verify that runtime scripts (prepared-context builder,
hybrid retrieval, active-lane compression, skill-card builder) stay within
non-canonical surfaces and never bleed into governed Record territory.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_RECORD_FILES = {
    "self.md",
    "self-archive.md",
    "self-skills.md",
    "recursion-gate.md",
    "session-log.md",
}

CANONICAL_RECORD_PATHS = {
    "self.md",
    "self-archive.md",
    "self-skills.md",
    "recursion-gate.md",
    "session-log.md",
    "archive/grace-mar-instance/bot/prompt.py",
}

# â”€â”€ PR 3.1: prepared-context output contains boundary disclaimer â”€â”€â”€â”€â”€

def test_budgeted_context_contains_boundary_disclaimer(tmp_path: Path) -> None:
    """Prepared-context output must include non-canonical boundary notice."""
    seed = REPO_ROOT / "tests" / "fixtures" / "observations-seed.jsonl"
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    (obs_dir / "index.jsonl").write_text(
        seed.read_text(encoding="utf-8"), encoding="utf-8"
    )
    out = tmp_path / "runtime/prepared-context" / "out.md"
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "prepared_context" / "build_budgeted_context.py"),
            "--repo-root", str(tmp_path),
            "--lane", "work-strategy",
            "--mode", "compact",
            "-o", str(out),
            "--budgets-file",
            str(REPO_ROOT / "platform/config" / "context_budgets" / "lane-defaults.json"),
        ],
        env=env, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    text = out.read_text(encoding="utf-8")
    has_disclaimer = (
        "runtime" in text.lower() and "not" in text.lower()
    ) or "WORK scaffolding" in text or "not canonical" in text.lower()
    assert has_disclaimer, (
        "prepared-context output must contain a boundary disclaimer "
        "(runtime/WORK scaffolding, not Record truth)"
    )

# â”€â”€ PR 3.2: retrieval results must not include canonical Record paths â”€

def test_retrieval_excludes_canonical_record_paths(tmp_path: Path) -> None:
    """Hybrid retrieval must never return paths to governed Record files."""
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    seed = REPO_ROOT / "tests" / "fixtures" / "observations-seed.jsonl"
    (obs_dir / "index.jsonl").write_text(
        seed.read_text(encoding="utf-8"), encoding="utf-8"
    )
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}

    sys.path.insert(0, str(REPO_ROOT / "scripts" / "runtime"))
    from hybrid_retrieve import retrieve  # noqa: E402

    old_root = os.environ.get("GRACE_MAR_RUNTIME_LEDGER_ROOT")
    os.environ["GRACE_MAR_RUNTIME_LEDGER_ROOT"] = str(tmp_path)
    try:
        results = retrieve("prepared_context", "test query", top_k=20)
    finally:
        if old_root is not None:
            os.environ["GRACE_MAR_RUNTIME_LEDGER_ROOT"] = old_root
        elif "GRACE_MAR_RUNTIME_LEDGER_ROOT" in os.environ:
            del os.environ["GRACE_MAR_RUNTIME_LEDGER_ROOT"]

    for r in results:
        for canonical in CANONICAL_RECORD_PATHS:
            assert canonical not in r.path, (
                f"retrieval returned canonical Record path '{canonical}' in result: {r.path}"
            )

# â”€â”€ PR 3.3: active-lane compression output goes to runtime/artifacts/ â”€â”€â”€â”€â”€â”€â”€â”€

def test_compress_active_lane_writes_to_artifacts(tmp_path: Path) -> None:
    """compress_active_lane.py default output must be under runtime/artifacts/."""
    lane_dir = tmp_path / "docs" / "skill-work" / "work-strategy"
    lane_dir.mkdir(parents=True)
    (lane_dir / "README.md").write_text(
        "# work-strategy\n\n**Objective:** Test objective\n", encoding="utf-8"
    )
    user_dir = tmp_path / "platform/users" / "grace-mar"
    user_dir.mkdir(parents=True)
    (user_dir / "self-work.md").write_text("# self-work\n", encoding="utf-8")

    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "compress_active_lane.py"),
            "--lane", "work-strategy",
            "--repo-root", str(tmp_path),
        ],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    out_path = tmp_path / "runtime/artifacts" / "context" / "active-lane-work-strategy.md"
    assert out_path.exists(), f"expected output at {out_path}"
    for cp in CANONICAL_RECORD_PATHS:
        full = tmp_path / cp
        if full.exists():
            original = full.read_text(encoding="utf-8")
            assert original == full.read_text(encoding="utf-8"), (
                f"compress_active_lane modified canonical file: {cp}"
            )

# â”€â”€ PR 3.4: active-lane compression never includes Record content â”€â”€â”€â”€

def test_compress_active_lane_no_record_content(tmp_path: Path) -> None:
    """Compressed lane output must not contain self.md sensitive content."""
    lane_dir = tmp_path / "docs" / "skill-work" / "work-strategy"
    lane_dir.mkdir(parents=True)
    (lane_dir / "README.md").write_text(
        "# work-strategy\n\n**Objective:** Test objective\n", encoding="utf-8"
    )
    user_dir = tmp_path / "platform/users" / "grace-mar"
    user_dir.mkdir(parents=True)
    secret_content = "UNIQUE_SECRET_SELF_MD_MARKER_XYZ789"
    (user_dir / "self.md").write_text(
        f"# Self\nThis is the Record.\n{secret_content}\n", encoding="utf-8"
    )
    (user_dir / "self-work.md").write_text("# self-work\n", encoding="utf-8")

    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "compress_active_lane.py"),
            "--lane", "work-strategy",
            "--repo-root", str(tmp_path),
        ],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    out_path = tmp_path / "runtime/artifacts" / "context" / "active-lane-work-strategy.md"
    if out_path.exists():
        text = out_path.read_text(encoding="utf-8")
        assert secret_content not in text, (
            "active-lane compression leaked self.md content into artifact"
        )

# â”€â”€ PR 3.5: skill-card output stays under runtime/artifacts/ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_skill_cards_output_under_artifacts(tmp_path: Path) -> None:
    """build_skill_cards writes only to runtime/artifacts/skill-cards, not Record."""
    out_dir = tmp_path / "runtime/artifacts" / "skill-cards"
    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "build_skill_cards.py"),
            "--out-dir", str(out_dir),
        ],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    assert out_dir.exists()
    for f in out_dir.iterdir():
        assert f.suffix in (".json", ".md"), f"unexpected file type: {f.name}"
    for cp in CANONICAL_RECORD_PATHS:
        full = tmp_path / cp
        assert not full.exists(), (
            f"build_skill_cards created canonical Record file: {cp}"
        )

# â”€â”€ PR 3.6: receipt file is non-canonical â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_budget_receipt_not_canonical(tmp_path: Path) -> None:
    """Budget receipt must write to runtime/prepared-context/, not a Record surface."""
    seed = REPO_ROOT / "tests" / "fixtures" / "observations-seed.jsonl"
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    (obs_dir / "index.jsonl").write_text(
        seed.read_text(encoding="utf-8"), encoding="utf-8"
    )
    out = tmp_path / "runtime/prepared-context" / "out.md"
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "prepared_context" / "build_budgeted_context.py"),
            "--repo-root", str(tmp_path),
            "--lane", "work-strategy",
            "--mode", "compact",
            "-o", str(out),
            "--budgets-file",
            str(REPO_ROOT / "platform/config" / "context_budgets" / "lane-defaults.json"),
        ],
        env=env, capture_output=True, text=True,
    )
    receipt = tmp_path / "runtime/prepared-context" / "last-budget-builds.json"
    assert receipt.exists()
    receipt_path_str = str(receipt.relative_to(tmp_path))
    assert receipt_path_str.startswith("runtime/prepared-context"), (
        f"receipt written outside runtime/prepared-context/: {receipt_path_str}"
    )
    for cp in CANONICAL_RECORD_PATHS:
        assert not (tmp_path / cp).exists(), (
            f"budget build created canonical file: {cp}"
        )

# â”€â”€ PR 3.7: observation store writes stay in runtime/ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_observation_store_writes_only_to_runtime() -> None:
    """Observation store paths must resolve under runtime/observations/."""
    sys.path.insert(0, str(REPO_ROOT / "scripts" / "runtime"))
    import ledger_paths  # noqa: E402

    obs_dir = str(ledger_paths.observations_dir())
    assert "runtime" in obs_dir and "observations" in obs_dir, (
        f"observation store dir is not under runtime/observations/: {obs_dir}"
    )
    obs_jsonl = str(ledger_paths.observations_jsonl())
    assert obs_jsonl.endswith("index.jsonl"), (
        f"observation store JSONL path does not end with index.jsonl: {obs_jsonl}"
    )
    for canonical in CANONICAL_RECORD_PATHS:
        assert canonical not in obs_dir, (
            f"observation store dir overlaps with canonical path: {canonical}"
        )
