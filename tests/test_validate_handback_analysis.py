"""validate_handback_analysis - constitution line vs meta."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "work_dev" / "validate_handback_analysis.py"


def _run(stdin_json: str) -> tuple[int, str, str]:
    p = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=stdin_json,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    return p.returncode, p.stdout, p.stderr


def _openclaw_stage_payload(*, content: str, constitution_check_status: str, staged_risk_tier: str) -> dict[str, str]:
    """Minimal OpenClaw-shaped stage payload for handback-analysis validation."""
    return {
        "content": content,
        "user_id": "grace-mar",
        "title": "OpenClaw session handback",
        "selection_text": "",
        "source": "openclaw_stage",
        "artifact_path": "runtime/artifacts/openclaw/session-note.md",
        "artifact_sha256": "deadbeef" * 8,
        "constitution_check_status": constitution_check_status,
        "staged_risk_tier": staged_risk_tier,
    }


def test_validate_ok_clear() -> None:
    payload = {
        "content": "summary\n\nCONSTITUTION_ADVISORY: status=advisory_clear; rule_ids=none",
        "constitution_check_status": "advisory_clear",
    }
    rc, out, err = _run(json.dumps(payload))
    assert rc == 0
    assert err == ""


def test_validate_mismatch_fails() -> None:
    payload = {
        "content": "CONSTITUTION_ADVISORY: status=advisory_flagged; rule_ids=R1",
        "constitution_check_status": "advisory_clear",
    }
    rc, _, err = _run(json.dumps(payload))
    assert rc == 1
    assert "embedded" in err.lower() or "advisory" in err.lower()


def test_validate_flagged_without_line_fails() -> None:
    payload = {
        "content": "no advisory line here",
        "constitution_check_status": "advisory_flagged",
    }
    rc, _, err = _run(json.dumps(payload))
    assert rc == 1
    assert "advisory_flagged" in err


def test_staged_risk_low_conflicts_with_high_concern_narrative() -> None:
    payload = {
        "content": "Summary: high risk - do not merge until reconciled.",
        "constitution_check_status": "advisory_clear",
        "staged_risk_tier": "low",
    }
    rc, _, err = _run(json.dumps(payload))
    assert rc == 1
    assert "staged_risk_tier" in err and "high-concern" in err


def test_quick_merge_conflicts_with_high_concern_summary() -> None:
    payload = {
        "content": "CONSTITUTION_ADVISORY: status=advisory_clear; rule_ids=none",
        "summary": "Requires manual review before approval.",
        "constitution_check_status": "advisory_clear",
        "staged_risk_tier": "quick_merge_eligible",
    }
    rc, _, err = _run(json.dumps(payload))
    assert rc == 1
    assert "high-concern" in err


def test_manual_escalate_conflicts_with_approval_like_narrative() -> None:
    payload = {
        "content": "Analysis: safe to merge; low risk after review.",
        "constitution_check_status": "advisory_clear",
        "staged_risk_tier": "manual_escalate",
    }
    rc, _, err = _run(json.dumps(payload))
    assert rc == 1
    assert "approval-like" in err


def test_manual_escalate_conflicts_with_no_blockers_narrative() -> None:
    payload = {
        "content": "Analysis: mergeable; no blockers remain.",
        "constitution_check_status": "advisory_clear",
        "staged_risk_tier": "manual_escalate",
    }
    rc, _, err = _run(json.dumps(payload))
    assert rc == 1
    assert "approval-like" in err


def test_low_tier_conflicts_with_escalation_narrative() -> None:
    payload = {
        "content": "Analysis: needs escalation before any handback action.",
        "constitution_check_status": "advisory_clear",
        "staged_risk_tier": "low",
    }
    rc, _, err = _run(json.dumps(payload))
    assert rc == 1
    assert "high-concern" in err


def test_manual_escalate_allows_matching_rejection_narrative() -> None:
    payload = {
        "content": "Analysis: cannot approve; requires manual review.",
        "constitution_check_status": "advisory_clear",
        "staged_risk_tier": "manual_escalate",
    }
    rc, out, err = _run(json.dumps(payload))
    assert rc == 0
    assert err == ""


def test_openclaw_stage_payload_structured_conflict_manual_but_approves_fails() -> None:
    payload = _openclaw_stage_payload(
        content=(
            "OpenClaw handback summary.\n\n"
            "Structured risk tier says manual escalation is required, but the analysis says "
            "this candidate is mergeable and no blockers remain.\n\n"
            "CONSTITUTION_ADVISORY: status=advisory_clear; rule_ids=none"
        ),
        constitution_check_status="advisory_clear",
        staged_risk_tier="manual_escalate",
    )
    rc, _, err = _run(json.dumps(payload))
    assert rc == 1
    assert "approval-like" in err


def test_staged_risk_tier_omitted_skips_narrative_heuristic() -> None:
    payload = {
        "content": "high risk - do not merge (no structured tier in payload).",
        "constitution_check_status": "",
    }
    rc, out, err = _run(json.dumps(payload))
    assert rc == 0
    assert err == ""
