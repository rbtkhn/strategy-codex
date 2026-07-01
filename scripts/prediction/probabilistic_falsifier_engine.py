"""Heuristic probabilistic falsifier inference — Phase 3.5 stub."""

from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.contracts import (  # noqa: E402
    HIGH_ENTROPY_THRESHOLD,
    falsifier_confidence_from_entropy,
    has_falsifier_coverage,
    has_string_falsifier,
    has_valid_falsifier_model,
    shannon_entropy,
)

OUTPUT = _REPO_ROOT / "runtime" / "artifacts" / "falsifier-inference-report.json"
QUEUE = _REPO_ROOT / "runtime" / "artifacts" / "prediction-review-queue.json"


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", str(text).lower()).strip("_")
    return slug[:48] or "mode"


def _normalize_model(modes: list[dict[str, Any]], *, inference_source: str = "heuristic_v1") -> dict[str, Any]:
    total = sum(float(m["probability"]) for m in modes)
    if total <= 0:
        weights = [1.0 / len(modes)] * len(modes)
    else:
        weights = [float(m["probability"]) / total for m in modes]
    normalized_modes: list[dict[str, Any]] = []
    for mode, weight in zip(modes, weights):
        normalized_modes.append(
            {
                "id": str(mode["id"]),
                "condition": str(mode["condition"]),
                "probability": round(weight, 4),
            }
        )
    entropy = shannon_entropy([m["probability"] for m in normalized_modes])
    return {
        "failure_modes": normalized_modes,
        "confidence_distribution": "entropy-weighted",
        "inference_source": inference_source,
        "entropy": entropy,
    }


def _template_modes(event_id: str, event: dict[str, Any]) -> list[dict[str, Any]]:
    question = str(event.get("question") or event_id).casefold()
    tags = [str(t).casefold() for t in (event.get("tags") or [])]
    blob = " ".join([event_id, question, " ".join(tags)])

    if "trajectory" in str(event.get("event_type") or "") or "trajectory" in event_id:
        dims = event.get("dimensions") or []
        if dims:
            modes = []
            for dim in dims[:6]:
                modes.append(
                    {
                        "id": str(dim.get("id") or _slug(str(dim.get("label") or "dim"))),
                        "condition": str(dim.get("falsifier") or dim.get("label") or ""),
                        "probability": 1.0 / max(len(dims), 1),
                    }
                )
            if len(modes) >= 2:
                return modes

    if "iran" in blob or "airpower" in blob:
        return [
            {
                "id": "no_escalation_under_strikes",
                "condition": "Target state does not escalate despite sustained air/naval coercion.",
                "probability": 0.35,
            },
            {
                "id": "internal_fragmentation",
                "condition": "Target fragments internally under pressure without strategic submission.",
                "probability": 0.20,
            },
            {
                "id": "us_withdrawal_before_peak",
                "condition": "Coercer withdraws or de-escalates before escalation peak.",
                "probability": 0.45,
            },
        ]

    if "ukraine" in blob or "russian" in blob or "capitulation" in blob:
        return [
            {
                "id": "russian_capitulation",
                "condition": "Russia capitulates under Western escalation or aid-max pressure.",
                "probability": 0.15,
            },
            {
                "id": "prolonged_stalemate",
                "condition": "War prolongs without decisive capitulation either side.",
                "probability": 0.55,
            },
            {
                "id": "escalation_spiral",
                "condition": "Escalation materially widens without settlement.",
                "probability": 0.30,
            },
        ]

    if "nato" in blob:
        return [
            {
                "id": "alliance_retrenchment",
                "condition": "NATO limits exposure and war ends without alliance strategic damage.",
                "probability": 0.30,
            },
            {
                "id": "sustained_exposure",
                "condition": "Alliance faces sustained resource drain tied to the conflict.",
                "probability": 0.45,
            },
            {
                "id": "credibility_loss",
                "condition": "Alliance credibility erodes without favorable settlement.",
                "probability": 0.25,
            },
        ]

    return [
        {
            "id": "claim_holds",
            "condition": f"Observable evidence supports the claim in {event_id}.",
            "probability": 0.34,
        },
        {
            "id": "claim_partially_fails",
            "condition": f"Claim partially fails under observable counter-evidence for {event_id}.",
            "probability": 0.33,
        },
        {
            "id": "claim_fails",
            "condition": f"Claim fails decisively on operator-scorable observables for {event_id}.",
            "probability": 0.33,
        },
    ]


def infer_falsifier_model(event_id: str, event: dict[str, Any]) -> dict[str, Any]:
    modes = _template_modes(event_id, event)
    return _normalize_model(modes, inference_source="heuristic_v1")


