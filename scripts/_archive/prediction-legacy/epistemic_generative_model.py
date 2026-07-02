"""PR1 ENGM — heuristic epistemic narrative generative model (read-only advisory layer)."""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.contracts import has_string_falsifier, has_valid_falsifier_model
from prediction.signal_math import clamp01

LATENT_DIMENSIONS = (
    "geopolitical_tension",
    "regime_stability",
    "alliance_coherence",
    "escalation_pressure",
)

OBSERVATION_CLASSES = (
    "affirm_escalation",
    "affirm_deescalation",
    "withhold",
)

VOICES = ("freeman", "mercouris", "macgregor")

# Hand-calibrated W_v rows: [tension, stability, coherence, escalation] -> logits per class
VOICE_WEIGHTS: dict[str, list[list[float]]] = {
    "freeman": [
        [0.8, -0.6, 0.2, 0.4],
        [-0.9, 0.7, 0.3, -0.5],
        [0.1, 0.2, -0.3, 0.0],
    ],
    "mercouris": [
        [0.4, -0.2, 0.3, 0.3],
        [-0.4, 0.3, 0.2, -0.3],
        [0.2, 0.3, -0.1, 0.1],
    ],
    "macgregor": [
        [1.0, -0.4, -0.2, 0.9],
        [-0.5, 0.2, -0.1, -0.4],
        [0.0, 0.1, -0.2, 0.0],
    ],
}

VOICE_BIAS: dict[str, list[float]] = {
    "freeman": [-0.2, 0.3, 0.0],
    "mercouris": [0.0, 0.0, 0.1],
    "macgregor": [0.2, -0.3, -0.1],
}

EVENT_BUCKET_WEIGHTS: dict[str, list[float]] = {
    "iran": [0.35, 0.15, 0.15, 0.35],
    "ukraine": [0.30, 0.20, 0.20, 0.30],
    "nato": [0.25, 0.25, 0.35, 0.15],
    "israel": [0.30, 0.20, 0.20, 0.30],
    "gaza": [0.35, 0.15, 0.15, 0.35],
    "default": [0.25, 0.25, 0.25, 0.25],
}

PROB_EPSILON = 0.02
PROB_CEILING = 0.98

def softmax(logits: list[float]) -> list[float]:
    if not logits:
        return []
    max_logit = max(float(x) for x in logits)
    exps = [math.exp(float(x) - max_logit) for x in logits]
    total = sum(exps) or 1.0
    return [round(v / total, 4) for v in exps]

def clamp_probability(value: float) -> float:
    return max(PROB_EPSILON, min(PROB_CEILING, float(value)))

def _dot(weights: list[float], z: list[float]) -> float:
    return sum(float(w) * float(v) for w, v in zip(weights, z))

def _escalation_label_to_scalar(label: str) -> float:
    mapping = {"increasing": 0.75, "stable": 0.5, "decreasing": 0.25}
    return mapping.get(str(label or "").casefold(), 0.5)

def _alignment_label_to_scalar(label: str) -> float:
    mapping = {"high": 0.8, "moderate": 0.55, "low": 0.3}
    return mapping.get(str(label or "").casefold(), 0.5)

def _mean_signal_drift(signals: dict[str, Any]) -> float:
    deltas: list[float] = []
    for block in (signals or {}).values():
        if not isinstance(block, dict):
            continue
        drift = block.get("drift_vector") or []
        if isinstance(drift, list) and len(drift) >= 2:
            deltas.append(float(drift[-1]) - float(drift[0]))
        elif isinstance(drift, list) and drift:
            deltas.append(float(drift[-1]))
    if not deltas:
        return 0.5
    return clamp01(sum(deltas) / len(deltas))

def _mean_escalation_tail(signals: dict[str, Any]) -> float:
    tails: list[float] = []
    for block in (signals or {}).values():
        if not isinstance(block, dict):
            continue
        drift = block.get("drift_vector") or []
        if isinstance(drift, list) and drift:
            tails.append(float(drift[-1]))
    if not tails:
        return 0.5
    return clamp01(sum(tails) / len(tails))

def _resolved_ratio(registry: dict[str, dict[str, Any]]) -> float:
    if not registry:
        return 0.5
    resolved = sum(1 for ev in registry.values() if str(ev.get("status") or "") == "resolved")
    return clamp01(resolved / len(registry))

