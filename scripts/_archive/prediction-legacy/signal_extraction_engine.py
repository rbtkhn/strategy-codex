"""Phase 4.5 signal extraction — directional intelligence from probabilistic views."""

from __future__ import annotations

import contextvars
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.contracts import has_string_falsifier, has_valid_falsifier_model, validate_falsifier_model
from prediction.probabilistic_falsifier_engine import infer_falsifier_model
from prediction.signal_math import (
    clamp01,
    detect_step_change,
    drift_vector,
    entropy_stable_high,
    is_monotonic_decreasing,
    is_monotonic_increasing,
)

_ablation_no_falsifier: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "ablation_no_falsifier",
    default=False,
)

SIGNAL_TYPES = frozenset(
    {"directional", "convergence", "divergence", "regime_shift", "saturation"}
)

ESCALATION_KEYWORDS = (
    "escalation",
    "escalate",
    "exposure",
    "holds",
    "hold",
    "increase",
    "expand",
)
CAPITULATION_KEYWORDS = (
    "capitulation",
    "capitulate",
    "fail",
    "fails",
    "withdrawal",
    "retrenchment",
    "stalemate",
    "fragmentation",
)

def _mode_ids(model: dict[str, Any]) -> list[str]:
    modes = model.get("failure_modes") or []
    return [str(m.get("id") or "") for m in modes if isinstance(m, dict)]

def _mode_probabilities(model: dict[str, Any]) -> list[float]:
    modes = model.get("failure_modes") or []
    return [float(m.get("probability") or 0) for m in modes if isinstance(m, dict)]

def effective_falsifier_model(
    event_id: str,
    event: dict[str, Any],
    *,
    ablation_no_falsifier: bool | None = None,
) -> tuple[dict[str, Any], str]:
    disabled = (
        ablation_no_falsifier
        if ablation_no_falsifier is not None
        else _ablation_no_falsifier.get()
    )
    if disabled:
        return (
            {
                "failure_modes": [{"id": "ablation_uniform", "probability": 1.0, "label": "uniform"}],
                "distribution_source": "ablation_stub",
            },
            "ablation_stub",
        )
    model = event.get("falsifier_model")
    if isinstance(model, dict) and not validate_falsifier_model(model):
        return model, "persisted"
    inferred = infer_falsifier_model(event_id, event)
    return inferred, "inferred_view"

@contextmanager
def ablation_falsifier_context(disabled: bool) -> Iterator[None]:
    token = _ablation_no_falsifier.set(bool(disabled))
    try:
        yield
    finally:
        _ablation_no_falsifier.reset(token)

def _keyword_boost(mode_id: str, keywords: tuple[str, ...]) -> bool:
    slug = mode_id.casefold()
    return any(k in slug for k in keywords)

def _normalize_probs(probs: list[float]) -> list[float]:
    total = sum(probs)
    if total <= 0:
        n = len(probs) or 1
        return [1.0 / n] * n
    return [round(p / total, 4) for p in probs]

def _apply_stance_tilt(
    probs: list[float],
    mode_ids: list[str],
    stance: str,
    *,
    tilt_cap: float,
) -> list[float]:
    if not probs:
        return probs
    stance_key = str(stance or "").casefold()
    epsilon = min(0.08, tilt_cap)
    adjusted = list(probs)
    for idx, mode_id in enumerate(mode_ids):
        if stance_key == "yes" and _keyword_boost(mode_id, ESCALATION_KEYWORDS):
            adjusted[idx] += epsilon
        elif stance_key == "no" and _keyword_boost(mode_id, CAPITULATION_KEYWORDS):
            adjusted[idx] += epsilon
        elif stance_key in {"uncertain", "conditional"}:
            adjusted[idx] = adjusted[idx] * (1.0 - epsilon) + (1.0 / len(adjusted)) * epsilon
    return _normalize_probs(adjusted)

def _primary_mode_index(mode_ids: list[str], probs: list[float]) -> int:
    escalation_scores = [
        (idx, prob + (0.05 if _keyword_boost(mid, ESCALATION_KEYWORDS) else 0.0))
        for idx, (mid, prob) in enumerate(zip(mode_ids, probs))
    ]
    return max(escalation_scores, key=lambda t: t[1])[0]

def _escalation_index(mode_ids: list[str], probs: list[float]) -> float:
    if not probs:
        return 0.0
    weighted = 0.0
    for mode_id, prob in zip(mode_ids, probs):
        if _keyword_boost(mode_id, ESCALATION_KEYWORDS):
            weighted += prob
        elif _keyword_boost(mode_id, CAPITULATION_KEYWORDS):
            weighted += prob * 0.25
        else:
            weighted += prob * 0.5
    return clamp01(weighted)

