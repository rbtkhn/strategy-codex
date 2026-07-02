"""Verbatim grounding helpers — shared with voice prediction shelf."""

from __future__ import annotations

import re

from voice_prediction_pilot import excerpt_in_capture, excerpt_segments_in_capture, word_count

__all__ = [
    "excerpt_in_capture",
    "excerpt_segments_in_capture",
    "word_count",
    "is_stitched_evidence",
]

_STITCH_MARKER_RE = re.compile(r"\s*\|\|\|\s*")

def is_stitched_evidence(text: str) -> bool:
    return bool(_STITCH_MARKER_RE.search(text))
