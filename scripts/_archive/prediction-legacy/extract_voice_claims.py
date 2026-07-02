"""PR7 MVEL — extract curated claims from voice capture maps."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from voice_prediction_pilot import (  # noqa: E402
    VOICE_REGISTRY,
    get_voice_config,
    load_capture_map,
    source_citation,
)

def load_statecraft_voices() -> list[dict[str, Any]]:
    """Load capture-map rows for every enrolled voice."""
    voices: list[dict[str, Any]] = []
    for speaker in sorted(VOICE_REGISTRY.keys()):
        cfg = get_voice_config(speaker)
        if not cfg.capture_map_path.is_file():
            continue
        rows = load_capture_map(cfg.capture_map_path, guest_speaker=speaker)
        voices.append(
            {
                "speaker": speaker,
                "default_channel": cfg.default_channel,
                "rows": rows,
            }
        )
    return voices

def _timestamp_for_row(row: dict[str, Any], *, default_channel: str) -> str:
    appearance = str(row.get("appearance_date") or "").strip()
    if appearance:
        return appearance[:10]
    capture_rel = str(row.get("capture") or "").replace("\\", "/")
    capture_path = _REPO_ROOT / capture_rel
    if capture_path.is_file():
        citation = source_citation(capture_path, default_channel=default_channel)
        pub = str(citation.get("pub_date") or "").strip()
        if pub:
            return pub[:10]
    return "1970-01-01"

def extract_claims(voices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten capture-map rows into MVEL claim records."""
    results: list[dict[str, Any]] = []
    for voice_block in voices:
        speaker = str(voice_block["speaker"])
        default_channel = str(voice_block.get("default_channel") or "")
        for row in voice_block.get("rows") or []:
            if not isinstance(row, dict):
                continue
            claim = str(row.get("public_excerpt_raw") or row.get("public_excerpt") or "").strip()
            if not claim:
                continue
            results.append(
                {
                    "voice": speaker,
                    "event_id": str(row.get("event_id") or "").strip(),
                    "claim": claim,
                    "stance": str(row.get("stance") or "uncertain"),
                    "speech_act": str(row.get("speech_act") or "restated"),
                    "timestamp": _timestamp_for_row(row, default_channel=default_channel),
                    "capture": str(row.get("capture") or "").replace("\\", "/"),
                    "confidence_hint": str(row.get("confidence") or ""),
                }
            )
    results.sort(key=lambda r: (r["voice"], r["event_id"], r["timestamp"], r["capture"]))
    return results
