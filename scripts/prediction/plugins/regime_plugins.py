"""Regime refinement plugins — confidence adjustments only."""

from __future__ import annotations

from typing import Any

from prediction.plugins.base import EpistemicPlugin


class RegimeConfidenceRefinement(EpistemicPlugin):
    """Stub — nudge confidence down when fragmentation + high entropy."""

    def name(self) -> str:
        return "regime_confidence_refinement_v0"

    def version(self) -> str:
        return "0.1.0"

    def plugin_type(self) -> str:
        return "regime"

    def apply(self, core_input: dict[str, Any]) -> dict[str, Any]:
        regime = core_input.get("regime") or {}
        label = str(regime.get("label") or "")
        entropy = float(core_input.get("alignment_entropy") or 0.0)
        delta = 0.0
        if label == "fragmentation" and entropy > 1.2:
            delta = -0.05
        return {
            "plugin_name": self.name(),
            "modifications": {
                "signals": {},
                "regime_adjustments": {"confidence_delta": delta},
                "annotations": {},
            },
            "confidence": 0.1,
        }
