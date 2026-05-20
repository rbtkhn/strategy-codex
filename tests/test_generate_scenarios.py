"""generate_scenarios — factorial matrix expansion (BUILD-AI-GAP-005)."""

from __future__ import annotations

from pathlib import Path

from scripts.work_dev.generate_scenarios import build_matrix, matrix_markdown_matches

REPO_ROOT = Path(__file__).resolve().parent.parent
HAND_BACK_MATRIX = (
    REPO_ROOT / "docs/skill-work/work-dev/scenarios/handback_tail_stress.matrix.md"
)


def test_handback_tail_stress_openclaw_stressors_by_risk_stance() -> None:
    """handback_tail_stress.yaml: 1 runtime × 8 stressor dimension values."""
    rows = build_matrix(scenario_filter="handback_tail", runtimes=["openclaw"])
    assert len(rows) == 24
    stressor_tags = []
    risk_stances = []
    for r in rows:
        assert r.scenario_id == "handback_tail_stress"
        assert r.runtime == "openclaw"
        assert "handback_analysis" in r.required_checks
        assert r.values.get("base_task") == "stage_openclaw_handback"
        s = r.values.get("stressor")
        assert s is not None
        stressor_tags.append(str(s))
        risk_stance = r.values.get("risk_stance")
        assert risk_stance is not None
        risk_stances.append(str(risk_stance))
    assert sorted(set(stressor_tags)) == [
        "V-01_minimize",
        "V-02_authority",
        "V-03_time_pressure",
        "V-04_structured_conflict",
        "V-05_tool_failure",
        "V-06_hedging",
        "V-07_contradictory_prior",
        "V-08_ood_tail",
    ]
    assert sorted(set(risk_stances)) == [
        "aligned_low",
        "low_but_warns",
        "manual_but_approves",
    ]


def test_handback_tail_matrix_file_matches_generator() -> None:
    """Checked-in matrix stays in sync with YAML (CI drift guard)."""
    rows = build_matrix(scenario_filter="handback_tail", runtimes=["openclaw"])
    ok, msg = matrix_markdown_matches(rows, HAND_BACK_MATRIX)
    assert ok, msg
