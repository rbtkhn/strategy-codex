#!/usr/bin/env python3
"""Validate MVEL artifacts — advisory only (never blocks)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = REPO_ROOT / "runtime" / "artifacts" / "multivoice-extracted-dataset.json"
DEFAULT_ALIGNMENT = REPO_ROOT / "runtime" / "artifacts" / "event-alignment-map.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_multivoice_extraction import check_artifact as check_fresh  # noqa: E402
from prediction.run_multivoice_extraction import LOW_N_TRAJECTORY_THRESHOLD  # noqa: E402
from voice_prediction_pilot import VOICE_REGISTRY  # noqa: E402


def validate_dataset(payload: dict) -> list[str]:
    issues: list[str] = []
    if payload.get("interpretation") != "multivoice_extraction":
        issues.append("dataset interpretation must be multivoice_extraction")

    meta = payload.get("_meta")
    if not isinstance(meta, dict):
        issues.append("dataset missing _meta")
    else:
        if meta.get("extraction_source") != "heuristic_v1":
            issues.append("_meta.extraction_source must be heuristic_v1")
        if meta.get("claim_source") != "capture_map":
            issues.append("_meta.claim_source must be capture_map")
        if meta.get("registry_mutation") is not False:
            issues.append("_meta.registry_mutation must be false")

    trajectories = payload.get("trajectories")
    if not isinstance(trajectories, list):
        issues.append("trajectories must be a list")
    else:
        for idx, traj in enumerate(trajectories):
            if not isinstance(traj, dict):
                issues.append(f"trajectories[{idx}] must be object")
                continue
            for field in ("event_id", "voice", "trajectory", "alignment_score"):
                if field not in traj:
                    issues.append(f"trajectories[{idx}] missing {field}")
            points = traj.get("trajectory")
            if isinstance(points, list):
                for pidx, point in enumerate(points):
                    if not isinstance(point, dict):
                        continue
                    for pf in ("timestamp", "claim", "stance", "probability", "confidence"):
                        if pf not in point:
                            issues.append(f"trajectories[{idx}].trajectory[{pidx}] missing {pf}")

    return issues


def validate_alignment(payload: dict) -> list[str]:
    issues: list[str] = []
    if payload.get("interpretation") != "event_alignment_audit":
        issues.append("alignment interpretation must be event_alignment_audit")
    for field in ("matched", "unmatched", "stats"):
        if field not in payload:
            issues.append(f"alignment map missing {field}")
    return issues


def run_check(*, dataset_path: Path | None = None, advisory: bool = False) -> int:
    dataset = dataset_path or DEFAULT_DATASET
    if not dataset.is_file():
        msg = f"missing {dataset.relative_to(REPO_ROOT)}"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    payload = json.loads(dataset.read_text(encoding="utf-8"))
    issues = validate_dataset(payload)
    if DEFAULT_ALIGNMENT.is_file():
        alignment = json.loads(DEFAULT_ALIGNMENT.read_text(encoding="utf-8"))
        issues.extend(validate_alignment(alignment))
    else:
        issues.append("missing event-alignment-map.json")

    for speaker in sorted(VOICE_REGISTRY.keys()):
        voice_path = REPO_ROOT / "runtime" / "artifacts" / f"voice-trajectories-{speaker}.json"
        if not voice_path.is_file():
            issues.append(f"missing voice-trajectories-{speaker}.json")

    if issues:
        for line in issues:
            if advisory:
                print(f"WARN: {line}", file=sys.stderr)
            else:
                print(line, file=sys.stderr)
        return 0 if advisory else 1

    scope = (payload.get("_meta") or {}).get("extraction_scope") or {}
    traj_n = int(scope.get("trajectory_count") or 0)
    unmatched = int(scope.get("unmatched_count") or 0)
    if traj_n < LOW_N_TRAJECTORY_THRESHOLD:
        print(
            f"WARN: sparse trajectory corpus ({traj_n} < {LOW_N_TRAJECTORY_THRESHOLD}); advisory only",
            file=sys.stderr,
        )
    if unmatched > 0:
        print(f"WARN: {unmatched} unmatched claim(s) in review queue", file=sys.stderr)
    if (payload.get("_meta") or {}).get("low_n_advisory"):
        print("WARN: low_n_advisory flagged in dataset _meta", file=sys.stderr)

    rc = check_fresh(dataset_path=dataset)
    if rc != 0:
        if advisory:
            print("WARN: multivoice extraction artifacts stale vs generator", file=sys.stderr)
            return 0
        return rc

    print("[ok] multivoice extraction valid (advisory)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=DEFAULT_DATASET)
    ap.add_argument("--advisory", action="store_true")
    args = ap.parse_args()
    return run_check(dataset_path=args.path, advisory=args.advisory)


if __name__ == "__main__":
    raise SystemExit(main())
