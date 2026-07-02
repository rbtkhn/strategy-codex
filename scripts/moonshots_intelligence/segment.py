"""Sentence segmentation — lossless partition of verbatim transcript body."""

from __future__ import annotations

import re
from dataclasses import dataclass

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


@dataclass(frozen=True)
class Segment:
    text: str
    start: int
    end: int
    line_index: int


def line_index_at(offset: int, body: str) -> int:
    return body.count("\n", 0, offset) + 1


def segment_body(body: str) -> list[Segment]:
    if not body:
        return []
    segments: list[Segment] = []
    cursor = 0
    for match in _SENTENCE_END.finditer(body):
        chunk_end = match.end()
        chunk = body[cursor:chunk_end]
        if chunk.strip():
            segments.append(
                Segment(
                    text=chunk,
                    start=cursor,
                    end=chunk_end,
                    line_index=line_index_at(cursor, body),
                )
            )
        cursor = chunk_end
    tail = body[cursor:]
    if tail.strip():
        segments.append(
            Segment(
                text=tail,
                start=cursor,
                end=len(body),
                line_index=line_index_at(cursor, body),
            )
        )
    if not segments:
        segments.append(
            Segment(text=body, start=0, end=len(body), line_index=1)
        )
    return segments


def segments_lossless(body: str, segments: list[Segment]) -> bool:
    if not segments:
        return not body.strip()
    reconstructed = "".join(seg.text for seg in segments)
    return reconstructed == body
