"""Episystem canonical core — claim → SAL → signal → regime (single inference authority)."""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.soft_alignment import (  # noqa: E402
    load_terms_index,
    soft_align,
)
from prediction_lib import load_event_registry  # noqa: E402
from registry_pipeline.signal_math import clamp01, cosine_similarity  # noqa: E402
from voice_prediction_pilot import (  # noqa: E402
    VOICE_REGISTRY,
    get_voice_config,
    load_capture_map,
    source_citation,
)

MACGREGOR_ENTROPY_THRESHOLD = 0.85
MACGREGOR_VOLatility_DAMP = 0.45
MACGREGOR_ENTROPY_DOWNWEIGHT = 0.55
LOW_N_TRAJECTORY_THRESHOLD = 5

REGIME_LABELS = frozenset(
    {"escalation", "stabilization", "fragmentation", "convergence", "transition"}
)

STANCE_TO_PROBABILITY: dict[str, float] = {
    "yes": 0.75,
    "no": 0.25,
    "conditional": 0.55,
    "uncertain": 0.50,
}

SPEECH_ACT_CONFIDENCE: dict[str, float] = {
    "initial": 0.72,
    "restated": 0.70,
    "iterated": 0.65,
    "self_acknowledged_correct": 0.88,
    "self_acknowledged_incorrect": 0.88,
    "outcome_commentary": 0.60,
}

CONFIDENCE_HINT_BOOST: dict[str, float] = {
    "high": 0.12,
    "medium": 0.06,
    "low": -0.08,
}


def load_statecraft_voices() -> list[dict[str, Any]]:
    voices: list[dict[str, Any]] = []
    for speaker in sorted(VOICE_REGISTRY.keys()):
        cfg = get_voice_config(speaker)
        if not cfg.capture_map_path.is_file():
            continue
        rows = load_capture_map(cfg.capture_map_path, guest_speaker=speaker)
        voices.append(
            {
                "speaker": speaker,
                "default_channel": cfg.default_channel,
                "rows": rows,
            }
        )
    return voices


def _timestamp_for_row(row: dict[str, Any], *, default_channel: str) -> str:
    appearance = str(row.get("appearance_date") or "").strip()
    if appearance:
        return appearance[:10]
    capture_rel = str(row.get("capture") or "").replace("\\", "/")
    capture_path = _REPO_ROOT / capture_rel
    if capture_path.is_file():
        citation = source_citation(capture_path, default_channel=default_channel)
        pub = str(citation.get("pub_date") or "").strip()
        if pub:
            return pub[:10]
    return "1970-01-01"


