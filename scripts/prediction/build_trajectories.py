"""PR7 MVEL — time-ordered trajectories per event × voice."""

from __future__ import annotations

from typing import Any


def group_by_event_and_voice(
    claims: list[dict[str, Any]],
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for claim in claims:
        event_id = str(claim.get("event_id") or "")
        voice = str(claim.get("voice") or "")
        if not event_id or not voice:
            continue
        grouped.setdefault((event_id, voice), []).append(dict(claim))
    return grouped


def _trajectory_point(claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp": str(claim.get("timestamp") or ""),
        "claim": str(claim.get("claim") or ""),
        "stance": str(claim.get("stance") or "uncertain"),
        "probability": float(claim.get("probability") or 0.5),
        "confidence": float(claim.get("confidence") or 0.5),
        "interpretation": "probabilistic_projection",
        "speech_act": str(claim.get("speech_act") or ""),
        "capture": str(claim.get("capture") or ""),
    }


def build_trajectories(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group matched probabilistic claims into sorted trajectories."""
    grouped = group_by_event_and_voice(claims)
    output: list[dict[str, Any]] = []

    for (event_id, voice) in sorted(grouped.keys()):
        items = grouped[(event_id, voice)]
        sorted_items = sorted(items, key=lambda c: (str(c.get("timestamp") or ""), str(c.get("capture") or "")))
        output.append(
            {
                "event_id": event_id,
                "voice": voice,
                "trajectory": [_trajectory_point(item) for item in sorted_items],
            }
        )
    return output
