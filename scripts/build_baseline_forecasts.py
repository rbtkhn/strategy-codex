#!/usr/bin/env python3
"""Generate runtime/artifacts/baseline-forecast-metrics.json (PR5 advisory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = REPO_ROOT / "runtime" / "artifacts" / "epistemic-dataset.json"
DEFAULT_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "baseline-forecast-metrics.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.baseline_models import build_baseline_payload  # noqa: E402
from prediction_lib import render_json  # noqa: E402


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _split_date_from_artifact(path: Path) -> str | None:
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    meta = payload.get("_meta") if isinstance(payload, dict) else {}
    if isinstance(meta, dict) and meta.get("split_date"):
        return str(meta["split_date"])
    return None


def check_artifact(*, output_path: Path, dataset_path: Path | None = None) -> int:
    if not output_path.is_file():
        print(f"error: missing {output_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    dataset_file = dataset_path or DEFAULT_DATASET
    expected = render_json(build_baseline_payload(_load(dataset_file)))
    current = output_path.read_text(encoding="utf-8")
    if current != expected:
        print(
            f"error: {output_path.relative_to(REPO_ROOT)} is out of date; "
            "run build_baseline_forecasts.py",
            file=sys.stderr,
        )
        return 1
    print("[ok] baseline forecast metrics artifact matches generator output")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        return check_artifact(output_path=args.output, dataset_path=args.dataset)

    payload = build_baseline_payload(_load(args.dataset))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    scope = payload["_meta"]["eval_scope"]
    print(
        f"[ok] wrote {args.output.relative_to(REPO_ROOT)} "
        f"(test_probability_n={scope['test_probability_n']}, "
        f"low_n={payload['_meta']['low_n_advisory']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