def build_probability_snapshots(
    event_id: str,
    event: dict[str, Any],
    model: dict[str, Any],
    timeline_event: dict[str, Any] | None,
    *,
    semantic_block: dict[str, Any] | None,
) -> tuple[list[float], list[float], str]:
    mode_ids = _mode_ids(model)
    base_probs = _mode_probabilities(model)
    if not base_probs:
        return [], [], ""

    entropy_score = float((semantic_block or {}).get("entropy_score") or 0.0)
    tilt_cap = 0.04 if entropy_score >= 0.85 else 0.08

    entries = (timeline_event or {}).get("entries") or []
    if not entries:
        idx = _primary_mode_index(mode_ids, base_probs)
        primary = mode_ids[idx] if idx < len(mode_ids) else mode_ids[0]
        value = _escalation_index(mode_ids, base_probs)
        return [round(value, 4)], base_probs, primary

    snapshots: list[float] = []
    entropy_series: list[float] = []
    sorted_entries = sorted(entries, key=lambda e: str(e.get("date") or ""))
    for entry in sorted_entries:
        stance = str(entry.get("stance") or "")
        tilted = _apply_stance_tilt(base_probs, mode_ids, stance, tilt_cap=tilt_cap)
        snapshots.append(round(_escalation_index(mode_ids, tilted), 4))
        import math

        ent = 0.0
        for p in tilted:
            if p > 0:
                ent -= p * math.log2(p)
        entropy_series.append(round(ent, 4))

    idx = _primary_mode_index(mode_ids, base_probs)
    primary = mode_ids[idx] if idx < len(mode_ids) else mode_ids[0]
    return snapshots, entropy_series, primary

def _voice_weight(speaker: str, *, entropy_score: float) -> float:
    if str(speaker).casefold() == "macgregor" and entropy_score >= 0.85:
        return 0.5
    return 1.0

def cross_voice_alignment(
    event_id: str,
    event: dict[str, Any],
    model: dict[str, Any],
    timeline_event: dict[str, Any] | None,
    *,
    semantic_block: dict[str, Any] | None,
) -> float:
    latest = (timeline_event or {}).get("latest_by_speaker") or {}
    if not isinstance(latest, dict) or len(latest) < 2:
        return 1.0

    mode_ids = _mode_ids(model)
    base_probs = _mode_probabilities(model)
    vectors: list[list[float]] = []
    weights: list[float] = []
    for speaker, row in sorted(latest.items()):
        if not isinstance(row, dict):
            continue
        tilt_cap = 0.04 if float((semantic_block or {}).get("entropy_score") or 0) >= 0.85 else 0.08
        tilted = _apply_stance_tilt(
            base_probs,
            mode_ids,
            str(row.get("stance") or ""),
            tilt_cap=tilt_cap,
        )
        vectors.append(tilted)
        weights.append(_voice_weight(str(speaker), entropy_score=float((semantic_block or {}).get("entropy_score") or 0.0)))

    if len(vectors) < 2:
        return 1.0

    scores: list[float] = []
    pair_weights: list[float] = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            from prediction.signal_math import cosine_similarity

            scores.append(cosine_similarity(vectors[i], vectors[j]))
            pair_weights.append((weights[i] + weights[j]) / 2.0)
    if not scores:
        return 0.0
    total_w = sum(pair_weights) or len(scores)
    result = round(sum(s * w for s, w in zip(scores, pair_weights)) / total_w, 4)
    if float((semantic_block or {}).get("entropy_score") or 0) >= 0.85:
        if any(str(s).casefold() == "macgregor" for s in latest):
            result = round(result * 0.85, 4)
    return result

def _trend_text(signal_type: str, drift: list[float], primary_mode_id: str) -> str:
    if not drift:
        return f"stable probability around {primary_mode_id or 'primary mode'}"
    if is_monotonic_increasing(drift):
        return "steady escalation probability increase"
    if is_monotonic_decreasing(drift):
        return "steady de-escalation probability decrease"
    if signal_type == "convergence":
        return "cross-voice probability convergence"
    if signal_type == "divergence":
        return "cross-voice probability divergence"
    if signal_type == "regime_shift":
        return "step-change in probability trajectory"
    if signal_type == "saturation":
        return "entropy stable with unresolved stance variance"
    return f"mixed movement on {primary_mode_id or 'primary mode'}"

