"""Signal extension plugins — additive derived signals only."""

from __future__ import annotations

from typing import Any

from prediction.plugins.base import EpistemicPlugin

class NarrativeCoherenceSignal(EpistemicPlugin):
    """Stub — lower coherence when alignment entropy is high."""

    def name(self) -> str:
        return "narrative_coherence_signal_v0"

    def version(self) -> str:
        return "0.1.0"

    def plugin_type(self) -> str:
        return "signal"

    def apply(self, core_input: dict[str, Any]) -> dict[str, Any]:
        entropy = float(core_input.get("alignment_entropy") or 0.0)
        # High entropy → lower narrative coherence score
        score = max(0.0, min(1.0, 1.0 - entropy / 2.0))
        return {
            "plugin_name": self.name(),
            "modifications": {
                "signals": {"narrative_coherence_score": round(score, 4)},
                "regime_adjustments": {},
                "annotations": {},
            },
            "confidence": 0.2,
        }
