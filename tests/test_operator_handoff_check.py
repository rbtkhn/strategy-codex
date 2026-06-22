"""Tests for operator_handoff_check gate section."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def handoff_mod():
    path = REPO_ROOT / "scripts" / "operator_handoff_check.py"
    spec = importlib.util.spec_from_file_location("operator_handoff_check", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def gate_unfrozen(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fork-revive gate parsing tests need Record unfrozen."""
    import strategy_codex_config as scc

    monkeypatch.setattr(scc, "record_frozen", lambda: False)


def test_gate_detail_lines_empty_queue(handoff_mod, gate_unfrozen):
    text = "## Candidates\n\n## Processed\n"
    lines = handoff_mod._gate_detail_lines(text, "grace-mar")
    joined = "\n".join(lines)
    assert "**Total pending:** 0" in joined
    assert "process_approved_candidates.py" in joined
    assert "operator_gate_review_pass.py" in joined


def test_gate_detail_lists_pending_wap_and_companion(handoff_mod, gate_unfrozen):
    gate = """## Candidates

### CANDIDATE-0998 (wap)

```yaml
status: pending
summary: WAP item one
territory: work-politics
```

### CANDIDATE-0999 (companion)

```yaml
status: pending
summary: Companion item two
channel_key: telegram:1
```

## Processed
"""
    lines = handoff_mod._gate_detail_lines(gate, "test-user")
    joined = "\n".join(lines)
    assert "**Total pending:** 2 (work-politics: 1 · companion: 1)" in joined
    assert "CANDIDATE-0998" in joined and "Work-politics" in joined
    assert "CANDIDATE-0999" in joined and "Companion" in joined
    assert "complete processing" in joined
    assert "test-user/recursion-gate.md" in joined


def test_gate_detail_lines_frozen_record(handoff_mod, monkeypatch: pytest.MonkeyPatch):
    import strategy_codex_config as scc

    monkeypatch.setattr(scc, "record_frozen", lambda: True)
    lines = handoff_mod._gate_detail_lines("## Candidates\n", "grace-mar")
    joined = "\n".join(lines)
    assert "## RECURSION-GATE (frozen)" in joined
    assert "fork revive" in joined
    assert "**Total pending:**" not in joined


def test_build_ship_receipt_ahead_and_mixed_slices(handoff_mod):
    lines = handoff_mod.build_ship_receipt(
        status_lines=[
            " M statecraft/synthesis/day/2026-06-08.md",
            " M public/ph-civ/README.md",
            "?? singularity/workshop/README.md",
        ],
        branch_lines=["main"],
        status_sb_lines=["## main...origin/main [ahead 2]"],
        origin_main_lines=["abc123def"],
        recent_commits=[
            "3e3517e6 feat(statecraft): Sachs June 8 intake",
            "e1442b0d chore: ph-civ bump",
        ],
    )
    joined = "\n".join(lines)
    assert "## Ship receipt" in joined
    assert "**Branch:** `main`" in joined
    assert "ahead 2" in joined
    assert "**statecraft:**" in joined
    assert "**ph-civ:**" in joined
    assert "**singularity:**" in joined
    assert "git push origin main" in joined
    assert "3e3517e6" in joined


def test_build_handoff_check_full_mode_does_not_raise(handoff_mod, monkeypatch: pytest.MonkeyPatch):
    import strategy_codex_config as scc

    monkeypatch.setattr(scc, "record_frozen", lambda: True)
    monkeypatch.setattr(handoff_mod, "_read", lambda _p: "## VIII\n\n2026-06-01 ACT-0001 sample activity\n")
    monkeypatch.setattr(handoff_mod, "_pending_candidates", lambda _g, _f: [])
    monkeypatch.setattr(
        handoff_mod,
        "_last_activity_oneliner",
        lambda evidence: "ACT-0001 sample" if evidence else "_none_",
    )
    monkeypatch.setattr(
        handoff_mod,
        "get_work_politics_snapshot",
        lambda _u: {"territory_blockers": [], "next_actions": []},
    )
    monkeypatch.setattr(handoff_mod, "_run_git_status_bundle", lambda: ([], [], "main"))
    monkeypatch.setattr(handoff_mod, "_run_git", lambda *_a, **_k: [])
    if handoff_mod.build_night_pulse_lines is not None:
        monkeypatch.setattr(handoff_mod, "build_night_pulse_lines", lambda _u: [])

    result = handoff_mod.build_handoff_check("strategy-codex", fast=False)
    assert "# Handoff check" in result
    assert "ACT-0001" in result
