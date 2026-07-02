#!/usr/bin/env python3
"""Validate Singularity loop run receipts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RUNS = REPO_ROOT / "runtime" / "operator-events" / "singularity-loop-runs.jsonl"
DEFAULT_REGISTRY = REPO_ROOT / "runtime" / "artifacts" / "loop-registry.json"

def load_loop_ids(registry_path: Path = DEFAULT_REGISTRY) -> set[str]:
    data = json.loads(registry_path.read_text(encoding="utf-8-sig"))
    return {str(row["id"]) for row in data.get("loops", [])}

def run_check(
    *,
    runs_path: Path = DEFAULT_RUNS,
    registry_path: Path = DEFAULT_REGISTRY,
) -> int:
    if not runs_path.exists():
        print("[ok] no singularity loop run receipts yet")
        return 0

    loop_ids = load_loop_ids(registry_path)
    failed = False
    count = 0

    for idx, line in enumerate(runs_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        count += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"[fail] line {idx}: invalid JSON: {exc}", file=sys.stderr)
            failed = True
            continue

        loop_id = row.get("loop_id")
        if loop_id not in loop_ids:
            print(f"[fail] line {idx}: unknown loop_id `{loop_id}`", file=sys.stderr)
            failed = True

        for next_loop_id in row.get("next_loop_ids") or []:
            if next_loop_id not in loop_ids:
                print(f"[fail] line {idx}: unknown next_loop_id `{next_loop_id}`", file=sys.stderr)
                failed = True

        if row.get("status") == "done" and not row.get("proof_artifact"):
            print(f"[warn] line {idx}: done receipt has no proof_artifact")

    if failed:
        print("check_singularity_loop_runs: validation failed", file=sys.stderr)
        return 1

    print(f"[ok] singularity loop run receipts valid ({count} rows)")
    return 0

def main() -> int:
    return run_check()

if __name__ == "__main__":
    raise SystemExit(main())
