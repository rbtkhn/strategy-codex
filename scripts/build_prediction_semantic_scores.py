#!/usr/bin/env python3
"""Generate runtime/artifacts/prediction-semantic-scores.json (Phase 3.5 advisory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "statecraft" / "data" / "event-registry.json"
DEFAULT_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from registry_pipeline.compression_engine import compression_report  # noqa: E402
from registry_pipeline.contracts import (  # noqa: E402
    falsifier_confidence_from_entropy,
    falsifier_key_for_fingerprint,
    has_string_falsifier,
    has_valid_falsifier_model,
    predictive_fingerprint,
)
from prediction_lib import load_event_registry, render_json  # noqa: E402


def _question_near_misses(events: dict[str, dict[str, Any]]) -> dict[str, int]:
    by_question: dict[str, list[str]] = {}
    for event_id, event in events.items():
        q = str(event.get("question") or event_id).strip().casefold()
        by_question.setdefault(q, []).append(event_id)
    return {eid: len(ids) for q, ids in by_question.items() for eid in ids if len(ids) > 1}


def build_semantic_scores_payload(
    events: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    registry = events or load_event_registry()
    report = compression_report(registry)
    dupe_ids = {eid for d in report["duplicate_fingerprints"] for eid in d["event_ids"]}
    near = _question_near_misses(registry)
    events_out: dict[str, Any] = {}

    for event_id, event in sorted(registry.items()):
        model = event.get("falsifier_model") if isinstance(event.get("falsifier_model"), dict) else None
        entropy = float(model.get("entropy") or 0) if model else 0.0
        if has_string_falsifier(event) and not model:
            entropy_score = 0.0
            confidence = "high"
            inference_source = "operator"
        elif model:
            entropy_score = entropy
            confidence = falsifier_confidence_from_entropy(entropy)
            inference_source = str(model.get("inference_source") or "operator")
        else:
            entropy_score = 1.0
            confidence = "low"
            inference_source = "none"

        if event_id in dupe_ids:
            compression_quality = "low"
            overcollapse = "high"
        elif near.get(event_id, 0) > 1:
            compression_quality = "medium"
            overcollapse = "medium"
        else:
            compression_quality = "high"
            overcollapse = "low"

        fp = predictive_fingerprint(event_id, event)
        events_out[event_id] = {
            "entropy_score": round(entropy_score, 4),
            "falsifier_confidence": confidence,
            "inference_source": inference_source,
            "compression_quality": compression_quality,
            "risk_of_overcollapse": overcollapse,
            "has_string_falsifier": has_string_falsifier(event),
            "has_falsifier_model": has_valid_falsifier_model(event),
            "fingerprint_key": str(falsifier_key_for_fingerprint(event))[:120],
            "fingerprint": fp,
        }

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_prediction_semantic_scores.py",
            "phase": "3.5-advisory",
        },
        "events": events_out,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = ap.parse_args()

    payload = build_semantic_scores_payload(load_event_registry(args.registry))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    print(f"[ok] wrote {args.output.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
