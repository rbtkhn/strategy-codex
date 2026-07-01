"""PR7 MVEL orchestrator — multi-voice epistemic extraction (read-only, stdlib)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.align_events import align_to_events  # noqa: E402
from prediction.build_trajectories import build_trajectories  # noqa: E402
from prediction.extract_voice_claims import extract_claims, load_statecraft_voices  # noqa: E402
from prediction.infer_probabilities import infer_probabilities  # noqa: E402
from prediction.normalize_voices import normalize_cross_voice  # noqa: E402
from prediction_lib import load_event_registry  # noqa: E402
from voice_prediction_pilot import VOICE_REGISTRY  # noqa: E402

LOW_N_TRAJECTORY_THRESHOLD = 5
ARTIFACT_DIR = _REPO_ROOT / "runtime" / "artifacts"


def build_mvel_payload(
    *,
    registry: dict[str, dict[str, Any]] | None = None,
    semantic_scores: dict[str, Any] | None = None,
    disagreement: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build full MVEL artifact bundle (deterministic, in-process)."""
    reg = registry if registry is not None else load_event_registry()
    voices = load_statecraft_voices()
    raw_claims = extract_claims(voices)
    aligned_claims, alignment_map = align_to_events(raw_claims, reg)
    probabilistic = infer_probabilities(aligned_claims)
    trajectories = build_trajectories(probabilistic)
    normalized = normalize_cross_voice(
        trajectories,
        semantic_scores=semantic_scores or {},
        disagreement=disagreement or {},
    )

    speaker_names = sorted(VOICE_REGISTRY.keys())
    sparse_advisory = len(normalized) < LOW_N_TRAJECTORY_THRESHOLD

    dataset_meta = {
        "generated": True,
        "do_not_edit": True,
        "source": "scripts/build_multivoice_extraction.py",
        "phase": "pr7-mvel-advisory",
        "extraction_source": "heuristic_v1",
        "claim_source": "capture_map",
        "registry_mutation": False,
        "voices": speaker_names,
        "low_n_advisory": sparse_advisory,
        "extraction_scope": {
            "claim_count": len(raw_claims),
            "matched_count": alignment_map["stats"]["matched_count"],
            "unmatched_count": alignment_map["stats"]["unmatched_count"],
            "trajectory_count": len(normalized),
        },
    }

    dataset = {
        "_meta": dataset_meta,
        "interpretation": "multivoice_extraction",
        "trajectories": normalized,
    }

    alignment_artifact = {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_multivoice_extraction.py",
            "phase": "pr7-mvel-advisory",
            "extraction_source": "heuristic_v1",
            "registry_mutation": False,
        },
        "interpretation": "event_alignment_audit",
        **alignment_map,
    }

    per_voice: dict[str, dict[str, Any]] = {}
    for speaker in speaker_names:
        voice_trajs = [t for t in normalized if str(t.get("voice") or "") == speaker]
        per_voice[speaker] = {
            "_meta": {
                "generated": True,
                "do_not_edit": True,
                "source": "scripts/build_multivoice_extraction.py",
                "phase": "pr7-mvel-advisory",
                "extraction_source": "heuristic_v1",
                "voice": speaker,
                "trajectory_count": len(voice_trajs),
            },
            "interpretation": "voice_trajectory_slice",
            "voice": speaker,
            "trajectories": voice_trajs,
        }

    return {
        "dataset": dataset,
        "alignment_map": alignment_artifact,
        "per_voice": per_voice,
        "status": {
            "status": "ok",
            "trajectory_count": len(normalized),
            "unmatched_count": alignment_map["stats"]["unmatched_count"],
        },
    }


def run_mvel(
    *,
    semantic_scores: dict[str, Any] | None = None,
    disagreement: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute MVEL and return status dict."""
    return build_mvel_payload(
        semantic_scores=semantic_scores,
        disagreement=disagreement,
    )["status"]


def main() -> int:
    import argparse
    import json

    from prediction_lib import render_json

    default_semantic = ARTIFACT_DIR / "prediction-semantic-scores.json"
    default_disagreement = ARTIFACT_DIR / "prediction-disagreement.json"
    default_dataset = ARTIFACT_DIR / "multivoice-extracted-dataset.json"
    default_alignment = ARTIFACT_DIR / "event-alignment-map.json"

    def _load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--semantic-scores", type=Path, default=default_semantic)
    parser.add_argument("--disagreement", type=Path, default=default_disagreement)
    parser.add_argument("--dataset-output", type=Path, default=default_dataset)
    parser.add_argument("--alignment-output", type=Path, default=default_alignment)
    args = parser.parse_args()

    bundle = build_mvel_payload(
        semantic_scores=_load(args.semantic_scores),
        disagreement=_load(args.disagreement),
    )
    args.dataset_output.parent.mkdir(parents=True, exist_ok=True)
    args.dataset_output.write_text(render_json(bundle["dataset"]), encoding="utf-8")
    args.alignment_output.write_text(render_json(bundle["alignment_map"]), encoding="utf-8")

    for speaker, payload in sorted(bundle["per_voice"].items()):
        out = ARTIFACT_DIR / f"voice-trajectories-{speaker}.json"
        out.write_text(render_json(payload), encoding="utf-8")

    status = bundle["status"]
    print(
        f"[ok] MVEL complete trajectories={status['trajectory_count']} "
        f"unmatched={status['unmatched_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
