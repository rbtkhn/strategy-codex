"""PR6 ablation study — subsystem contribution evaluation (read-only, stdlib)."""

from __future__ import annotations

import copy
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.baseline_models import (  # noqa: E402
    LOW_N_PROBABILITY_THRESHOLD,
    evaluate_model_on_test,
    predict_system,
    predict_regime_system,
    probability_rows,
)
from prediction.epistemic_dataset_builder import DEFAULT_SPLIT_DATE, build_dataset_payload  # noqa: E402
from prediction.epistemic_generative_model import OBSERVATION_CLASSES  # noqa: E402
from prediction.epistemic_generative_model import build_engm_payload  # noqa: E402
from prediction.epistemic_loss import regime_shift_delay, shannon_entropy  # noqa: E402
from prediction.signal_extraction_engine import (  # noqa: E402
    ablation_falsifier_context,
    build_signals_payload,
)

LOW_N_SHIFT_SUPPORT_THRESHOLD = 1
DROP_METRIC = "brier"

COMPONENT_BY_VARIANT = {
    "no_compression": "compression",
    "no_falsifier_model": "falsifier_model",
    "no_signal_extraction": "signal_extraction",
    "no_disagreement_graph": "disagreement_graph",
}


@dataclass(frozen=True)
class AblationFlags:
    compression: bool = True
    falsifier_model: bool = True
    signal_extraction: bool = True
    disagreement_graph: bool = True


