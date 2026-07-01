#!/usr/bin/env python3
"""Validate epistemic-intelligence-core.json — advisory only (never blocks)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORE = REPO_ROOT / "runtime" / "artifacts" / "epistemic-intelligence-core.json"
DEFAULT_EVENTS = REPO_ROOT / "runtime" / "artifacts" / "epistemic-intelligence-events.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_epistemic_intelligence_core import check_artifact as check_fresh  # noqa: E402
from prediction.epistemic_intelligence_core import REGIME_LABELS  # noqa: E402


def validate_core(payload: dict) -> list[str]:
    issues: list[str] = []
    if payload.get("interpretation") != "epistemic_intelligence_core":
        issues.append("core interpretation must be epistemic_intelligence_core")

    meta = payload.get("_meta")
    if not isinstance(meta, dict):
        issues.append("core missing _meta")
    else:
        if meta.get("eic_source") != "heuristic_v1":
            issues.append("_meta.eic_source must be heuristic_v1")
        if meta.get("registry_mutation") is not False:
            issues.append("_meta.registry_mutation must be false")

    objects = payload.get("objects")
    if not isinstance(objects, list):
        issues.append("objects must be a list")
    else:
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


def validate_events(payload: dict) -> list[str]:
    issues: list[str] = []
    if payload.get("interpretation") != "epistemic_intelligence_events":
        issues.append("events rollup interpretation must be epistemic_intelligence_events")
    if "events" not in payload:
        issues.append("events rollup missing events object")
    return issues


def run_check(*, core_path: Path | None = None, advisory: bool = False) -> int:
    target = core_path or DEFAULT_CORE
    if not target.is_file():
        msg = f"missing {target.relative_to(REPO_ROOT)}"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    payload = json.loads(target.read_text(encoding="utf-8"))
    issues = validate_core(payload)
    if DEFAULT_EVENTS.is_file():
        issues.extend(validate_events(json.loads(DEFAULT_EVENTS.read_text(encoding="utf-8"))))
    else:
        issues.append("missing epistemic-intelligence-events.json")

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

    rc = check_fresh(core_path=target)
    if rc != 0:
        if advisory:
            print("WARN: epistemic intelligence core artifacts stale vs generator", file=sys.stderr)
            return 0
        return rc

    print("[ok] epistemic intelligence core valid (advisory)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=DEFAULT_CORE)
    ap.add_argument("--advisory", action="store_true")
    args = ap.parse_args()
    return run_check(core_path=args.path, advisory=args.advisory)


if __name__ == "__main__":
    raise SystemExit(main())
