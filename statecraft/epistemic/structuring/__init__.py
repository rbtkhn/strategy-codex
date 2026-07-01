"""Structuring layer public API."""

from .event_matcher import match_event, similarity
from .normalize import (
    DEFAULT_OBSERVATIONS_IN,
    DEFAULT_REGISTRY,
    DEFAULT_STRUCTURED_OUT,
    load_event_registry,
    load_observations,
    normalize_observation,
    normalize_observations,
    write_structured_predictions,
)
from .schema import STRUCTURED_SCHEMA_KEYS, validate_structured
from .stance_classifier import classify_stance

__all__ = [
    "DEFAULT_OBSERVATIONS_IN",
    "DEFAULT_REGISTRY",
    "DEFAULT_STRUCTURED_OUT",
    "STRUCTURED_SCHEMA_KEYS",
    "classify_stance",
    "load_event_registry",
    "load_observations",
    "match_event",
    "normalize_observation",
    "normalize_observations",
    "similarity",
    "validate_structured",
    "write_structured_predictions",
]
