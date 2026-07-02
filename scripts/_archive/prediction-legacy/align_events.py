"""PR7 MVEL — align capture-map claims to event registry (read-only)."""

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
    load_public_map,
    patterns_match,
)

def _load_public_maps() -> dict[str, dict[str, dict[str, Any]]]:
    by_voice: dict[str, dict[str, dict[str, Any]]] = {}
    for speaker in sorted(VOICE_REGISTRY.keys()):
        cfg = get_voice_config(speaker)
        if not cfg.public_map_path.is_file():
            continue
        by_voice[speaker] = load_public_map(
            cfg.public_map_path,
            event_order=cfg.pilot_event_order,
        )
    return by_voice

def _terms_index(public_maps: dict[str, dict[str, dict[str, Any]]]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for events in public_maps.values():
        for event_id, entry in events.items():
            terms = entry.get("prediction_object_terms") or []
            if not isinstance(terms, list):
                continue
            existing = index.setdefault(str(event_id), [])
            for term in terms:
                t = str(term).strip()
                if t and t not in existing:
                    existing.append(t)
    return index

def semantic_match(claim: str, terms_index: dict[str, list[str]]) -> str | None:
    """Return best event_id whose prediction_object_terms match claim text."""
    hits: list[str] = []
    for event_id, terms in sorted(terms_index.items()):
        if patterns_match(claim, terms):
            hits.append(event_id)
    if len(hits) == 1:
        return hits[0]
    return None

def align_to_events(
    claims: list[dict[str, Any]],
    registry: dict[str, dict[str, Any]],
    *,
    public_maps: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Align claims to registry events; unmatched go to review queue only."""
    maps = public_maps if public_maps is not None else _load_public_maps()
    terms_index = _terms_index(maps)

    aligned: list[dict[str, Any]] = []
    matched_rows: list[dict[str, Any]] = []
    unmatched_rows: list[dict[str, Any]] = []

    for claim in claims:
        row = dict(claim)
        event_id = str(row.get("event_id") or "").strip()
        alignment_method = "capture_map_event_id"

        if event_id and event_id in registry:
            row["alignment_status"] = "matched"
            row["event_id"] = event_id
            row["alignment_method"] = alignment_method
            aligned.append(row)
            matched_rows.append(
                {
                    "voice": row["voice"],
                    "event_id": event_id,
                    "capture": row.get("capture"),
                    "alignment_method": alignment_method,
                }
            )
            continue

        fallback = semantic_match(str(row.get("claim") or ""), terms_index)
        if fallback and fallback in registry:
            row["alignment_status"] = "matched"
            row["event_id"] = fallback
            row["alignment_method"] = "semantic_terms"
            aligned.append(row)
            matched_rows.append(
                {
                    "voice": row["voice"],
                    "event_id": fallback,
                    "capture": row.get("capture"),
                    "alignment_method": "semantic_terms",
                    "original_event_id": event_id or None,
                }
            )
            continue

        row["alignment_status"] = "unmatched"
        row["alignment_method"] = "review_queue"
        row["review_status"] = "pending"
        aligned.append(row)
        unmatched_rows.append(
            {
                "voice": row["voice"],
                "event_id": event_id or None,
                "claim": row.get("claim"),
                "capture": row.get("capture"),
                "review_status": "pending",
            }
        )

    alignment_map = {
        "matched": matched_rows,
        "unmatched": unmatched_rows,
        "stats": {
            "claim_count": len(claims),
            "matched_count": len(matched_rows),
            "unmatched_count": len(unmatched_rows),
        },
    }
    return aligned, alignment_map
