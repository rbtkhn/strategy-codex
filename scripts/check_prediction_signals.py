#!/usr/bin/env python3
"""Validate prediction-signals.json shape — advisory only (never blocks)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
DEFAULT_REGIME = REPO_ROOT / "runtime" / "artifacts" / "prediction-regime-summary.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_prediction_signals import check_artifact as check_signals_fresh  # noqa: E402
from prediction.signal_extraction_engine import SIGNAL_TYPES  # noqa: E402

REQUIRED_EVENT_FIELDS = (
    "signal_type",
    "trend",
    "confidence",
    "cross_voice_alignment",
    "drift_vector",
    "regime_shift_detected",
    "distribution_source",
    "primary_mode_id",
)


def validate_signals(payload: dict) -> list[str]:
    issues: list[str] = []
    if "_meta" not in payload:
        issues.append("missing top-level `_meta`")
    events = payload.get("events")
    if not isinstance(events, dict):
        issues.append("`events` must be an object")
        return issues
    for event_id, block in events.items():
        if not isinstance(block, dict):
            issues.append(f"events.{event_id}: must be an object")
            continue
        for field in REQUIRED_EVENT_FIELDS:
            if field not in block:
                issues.append(f"events.{event_id}: missing `{field}`")
        signal_type = block.get("signal_type")
        if signal_type not in SIGNAL_TYPES:
            issues.append(f"events.{event_id}: invalid signal_type {signal_type!r}")
        for key in ("confidence", "cross_voice_alignment"):
            val = block.get(key)
            if isinstance(val, (int, float)) and (val < 0 or val > 1):
                issues.append(f"events.{event_id}: {key} out of range")
        drift = block.get("drift_vector")
        if drift is not None and not isinstance(drift, list):
            issues.append(f"events.{event_id}: drift_vector must be a list")
    return issues


def validate_regime_summary(path: Path) -> list[str]:
    issues: list[str] = []
    if not path.is_file():
        issues.append(f"missing {path.relative_to(REPO_ROOT)}")
        return issues
    payload = json.loads(path.read_text(encoding="utf-8"))
    global_signals = payload.get("global_signals")
    if not isinstance(global_signals, dict):
        issues.append("regime summary missing global_signals object")
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
    issues = validate_signals(payload)
    issues.extend(validate_regime_summary(DEFAULT_REGIME))
    if issues:
        for line in issues:
            if advisory:
                print(f"WARN: {line}", file=sys.stderr)
            else:
                print(line, file=sys.stderr)
        return 0 if advisory else 1

    fresh_rc = check_signals_fresh(output_path=target)
    if fresh_rc != 0:
        msg = f"{target.relative_to(REPO_ROOT)} is out of date; run build_prediction_signals.py"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    print("[ok] prediction signals valid (advisory)")
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