def _regime_shift_rate(signals: dict[str, Any]) -> float:
    if not signals:
        return 0.0
    hits = sum(1 for block in signals.values() if isinstance(block, dict) and block.get("regime_shift_detected"))
    return hits / max(len(signals), 1)

def infer_latent_state(
    *,
    registry: dict[str, dict[str, Any]],
    signals: dict[str, Any],
    regime: dict[str, Any],
) -> dict[str, Any]:
    global_signals = (regime or {}).get("global_signals") or {}
    tension = clamp01(
        0.55 * _escalation_label_to_scalar(str(global_signals.get("geopolitical_escalation") or "stable"))
        + 0.45 * _mean_signal_drift(signals)
    )
    stability = clamp01(
        0.5 * (1.0 - _regime_shift_rate(signals))
        + 0.5 * _resolved_ratio(registry)
    )
    coherence = _alignment_label_to_scalar(str(global_signals.get("voice_alignment") or "moderate"))
    escalation = clamp01(
        0.6 * _mean_escalation_tail(signals)
        + 0.4 * tension
    )
    z = [round(tension, 4), round(stability, 4), round(coherence, 4), round(escalation, 4)]
    return {
        "Z": z,
        "dimensions": list(LATENT_DIMENSIONS),
        "inference_source": "heuristic_v1",
    }

def sensor_weight_for_voice(voice: str, *, semantic_events: dict[str, Any] | None = None) -> float:
    if str(voice).casefold() != "macgregor":
        return 1.0
    scores = semantic_events or {}
    high_entropy = 0
    total = 0
    for block in scores.values():
        if not isinstance(block, dict):
            continue
        total += 1
        if float(block.get("entropy_score") or 0) >= 0.85:
            high_entropy += 1
    if total and high_entropy / total >= 0.5:
        return 0.5
    return 0.85

def project_voice(Z: list[float], voice: str, *, sensor_weight: float = 1.0) -> dict[str, Any]:
    key = str(voice).casefold()
    weights = VOICE_WEIGHTS.get(key, VOICE_WEIGHTS["mercouris"])
    bias = VOICE_BIAS.get(key, VOICE_BIAS["mercouris"])
    logits = [_dot(row, Z) + float(b) for row, b in zip(weights, bias)]
    probs = softmax(logits)
    observation_probs = {
        cls: round(float(p) * sensor_weight + (1.0 - sensor_weight) * (1.0 / len(OBSERVATION_CLASSES)), 4)
        for cls, p in zip(OBSERVATION_CLASSES, probs)
    }
    total = sum(observation_probs.values()) or 1.0
    observation_probs = {k: round(v / total, 4) for k, v in observation_probs.items()}
    dominant = max(observation_probs, key=observation_probs.get)
    return {
        "observation_probs": observation_probs,
        "sensor_weight": round(sensor_weight, 4),
        "dominant_class": dominant,
        "voice_projection": key,
    }

def _event_bucket(event_id: str, question: str) -> str:
    blob = f"{event_id} {question}".casefold()
    for key in ("iran", "ukraine", "nato", "israel", "gaza"):
        if key in blob:
            return key
    return "default"

def _stance_agreement(timeline_event: dict[str, Any] | None) -> float:
    latest = (timeline_event or {}).get("latest_by_speaker") or {}
    if not isinstance(latest, dict) or len(latest) < 2:
        return 1.0
    stances = {str(row.get("stance") or "") for row in latest.values() if isinstance(row, dict)}
    stances.discard("")
    if len(stances) <= 1:
        return 1.0
    return clamp01(1.0 - (len(stances) - 1) / max(len(latest), 1))

def decode_event_probability(
    event_id: str,
    event: dict[str, Any],
    Z: list[float],
    *,
    signal_block: dict[str, Any] | None,
    timeline_event: dict[str, Any] | None,
) -> float:
    bucket = _event_bucket(event_id, str(event.get("question") or event_id))
    w_event = EVENT_BUCKET_WEIGHTS.get(bucket, EVENT_BUCKET_WEIGHTS["default"])
    alpha, beta, gamma = 0.5, 0.3, 0.2
    latent_term = _dot(w_event, Z)
    signal_conf = float((signal_block or {}).get("confidence") or 0.35)
    agreement = _stance_agreement(timeline_event)
    raw = alpha * latent_term + beta * signal_conf + gamma * agreement
    return round(clamp_probability(raw), 4)

