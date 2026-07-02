"""Evaluation plugins — rollup metrics on canonical core outputs."""

from __future__ import annotations

from typing import Any

from prediction.plugins.base import EpistemicPlugin

class CanonicalCalibrationEval(EpistemicPlugin):
    """Stub Phase-D seed — Brier-style rollup on resolved registry events."""

    def name(self) -> str:
        return "canonical_calibration_eval_v0"

    def version(self) -> str:
        return "0.1.0"

    def plugin_type(self) -> str:
        return "evaluation"

    def apply(self, core_input: dict[str, Any]) -> dict[str, Any]:
        # Per-object hook unused for evaluation; runner calls evaluate() instead.
        return {
            "plugin_name": self.name(),
            "modifications": {
                "signals": {},
                "regime_adjustments": {},
                "annotations": {},
            },
            "confidence": 0.0,
        }

    def evaluate(
        self,
        *,
        core_objects: list[dict[str, Any]],
        registry: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        """Compute calibration metrics from core objects + registry outcomes."""
        rows: list[dict[str, Any]] = []
        for obj in core_objects:
            event_id = str(
                obj.get("primary_event_id") or obj.get("capture_map_event_id") or ""
            )
            reg = registry.get(event_id) or {}
            outcome = reg.get("outcome")
            if outcome not in ("yes", "no"):
                continue
            y_true = 1.0 if outcome == "yes" else 0.0
            signals = obj.get("trajectory_signals") or {}
            y_pred = float(signals.get("directional") or 0.5)
            rows.append(
                {
                    "event_id": event_id,
                    "voice": obj.get("voice"),
                    "y_true": y_true,
                    "y_pred": round(y_pred, 4),
                    "brier": round((y_pred - y_true) ** 2, 4),
                }
            )

        if not rows:
            return {
                "plugin_name": self.name(),
                "interpretation": "evaluation_rollup",
                "resolved_n": 0,
                "mean_brier": None,
                "note": "low_n",
            }

        mean_brier = sum(r["brier"] for r in rows) / len(rows)
        return {
            "plugin_name": self.name(),
            "interpretation": "evaluation_rollup",
            "resolved_n": len(rows),
            "mean_brier": round(mean_brier, 4),
            "rows": rows,
        }
