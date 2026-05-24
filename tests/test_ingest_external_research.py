from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "ingest_external_research.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("ingest_external_research_test", SCRIPT_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _sample_text() -> str:
    return """AI systems are becoming more useful in research-heavy workflows.

- Agent scaffolds can reduce operator rescue when evidence is visible and review remains local.
- Small-team adoption improves when reporting, receipts, and rollback are explicit.

Citation: Smith et al. 2024. Review-gated AI workflows. DOI: 10.1234/example-doi
PDF: https://example.org/research-paper.pdf
Reference: Workflow receipts under pressure https://example.org/control-plane-note

Open question: How much authority can be delegated before local review becomes ceremonial?
Tension: Faster synthesis can still weaken judgment if provenance is weak.
"""


def test_build_artifact_extracts_claims_and_citations():
    mod = _load_module()

    class Args:
        source = "sci-bot.ru"
        source_url = "https://sci-bot.ru/session/example"
        lane = "singularity-academy"
        topic = "AI workflow authority"
        record_impact = "none"
        query = "How should review-gated AI workflow research be applied to singularity academy?"
        summary = None
        prepared_context_tag = ["singularity", "workflow"]
        academy_surface = "workshop"
        acceleration_vector = "research synthesis and workflow routing"
        agent_type = "model plus operator workflow"
        alignment_risk = "faster synthesis can outrun review discipline"
        substrate_notes = "authority and rollback stay local"
        displacement_notes = "operator review may become ceremonial if receipts weaken"
        commercial_relevance = "research teams with weak review contracts"
        reuse_output = "derive one workshop note and one offer memo"
        ix_update = []
        skill_update = []

    artifact = mod.build_artifact(Args, _sample_text())
    mod.validate_artifact(artifact)

    assert artifact["lane"] == "singularity-academy"
    assert artifact["topic_slug"] == "ai-workflow-authority"
    assert len(artifact["key_claims"]) >= 2
    assert len(artifact["citations"]) == 2
    assert artifact["citations"][0]["doi"] == "10.1234/example-doi"
    assert artifact["citations"][0]["pdf_url"] == "https://example.org/research-paper.pdf"
    assert artifact["citations"][0]["title"] == "Smith et al. 2024. Review-gated AI workflows"
    assert artifact["citations"][1]["title"] == "Workflow receipts under pressure"
    assert artifact["tensions"] == ["Faster synthesis can still weaken judgment if provenance is weak."]
    assert artifact["open_questions"] == ["How much authority can be delegated before local review becomes ceremonial?"]


def test_write_outputs_keeps_gate_untouched(tmp_path, monkeypatch):
    mod = _load_module()
    monkeypatch.setattr(mod, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        mod,
        "LANE_ROOTS",
        {
            "singularity-academy": tmp_path / "research" / "external" / "singularity-academy",
            "work-dev": tmp_path / "research" / "external" / "work-dev" / "external-research",
            "work-strategy": tmp_path / "research" / "external" / "work-strategy" / "external-research",
            "work-business": tmp_path / "research" / "external" / "work-business" / "external-research",
        },
    )
    schema_copy = tmp_path / "schema-registry" / "external-research-artifact.v1.json"
    schema_copy.parent.mkdir(parents=True)
    schema_copy.write_text((ROOT / "schema-registry" / "external-research-artifact.v1.json").read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(mod, "SCHEMA_PATH", schema_copy)

    input_path = tmp_path / "sample.txt"
    input_path.write_text(_sample_text(), encoding="utf-8")

    exit_code = mod.main(
        [
            "--lane",
            "singularity-academy",
            "--topic",
            "AI workflow authority",
            "--query",
            "How should review-gated AI workflow research be applied to singularity academy?",
            "--input",
            str(input_path),
            "--emit-workshop-brief",
            "--emit-offer-memo",
            "--emit-self-proposal",
            "--academy-surface",
            "workshop",
            "--acceleration-vector",
            "research synthesis and workflow routing",
            "--agent-type",
            "model plus operator workflow",
            "--alignment-risk",
            "faster synthesis can outrun review discipline",
            "--substrate-notes",
            "authority and rollback stay local",
            "--displacement-notes",
            "operator review may become ceremonial if receipts weaken",
            "--commercial-relevance",
            "research teams with weak review contracts",
            "--reuse-output",
            "derive one workshop note and one offer memo",
        ]
    )

    assert exit_code == 0
    artifact_dir = tmp_path / "research" / "external" / "singularity-academy" / "queries"
    brief_dir = tmp_path / "research" / "external" / "singularity-academy" / "briefs"
    offer_dir = tmp_path / "docs" / "skill-work" / "work-business" / "singularity-academy-research-memos"
    proposal_dir = tmp_path / "auto-research" / "self-proposals" / "derived"

    artifact_paths = list(artifact_dir.glob("*.json"))
    assert len(artifact_paths) == 1
    assert list(brief_dir.glob("*academy-brief.md"))
    assert list(offer_dir.glob("*offer-memo.md"))
    proposal_paths = list(proposal_dir.glob("*.json"))
    assert len(proposal_paths) == 1

    proposal = json.loads(proposal_paths[0].read_text(encoding="utf-8"))
    assert proposal["proposal_type"] == "recursion_gate_candidate"
    assert proposal["candidate_bundle"]["signal_type"] == "external_research_proposal"

    assert not (tmp_path / "recursion-gate.md").exists()
    assert not list(tmp_path.rglob("recursion-gate.md"))


def test_unresolved_citations_are_preserved():
    mod = _load_module()
    text = """Summary paragraph.

- Claim with no direct link.
- Another claim.

Reference: A paper title without DOI or URL
"""
    citations = mod.infer_citations(text)
    assert citations
    assert citations[0]["resolution_status"] == "unresolved"
    assert citations[0]["title"] == "A paper title without DOI or URL"


def test_validation_falls_back_without_jsonschema(monkeypatch):
    mod = _load_module()
    monkeypatch.setattr(mod, "jsonschema", None)

    class Args:
        source = "sci-bot.ru"
        source_url = None
        lane = "singularity-academy"
        topic = "AI workflow authority"
        record_impact = "none"
        query = "How should review-gated AI workflow research be applied to singularity academy?"
        summary = None
        prepared_context_tag = []
        academy_surface = None
        acceleration_vector = None
        agent_type = None
        alignment_risk = None
        substrate_notes = None
        displacement_notes = None
        commercial_relevance = None
        reuse_output = None
        ix_update = []
        skill_update = []

    artifact = mod.build_artifact(Args, _sample_text())

    mod.validate_artifact(artifact)

    broken = dict(artifact)
    broken["lane"] = "not-a-lane"

    try:
        mod.validate_artifact(broken)
    except ValueError as exc:
        assert "Unsupported lane" in str(exc)
    else:
        raise AssertionError("fallback validation should still reject invalid artifacts")