def classify_signal(
    *,
    drift: list[float],
    alignment: float,
    entropy_score: float,
    gini_norm: float,
    stance_variance: float,
    entropy_series: list[float],
) -> tuple[str, float, bool]:
    regime_shift = detect_step_change(drift)
    if regime_shift:
        confidence = clamp01(0.55 + max(abs(d) for d in drift) if drift else 0.0)
        return "regime_shift", round(confidence, 4), True

    if alignment >= 0.7 and entropy_score <= 0.45:
        return "convergence", round(clamp01(0.5 + alignment * 0.4), 4), False

    if alignment <= 0.35 or gini_norm >= 0.45:
        return "divergence", round(clamp01(0.45 + gini_norm * 0.4), 4), False

    if entropy_stable_high(entropy_series or [entropy_score]) and stance_variance >= 0.2:
        return "saturation", round(clamp01(0.5 + entropy_score * 0.3), 4), False

    if is_monotonic_increasing(drift) and drift and max(abs(d) for d in drift) >= 0.03:
        confidence = clamp01(0.5 + min(0.35, sum(drift) / max(len(drift), 1)))
        return "directional", round(confidence, 4), False

    if is_monotonic_decreasing(drift) and drift and max(abs(d) for d in drift) >= 0.03:
        confidence = clamp01(0.5 + min(0.35, abs(sum(drift)) / max(len(drift), 1)))
        return "directional", round(confidence, 4), False

    return "directional", 0.35, False

def _stance_variance(timeline_event: dict[str, Any] | None) -> float:
    latest = (timeline_event or {}).get("latest_by_speaker") or {}
    if not isinstance(latest, dict) or len(latest) < 2:
        return 0.0
    stances = {str(row.get("stance") or "") for row in latest.values() if isinstance(row, dict)}
    stances.discard("")
    if len(stances) <= 1:
        return 0.0
    return min(1.0, len(stances) / max(len(latest), 1))

def extract_event_signal(
    event_id: str,
    event: dict[str, Any],
    *,
    timeline_event: dict[str, Any] | None,
    disagreement_event: dict[str, Any] | None,
    semantic_block: dict[str, Any] | None,
) -> dict[str, Any]:
    model, distribution_source = effective_falsifier_model(event_id, event)
    snapshots, entropy_series, primary_mode_id = build_probability_snapshots(
        event_id,
        event,
        model,
        timeline_event,
        semantic_block=semantic_block,
    )
    drift = drift_vector(snapshots)
    alignment = cross_voice_alignment(
        event_id,
        event,
        model,
        timeline_event,
        semantic_block=semantic_block,
    )
    entropy_score = float((semantic_block or {}).get("entropy_score") or float(model.get("entropy") or 0.0))
    gini_norm = float(
        ((disagreement_event or {}).get("latest_voice_level") or {}).get("disagreement_score_normalized") or 0.0
    )
    stance_var = _stance_variance(timeline_event or {})
    signal_type, confidence, regime_shift = classify_signal(
        drift=drift,
        alignment=alignment,
        entropy_score=entropy_score,
        gini_norm=gini_norm,
        stance_variance=stance_var,
        entropy_series=entropy_series,
    )
    return {
        "signal_type": signal_type,
        "trend": _trend_text(signal_type, drift, primary_mode_id),
        "confidence": confidence,
        "cross_voice_alignment": alignment,
        "drift_vector": snapshots,
        "regime_shift_detected": regime_shift,
        "distribution_source": distribution_source,
        "primary_mode_id": primary_mode_id,
    }

def extract_signals(
    events: dict[str, dict[str, Any]],
    *,
    timeline: dict[str, Any],
    disagreement: dict[str, Any],
    semantic_scores: dict[str, Any],
) -> dict[str, Any]:
    timeline_events = timeline.get("events") or {}
    disagreement_events = disagreement.get("events") or {}
    semantic_events = semantic_scores.get("events") or {}
    out: dict[str, Any] = {}
    for event_id in sorted(events):
        event = events[event_id]
        if event.get("not_falsifiable"):
            continue
        if not has_string_falsifier(event) and not has_valid_falsifier_model(event):
            continue
        out[event_id] = extract_event_signal(
            event_id,
            event,
            timeline_event=timeline_events.get(event_id) if isinstance(timeline_events, dict) else None,
            disagreement_event=disagreement_events.get(event_id) if isinstance(disagreement_events, dict) else None,
            semantic_block=semantic_events.get(event_id) if isinstance(semantic_events, dict) else None,
        )
    return out

def _bucket_label(event_id: str, question: str) -> str | None:
    blob = f"{event_id} {question}".casefold()
    for key in ("iran", "ukraine", "nato", "israel", "gaza"):
        if key in blob:
            return key
    return None

