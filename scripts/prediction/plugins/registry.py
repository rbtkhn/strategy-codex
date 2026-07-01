"""Static plugin registry — repo-local v1, no dynamic loading."""

from __future__ import annotations

from prediction.plugins.base import EpistemicPlugin
from prediction.plugins.evaluation_plugins import CanonicalCalibrationEval
from prediction.plugins.regime_plugins import RegimeConfidenceRefinement
from prediction.plugins.signal_plugins import NarrativeCoherenceSignal
from prediction.plugins.voice_adapters import MearsheimerAdapter


def load_plugins() -> list[EpistemicPlugin]:
    """Return ordered list of registered plugins (object-level + evaluation)."""
    return [
        MearsheimerAdapter(),
        NarrativeCoherenceSignal(),
        RegimeConfidenceRefinement(),
    ]


def load_evaluation_plugins() -> list[EpistemicPlugin]:
    return [CanonicalCalibrationEval()]
