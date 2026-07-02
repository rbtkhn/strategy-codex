"""Strict validation gate for dual-layer bullets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from moonshots_intelligence import MIN_EVIDENCE_WORDS, MIN_MECHANISM_WORDS, CAUSAL_CUES
from moonshots_intelligence.evidence import EvidenceBlock
from moonshots_intelligence.grounding import (
    excerpt_in_capture,
    is_stitched_evidence,
    word_count,
)


@dataclass(frozen=True)
class ValidationError:
    bullet_index: int
    reason: str


def mechanism_has_causal_structure(mechanism: str) -> bool:
    text = mechanism.strip().lower()
    if word_count(mechanism) >= MIN_MECHANISM_WORDS:
        return True
    return any(cue in text for cue in CAUSAL_CUES)


def validate_bullet(
    bullet: dict[str, Any],
    *,
    archive_body: str,
    evidence_by_id: dict[str, EvidenceBlock],
    bullet_index: int = 0,
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    evidence = str(bullet.get("evidence") or "")
    mechanism = str(bullet.get("mechanism") or "").strip()
    evidence_ref = str(bullet.get("evidence_ref") or "")

    if word_count(evidence) < MIN_EVIDENCE_WORDS:
        errors.append(ValidationError(bullet_index, "evidence < 30 words"))
    if not excerpt_in_capture(evidence, archive_body):
        errors.append(ValidationError(bullet_index, "evidence is paraphrased or not in archive"))
    if is_stitched_evidence(evidence):
        errors.append(ValidationError(bullet_index, "evidence is stitched"))
    if not mechanism:
        errors.append(ValidationError(bullet_index, "missing mechanism layer"))
    elif not mechanism_has_causal_structure(mechanism):
        errors.append(ValidationError(bullet_index, "missing causal structure in mechanism"))
    if evidence_ref not in evidence_by_id:
        errors.append(ValidationError(bullet_index, "evidence_ref does not resolve"))
    else:
        canonical = evidence_by_id[evidence_ref].text
        if not excerpt_in_capture(evidence, canonical) and evidence.strip() != canonical.strip():
            if not excerpt_in_capture(evidence, archive_body):
                errors.append(ValidationError(bullet_index, "evidence_ref mismatch"))
    return errors


def validate_bullets(
    bullets: list[dict[str, Any]],
    *,
    archive_body: str,
    evidence_by_id: dict[str, EvidenceBlock],
) -> list[ValidationError]:
    all_errors: list[ValidationError] = []
    for i, bullet in enumerate(bullets):
        all_errors.extend(
            validate_bullet(
                bullet,
                archive_body=archive_body,
                evidence_by_id=evidence_by_id,
                bullet_index=i,
            )
        )
    return all_errors
