"""Plugin orchestration — clone, apply, merge, build enriched artifact."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.plugins.base import (  # noqa: E402
    MAX_PLUGIN_INFLUENCE,
    core_object_to_plugin_input,
    deep_clone,
)
from prediction.plugins.conflict_resolver import (  # noqa: E402
    merge_evaluation_rollups,
    merge_object,
)
from prediction.plugins.evaluation_plugins import CanonicalCalibrationEval  # noqa: E402
from prediction.plugins.registry import load_evaluation_plugins, load_plugins  # noqa: E402
from prediction_lib import load_event_registry  # noqa: E402


def run_plugins_on_object(
    core_obj: dict[str, Any],
    plugins: list[Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Apply each plugin in isolation on cloned input; return outputs + merged view."""
    plugin_list = plugins if plugins is not None else load_plugins()
    outputs: list[dict[str, Any]] = []
    for plugin in plugin_list:
        if plugin.plugin_type() == "evaluation":
            continue
        core_input = core_object_to_plugin_input(core_obj)
        outputs.append(plugin.apply_safe(core_input))
    merged = merge_object(core_obj, outputs)
    return outputs, merged


def build_enriched_payload(
    bundle: dict[str, Any],
    *,
    registry: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build epistemic_enriched.json from core bundle."""
    epistemic_state = bundle.get("epistemic_state") or {}
    objects = epistemic_state.get("objects") or []
    meta = epistemic_state.get("_meta") or {}

    plugins = load_plugins()
    plugin_names = [p.name() for p in plugins]

    enriched_objects: list[dict[str, Any]] = []
    for core_obj in objects:
        if not isinstance(core_obj, dict):
            continue
        core_copy = deep_clone(core_obj)
        plugin_results, merged = run_plugins_on_object(core_copy, plugins)
        enriched_objects.append(
            {
                "core": core_copy,
                "plugin_results": plugin_results,
                "merged": merged,
            }
        )

    reg = registry if registry is not None else load_event_registry()
    eval_rollups: list[dict[str, Any]] = []
    for eval_plugin in load_evaluation_plugins():
        if isinstance(eval_plugin, CanonicalCalibrationEval):
            eval_rollups.append(
                eval_plugin.evaluate(core_objects=objects, registry=reg)
            )

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/prediction/plugins/runner.py",
            "phase": "episystem-plugin-layer",
            "core_artifact": "runtime/artifacts/epistemic_state.json",
            "plugin_influence_cap": MAX_PLUGIN_INFLUENCE,
            "plugins_applied": plugin_names,
        },
        "interpretation": "epistemic_enriched",
        "core_ref": {
            "object_count": meta.get("object_count", len(objects)),
            "epistemic_source": meta.get("epistemic_source", "heuristic_v1"),
        },
        "objects": enriched_objects,
        "evaluation": merge_evaluation_rollups(eval_rollups),
    }
