"""Deterministic temporal ordering over enriched structured predictions."""

from __future__ import annotations

from typing import Any

def sort_key(pred: dict[str, Any]) -> tuple[str, str, str]:
    timestamp = str(pred.get("timestamp") or "")
    if not timestamp:
        timestamp = "9999"
    return (timestamp, str(pred.get("voice") or ""), str(pred.get("observation_id") or ""))

def assign_time_index(enriched_preds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(enriched_preds, key=sort_key)
    indexed: list[dict[str, Any]] = []
    for index, pred in enumerate(ordered):
        copy = dict(pred)
        copy["time_index"] = index
        indexed.append(copy)
    return indexed