VARIANTS: dict[str, AblationFlags] = {
    "full": AblationFlags(),
    "no_compression": AblationFlags(compression=False),
    "no_falsifier_model": AblationFlags(falsifier_model=False),
    "no_signal_extraction": AblationFlags(signal_extraction=False),
    "no_disagreement_graph": AblationFlags(disagreement_graph=False),
}


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def neutralize_signals_payload(signals: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(signals)
    events = payload.get("events")
    if not isinstance(events, dict):
        return payload
    for event_id, block in events.items():
        if not isinstance(block, dict):
            continue
        drift = block.get("drift_vector")
        if isinstance(drift, list) and drift:
            neutral_drift = [round(float(drift[0]), 4)] * len(drift)
        else:
            neutral_drift = [0.444]
        events[event_id] = {
            **block,
            "confidence": 0.5,
            "cross_voice_alignment": 1.0,
            "drift_vector": neutral_drift,
            "regime_shift_detected": False,
            "signal_type": "directional",
        }
    return payload


def neutralize_disagreement_payload(disagreement: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(disagreement)
    events = payload.get("events")
    if not isinstance(events, dict):
        return payload
    for event_id, block in events.items():
        if not isinstance(block, dict):
            continue
        empty_dist = {"yes": 0, "no": 0, "uncertain": 0, "conditional": 0}
        neutral_level = {
            "total_predictions": 0,
            "distribution": empty_dist,
            "disagreement_score_raw": 0.0,
            "disagreement_score_normalized": 0.0,
        }
        events[event_id] = {
            **block,
            "disagreements": {"stance": {}, "mechanism": [], "horizon": []},
            "prediction_level": dict(neutral_level),
            "latest_voice_level": {
                **neutral_level,
                "total_voices": 0,
            },
            "legacy_gini": {
                "prediction_level": dict(neutral_level),
                "latest_voice_level": dict(neutral_level),
            },
        }
    return payload


def prepare_ablation_inputs(
    flags: AblationFlags,
    *,
    registry: dict[str, dict[str, Any]],
    timeline: dict[str, Any],
    signals: dict[str, Any],
    disagreement: dict[str, Any],
    semantic_scores: dict[str, Any],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    reg = dict(registry)
    tl = timeline
    sem = semantic_scores

    if not flags.disagreement_graph:
        dis = neutralize_disagreement_payload(disagreement)
    else:
        dis = disagreement

    if not flags.signal_extraction:
        sig = neutralize_signals_payload(signals)
    elif not flags.disagreement_graph:
        sig = build_signals_payload(
            events=reg,
            timeline=tl,
            disagreement=dis,
            semantic_scores=sem,
        )
    else:
        sig = signals

    return reg, tl, sig, dis, sem


def rebuild_membrane(
    flags: AblationFlags,
    *,
    registry: dict[str, dict[str, Any]],
    timeline: dict[str, Any],
    signals: dict[str, Any],
    disagreement: dict[str, Any],
    semantic_scores: dict[str, Any],
    regime: dict[str, Any],
    split_date: str,
) -> dict[str, Any]:
    reg, tl, sig, dis, sem = prepare_ablation_inputs(
        flags,
        registry=registry,
        timeline=timeline,
        signals=signals,
        disagreement=disagreement,
        semantic_scores=semantic_scores,
    )

    with ablation_falsifier_context(not flags.falsifier_model):
        engm = build_engm_payload(
            registry=reg,
            timeline=tl,
            disagreement=dis,
            semantic_scores=sem,
            signals=sig,
            regime=regime,
        )
        dataset = build_dataset_payload(
            registry=reg,
            timeline=tl,
            signals=sig,
            semantic_scores=sem,
            engm=engm,
            split_date=split_date,
            include_duplicate_fingerprint_events=not flags.compression,
            compression_checked=flags.compression,
        )

    return {
        "engm": engm,
        "dataset": dataset,
        "signals": sig,
        "disagreement": dis,
    }


def _pooled_observation_probs(engm: dict[str, Any]) -> list[float]:
    events = engm.get("events") if isinstance(engm, dict) else {}
    pooled = {cls: 0.0 for cls in OBSERVATION_CLASSES}
    count = 0
    if not isinstance(events, dict):
        return [0.0] * len(OBSERVATION_CLASSES)
    for block in events.values():
        if not isinstance(block, dict):
            continue
        projections = block.get("voice_projections") or {}
        if not isinstance(projections, dict):
            continue
        for projection in projections.values():
            if not isinstance(projection, dict):
                continue
            probs = projection.get("observation_probs") or {}
            if not isinstance(probs, dict):
                continue
            count += 1
            for cls in OBSERVATION_CLASSES:
                pooled[cls] += float(probs.get(cls) or 0.0)
    if count <= 0:
        return [1.0 / len(OBSERVATION_CLASSES)] * len(OBSERVATION_CLASSES)
    return [round(pooled[cls] / count, 4) for cls in OBSERVATION_CLASSES]


def _graph_coherence(disagreement: dict[str, Any]) -> float | None:
    events = disagreement.get("events") if isinstance(disagreement, dict) else {}
    if not isinstance(events, dict) or not events:
        return None
    norms: list[float] = []
    for block in events.values():
        if not isinstance(block, dict):
            continue
        level = block.get("latest_voice_level") or {}
        if isinstance(level, dict):
            norms.append(float(level.get("disagreement_score_normalized") or 0.0))
    if not norms:
        return None
    return round(1.0 - (sum(norms) / len(norms)), 4)


def _mean_cross_voice_alignment(test_rows: list[dict[str, Any]]) -> float | None:
    values: list[float] = []
    for row in test_rows:
        latent = row.get("latent_features") or {}
        if not isinstance(latent, dict):
            continue
        signal = latent.get("signal_vector")
        if isinstance(signal, list) and len(signal) > 1:
            values.append(float(signal[1]))
    if not values:
        return None
    return round(sum(values) / len(values), 4)


def _regime_shift_delay_mean(
    test_rows: list[dict[str, Any]],
    *,
    timeline: dict[str, Any],
    signals: dict[str, Any],
    regime: dict[str, Any],
    split_date: str,
) -> float | None:
    timeline_events = timeline.get("events") if isinstance(timeline, dict) else {}
    signal_events = signals.get("events") if isinstance(signals, dict) else {}
    if not isinstance(timeline_events, dict):
        return None

    seen: set[str] = set()
    delays: list[float] = []
    eval_date = split_date
    for row in test_rows:
        event_id = str(row.get("event_id") or "")
        if not event_id or event_id in seen:
            continue
        seen.add(event_id)
        block = regime_shift_delay(
            timeline_event=timeline_events.get(event_id),
            signal_block=signal_events.get(event_id) if isinstance(signal_events, dict) else None,
            regime=regime,
            eval_date=eval_date,
        )
        if isinstance(block, dict) and block.get("shift_count", 0):
            delays.append(float(block.get("value") or 0.0))
    if not delays:
        return 0.0
    return round(sum(delays) / len(delays), 4)


def score_variant(
    membrane: dict[str, Any],
    *,
    timeline: dict[str, Any],
    regime: dict[str, Any],
    split_date: str,
) -> dict[str, Any]:
    dataset = membrane.get("dataset") or {}
    engm = membrane.get("engm") or {}
    signals = membrane.get("signals") or {}
    disagreement = membrane.get("disagreement") or {}
    test_rows = list(dataset.get("test") or [])

    system_metrics = evaluate_model_on_test(
        test_rows,
        probability_predict=predict_system,
        regime_predict=predict_regime_system,
    )
    prob_n = system_metrics.get("n_probability") or 0

    entropy_probs = _pooled_observation_probs(engm)
    entropy_value = shannon_entropy(entropy_probs)

    return {
        "core": {
            "n_probability": prob_n,
            "brier": system_metrics.get("brier"),
            "accuracy": system_metrics.get("accuracy"),
            "regime_shift_delay_mean": _regime_shift_delay_mean(
                test_rows,
                timeline=timeline,
                signals=signals,
                regime=regime,
                split_date=split_date,
            ),
        },
        "structural": {
            "entropy_stability": entropy_value,
            "graph_coherence": _graph_coherence(disagreement),
            "cross_voice_alignment_mean": _mean_cross_voice_alignment(test_rows),
        },
    }


def compute_drops(
    variants: dict[str, dict[str, Any]],
    *,
    metric: str = DROP_METRIC,
    reference: str = "full",
) -> list[dict[str, Any]]:
    ref = variants.get(reference) or {}
    ref_core = ref.get("core") if isinstance(ref, dict) else {}
    ref_value = (ref_core or {}).get(metric) if isinstance(ref_core, dict) else None
    ref_n = (ref_core or {}).get("n_probability") if isinstance(ref_core, dict) else 0

    drops: list[dict[str, Any]] = []
    for variant_name, flags in VARIANTS.items():
        if variant_name == reference:
            continue
        component = COMPONENT_BY_VARIANT.get(variant_name, variant_name)
        block = variants.get(variant_name) or {}
        core = block.get("core") if isinstance(block, dict) else {}
        value = (core or {}).get(metric) if isinstance(core, dict) else None
        n_prob = (core or {}).get("n_probability") if isinstance(core, dict) else 0

        entry: dict[str, Any] = {
            "component": component,
            "variant": variant_name,
            "metric": metric,
            "performance_drop": None,
        }
        if ref_n < 1 or n_prob < 1 or ref_value is None or value is None:
            entry["note"] = "low_n"
        else:
            entry["performance_drop"] = round(float(value) - float(ref_value), 4)
        drops.append(entry)
    return drops


def build_ablation_payload(
    *,
    registry: dict[str, dict[str, Any]] | None = None,
    timeline: dict[str, Any] | None = None,
    signals: dict[str, Any] | None = None,
    disagreement: dict[str, Any] | None = None,
    semantic_scores: dict[str, Any] | None = None,
    regime: dict[str, Any] | None = None,
    split_date: str | None = None,
) -> dict[str, Any]:
    from prediction_lib import load_event_registry

    events = registry if registry is not None else load_event_registry()
    tl = timeline or {}
    sig = signals or {}
    dis = disagreement or {}
    sem = semantic_scores or {}
    reg = regime or {}
    pinned_split = split_date or DEFAULT_SPLIT_DATE

    variant_scores: dict[str, Any] = {}
    membranes: dict[str, Any] = {}
    for name, flags in VARIANTS.items():
        membrane = rebuild_membrane(
            flags,
            registry=events,
            timeline=tl,
            signals=sig,
            disagreement=dis,
            semantic_scores=sem,
            regime=reg,
            split_date=pinned_split,
        )
        membranes[name] = membrane
        variant_scores[name] = score_variant(
            membrane,
            timeline=tl,
            regime=reg,
            split_date=pinned_split,
        )

    full_core = (variant_scores.get("full") or {}).get("core") or {}
    test_prob_n = int(full_core.get("n_probability") or 0)
    full_test = list((membranes.get("full") or {}).get("dataset", {}).get("test") or [])
    regime_f1_support = sum(
        1
        for row in full_test
        if str((row.get("task_labels") or {}).get("regime_shift") or "") == "shift"
    )

    low_n = (
        test_prob_n < LOW_N_PROBABILITY_THRESHOLD
        or regime_f1_support < LOW_N_SHIFT_SUPPORT_THRESHOLD
    )

    drops = compute_drops(variant_scores, metric=DROP_METRIC, reference="full")
    insight = (
        "Each drop row measures Brier delta vs full system on the PR4 test split; "
        "low_n when test_probability_n < 5."
    )
    if low_n:
        insight += " Current corpus is structurally valid but not yet discriminative."

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_ablation_study.py",
            "phase": "pr6-advisory",
            "ablation_source": "heuristic_v1",
            "split_date": pinned_split,
            "low_n_advisory": low_n,
            "reference_variant": "full",
            "drop_metric": DROP_METRIC,
            "eval_scope": {
                "test_probability_n": test_prob_n,
                "test_shift_support": regime_f1_support,
            },
        },
        "interpretation": "ablation_evaluation",
        "variants": variant_scores,
        "drops": drops,
        "insight": insight,
    }


def main() -> int:
    import argparse
    import json

    from prediction_lib import render_json

    default_timeline = _REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
    default_signals = _REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
    default_disagreement = _REPO_ROOT / "runtime" / "artifacts" / "prediction-disagreement.json"
    default_semantic = _REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"
    default_regime = _REPO_ROOT / "runtime" / "artifacts" / "prediction-regime-summary.json"
    default_dataset = _REPO_ROOT / "runtime" / "artifacts" / "epistemic-dataset.json"
    default_output = _REPO_ROOT / "runtime" / "artifacts" / "ablation-study.json"

    def _load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=default_output)
    args = parser.parse_args()

    dataset_meta = (_load(default_dataset).get("_meta") or {}) if default_dataset.is_file() else {}
    split_date = str(dataset_meta.get("split_date") or DEFAULT_SPLIT_DATE)

    payload = build_ablation_payload(
        timeline=_load(default_timeline),
        signals=_load(default_signals),
        disagreement=_load(default_disagreement),
        semantic_scores=_load(default_semantic),
        regime=_load(default_regime),
        split_date=split_date,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    scope = payload["_meta"]["eval_scope"]
    print(
        f"[ok] wrote {args.output.relative_to(_REPO_ROOT)} "
        f"(test_probability_n={scope['test_probability_n']}, low_n={payload['_meta']['low_n_advisory']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
