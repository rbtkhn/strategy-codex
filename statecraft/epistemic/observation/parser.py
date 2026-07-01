"""Deterministic parsing of raw voice captures into observation objects."""

from __future__ import annotations

import re
import uuid
from typing import Any

PREDICTIVE_MARKERS = [
    "will",
    "likely",
    "cannot",
    "expected",
    "risk",
    "would",
    "inevitable",
]

_OBSERVATION_NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")


def extract_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]


def is_predictive(sentence: str) -> bool:
    lowered = sentence.lower()
    return any(marker in lowered for marker in PREDICTIVE_MARKERS)


def observation_id_for(voice: str, source_file: str, raw_text: str) -> str:
    key = f"{voice}|{source_file}|{raw_text}"
    return str(uuid.uuid5(_OBSERVATION_NAMESPACE, key))


def parse_voice_capture(
    voice: str,
    source_file: str,
    text: str,
    *,
    mtime_iso: str,
) -> dict[str, Any]:
    sentences = extract_sentences(text)
    return {
        "observation_id": observation_id_for(voice, source_file, text),
        "voice": voice,
        "source_file": source_file,
        "timestamp": mtime_iso,
        "raw_text": text,
        "extracted_sentences": [s for s in sentences if is_predictive(s)],
    }
