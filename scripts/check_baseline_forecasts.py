#!/usr/bin/env python3
"""Validate baseline-forecast-metrics.json shape — advisory only (never blocks)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "runtime" / "artifacts" / "baseline-forecast-metrics.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_baseline_forecasts import check_artifact as check_fresh  # noqa: E402
from prediction.baseline_models import (  # noqa: E402
    LOW_N_PROBABILITY_THRESHOLD,
    LOW_N_SHIFT_SUPPORT_THRESHOLD,
)


def validate_payload(payload: dict) -> list[str]:
    issues: list[str] = []
    if payload.get("interpretation") != "baseline_evaluation":
        issues.append("top-level interpretation must be baseline_evaluation")
    if payload.get("system_reference") != "engm_event_probability":
        issues.append("system_reference must be engm_event_probability")

    meta = payload.get("_meta")
    if not isinstance(meta, dict):
        issues.append("missing _meta object")
    else:
        if meta.get("baseline_source") != "heuristic_v1":
            issues.append("_meta.baseline_source must be heuristic_v1")
        if not meta.get("split_date"):
            issues.append("_meta.split_date required")

    baselines = payload.get("baselines")
    if not isinstance(baselines, dict):
        issues.append("baselines must be an object")
    else:
        for name in ("persistence", "bayesian", "logistic_trend", "transformer"):
            if name not in baselines:
                issues.append(f"baselines.{name} required")

    comparison = payload.get("comparison")
    if not isinstance(comparison, dict) or "test" not in comparison:
        issues.append("comparison.test required")

    system = payload.get("system")
    if not isinstance(system, dict) or "test" not in system:
        issues.append("system.test required")

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

    scope = (payload.get("_meta") or {}).get("eval_scope") or {}
    if isinstance(scope, dict):
        prob_n = int(scope.get("test_probability_n") or 0)
        shift_support = int(scope.get("test_shift_support") or 0)
        if prob_n < LOW_N_PROBABILITY_THRESHOLD:
            print(
                f"WARN: low test probability N ({prob_n} < {LOW_N_PROBABILITY_THRESHOLD}); advisory only",
                file=sys.stderr,
            )
        if shift_support < LOW_N_SHIFT_SUPPORT_THRESHOLD:
            print(
                f"WARN: no test shift support ({shift_support} < {LOW_N_SHIFT_SUPPORT_THRESHOLD}); "
                "regime F1 uninformative",
                file=sys.stderr,
            )

    if (payload.get("_meta") or {}).get("low_n_advisory"):
        print("WARN: low_n_advisory flagged in artifact _meta", file=sys.stderr)

    fresh_rc = check_fresh(output_path=target)
    if fresh_rc != 0:
        msg = f"{target.relative_to(REPO_ROOT)} is out of date; run build_baseline_forecasts.py"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    print("[ok] baseline forecast metrics valid (advisory)")
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
