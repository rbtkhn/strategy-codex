"""Tests for Moonshots intelligence compiler."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from moonshots_intelligence.assemble import assemble_document  # noqa: E402
from moonshots_intelligence.cli import compile_archive  # noqa: E402
from moonshots_intelligence.evidence import extract_evidence  # noqa: E402
from moonshots_intelligence.grounding import excerpt_in_capture  # noqa: E402
from moonshots_intelligence.ingest import ingest_archive  # noqa: E402
from moonshots_intelligence.segment import segment_body, segments_lossless  # noqa: E402
from moonshots_intelligence.validate import validate_bullet  # noqa: E402
from mcp_receipt_lib import validate_json_schema  # noqa: E402

FIXTURE_ARCHIVE = REPO_ROOT / "tests" / "fixtures" / "moonshots_synthetic_archive.md"
SCHEMA_PATH = REPO_ROOT / "schemas" / "singularity" / "moonshots-intelligence.schema.json"


def _load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _make_bullet(evidence_id: str, evidence_text: str, n: int) -> dict:
    return {
        "claim": f"Interpretive claim number {n} from panel discourse.",
        "mechanism": f"Because market structure drives incentive alignment when {n} actors compete for control.",
        "implication": f"System-level consequence {n} projects institutional adaptation pressure.",
        "evidence_ref": evidence_id,
        "evidence": evidence_text,
    }


def test_segment_lossless_synthetic():
    ingested = ingest_archive(FIXTURE_ARCHIVE)
    segments = segment_body(ingested.body)
    assert segments_lossless(ingested.body, segments)


def test_evidence_extraction_min_words():
    ingested = ingest_archive(FIXTURE_ARCHIVE)
    segments = segment_body(ingested.body)
    blocks = extract_evidence(segments)
    assert len(blocks) >= 3
    for block in blocks:
        assert block.word_count >= 30
        assert excerpt_in_capture(block.text, ingested.body)


def test_reject_paraphrased_evidence():
    ingested = ingest_archive(FIXTURE_ARCHIVE)
    segments = segment_body(ingested.body)
    blocks = extract_evidence(segments)
    evidence_by_id = {b.evidence_id: b for b in blocks}
    bad = _make_bullet(blocks[0].evidence_id, "This is completely paraphrased evidence text.", 0)
    errors = validate_bullet(
        bad,
        archive_body=ingested.body,
        evidence_by_id=evidence_by_id,
    )
    assert any("paraphrased" in e.reason for e in errors)


def test_reject_stitched_evidence():
    ingested = ingest_archive(FIXTURE_ARCHIVE)
    segments = segment_body(ingested.body)
    blocks = extract_evidence(segments)
    if len(blocks) < 2:
        pytest.skip("need >= 2 evidence blocks")
    evidence_by_id = {b.evidence_id: b for b in blocks}
    stitched = f"{blocks[0].text} ||| {blocks[1].text}"
    bad = _make_bullet(blocks[0].evidence_id, stitched, 0)
    errors = validate_bullet(
        bad,
        archive_body=ingested.body,
        evidence_by_id=evidence_by_id,
    )
    assert any("stitched" in e.reason for e in errors)


def test_assemble_and_schema_validate():
    ingested = ingest_archive(FIXTURE_ARCHIVE)
    segments = segment_body(ingested.body)
    blocks = extract_evidence(segments)
    evidence_by_id = {b.evidence_id: b for b in blocks}
    bullets = [
        _make_bullet(blocks[i % len(blocks)].evidence_id, blocks[i % len(blocks)].text, i + 1)
        for i in range(10)
    ]
    draft = {
        "core_thesis": "Synthetic episode tests compute and access control coupling.",
        "bullets": bullets,
        "concept_primitives": ["access governance", "capital markets"],
        "feedback_loops": {
            "reinforcing": ["IPO scale reinforces narrative abundance"],
            "balancing": ["export control introduces access friction"],
        },
        "meta_insight": "Frontier intelligence becomes jurisdictional when vendors can global kill-switch.",
    }
    receipt = {
        "prompt_id": "dual_layer_v1",
        "prompt_hash": "test",
        "model": "test-fixture",
        "generated_at": "2026-01-01T00:00:00+00:00",
    }
    document = assemble_document(
        archive_path=ingested.archive_path,
        meta=ingested.meta,
        archive_body=ingested.body,
        evidence_blocks=blocks,
        draft=draft,
        receipt=receipt,
        strict=True,
    )
    validate_json_schema(document, SCHEMA_PATH)


def test_output_basename_includes_episode_number():
    ingested = ingest_archive(FIXTURE_ARCHIVE)
    assert ingested.meta.get("episode_number") == 999


def test_compile_dry_run():
    result = compile_archive(
        FIXTURE_ARCHIVE,
        out_dir=REPO_ROOT / "research" / "singularity-science" / "moonshots",
        dry_run=True,
        write=False,
    )
    assert result["evidence_count"] >= 3
    assert result.get("dry_run") is True


def test_compile_with_bullets_json(tmp_path: Path):
    ingested = ingest_archive(FIXTURE_ARCHIVE)
    segments = segment_body(ingested.body)
    blocks = extract_evidence(segments)
    bullets = [
        _make_bullet(blocks[i % len(blocks)].evidence_id, blocks[i % len(blocks)].text, i + 1)
        for i in range(10)
    ]
    draft = {
        "core_thesis": "Fixture compile path.",
        "bullets": bullets,
        "concept_primitives": ["test"],
        "feedback_loops": {"reinforcing": ["r1"], "balancing": ["b1"]},
        "meta_insight": "Meta test.",
    }
    bullets_path = tmp_path / "bullets.json"
    bullets_path.write_text(json.dumps(draft), encoding="utf-8")
    result = compile_archive(
        FIXTURE_ARCHIVE,
        out_dir=tmp_path,
        strict=True,
        bullets_json=bullets_path,
        write=True,
    )
    json_out = Path(result["output_json"])
    assert json_out.name == "moonshots-ep-999-intelligence.json"
    data = json.loads(json_out.read_text(encoding="utf-8"))
    validate_json_schema(data, SCHEMA_PATH)
