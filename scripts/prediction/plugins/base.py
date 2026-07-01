"""Epistemic plugin base contract — read-only core input, bounded output."""

from __future__ import annotations

import copy
import json
from abc import ABC, abstractmethod
from typing import Any, Literal

MAX_PLUGIN_INFLUENCE = 0.3

PluginType = Literal["voice", "signal", "regime", "evaluation"]

FORBIDDEN_MODIFICATION_KEYS = frozenset(
    {
        "event_distribution",
        "alignment_entropy",
        "regime.label",
        "label",
        "capture_map_event_id",
        "primary_event_id",
        "interpretation",
    }
)

FORBIDDEN_SIGNAL_OVERWRITE = frozenset({"directional", "volatility", "drift"})


def deep_clone(obj: Any) -> Any:
    return copy.deepcopy(obj)


def core_object_to_plugin_input(core_obj: dict[str, Any]) -> dict[str, Any]:
    """Extract plugin input contract from a unified epistemic core object."""
    event_id = str(
        core_obj.get("primary_event_id") or core_obj.get("capture_map_event_id") or ""
    )
    return {
        "event_id": event_id,
        "event_distribution": deep_clone(core_obj.get("event_distribution") or []),
        "signals": deep_clone(core_obj.get("trajectory_signals") or {}),
        "regime": deep_clone(core_obj.get("regime") or {}),
        "alignment_entropy": float(core_obj.get("alignment_entropy") or 0.0),
        "voice": str(core_obj.get("voice") or ""),
        "timestamp": str(core_obj.get("timestamp") or ""),
    }


def _forbidden_in_modifications(modifications: dict[str, Any], path: str = "") -> list[str]:
    issues: list[str] = []
    if not isinstance(modifications, dict):
        return [f"modifications must be object at {path or 'root'}"]

    signals = modifications.get("signals")
    if isinstance(signals, dict):
        for key in signals:
            if key in FORBIDDEN_SIGNAL_OVERWRITE:
                issues.append(f"forbidden signal overwrite: {key}")

    regime_adj = modifications.get("regime_adjustments")
    if isinstance(regime_adj, dict):
        if "label" in regime_adj:
            issues.append("forbidden regime_adjustments.label")
        for key in regime_adj:
            if key not in ("confidence_delta", "confidence"):
                issues.append(f"forbidden regime_adjustments key: {key}")

    annotations = modifications.get("annotations")
    if annotations is not None and not isinstance(annotations, dict):
        issues.append("modifications.annotations must be object")

    for forbidden in ("event_distribution", "alignment_entropy", "trajectory_signals"):
        if forbidden in modifications:
            issues.append(f"forbidden top-level modification key: {forbidden}")

    return issues


def validate_plugin_output(output: dict[str, Any], *, expected_name: str | None = None) -> list[str]:
    issues: list[str] = []
    if not isinstance(output, dict):
        return ["plugin output must be object"]

    name = output.get("plugin_name")
    if not isinstance(name, str) or not name.strip():
        issues.append("plugin_name must be non-empty string")
    elif expected_name and name != expected_name:
        issues.append(f"plugin_name mismatch: expected {expected_name!r}, got {name!r}")

    confidence = output.get("confidence")
    if not isinstance(confidence, (int, float)):
        issues.append("confidence must be number")
    elif not 0.0 <= float(confidence) <= 1.0:
        issues.append("confidence must be in [0.0, 1.0]")

    modifications = output.get("modifications")
    if not isinstance(modifications, dict):
        issues.append("modifications must be object")
    else:
        for key in ("signals", "regime_adjustments", "annotations"):
            if key not in modifications:
                issues.append(f"modifications missing {key}")
        issues.extend(_forbidden_in_modifications(modifications))

    return issues


def normalize_plugin_weights(outputs: list[dict[str, Any]]) -> list[float]:
    """Return per-plugin weights capped so aggregate <= MAX_PLUGIN_INFLUENCE."""
    raw = [max(0.0, min(1.0, float(o.get("confidence") or 0.0))) for o in outputs]
    total = sum(raw)
    if total <= 0:
        return [0.0] * len(raw)
    if total <= MAX_PLUGIN_INFLUENCE:
        return raw
    scale = MAX_PLUGIN_INFLUENCE / total
    return [round(w * scale, 6) for w in raw]


def detect_input_mutation(before: dict[str, Any], after: dict[str, Any]) -> bool:
    return json.dumps(before, sort_keys=True) != json.dumps(after, sort_keys=True)


class EpistemicPlugin(ABC):
    """Base plugin — operates on cloned core input only."""

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def version(self) -> str:
        pass

    @abstractmethod
    def plugin_type(self) -> PluginType:
        pass

    @abstractmethod
    def apply(self, core_input: dict[str, Any]) -> dict[str, Any]:
        """Return PluginOutput dict; must not mutate core_input."""
        pass

    def apply_safe(self, core_input: dict[str, Any]) -> dict[str, Any]:
        snapshot = deep_clone(core_input)
        result = self.apply(deep_clone(core_input))
        if detect_input_mutation(snapshot, core_input):
            raise ValueError(f"plugin {self.name()} mutated input")
        issues = validate_plugin_output(result, expected_name=self.name())
        if issues:
            raise ValueError(f"plugin {self.name()} invalid output: {'; '.join(issues)}")
        return result
