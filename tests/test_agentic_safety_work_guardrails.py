from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def test_plan_mission_has_agentic_risk_review_block():
    text = read("docs/templates/plan-mission.md")

    assert "## 7. Agentic Risk & Safety Review" in text
    assert "Human-context vs agent-context" in text
    assert "blast radius" in text
    assert "Audit receipts" in text
    assert "Revocation / stop path" in text
    assert "Pressure default" in text
    assert "deny" in text and "escalate" in text

def test_agent_surface_template_has_agentic_safety_fields():
    text = read("docs/skill-work/work-dev/agent-surface-template.yaml")

    for expected in [
        "context:",
        "human_context:",
        "agent_context:",
        "permissions:",
        "authority_class:",
        "allowed_actions:",
        "denied_actions:",
        "delegation_allowed:",
        "blast_radius:",
        "audit:",
        "receipt_surfaces:",
        "review_cadence:",
        "revocation:",
        "stop_path:",
        "pressure_default:",
    ]:
        assert expected in text

def test_managed_agent_runbook_requires_revocation_and_review_cadence():
    text = read("docs/skill-work/work-dev/managed-agent-design.md")

    assert "Review cadence declared before first run" in text
    assert "Revocation path documented" in text
    assert "Pressure default declared" in text
    assert "halt if receipts fail or scope widens" in text
    assert "Stop/revocation receipt written" in text

def test_receipt_map_documents_existing_surfaces_and_future_gap():
    text = read("docs/skill-work/work-dev/agentic-receipt-map.md")

    for expected in [
        "Git history",
        "`pipeline-events.jsonl`",
        "`merge-receipts.jsonl`",
        "Cadence events",
        "Compute ledger",
        "Sandbox receipts",
        "Runtime observability",
        "universal Agent Action Log",
        "future gap, not v1",
    ]:
        assert expected in text

def test_agentic_guardrail_docs_do_not_introduce_lily_role_name():
    paths = [
        "docs/templates/plan-mission.md",
        "docs/skill-work/work-dev/agentic-environment-principles.md",
        "docs/skill-work/work-dev/agent-surface-template.yaml",
        "docs/skill-work/work-dev/managed-agent-design.md",
        "docs/skill-work/work-dev/agentic-receipt-map.md",
    ]

    for path in paths:
        assert "Lily" not in read(path)
