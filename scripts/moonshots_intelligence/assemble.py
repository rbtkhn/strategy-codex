"""Assemble validated intelligence document."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from moonshots_intelligence import COMPILER_VERSION, MIN_BULLETS_STRICT, PROMPT_ID
from moonshots_intelligence.evidence import EvidenceBlock
from moonshots_intelligence.ingest import output_basename
from moonshots_intelligence.validate import validate_bullets

def _attach_canonical_evidence(
    bullets: list[dict[str, Any]],
    evidence_by_id: dict[str, EvidenceBlock],
) -> list[dict[str, Any]]:
    attached: list[dict[str, Any]] = []
    for bullet in bullets:
        ref = str(bullet.get("evidence_ref") or "")
        block = evidence_by_id.get(ref)
        evidence_text = str(bullet.get("evidence") or "")
        if block is not None:
            evidence_text = block.text
        attached.append(
            {
                "claim": str(bullet.get("claim") or "").strip(),
                "mechanism": str(bullet.get("mechanism") or "").strip(),
                "implication": str(bullet.get("implication") or "").strip(),
                "evidence_ref": ref,
                "evidence": evidence_text,
            }
        )
    return attached

def assemble_document(
    *,
    archive_path: Path,
    meta: dict[str, Any],
    archive_body: str,
    evidence_blocks: list[EvidenceBlock],
    draft: dict[str, Any],
    receipt: dict[str, Any],
    strict: bool,
) -> dict[str, Any]:
    evidence_by_id = {block.evidence_id: block for block in evidence_blocks}
    bullets = _attach_canonical_evidence(
        list(draft.get("bullets") or []),
        evidence_by_id,
    )
    errors = validate_bullets(bullets, archive_body=archive_body, evidence_by_id=evidence_by_id)
    if errors:
        reasons = "; ".join(f"bullet[{e.bullet_index}]: {e.reason}" for e in errors)
        raise ValueError(f"validation failed: {reasons}")
    if strict and len(bullets) < MIN_BULLETS_STRICT:
        raise ValueError(
            f"strict mode requires >= {MIN_BULLETS_STRICT} validated bullets; got {len(bullets)}"
        )

    basename = output_basename(meta)
    rel_archive = archive_path.as_posix()
    try:
        from prediction_lib import repo_relative

        rel_archive = repo_relative(archive_path)
    except Exception:
        pass

    episode_number = meta.get("episode_number")
    try:
        episode_number = int(episode_number) if episode_number is not None else None
    except (TypeError, ValueError):
        episode_number = None

    return {
        "schema_version": "1",
        "core_thesis": str(draft.get("core_thesis") or "").strip()
        or "Episode intelligence compile pending thesis.",
        "bullets": bullets,
        "concept_primitives": [
            str(x).strip() for x in (draft.get("concept_primitives") or []) if str(x).strip()
        ],
        "feedback_loops": {
            "reinforcing": [
                str(x).strip()
                for x in (draft.get("feedback_loops") or {}).get("reinforcing", [])
                if str(x).strip()
            ],
            "balancing": [
                str(x).strip()
                for x in (draft.get("feedback_loops") or {}).get("balancing", [])
                if str(x).strip()
            ],
        },
        "meta_insight": str(draft.get("meta_insight") or "").strip()
        or "Meta-insight pending.",
        "provenance": {
            "archive_path": rel_archive,
            "output_basename": basename,
            "episode_number": episode_number,
            "episode_type": str(meta.get("episode_type") or ""),
            "source_url": str(meta.get("source_url") or ""),
            "slug": str(meta.get("slug") or ""),
            "compiler_version": COMPILER_VERSION,
            "prompt_id": receipt.get("prompt_id") or PROMPT_ID,
            "prompt_hash": receipt.get("prompt_hash"),
            "model": receipt.get("model"),
            "generated_at": receipt.get("generated_at")
            or datetime.now(timezone.utc).isoformat(),
        },
    }
