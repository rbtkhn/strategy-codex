#!/usr/bin/env python3
"""Validate epistemic-calibration-loss.json shape — advisory only (never blocks)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "runtime" / "artifacts" / "epistemic-calibration-loss.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_epistemic_calibration_loss import check_artifact as check_fresh  # noqa: E402
from prediction.epistemic_loss import DEFAULT_WEIGHTS, LOW_N_ADVISORY_THRESHOLD  # noqa: E402


def validate_payload(payload: dict) -> list[str]:
    issues: list[str] = []
    if payload.get("interpretation") != "calibration_metric":
        issues.append("top-level interpretation must be calibration_metric")

    meta = payload.get("_meta")
    if not isinstance(meta, dict):
        issues.append("missing _meta object")
    else:
        if meta.get("calibration_source") != "heuristic_v1":
            issues.append("_meta.calibration_source must be heuristic_v1")
        scope = meta.get("calibration_scope")
        if not isinstance(scope, dict):
            issues.append("_meta.calibration_scope must be an object")

    weights = payload.get("weights")
    if not isinstance(weights, dict):
        issues.append("missing weights object")
    else:
        for key, default in DEFAULT_WEIGHTS.items():
            if key not in weights:
                issues.append(f"weights missing {key!r}")

    components = payload.get("components")
    if not isinstance(components, dict):
        issues.append("missing components object")
    else:
        for name in ("prediction_error", "brier_score", "entropy_misalignment", "regime_shift_delay"):
            if name not in components:
                issues.append(f"components missing {name!r}")

    total_loss = payload.get("total_loss")
    if not isinstance(total_loss, (int, float)):
        issues.append("total_loss must be numeric")
    elif total_loss < 0 or total_loss > 1:
        issues.append("total_loss out of [0, 1] range")

    events = payload.get("events")
    if not isinstance(events, dict):
        issues.append("`events` must be an object")
        return issues

    for event_id, block in events.items():
        if not isinstance(block, dict):
            issues.append(f"events.{event_id}: must be an object")
            continue
        if "included_in_brier" not in block:
            issues.append(f"events.{event_id}: missing included_in_brier")
        if block.get("included_in_brier"):
            for field in ("y_true", "y_pred", "prediction_error", "brier_score"):
                if field not in block:
                    issues.append(f"events.{event_id}: missing {field}")

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

    scope = (payload.get("_meta") or {}).get("calibration_scope") or {}
    if isinstance(scope, dict) and scope.get("low_n_advisory"):
        brier_eligible = scope.get("brier_eligible", 0)
        print(
            f"WARN: low resolved calibration N ({brier_eligible} < {LOW_N_ADVISORY_THRESHOLD}); "
            "advisory only",
            file=sys.stderr,
        )

    fresh_rc = check_fresh(output_path=target)
    if fresh_rc != 0:
        msg = f"{target.relative_to(REPO_ROOT)} is out of date; run build_epistemic_calibration_loss.py"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    print("[ok] epistemic calibration loss valid (advisory)")
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
