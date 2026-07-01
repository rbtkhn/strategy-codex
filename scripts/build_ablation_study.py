#!/usr/bin/env python3
"""Generate runtime/artifacts/ablation-study.json (PR6 advisory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
DEFAULT_SIGNALS = REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
DEFAULT_DISAGREEMENT = REPO_ROOT / "runtime" / "artifacts" / "prediction-disagreement.json"
DEFAULT_SEMANTIC = REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"
DEFAULT_REGIME = REPO_ROOT / "runtime" / "artifacts" / "prediction-regime-summary.json"
DEFAULT_DATASET = REPO_ROOT / "runtime" / "artifacts" / "epistemic-dataset.json"
DEFAULT_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "ablation-study.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.ablation_study import build_ablation_payload  # noqa: E402
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
    pinned = split_date or _split_date_from_artifact(DEFAULT_DATASET) or _split_date_from_artifact(output_path)
    expected = render_json(
        build_ablation_payload(
            timeline=_load(DEFAULT_TIMELINE),
            signals=_load(DEFAULT_SIGNALS),
            disagreement=_load(DEFAULT_DISAGREEMENT),
            semantic_scores=_load(DEFAULT_SEMANTIC),
            regime=_load(DEFAULT_REGIME),
            split_date=pinned,
        )
    )
    current = output_path.read_text(encoding="utf-8")
    if current != expected:
        print(
            f"error: {output_path.relative_to(REPO_ROOT)} is out of date; "
            "run build_ablation_study.py",
            file=sys.stderr,
        )
        return 1
    print("[ok] ablation study artifact matches generator output")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument("--signals", type=Path, default=DEFAULT_SIGNALS)
    ap.add_argument("--disagreement", type=Path, default=DEFAULT_DISAGREEMENT)
    ap.add_argument("--semantic-scores", type=Path, default=DEFAULT_SEMANTIC)
    ap.add_argument("--regime", type=Path, default=DEFAULT_REGIME)
    ap.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        split_date = _split_date_from_artifact(args.dataset)
        return check_artifact(output_path=args.output, split_date=split_date)

    dataset_meta = (_load(args.dataset).get("_meta") or {}) if args.dataset.is_file() else {}
    split_date = str(dataset_meta.get("split_date") or "2026-01-01")

    payload = build_ablation_payload(
        timeline=_load(args.timeline),
        signals=_load(args.signals),
        disagreement=_load(args.disagreement),
        semantic_scores=_load(args.semantic_scores),
        regime=_load(args.regime),
        split_date=split_date,
    )
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
