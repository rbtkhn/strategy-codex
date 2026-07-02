"""Deterministic parsing of raw voice captures into observation objects."""

from __future__ import annotations

import re
import uuid
from typing import Any

_OBSERVATION_NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

def extract_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

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
    return {
        "observation_id": observation_id_for(voice, source_file, text),
        "voice": voice,
        "source_file": source_file,
        "timestamp": mtime_iso,
        "raw_text": text,
        "sentences": extract_sentences(text),
    }
