"""Regression coverage for root-layout holdout scripts."""

from __future__ import annotations

import json
import shutil
import sys
import uuid
from datetime import date
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import analyze_rejection_feedback as arf  # noqa: E402
import assess_session_load as asl  # noqa: E402
import batch_ingest_observations as bio  # noqa: E402
import detect_capture_gap as dcg  # noqa: E402
import generate_gate_dashboard as ggd  # noqa: E402
import import_working_identity_candidates as iwic  # noqa: E402


USER = "strategy-codex"


@pytest.fixture
def work_root():
    base = REPO / ".test-tmp" / "root-layout-holdouts"
    root = base / uuid.uuid4().hex
    root.mkdir(parents=True)
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _write_root_profile(root: Path) -> None:
    (root / "self.md").write_text("# Self\n", encoding="utf-8")
    (root / "self-knowledge.md").write_text("# Knowledge\n", encoding="utf-8")
    (root / "self-archive.md").write_text(
        "- id: READ-0001\n  date: 2026-05-01\n",
        encoding="utf-8",
    )
    (root / "recursion-gate.md").write_text(
        """# Gate

## Candidates

### CANDIDATE-0001 (old rejection)
```yaml
status: rejected
timestamp: 2026-05-01
summary: duplicate sample
rejection_reason: duplicate sample
```

## Processed
""",
        encoding="utf-8",
    )
    (root / "pipeline-events.jsonl").write_text(
        json.dumps({"event": "applied", "timestamp": "2026-05-02T00:00:00Z"}) + "\n",
        encoding="utf-8",
    )
    (root / "last-dream.json").write_text(json.dumps({"ok": True}) + "\n", encoding="utf-8")


def _assert_no_strategy_codex_user(root: Path) -> None:
    assert not (root / "platform/users" / USER).exists()


def test_analyze_rejection_feedback_uses_root_profile(work_root, monkeypatch):
    _write_root_profile(work_root)
    monkeypatch.setattr(arf, "REPO_ROOT", work_root)
    monkeypatch.setattr(arf, "profile_dir", lambda user_id: work_root)
    monkeypatch.setattr(
        sys,
        "argv",
        ["analyze_rejection_feedback.py", "-u", USER, "--quiet"],
    )

    assert arf.main() == 0
    assert (work_root / "runtime/artifacts" / "rejection_analysis.json").is_file()
    _assert_no_strategy_codex_user(work_root)


def test_assess_session_load_uses_root_profile(work_root, monkeypatch):
    _write_root_profile(work_root)
    monkeypatch.setattr(asl, "profile_dir", lambda user_id: work_root)
    monkeypatch.setattr(asl, "_collect_cadence_today", lambda user_id: None)
    monkeypatch.setattr(asl, "_collect_capture_gap", lambda user_id: {"level": "ok"})
    monkeypatch.setattr(asl, "_collect_branch_count", lambda: 0)

    result = asl.assess_load(USER)

    assert result["load_level"] in {"light", "moderate", "heavy"}
    _assert_no_strategy_codex_user(work_root)


def test_batch_ingest_observations_writes_root_gate(work_root, monkeypatch):
    _write_root_profile(work_root)
    monkeypatch.setattr(bio, "profile_dir", lambda user_id: work_root)

    results = bio.batch_ingest(USER, [{"category": "knowledge", "body": "Saw root layout holdout."}])

    assert results[0]["id"] == "CANDIDATE-0002"
    assert "Saw root layout holdout." in (work_root / "recursion-gate.md").read_text(encoding="utf-8")
    _assert_no_strategy_codex_user(work_root)


def test_detect_capture_gap_uses_root_profile(work_root, monkeypatch):
    _write_root_profile(work_root)
    monkeypatch.setattr(dcg, "profile_dir", lambda user_id: work_root)

    result = dcg.detect_gap(USER, today=date(2026, 5, 8))

    assert result["last_evidence_id"] == "READ-0001"
    assert result["pending_count"] == 0
    _assert_no_strategy_codex_user(work_root)


def test_generate_gate_dashboard_writes_root_dashboard(work_root, monkeypatch):
    _write_root_profile(work_root)
    monkeypatch.setattr(ggd, "REPO_ROOT", work_root)
    monkeypatch.setattr(ggd, "profile_dir", lambda user_id: work_root)
    monkeypatch.setattr(ggd, "parse_review_candidates", lambda user_id: [])
    monkeypatch.setattr(sys, "argv", ["generate_gate_dashboard.py", "-u", USER])

    assert ggd.main() == 0
    assert (work_root / "gate-dashboard.html").is_file()
    _assert_no_strategy_codex_user(work_root)


def test_import_working_identity_candidates_writes_root_gate_and_digest(work_root, monkeypatch):
    _write_root_profile(work_root)
    input_path = work_root / "extract.json"
    input_path.write_text(
        json.dumps({"behavioral_calibration": [{"claim": "Prefers root contract."}]}),
        encoding="utf-8",
    )
    monkeypatch.setattr(iwic, "REPO_ROOT", work_root)
    monkeypatch.setattr(iwic, "profile_dir", lambda user_id: work_root)
    monkeypatch.setattr(
        sys,
        "argv",
        ["import_working_identity_candidates.py", "-u", USER, "-f", str(input_path)],
    )

    assert iwic.main() == 0
    assert "Prefers root contract." in (work_root / "recursion-gate.md").read_text(encoding="utf-8")
    assert any((work_root / "runtime/artifacts" / "portable-record").glob("import-digest-*.md"))
    _assert_no_strategy_codex_user(work_root)
