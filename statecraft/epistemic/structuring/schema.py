"""Canonical structured prediction object schema."""

from __future__ import annotations

STRUCTURED_SCHEMA_KEYS = frozenset(
    {
        "observation_id",
        "voice",
        "event_id",
        "prediction",
        "stance",
        "confidence",
        "sentences",
    }
)


def validate_structured(obj: dict) -> None:
    keys = set(obj)
    missing = STRUCTURED_SCHEMA_KEYS - keys
    extra = keys - STRUCTURED_SCHEMA_KEYS
    if missing:
        raise ValueError(f"missing structured keys: {sorted(missing)}")
    if extra:
        raise ValueError(f"unexpected structured keys: {sorted(extra)}")
