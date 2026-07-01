#!/usr/bin/env python3
"""Validate epistemic-generative-state.json shape — advisory only (never blocks)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "runtime" / "artifacts" / "epistemic-generative-state.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_epistemic_generative_state import check_artifact as check_fresh  # noqa: E402
from prediction.epistemic_generative_model import OBSERVATION_CLASSES, PROB_CEILING, PROB_EPSILON  # noqa: E402


def validate_payload(payload: dict) -> list[str]:
    issues: list[str] = []
    if "_meta" not in payload:
        issues.append("missing top-level `_meta`")
    latent = payload.get("latent_state")
    if not isinstance(latent, dict):
        issues.append("missing latent_state object")
    else:
        z = latent.get("Z")
        if not isinstance(z, list) or len(z) != 4:
            issues.append("latent_state.Z must be a 4-element list")
        if latent.get("inference_source") != "heuristic_v1":
            issues.append("latent_state.inference_source must be heuristic_v1")

    events = payload.get("events")
    if not isinstance(events, dict):
        issues.append("`events` must be an object")
        return issues

    for event_id, block in events.items():
        if not isinstance(block, dict):
            issues.append(f"events.{event_id}: must be an object")
            continue
        if block.get("interpretation") != "probabilistic_projection":
            issues.append(f"events.{event_id}: interpretation must be probabilistic_projection")
        prob = block.get("event_probability")
        if not isinstance(prob, (int, float)):
            issues.append(f"events.{event_id}: event_probability must be numeric")
        elif prob < PROB_EPSILON or prob > PROB_CEILING:
            issues.append(f"events.{event_id}: event_probability out of clamp bounds")
        voice_projections = block.get("voice_projections")
        if not isinstance(voice_projections, dict):
            issues.append(f"events.{event_id}: voice_projections must be an object")
            continue
        for voice, projection in voice_projections.items():
            if not isinstance(projection, dict):
                issues.append(f"events.{event_id}.voice_projections.{voice}: must be an object")
                continue
            probs = projection.get("observation_probs")
            if not isinstance(probs, dict):
                issues.append(f"events.{event_id}.voice_projections.{voice}: missing observation_probs")
            else:
                for cls in OBSERVATION_CLASSES:
                    if cls not in probs:
                        issues.append(
                            f"events.{event_id}.voice_projections.{voice}: missing class {cls!r}"
                        )
    return issues


def run_check(*, path: Path | None = None, advisory: bool = False) -> int:
    target = path or DEFAULT_PATH
    if not target.is_file():
        msg = f"missing {target.relative_to(REPO_ROOT)}"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    payload = json.loads(target.read_text(encoding="utf-8"))
    issues = validate_payload(payload)
    if issues:
        for line in issues:
            if advisory:
                print(f"WARN: {line}", file=sys.stderr)
            else:
                print(line, file=sys.stderr)
        return 0 if advisory else 1

    fresh_rc = check_fresh(output_path=target)
    if fresh_rc != 0:
        msg = f"{target.relative_to(REPO_ROOT)} is out of date; run build_epistemic_generative_state.py"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    print("[ok] epistemic generative state valid (advisory)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=DEFAULT_PATH)
    ap.add_argument(
        "--advisory",
        action="store_true",
        help="Never block exit code; emit WARN lines only (check_repo_health)",
    )
    args = ap.parse_args()
    return run_check(path=args.path, advisory=args.advisory)


if __name__ == "__main__":
    raise SystemExit(main())
