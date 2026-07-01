"""Temporal scaffolding layer public API."""

from .grouping import group_by_event
from .ordering import assign_time_index, sort_key
from .temporal_engine import (
    DEFAULT_OBSERVATIONS_IN,
    DEFAULT_STRUCTURED_IN,
    DEFAULT_TEMPORAL_OUT,
    build_temporal_view,
    build_timeline_entry,
    enrich_with_timestamps,
    load_structured_predictions,
    ordering_confidence_for_event,
    write_temporal_view,
)
from .trends import compute_trend

__all__ = [
    "DEFAULT_OBSERVATIONS_IN",
    "DEFAULT_STRUCTURED_IN",
    "DEFAULT_TEMPORAL_OUT",
    "assign_time_index",
    "build_temporal_view",
    "build_timeline_entry",
    "compute_trend",
    "enrich_with_timestamps",
    "group_by_event",
    "load_structured_predictions",
    "ordering_confidence_for_event",
    "sort_key",
    "write_temporal_view",
]
