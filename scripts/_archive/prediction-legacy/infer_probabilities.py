"""PR7 MVEL — heuristic stance → probability mapping."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.signal_math import clamp01  # noqa: E402

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

def map_stance_to_probability(stance: str) -> float:
    return STANCE_TO_PROBABILITY.get(str(stance or "").strip().lower(), 0.50)

def compute_confidence(claim_row: dict[str, Any]) -> float:
    speech_act = str(claim_row.get("speech_act") or "restated")
    base = SPEECH_ACT_CONFIDENCE.get(speech_act, 0.65)
    hint = str(claim_row.get("confidence_hint") or "").strip().lower()
    boost = CONFIDENCE_HINT_BOOST.get(hint, 0.0)
    return round(clamp01(base + boost), 4)

def infer_probabilities(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add probability and confidence to aligned claims."""
    output: list[dict[str, Any]] = []
    for claim in claims:
        row = dict(claim)
        if row.get("alignment_status") != "matched":
            continue
        row["probability"] = round(clamp01(map_stance_to_probability(str(row.get("stance") or ""))), 4)
        row["confidence"] = compute_confidence(row)
        row["interpretation"] = "probabilistic_projection"
        output.append(row)
    return output
