"""Evidence extraction — verbatim spans ≥ MIN_EVIDENCE_WORDS."""

from __future__ import annotations

from dataclasses import dataclass

from moonshots_intelligence import MIN_EVIDENCE_WORDS
from moonshots_intelligence.grounding import word_count
from moonshots_intelligence.segment import Segment


@dataclass(frozen=True)
class EvidenceBlock:
    evidence_id: str
    text: str
    source_location: str
    word_count: int


def extract_evidence(segments: list[Segment]) -> list[EvidenceBlock]:
    blocks: list[EvidenceBlock] = []
    counter = 1
    for seg in segments:
        wc = word_count(seg.text)
        if wc < MIN_EVIDENCE_WORDS:
            continue
        eid = f"E{counter}"
        counter += 1
        blocks.append(
            EvidenceBlock(
                evidence_id=eid,
                text=seg.text,
                source_location=f"line:{seg.line_index}:chars:{seg.start}-{seg.end}",
                word_count=wc,
            )
        )
    return blocks


def evidence_map(blocks: list[EvidenceBlock]) -> dict[str, EvidenceBlock]:
    return {block.evidence_id: block for block in blocks}
