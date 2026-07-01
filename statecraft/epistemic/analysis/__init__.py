"""Analysis layer public API."""

from .divergence import compute_divergence
from .engine import (
    DEFAULT_ANALYSIS_OUT,
    DEFAULT_STRUCTURED_IN,
    analyze,
    analyze_all,
    analyze_event,
    load_structured_predictions,
    write_analysis,
)
from .metrics import population_variance
from .spread import compute_voice_spread

__all__ = [
    "DEFAULT_ANALYSIS_OUT",
    "DEFAULT_STRUCTURED_IN",
    "analyze",
    "analyze_all",
    "analyze_event",
    "compute_divergence",
    "compute_voice_spread",
    "load_structured_predictions",
    "population_variance",
    "write_analysis",
]
