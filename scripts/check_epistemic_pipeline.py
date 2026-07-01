#!/usr/bin/env python3
"""Validate episystem canonical artifacts — advisory only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE = REPO_ROOT / "runtime" / "artifacts" / "epistemic_state.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.epistemic_core import REGIME_LABELS  # noqa: E402
from prediction.run_pipeline import check_artifacts  # noqa: E402


def validate_state(payload: dict) -> list[str]:
    issues: list[str] = []
    if payload.get("interpretation") != "epistemic_state":
        issues.append("interpretation must be epistemic_state")
    meta = payload.get("_meta")
    if not isinstance(meta, dict):
        issues.append("missing _meta")
    else:
        if meta.get("epistemic_source") != "heuristic_v1":
            issues.append("_meta.epistemic_source must be heuristic_v1")
        if meta.get("registry_mutation") is not False:
            issues.append("_meta.registry_mutation must be false")

    objects = payload.get("objects")
    if not isinstance(objects, list):
        issues.append("objects must be a list")
        return issues

    for idx, obj in enumerate(objects):
        if not isinstance(obj, dict):
            issues.append(f"objects[{idx}] must be object")
            continue
        if obj.get("interpretation") != "unified_epistemic_state":
            issues.append(f"objects[{idx}] interpretation must be unified_epistemic_state")
        for field in (
            "voice",
            "timestamp",
            "claim",
            "capture_map_event_id",
            "event_distribution",
            "trajectory_signals",
            "regime",
            "alignment_entropy",
        ):
            if field not in obj:
                issues.append(f"objects[{idx}] missing {field}")
        regime = obj.get("regime") if isinstance(obj.get("regime"), dict) else {}
        label = str(regime.get("label") or "")
        if label and label not in REGIME_LABELS:
            issues.append(f"objects[{idx}] invalid regime label {label!r}")
    return issues


def run_check(*, state_path: Path | None = None, advisory: bool = False) -> int:
    target = state_path or DEFAULT_STATE
    if not target.is_file():
        msg = f"missing {target.relative_to(REPO_ROOT)}"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    payload = json.loads(target.read_text(encoding="utf-8"))
    issues = validate_state(payload)

    signals_path = REPO_ROOT / "runtime" / "artifacts" / "signals.json"
    regimes_path = REPO_ROOT / "runtime" / "artifacts" / "regimes.json"
    if not signals_path.is_file():
        issues.append("missing signals.json")
    if not regimes_path.is_file():
        issues.append("missing regimes.json")

    if issues:
        for line in issues:
            if advisory:
                print(f"WARN: {line}", file=sys.stderr)
            else:
                print(line, file=sys.stderr)
        return 0 if advisory else 1

    meta = payload.get("_meta") or {}
    high_n = int(meta.get("high_entropy_object_count") or 0)
    if high_n > 0:
        print(
            f"WARN: {high_n} object(s) with alignment_entropy > 1.2 nats; advisory only",
            file=sys.stderr,
        )

    rc = check_artifacts()
    if rc != 0:
        if advisory:
            print("WARN: episystem artifacts stale vs generator", file=sys.stderr)
            return 0
        return rc

    print("[ok] episystem pipeline valid (advisory)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=DEFAULT_STATE)
    ap.add_argument("--advisory", action="store_true")
    args = ap.parse_args()
    return run_check(state_path=args.path, advisory=args.advisory)


if __name__ == "__main__":
    raise SystemExit(main())
