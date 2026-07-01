#!/usr/bin/env python3
"""Generate MVEL artifacts (PR7 advisory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SEMANTIC = REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"
DEFAULT_DISAGREEMENT = REPO_ROOT / "runtime" / "artifacts" / "prediction-disagreement.json"
DEFAULT_DATASET = REPO_ROOT / "runtime" / "artifacts" / "multivoice-extracted-dataset.json"
DEFAULT_ALIGNMENT = REPO_ROOT / "runtime" / "artifacts" / "event-alignment-map.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.run_multivoice_extraction import build_mvel_payload  # noqa: E402
from prediction_lib import render_json  # noqa: E402


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _voice_output(speaker: str) -> Path:
    return REPO_ROOT / "runtime" / "artifacts" / f"voice-trajectories-{speaker}.json"


def check_artifact(*, dataset_path: Path = DEFAULT_DATASET) -> int:
    if not dataset_path.is_file():
        print(f"error: missing {dataset_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    expected_bundle = build_mvel_payload(
        semantic_scores=_load(DEFAULT_SEMANTIC),
        disagreement=_load(DEFAULT_DISAGREEMENT),
    )
    paths = [
        (dataset_path, expected_bundle["dataset"]),
        (DEFAULT_ALIGNMENT, expected_bundle["alignment_map"]),
    ]
    for speaker, payload in sorted(expected_bundle["per_voice"].items()):
        paths.append((_voice_output(speaker), payload))

    for path, expected in paths:
        if not path.is_file():
            print(f"error: missing {path.relative_to(REPO_ROOT)}", file=sys.stderr)
            return 1
        current = path.read_text(encoding="utf-8")
        rendered = render_json(expected)
        if current != rendered:
            print(
                f"error: {path.relative_to(REPO_ROOT)} is out of date; "
                "run build_multivoice_extraction.py",
                file=sys.stderr,
            )
            return 1

    print("[ok] multivoice extraction artifacts match generator output")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--semantic-scores", type=Path, default=DEFAULT_SEMANTIC)
    ap.add_argument("--disagreement", type=Path, default=DEFAULT_DISAGREEMENT)
    ap.add_argument("--dataset-output", type=Path, default=DEFAULT_DATASET)
    ap.add_argument("--alignment-output", type=Path, default=DEFAULT_ALIGNMENT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        return check_artifact(dataset_path=args.dataset_output)

    bundle = build_mvel_payload(
        semantic_scores=_load(args.semantic_scores),
        disagreement=_load(args.disagreement),
    )
    args.dataset_output.parent.mkdir(parents=True, exist_ok=True)
    args.dataset_output.write_text(render_json(bundle["dataset"]), encoding="utf-8")
    args.alignment_output.write_text(render_json(bundle["alignment_map"]), encoding="utf-8")

    for speaker, payload in sorted(bundle["per_voice"].items()):
        out = _voice_output(speaker)
        out.write_text(render_json(payload), encoding="utf-8")

    scope = bundle["dataset"]["_meta"]["extraction_scope"]
    print(
        f"[ok] wrote MVEL artifacts "
        f"(trajectories={scope['trajectory_count']}, unmatched={scope['unmatched_count']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