def build_event_engm_block(
    event_id: str,
    event: dict[str, Any],
    Z: list[float],
    *,
    timeline_event: dict[str, Any] | None,
    signal_block: dict[str, Any] | None,
    semantic_events: dict[str, Any] | None,
) -> dict[str, Any]:
    latest = (timeline_event or {}).get("latest_by_speaker") or {}
    voices_present = sorted(latest.keys()) if isinstance(latest, dict) else list(VOICES)
    if not voices_present:
        voices_present = list(VOICES)

    voice_projections: dict[str, Any] = {}
    for voice in voices_present:
        weight = sensor_weight_for_voice(str(voice), semantic_events=semantic_events)
        voice_projections[str(voice)] = project_voice(Z, str(voice), sensor_weight=weight)

    return {
        "event_probability": decode_event_probability(
            event_id,
            event,
            Z,
            signal_block=signal_block,
            timeline_event=timeline_event,
        ),
        "interpretation": "probabilistic_projection",
        "voice_projections": voice_projections,
    }

def build_engm_payload(
    *,
    registry: dict[str, dict[str, Any]] | None = None,
    timeline: dict[str, Any] | None = None,
    disagreement: dict[str, Any] | None = None,
    semantic_scores: dict[str, Any] | None = None,
    signals: dict[str, Any] | None = None,
    regime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from prediction_lib import load_event_registry

    events = registry or load_event_registry()
    timeline_payload = timeline or {}
    signals_payload = signals or {}
    semantic_payload = semantic_scores or {}
    regime_payload = regime or {}

    signal_events = signals_payload.get("events") if isinstance(signals_payload, dict) else {}
    semantic_events = semantic_payload.get("events") if isinstance(semantic_payload, dict) else {}
    timeline_events = timeline_payload.get("events") if isinstance(timeline_payload, dict) else {}

    latent_state = infer_latent_state(
        registry=events,
        signals=signal_events if isinstance(signal_events, dict) else {},
        regime=regime_payload,
    )
    z = latent_state["Z"]

    events_out: dict[str, Any] = {}
    for event_id in sorted(events):
        event = events[event_id]
        if event.get("not_falsifiable"):
            continue
        if not has_string_falsifier(event) and not has_valid_falsifier_model(event):
            continue
        events_out[event_id] = build_event_engm_block(
            event_id,
            event,
            z,
            timeline_event=timeline_events.get(event_id) if isinstance(timeline_events, dict) else None,
            signal_block=signal_events.get(event_id) if isinstance(signal_events, dict) else None,
            semantic_events=semantic_events if isinstance(semantic_events, dict) else None,
        )

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_epistemic_generative_state.py",
            "phase": "engm-v1-advisory",
            "inference_source": "heuristic_v1",
        },
        "latent_state": latent_state,
        "events": events_out,
    }

def main() -> int:
    import argparse
    import json

    from prediction_lib import render_json

    default_timeline = _REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
    default_disagreement = _REPO_ROOT / "runtime" / "artifacts" / "prediction-disagreement.json"
    default_semantic = _REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"
    default_signals = _REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
    default_regime = _REPO_ROOT / "runtime" / "artifacts" / "prediction-regime-summary.json"
    default_output = _REPO_ROOT / "runtime" / "artifacts" / "epistemic-generative-state.json"

    def _load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeline", type=Path, default=default_timeline)
    parser.add_argument("--disagreement", type=Path, default=default_disagreement)
    parser.add_argument("--semantic-scores", type=Path, default=default_semantic)
    parser.add_argument("--signals", type=Path, default=default_signals)
    parser.add_argument("--regime", type=Path, default=default_regime)
    parser.add_argument("--output", type=Path, default=default_output)
    args = parser.parse_args()

    payload = build_engm_payload(
        timeline=_load(args.timeline),
        disagreement=_load(args.disagreement),
        semantic_scores=_load(args.semantic_scores),
        signals=_load(args.signals),
        regime=_load(args.regime),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    print(f"[ok] wrote {args.output.relative_to(_REPO_ROOT)} ({len(payload.get('events') or {})} event(s))")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
