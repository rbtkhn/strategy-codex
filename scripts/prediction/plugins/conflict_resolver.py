"""Merge core + plugin outputs — core dominates; bounded perturbation."""

from __future__ import annotations

from typing import Any

from prediction.plugins.base import MAX_PLUGIN_INFLUENCE, deep_clone, normalize_plugin_weights


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def merge_object(
    core_obj: dict[str, Any],
    plugin_outputs: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build merged view for one epistemic object."""
    core_signals = deep_clone(core_obj.get("trajectory_signals") or {})
    core_regime = deep_clone(core_obj.get("regime") or {})
    core_label = str(core_regime.get("label") or "transition")
    core_confidence = float(core_regime.get("confidence") or 0.55)

    merged_signals: dict[str, Any] = dict(core_signals)
    annotations: dict[str, Any] = {}
    confidence_delta_sum = 0.0

    weights = normalize_plugin_weights(plugin_outputs)
    for output, weight in zip(plugin_outputs, weights):
        if weight <= 0:
            continue
        mods = output.get("modifications") or {}
        if not isinstance(mods, dict):
            continue

        sig_ext = mods.get("signals") or {}
        if isinstance(sig_ext, dict):
            for key, val in sig_ext.items():
                if key in merged_signals:
                    # blend extension into merged view only for new keys;
                    # core keys stay at core value
                    continue
                if isinstance(val, (int, float)):
                    merged_signals[key] = round(float(val), 4)
                else:
                    merged_signals[key] = val

        ann = mods.get("annotations") or {}
        if isinstance(ann, dict):
            for k, v in ann.items():
                annotations[k] = v

        regime_adj = mods.get("regime_adjustments") or {}
        if isinstance(regime_adj, dict):
            delta = regime_adj.get("confidence_delta")
            if delta is None and "confidence" in regime_adj:
                delta = float(regime_adj["confidence"]) - core_confidence
            if isinstance(delta, (int, float)):
                confidence_delta_sum += float(delta) * weight

    # Core dominates: bounded confidence perturbation
    merged_confidence = _clamp01(core_confidence + confidence_delta_sum)

    return {
        "trajectory_signals": merged_signals,
        "regime": {
            "label": core_label,
            "confidence": round(merged_confidence, 4),
            "core_confidence": round(core_confidence, 4),
        },
        "annotations": annotations,
    }


def merge_evaluation_rollups(
    rollups: list[dict[str, Any]],
) -> dict[str, Any]:
    combined: dict[str, Any] = {"plugins": []}
    for block in rollups:
        if isinstance(block, dict):
            combined["plugins"].append(block)
    return combined