def enrich_row_falsifiers(row: dict[str, Any], *, event_id: str, path: str) -> tuple[dict[str, Any], dict[str, Any] | None]:
    out = dict(row)
    meta: dict[str, Any] | None = None
    if has_falsifier_coverage(out):
        return out, meta
    model = infer_falsifier_model(event_id, out)
    out["falsifier_model"] = model
    from prediction.contracts import infer_prediction_type as _infer_pt

    if not out.get("prediction_type") or out.get("prediction_type") == "falsifiable_claim":
        out["prediction_type"] = "probabilistic_claim"
    confidence = falsifier_confidence_from_entropy(float(model["entropy"]))
    meta = {
        "path": path,
        "event_id": event_id,
        "inference_source": model["inference_source"],
        "entropy": model["entropy"],
        "falsifier_confidence": confidence,
        "high_entropy": float(model["entropy"]) >= HIGH_ENTROPY_THRESHOLD,
    }
    return out, meta


def enrich_event_falsifiers(event_id: str, event: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    from prediction.contracts import infer_prediction_type

    out = deepcopy(event)
    inferences: list[dict[str, Any]] = []

    if not has_falsifier_coverage(out):
        enriched, meta = enrich_row_falsifiers(out, event_id=event_id, path=event_id)
        out = enriched
        if meta:
            inferences.append(meta)

    dims = out.get("dimensions") or []
    if isinstance(dims, list):
        new_dims: list[dict[str, Any]] = []
        for dim in dims:
            dim_row = dict(dim)
            dim_id = str(dim_row.get("id") or "?")
            if has_string_falsifier(dim_row) or has_valid_falsifier_model(dim_row):
                new_dims.append(dim_row)
                continue
            enriched, meta = enrich_row_falsifiers(
                dim_row,
                event_id=event_id,
                path=f"{event_id}/dimensions/{dim_id}",
            )
            new_dims.append(enriched)
            if meta:
                inferences.append(meta)
        out["dimensions"] = new_dims

    if out.get("prediction_type") is None and infer_prediction_type(out) == "probabilistic_claim":
        out["prediction_type"] = "probabilistic_claim"

    return out, inferences


def enrich_registry(registry: dict[str, dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    enriched: dict[str, dict[str, Any]] = {}
    all_inferences: list[dict[str, Any]] = []
    for event_id, event in sorted(registry.items()):
        event_out, inferences = enrich_event_falsifiers(event_id, event)
        enriched[event_id] = event_out
        all_inferences.extend(inferences)
    return enriched, all_inferences


def build_inference_report(
    registry: dict[str, dict[str, Any]],
    inferences: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "_meta": {
            "generated": True,
            "source": "scripts/prediction/probabilistic_falsifier_engine.py",
            "phase": "3.5-heuristic-stub",
        },
        "event_count": len(registry),
        "inferred_count": len(inferences),
        "inferences": inferences,
        "high_entropy": [row for row in inferences if row.get("high_entropy")],
    }


def review_queue_items(inferences: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for row in inferences:
        items.append(
            {
                "type": "inferred_falsifier",
                "event_id": row.get("event_id"),
                "path": row.get("path"),
                "message": (
                    f"{row.get('path')}: inferred falsifier_model "
                    f"(entropy={row.get('entropy')}, confidence={row.get('falsifier_confidence')})"
                ),
            }
        )
        if row.get("high_entropy"):
            items.append(
                {
                    "type": "high_entropy_falsifier",
                    "event_id": row.get("event_id"),
                    "path": row.get("path"),
                    "message": f"{row.get('path')}: high-entropy inferred falsifier — operator review",
                }
            )
    return items


def run_inference(registry: dict[str, dict[str, Any]]) -> dict[str, Any]:
    _, inferences = enrich_registry(registry)
    return build_inference_report(registry, inferences)


def main() -> int:
    import argparse

    from prediction.registry_writer import REGISTRY_PATH, load_registry

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--emit-review-queue", action="store_true")
    parser.add_argument("--queue-output", type=Path, default=QUEUE)
    args = parser.parse_args()

    registry = load_registry(args.registry)
    enriched, inferences = enrich_registry(registry)
    report = build_inference_report(enriched, inferences)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[ok] wrote {args.output} ({report['inferred_count']} inference(s))")

    if args.emit_review_queue and inferences:
        payload = {
            "_meta": {
                "generated": True,
                "source": "scripts/prediction/probabilistic_falsifier_engine.py",
            },
            "items": review_queue_items(inferences),
        }
        args.queue_output.parent.mkdir(parents=True, exist_ok=True)
        args.queue_output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[ok] wrote {args.queue_output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
