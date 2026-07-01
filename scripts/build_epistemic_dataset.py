#!/usr/bin/env python3
"""Generate runtime/artifacts/epistemic-dataset.json (PR4 advisory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
DEFAULT_SIGNALS = REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
DEFAULT_SEMANTIC = REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"
DEFAULT_ENGM = REPO_ROOT / "runtime" / "artifacts" / "epistemic-generative-state.json"
DEFAULT_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "epistemic-dataset.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.epistemic_dataset_builder import (  # noqa: E402
    DEFAULT_HORIZON_DAYS,
    DEFAULT_SPLIT_DATE,
    build_dataset_payload,
)
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


def check_artifact(*, output_path: Path, split_date: str | None = None) -> int:
    if not output_path.is_file():
        print(f"error: missing {output_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    pinned = split_date or _split_date_from_artifact(output_path) or DEFAULT_SPLIT_DATE
    expected = render_json(
        build_dataset_payload(
            timeline=_load(DEFAULT_TIMELINE),
            signals=_load(DEFAULT_SIGNALS),
            semantic_scores=_load(DEFAULT_SEMANTIC),
            engm=_load(DEFAULT_ENGM),
            split_date=pinned,
            horizon_days=DEFAULT_HORIZON_DAYS,
        )
    )
    current = output_path.read_text(encoding="utf-8")
    if current != expected:
        print(
            f"error: {output_path.relative_to(REPO_ROOT)} is out of date; "
            "run build_epistemic_dataset.py",
            file=sys.stderr,
        )
        return 1
    print("[ok] epistemic dataset artifact matches generator output")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument("--signals", type=Path, default=DEFAULT_SIGNALS)
    ap.add_argument("--semantic-scores", type=Path, default=DEFAULT_SEMANTIC)
    ap.add_argument("--engm", type=Path, default=DEFAULT_ENGM)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--split-date", default=DEFAULT_SPLIT_DATE)
    ap.add_argument("--horizon-days", type=int, default=DEFAULT_HORIZON_DAYS)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        return check_artifact(output_path=args.output, split_date=args.split_date)

    payload = build_dataset_payload(
        timeline=_load(args.timeline),
        signals=_load(args.signals),
        semantic_scores=_load(args.semantic_scores),
        engm=_load(args.engm),
        split_date=args.split_date,
        horizon_days=args.horizon_days,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    scope = payload["_meta"]["dataset_scope"]
    print(
        f"[ok] wrote {args.output.relative_to(REPO_ROOT)} "
        f"(train={scope['train_count']}, test={scope['test_count']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
