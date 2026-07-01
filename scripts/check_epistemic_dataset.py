#!/usr/bin/env python3
"""Validate epistemic-dataset.json shape — advisory only (never blocks)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "runtime" / "artifacts" / "epistemic-dataset.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_epistemic_dataset import check_artifact as check_fresh  # noqa: E402
from prediction.epistemic_dataset_builder import LOW_N_ADVISORY_THRESHOLD  # noqa: E402


def validate_payload(payload: dict) -> list[str]:
    issues: list[str] = []
    if payload.get("interpretation") != "ml_ready_dataset":
        issues.append("top-level interpretation must be ml_ready_dataset")

    meta = payload.get("_meta")
    if not isinstance(meta, dict):
        issues.append("missing _meta object")
    else:
        if meta.get("dataset_source") != "heuristic_v1":
            issues.append("_meta.dataset_source must be heuristic_v1")
        if not meta.get("split_date"):
            issues.append("_meta.split_date required")
        guarantees = meta.get("guarantees")
        if not isinstance(guarantees, dict):
            issues.append("_meta.guarantees must be an object")

    for split_name in ("train", "test"):
        rows = payload.get(split_name)
        if not isinstance(rows, list):
            issues.append(f"{split_name} must be a list")
            continue
        for idx, row in enumerate(rows):
            if not isinstance(row, dict):
                issues.append(f"{split_name}[{idx}]: must be an object")
                continue
            if row.get("interpretation") != "epistemic_dataset_row":
                issues.append(f"{split_name}[{idx}]: interpretation must be epistemic_dataset_row")
            for field in ("event_id", "anchor_date", "split", "voice_observations", "latent_features"):
                if field not in row:
                    issues.append(f"{split_name}[{idx}]: missing {field}")
            if row.get("split") != split_name:
                issues.append(f"{split_name}[{idx}]: split field mismatch")

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

    scope = (payload.get("_meta") or {}).get("dataset_scope") or {}
    if isinstance(scope, dict) and scope.get("low_n_advisory"):
        total = int(scope.get("row_count") or 0)
        print(
            f"WARN: low dataset row count ({total} < {LOW_N_ADVISORY_THRESHOLD}); advisory only",
            file=sys.stderr,
        )

    fresh_rc = check_fresh(output_path=target)
    if fresh_rc != 0:
        msg = f"{target.relative_to(REPO_ROOT)} is out of date; run build_epistemic_dataset.py"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    print("[ok] epistemic dataset valid (advisory)")
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
