"""Tests for PR7 multivoice extraction layer."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.align_events import align_to_events, semantic_match  # noqa: E402
from prediction.build_trajectories import build_trajectories  # noqa: E402
from prediction.extract_voice_claims import extract_claims  # noqa: E402
from prediction.infer_probabilities import infer_probabilities, map_stance_to_probability  # noqa: E402
from prediction.normalize_voices import compute_alignment_score, normalize_cross_voice  # noqa: E402
from prediction.run_multivoice_extraction import build_mvel_payload  # noqa: E402


def _fixture_voices() -> list[dict]:
    return [
        {
            "speaker": "freeman",
            "default_channel": "Judging Freedom",
            "rows": [
                {
                    "event_id": "evt_a",
                    "capture": "source-archive/statecraft/2025-01-01/source-a.md",
                    "stance": "yes",
                    "speech_act": "initial",
                    "public_excerpt": "Event A will happen.",
                    "appearance_date": "2025-01-01",
                },
                {
                    "event_id": "evt_a",
                    "capture": "source-archive/statecraft/2025-06-01/source-b.md",
                    "stance": "yes",
                    "speech_act": "restated",
                    "public_excerpt": "Still yes on event A.",
                    "appearance_date": "2025-06-01",
                },
            ],
        },
        {
            "speaker": "mercouris",
            "default_channel": "Alexander Mercouris",
            "rows": [
                {
                    "event_id": "evt_a",
                    "capture": "source-archive/statecraft/2025-03-01/source-c.md",
                    "stance": "no",
                    "speech_act": "initial",
                    "public_excerpt": "Event A is unlikely.",
                    "appearance_date": "2025-03-01",
                }
            ],
        },
    ]


def _fixture_registry() -> dict:
    return {
        "evt_a": {
            "question": "Will event A happen?",
            "falsifier": "Observable outcome for A",
            "status": "open",
            "outcome": None,
        }
    }


def test_map_stance_to_probability_table() -> None:
    assert map_stance_to_probability("yes") == 0.75
    assert map_stance_to_probability("no") == 0.25
    assert map_stance_to_probability("unknown") == 0.50


def test_extract_and_align_pipeline() -> None:
    claims = extract_claims(_fixture_voices())
    assert len(claims) == 3
    aligned, alignment_map = align_to_events(claims, _fixture_registry())
    assert alignment_map["stats"]["matched_count"] == 3
    assert alignment_map["stats"]["unmatched_count"] == 0
    probabilistic = infer_probabilities(aligned)
    trajectories = build_trajectories(probabilistic)
    assert len(trajectories) == 2
    freeman_traj = next(t for t in trajectories if t["voice"] == "freeman")
    assert len(freeman_traj["trajectory"]) == 2
    assert freeman_traj["trajectory"][0]["timestamp"] <= freeman_traj["trajectory"][1]["timestamp"]


def test_semantic_match_single_hit() -> None:
    terms = {"evt_b": ["tariff", "china"]}
    assert semantic_match("China tariff capitulation is coming", terms) == "evt_b"
    assert semantic_match("unrelated text", terms) is None


def test_normalize_cross_voice_alignment() -> None:
    claims = extract_claims(_fixture_voices())
    aligned, _ = align_to_events(claims, _fixture_registry())
    probabilistic = infer_probabilities(aligned)
    trajectories = build_trajectories(probabilistic)
    normalized = normalize_cross_voice(trajectories, semantic_scores={"events": {}})
    assert all("alignment_score" in t for t in normalized)
    score = compute_alignment_score("evt_a", normalized)
    assert 0.0 <= score <= 1.0


def test_unmatched_goes_to_review_queue() -> None:
    voices = [
        {
            "speaker": "freeman",
            "default_channel": "Judging Freedom",
            "rows": [
                {
                    "event_id": "not_in_registry",
                    "capture": "source-archive/statecraft/2025-01-01/source-x.md",
                    "stance": "yes",
                    "speech_act": "initial",
                    "public_excerpt": "orphan claim without terms",
                    "appearance_date": "2025-01-01",
                }
            ],
        }
    ]
    claims = extract_claims(voices)
    aligned, alignment_map = align_to_events(claims, _fixture_registry())
    assert alignment_map["stats"]["unmatched_count"] == 1
    assert aligned[0]["alignment_status"] == "unmatched"
    assert infer_probabilities(aligned) == []


def test_build_mvel_payload_shape() -> None:
    payload = build_mvel_payload(registry=_fixture_registry(), semantic_scores={}, disagreement={})
    assert payload["dataset"]["interpretation"] == "multivoice_extraction"
    assert payload["alignment_map"]["interpretation"] == "event_alignment_audit"
    assert payload["status"]["status"] == "ok"
    assert payload["dataset"]["_meta"]["registry_mutation"] is False