def extract_claims(voices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for voice_block in voices:
        speaker = str(voice_block["speaker"])
        default_channel = str(voice_block.get("default_channel") or "")
        for row in voice_block.get("rows") or []:
            if not isinstance(row, dict):
                continue
            claim = str(row.get("public_excerpt_raw") or row.get("public_excerpt") or "").strip()
            if not claim:
                continue
            results.append(
                {
                    "voice": speaker,
                    "event_id": str(row.get("event_id") or "").strip(),
                    "claim": claim,
                    "stance": str(row.get("stance") or "uncertain"),
                    "speech_act": str(row.get("speech_act") or "restated"),
                    "timestamp": _timestamp_for_row(row, default_channel=default_channel),
                    "capture": str(row.get("capture") or "").replace("\\", "/"),
                    "confidence_hint": str(row.get("confidence") or ""),
                    "quote_speaker": str(row.get("quote_speaker") or speaker),
                    "public_display": bool(row.get("public_display", True)),
                }
            )
    results.sort(key=lambda r: (r["voice"], r["event_id"], r["timestamp"], r["capture"]))
    return results


def partition_claims(
    claims: list[dict[str, Any]],
    registry: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    matched: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []
    matched_rows: list[dict[str, Any]] = []
    unmatched_rows: list[dict[str, Any]] = []

    for claim in claims:
        row = dict(claim)
        event_id = str(row.get("event_id") or "").strip()
        if event_id and event_id in registry:
            row["alignment_status"] = "matched"
            row["capture_map_event_id"] = event_id
            matched.append(row)
            matched_rows.append(
                {
                    "voice": row["voice"],
                    "event_id": event_id,
                    "capture": row.get("capture"),
                    "alignment_method": "capture_map_event_id",
                }
            )
        else:
            row["alignment_status"] = "unmatched"
            row["review_status"] = "pending"
            unmatched.append(row)
            unmatched_rows.append(
                {
                    "voice": row["voice"],
                    "event_id": event_id or None,
                    "claim": row.get("claim"),
                    "capture": row.get("capture"),
                    "review_status": "pending",
                }
            )

    audit = {
        "matched": matched_rows,
        "unmatched": unmatched_rows,
        "stats": {
            "claim_count": len(claims),
            "matched_count": len(matched_rows),
            "unmatched_count": len(unmatched_rows),
        },
    }
    return matched, unmatched, audit


def infer_probabilities(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for claim in claims:
        row = dict(claim)
        stance = str(row.get("stance") or "").strip().lower()
        row["probability"] = round(
            clamp01(STANCE_TO_PROBABILITY.get(stance, 0.5)),
            4,
        )
        speech_act = str(row.get("speech_act") or "restated")
        base = SPEECH_ACT_CONFIDENCE.get(speech_act, 0.65)
        hint = str(row.get("confidence_hint") or "").strip().lower()
        boost = CONFIDENCE_HINT_BOOST.get(hint, 0.0)
        row["confidence"] = round(clamp01(base + boost), 4)
        row["interpretation"] = "probabilistic_projection"
        output.append(row)
    return output


def build_trajectories(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for claim in claims:
        event_id = str(claim.get("capture_map_event_id") or claim.get("event_id") or "")
        voice = str(claim.get("voice") or "")
        if not event_id or not voice:
            continue
        grouped.setdefault((event_id, voice), []).append(dict(claim))

    output: list[dict[str, Any]] = []
    for (event_id, voice) in sorted(grouped.keys()):
        items = sorted(
            grouped[(event_id, voice)],
            key=lambda c: (str(c.get("timestamp") or ""), str(c.get("capture") or "")),
        )
        trajectory = [
            {
                "timestamp": str(item.get("timestamp") or ""),
                "claim": str(item.get("claim") or ""),
                "stance": str(item.get("stance") or "uncertain"),
                "probability": float(item.get("probability") or 0.5),
                "confidence": float(item.get("confidence") or 0.5),
                "interpretation": "probabilistic_projection",
                "speech_act": str(item.get("speech_act") or ""),
                "capture": str(item.get("capture") or ""),
                "quote_speaker": str(item.get("quote_speaker") or voice),
                "public_display": bool(item.get("public_display", True)),
            }
            for item in items
        ]
        output.append({"event_id": event_id, "voice": voice, "trajectory": trajectory})
    return output


def _semantic_entropy(semantic_scores: dict[str, Any], event_id: str | None) -> float:
    if not event_id:
        return 0.0
    events = semantic_scores.get("events") if isinstance(semantic_scores, dict) else {}
    if not isinstance(events, dict):
        return 0.0
    block = events.get(event_id) or {}
    if not isinstance(block, dict):
        return 0.0
    return float(block.get("entropy_score") or 0.0)


def _latest_probability_vector(
    trajectories: list[dict[str, Any]],
    event_id: str,
) -> dict[str, float]:
    latest: dict[str, float] = {}
    for traj in trajectories:
        if str(traj.get("event_id") or "") != event_id:
            continue
        voice = str(traj.get("voice") or "")
        points = traj.get("trajectory") or []
        if not voice or not isinstance(points, list) or not points:
            continue
        last = points[-1]
        if isinstance(last, dict):
            latest[voice] = float(last.get("probability") or 0.5)
    return latest


def compute_alignment_score(
    event_id: str,
    trajectories: list[dict[str, Any]],
    *,
    semantic_scores: dict[str, Any] | None = None,
) -> float:
    probs = _latest_probability_vector(trajectories, event_id)
    if len(probs) < 2:
        return 1.0
    entropy = _semantic_entropy(semantic_scores or {}, event_id)
    voices = sorted(probs.keys())
    vectors: list[list[float]] = []
    weights: list[float] = []
    for voice in voices:
        p = clamp01(probs[voice])
        vectors.append([p, 1.0 - p])
        w = 1.0
        if voice == "macgregor" and entropy >= 0.85:
            w *= MACGREGOR_ENTROPY_DOWNWEIGHT
        weights.append(w)
    scores: list[float] = []
    pair_weights: list[float] = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            scores.append(cosine_similarity(vectors[i], vectors[j]))
            pair_weights.append((weights[i] + weights[j]) / 2.0)
    if not scores:
        return 1.0
    total_w = sum(pair_weights) or 1.0
    return round(sum(s * w for s, w in zip(scores, pair_weights)) / total_w, 4)


def enrich_trajectories(
    trajectories: list[dict[str, Any]],
    *,
    semantic_scores: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for traj in trajectories:
        block = dict(traj)
        event_id = str(block.get("event_id") or "")
        points = block.get("trajectory") or []
        entropy = _semantic_entropy(semantic_scores or {}, event_id)
        block["alignment_score"] = compute_alignment_score(
            event_id,
            trajectories,
            semantic_scores=semantic_scores,
        )
        if isinstance(points, list) and points:
            weight = 1.0 / (1.0 + max(0.0, entropy))
            total = 0.0
            weighted_sum = 0.0
            for point in points:
                if not isinstance(point, dict):
                    continue
                conf = float(point.get("confidence") or 0.5)
                p = float(point.get("probability") or 0.5)
                w = weight * conf
                weighted_sum += p * w
                total += w
            block["entropy_weighted_probability"] = round(
                weighted_sum / total if total > 0 else float(points[-1].get("probability") or 0.5),
                4,
            )
        else:
            block["entropy_weighted_probability"] = 0.5
        output.append(block)
    return output


def _trajectory_index(
    trajectories: list[dict[str, Any]],
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    index: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for block in trajectories:
        event_id = str(block.get("event_id") or "")
        voice = str(block.get("voice") or "")
        points = block.get("trajectory") or []
        if event_id and voice and isinstance(points, list):
            index[(event_id, voice)] = [p for p in points if isinstance(p, dict)]
    return index


def _point_at_or_before(points: list[dict[str, Any]], timestamp: str) -> dict[str, Any] | None:
    if not points:
        return None
    ts = str(timestamp or "")
    eligible = [p for p in points if str(p.get("timestamp") or "") <= ts] if ts else points
    if not eligible:
        return points[0]
    return sorted(eligible, key=lambda p: str(p.get("timestamp") or ""))[-1]


def project_trajectories(
    event_distribution: list[dict[str, Any]],
    trajectories: list[dict[str, Any]],
    claim_meta: dict[str, Any],
) -> list[dict[str, Any]]:
    index = _trajectory_index(trajectories)
    voice = str(claim_meta.get("voice") or "")
    timestamp = str(claim_meta.get("timestamp") or "")
    projections: list[dict[str, Any]] = []
    for entry in event_distribution:
        event_id = str(entry.get("event_id") or "")
        weight = float(entry.get("weight") or 0.0)
        if not event_id or weight <= 0:
            continue
        points = index.get((event_id, voice)) or []
        point = _point_at_or_before(points, timestamp)
        if not point:
            continue
        projections.append(
            {
                "event_id": event_id,
                "weight": round(weight, 4),
                "probability": float(point.get("probability") or 0.5),
                "stance": str(point.get("stance") or "uncertain"),
                "confidence": float(point.get("confidence") or 0.5),
            }
        )
    return projections


def compute_signal(
    projections: list[dict[str, Any]],
    *,
    trajectories: list[dict[str, Any]],
    voice: str,
    primary_event_id: str | None,
    semantic_entropy: float = 0.0,
) -> dict[str, float]:
    if not projections:
        return {"directional": 0.5, "volatility": 0.0, "drift": 0.0}

    directional = sum(float(p["weight"]) * float(p["probability"]) for p in projections)
    top_event = primary_event_id or str(projections[0].get("event_id") or "")
    index = _trajectory_index(trajectories)
    top_points = index.get((top_event, voice)) or []
    probs = [float(p.get("probability") or 0.5) for p in top_points]
    if len(probs) >= 2:
        mean_p = sum(probs) / len(probs)
        variance = sum((p - mean_p) ** 2 for p in probs) / len(probs)
        volatility = math.sqrt(variance)
    else:
        volatility = 0.0

    if voice == "macgregor" and semantic_entropy >= MACGREGOR_ENTROPY_THRESHOLD:
        volatility *= MACGREGOR_VOLatility_DAMP

    drift = 0.0
    if len(probs) >= 2:
        drift = abs(probs[-1] - probs[-2])

    return {
        "directional": round(clamp01(directional), 4),
        "volatility": round(clamp01(volatility), 4),
        "drift": round(clamp01(drift), 4),
    }


def classify_regime(
    signal: dict[str, float],
    event_distribution: list[dict[str, Any]],
    alignment_entropy: float,
    *,
    projections: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    directional = float(signal.get("directional") or 0.5)
    drift = float(signal.get("drift") or 0.0)
    label = "transition"
    confidence = 0.55

    if alignment_entropy > 1.2 and directional < 0.55:
        label = "fragmentation"
        confidence = 0.65 + min(0.2, alignment_entropy / 10.0)
    elif directional > 0.65 and drift > 0.05:
        label = "escalation"
        confidence = 0.6 + min(0.25, drift)
    elif drift < 0.08 and alignment_entropy < 0.8:
        label = "stabilization"
        confidence = 0.7
    elif projections and len(event_distribution) >= 2:
        stances = {str(p.get("stance") or "") for p in projections}
        if len(stances) == 1 and stances <= {"yes", "no"}:
            label = "convergence"
            confidence = 0.68

    return {
        "label": label if label in REGIME_LABELS else "transition",
        "confidence": round(clamp01(confidence), 4),
    }


def _primary_event_id(event_distribution: list[dict[str, Any]]) -> str | None:
    if not event_distribution:
        return None
    best = max(event_distribution, key=lambda e: float(e.get("weight") or 0.0))
    return str(best.get("event_id") or "") or None


def process_claim(
    point: dict[str, Any],
    *,
    capture_map_event_id: str,
    trajectories: list[dict[str, Any]],
    terms_index: dict[str, list[str]],
    registry: dict[str, dict[str, Any]],
    semantic_scores: dict[str, Any],
) -> dict[str, Any]:
    claim = str(point.get("claim") or "")
    voice = str(point.get("voice") or "")
    timestamp = str(point.get("timestamp") or "")
    capture = str(point.get("capture") or "")

    event_distribution, alignment_entropy = soft_align(
        claim,
        capture_event_id=capture_map_event_id,
        terms_index=terms_index,
        registry=registry,
    )
    primary = _primary_event_id(event_distribution)
    claim_meta = {"voice": voice, "timestamp": timestamp}
    projections = project_trajectories(event_distribution, trajectories, claim_meta)
    sem_ent = _semantic_entropy(semantic_scores, primary)
    trajectory_signals = compute_signal(
        projections,
        trajectories=trajectories,
        voice=voice,
        primary_event_id=primary,
        semantic_entropy=sem_ent,
    )
    regime = classify_regime(
        trajectory_signals,
        event_distribution,
        alignment_entropy,
        projections=projections,
    )

    return {
        "voice": voice,
        "timestamp": timestamp,
        "capture": capture,
        "claim": claim,
        "interpretation": "unified_epistemic_state",
        "capture_map_event_id": capture_map_event_id,
        "event_distribution": event_distribution,
        "trajectory_signals": trajectory_signals,
        "regime": regime,
        "alignment_entropy": alignment_entropy,
        "primary_event_id": primary,
        "quote_speaker": str(point.get("quote_speaker") or voice),
        "public_display": bool(point.get("public_display", True)),
        "stance": str(point.get("stance") or "uncertain"),
    }


def build_signals_rollup(objects: list[dict[str, Any]]) -> dict[str, Any]:
    by_event: dict[str, list[dict[str, Any]]] = {}
    for obj in objects:
        eid = str(obj.get("primary_event_id") or obj.get("capture_map_event_id") or "")
        if eid:
            by_event.setdefault(eid, []).append(obj)

    events: dict[str, Any] = {}
    for event_id in sorted(by_event.keys()):
        rows = by_event[event_id]
        sigs = [r["trajectory_signals"] for r in rows]
        events[event_id] = {
            "object_count": len(rows),
            "mean_directional": round(
                sum(float(s["directional"]) for s in sigs) / len(sigs),
                4,
            ),
            "mean_volatility": round(
                sum(float(s["volatility"]) for s in sigs) / len(sigs),
                4,
            ),
            "mean_drift": round(sum(float(s["drift"]) for s in sigs) / len(sigs), 4),
            "signal_source": "epistemic_core",
        }

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/prediction/run_pipeline.py",
            "phase": "episystem-canonical",
            "epistemic_source": "heuristic_v1",
            "registry_mutation": False,
        },
        "interpretation": "epistemic_signals",
        "events": events,
    }


def build_regimes_rollup(objects: list[dict[str, Any]]) -> dict[str, Any]:
    by_event: dict[str, list[dict[str, Any]]] = {}
    global_counts: dict[str, int] = {}
    for obj in objects:
        label = str((obj.get("regime") or {}).get("label") or "transition")
        global_counts[label] = global_counts.get(label, 0) + 1
        eid = str(obj.get("primary_event_id") or "")
        if eid:
            by_event.setdefault(eid, []).append(obj)

    event_regimes: dict[str, Any] = {}
    for event_id in sorted(by_event.keys()):
        rows = by_event[event_id]
        entropies = [float(r.get("alignment_entropy") or 0.0) for r in rows]
        regimes: dict[str, int] = {}
        for r in rows:
            lbl = str((r.get("regime") or {}).get("label") or "transition")
            regimes[lbl] = regimes.get(lbl, 0) + 1
        dominant = max(regimes.items(), key=lambda kv: kv[1])[0] if regimes else "transition"
        event_regimes[event_id] = {
            "object_count": len(rows),
            "mean_alignment_entropy": round(sum(entropies) / len(entropies), 4),
            "dominant_regime": dominant,
            "regime_counts": regimes,
        }

    high_entropy = sum(1 for o in objects if float(o.get("alignment_entropy") or 0.0) > 1.2)
    dominant_global = (
        max(global_counts.items(), key=lambda kv: kv[1])[0] if global_counts else "transition"
    )

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/prediction/run_pipeline.py",
            "phase": "episystem-canonical",
            "epistemic_source": "heuristic_v1",
            "registry_mutation": False,
        },
        "interpretation": "epistemic_regimes",
        "global": {
            "dominant_regime": dominant_global,
            "regime_counts": global_counts,
            "high_entropy_object_count": high_entropy,
            "regime_shift_detected": False,
        },
        "events": event_regimes,
    }


def build_epistemic_payload(
    *,
    registry: dict[str, dict[str, Any]] | None = None,
    semantic_scores: dict[str, Any] | None = None,
    disagreement: dict[str, Any] | None = None,
    include_multivoice: bool = True,
) -> dict[str, Any]:
    _ = disagreement
    reg = registry if registry is not None else load_event_registry()
    semantic = semantic_scores or {}

    voices = load_statecraft_voices()
    raw_claims = extract_claims(voices)
    matched, _unmatched, alignment_audit = partition_claims(raw_claims, reg)
    prob_claims = infer_probabilities(matched)
    trajectories = enrich_trajectories(
        build_trajectories(prob_claims),
        semantic_scores=semantic,
    )
    terms_index = load_terms_index()

    objects: list[dict[str, Any]] = []
    for block in trajectories:
        capture_map_event_id = str(block.get("event_id") or "")
        voice = str(block.get("voice") or "")
        for point in block.get("trajectory") or []:
            if not isinstance(point, dict):
                continue
            row = dict(point)
            row["voice"] = voice
            objects.append(
                process_claim(
                    row,
                    capture_map_event_id=capture_map_event_id,
                    trajectories=trajectories,
                    terms_index=terms_index,
                    registry=reg,
                    semantic_scores=semantic,
                )
            )

    high_entropy_count = sum(
        1 for o in objects if float(o.get("alignment_entropy") or 0.0) > 1.2
    )
    speaker_names = sorted(VOICE_REGISTRY.keys())

    epistemic_state = {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/prediction/run_pipeline.py",
            "phase": "episystem-canonical",
            "epistemic_source": "heuristic_v1",
            "registry_mutation": False,
            "object_count": len(objects),
            "high_entropy_object_count": high_entropy_count,
            "voices": speaker_names,
            "low_n_advisory": len(trajectories) < LOW_N_TRAJECTORY_THRESHOLD,
        },
        "interpretation": "epistemic_state",
        "objects": objects,
    }

    result: dict[str, Any] = {
        "epistemic_state": epistemic_state,
        "signals": build_signals_rollup(objects),
        "regimes": build_regimes_rollup(objects),
        "object_count": len(objects),
        "trajectory_count": len(trajectories),
        "alignment_audit": alignment_audit,
    }

    if include_multivoice:
        result["multivoice_dataset"] = {
            "_meta": {
                "generated": True,
                "do_not_edit": True,
                "source": "scripts/prediction/run_pipeline.py",
                "phase": "episystem-canonical",
                "epistemic_source": "heuristic_v1",
                "registry_mutation": False,
                "voices": speaker_names,
                "trajectory_count": len(trajectories),
            },
            "interpretation": "multivoice_dataset",
            "trajectories": trajectories,
            "alignment_audit": alignment_audit,
        }

    return result
