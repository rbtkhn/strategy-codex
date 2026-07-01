"""Deterministic top-1 event alignment against operator event registry."""

from __future__ import annotations

import re
from typing import Any


def _token_set(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2}


def similarity(observation_text: str, event_text: str) -> float:
    obs_tokens = _token_set(observation_text)
    event_tokens = _token_set(event_text)
    if not obs_tokens or not event_tokens:
        return 0.0
    return len(obs_tokens & event_tokens) / len(obs_tokens | event_tokens)


def event_match_text(event: dict[str, Any]) -> str:
    parts = [
        str(event.get("question") or ""),
        str(event.get("falsifier") or ""),
        str(event.get("confirmation_criteria") or ""),
    ]
    return " ".join(part.strip() for part in parts if part.strip())


def observation_match_text(observation: dict[str, Any]) -> str:
    raw = str(observation.get("raw_text") or "")
    sentences = observation.get("sentences") or []
    if sentences:
        return f"{raw} {' '.join(str(s) for s in sentences)}"
    return raw


def match_event(observation: dict[str, Any], event_registry: dict[str, dict[str, Any]]) -> str:
    if not event_registry:
        return "unmatched"

    obs_text = observation_match_text(observation)
    candidates: list[tuple[str, float]] = []
    for event_id, event in event_registry.items():
        score = similarity(obs_text, event_match_text(event))
        candidates.append((event_id, score))

    candidates.sort(key=lambda item: (-item[1], item[0]))
    best_event_id, best_score = candidates[0]
    if best_score == 0.0:
        return "unmatched"
    return best_event_id