def build_regime_summary(signals: dict[str, Any], events: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if not signals:
        return {
            "global_signals": {
                "geopolitical_escalation": "stable",
                "system_entropy": "stable_low",
                "voice_alignment": "moderate",
                "regime_shift_detected": False,
            }
        }

    alignments = [float(s.get("cross_voice_alignment") or 0) for s in signals.values()]
    avg_alignment = sum(alignments) / len(alignments) if alignments else 0.0
    if avg_alignment >= 0.65:
        voice_alignment = "high"
    elif avg_alignment >= 0.4:
        voice_alignment = "moderate"
    else:
        voice_alignment = "low"

    bucket_drifts: dict[str, list[float]] = {}
    regime_any = False
    entropy_hits = 0
    for event_id, signal in signals.items():
        if signal.get("regime_shift_detected"):
            regime_any = True
        question = str((events.get(event_id) or {}).get("question") or event_id)
        bucket = _bucket_label(event_id, question)
        drift = signal.get("drift_vector") or []
        if isinstance(drift, list) and len(drift) >= 2:
            delta = float(drift[-1]) - float(drift[0])
            if bucket:
                bucket_drifts.setdefault(bucket, []).append(delta)
        if signal.get("distribution_source") == "inferred_view":
            entropy_hits += 1

    escalation_label = "stable"
    if bucket_drifts:
        avg_delta = sum(sum(v) / len(v) for v in bucket_drifts.values() if v) / len(bucket_drifts)
        if avg_delta >= 0.05:
            escalation_label = "increasing"
        elif avg_delta <= -0.05:
            escalation_label = "decreasing"

    entropy_ratio = entropy_hits / max(len(signals), 1)
    if entropy_ratio >= 0.5:
        system_entropy = "stable_high"
    elif entropy_ratio >= 0.2:
        system_entropy = "rising"
    else:
        system_entropy = "stable_low"

    return {
        "global_signals": {
            "geopolitical_escalation": escalation_label,
            "system_entropy": system_entropy,
            "voice_alignment": voice_alignment,
            "regime_shift_detected": regime_any,
        }
    }

def build_signals_payload(
    events: dict[str, dict[str, Any]] | None = None,
    *,
    timeline: dict[str, Any] | None = None,
    disagreement: dict[str, Any] | None = None,
    semantic_scores: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from prediction_lib import load_event_registry

    registry = events or load_event_registry()
    timeline_payload = timeline or {}
    disagreement_payload = disagreement or {}
    semantic_payload = semantic_scores or {}
    signals = extract_signals(
        registry,
        timeline=timeline_payload,
        disagreement=disagreement_payload,
        semantic_scores=semantic_payload,
    )
    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_prediction_signals.py",
            "phase": "4.5-advisory",
        },
        "events": signals,
    }

def build_regime_summary_payload(
    signals_payload: dict[str, Any],
    events: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    from prediction_lib import load_event_registry

    registry = events or load_event_registry()
    signals = signals_payload.get("events") or {}
    summary = build_regime_summary(signals, registry)
    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_prediction_regime_summary.py",
            "phase": "4.5-advisory",
        },
        **summary,
    }

def main() -> int:
    import argparse
    import json
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]
    scripts = repo_root / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))

    from prediction_lib import render_json  # noqa: E402

    default_timeline = repo_root / "runtime" / "artifacts" / "prediction-timeline.json"
    default_disagreement = repo_root / "runtime" / "artifacts" / "prediction-disagreement.json"
    default_semantic = repo_root / "runtime" / "artifacts" / "prediction-semantic-scores.json"
    default_signals = repo_root / "runtime" / "artifacts" / "prediction-signals.json"
    default_regime = repo_root / "runtime" / "artifacts" / "prediction-regime-summary.json"

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeline", type=Path, default=default_timeline)
    parser.add_argument("--disagreement", type=Path, default=default_disagreement)
    parser.add_argument("--semantic-scores", type=Path, default=default_semantic)
    parser.add_argument("--signals-output", type=Path, default=default_signals)
    parser.add_argument("--regime-output", type=Path, default=default_regime)
    args = parser.parse_args()

    timeline = json.loads(args.timeline.read_text(encoding="utf-8")) if args.timeline.is_file() else {}
    disagreement = json.loads(args.disagreement.read_text(encoding="utf-8")) if args.disagreement.is_file() else {}
    semantic = json.loads(args.semantic_scores.read_text(encoding="utf-8")) if args.semantic_scores.is_file() else {}

    signals_payload = build_signals_payload(
        timeline=timeline,
        disagreement=disagreement,
        semantic_scores=semantic,
    )
    regime_payload = build_regime_summary_payload(signals_payload)

    args.signals_output.parent.mkdir(parents=True, exist_ok=True)
    args.regime_output.parent.mkdir(parents=True, exist_ok=True)
    args.signals_output.write_text(render_json(signals_payload), encoding="utf-8")
    args.regime_output.write_text(render_json(regime_payload), encoding="utf-8")
    print(f"[ok] wrote {args.signals_output.relative_to(repo_root)} ({len(signals_payload.get('events') or {})} signal(s))")
    print(f"[ok] wrote {args.regime_output.relative_to(repo_root)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
