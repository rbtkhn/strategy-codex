#!/usr/bin/env python3
"""Generate runtime/artifacts/epistemic-generative-state.json (ENGM PR1 advisory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
DEFAULT_DISAGREEMENT = REPO_ROOT / "runtime" / "artifacts" / "prediction-disagreement.json"
DEFAULT_SEMANTIC = REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"
DEFAULT_SIGNALS = REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
DEFAULT_REGIME = REPO_ROOT / "runtime" / "artifacts" / "prediction-regime-summary.json"
DEFAULT_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "epistemic-generative-state.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.epistemic_generative_model import build_engm_payload  # noqa: E402
from prediction_lib import render_json  # noqa: E402


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def check_artifact(*, output_path: Path) -> int:
    if not output_path.is_file():
        print(f"error: missing {output_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    expected = render_json(
        build_engm_payload(
            timeline=_load(DEFAULT_TIMELINE),
            disagreement=_load(DEFAULT_DISAGREEMENT),
            semantic_scores=_load(DEFAULT_SEMANTIC),
            signals=_load(DEFAULT_SIGNALS),
            regime=_load(DEFAULT_REGIME),
        )
    )
    current = output_path.read_text(encoding="utf-8")
    if current != expected:
        print(
            f"error: {output_path.relative_to(REPO_ROOT)} is out of date; "
            "run build_epistemic_generative_state.py",
            file=sys.stderr,
        )
        return 1
    print("[ok] epistemic generative state artifact matches generator output")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument("--disagreement", type=Path, default=DEFAULT_DISAGREEMENT)
    ap.add_argument("--semantic-scores", type=Path, default=DEFAULT_SEMANTIC)
    ap.add_argument("--signals", type=Path, default=DEFAULT_SIGNALS)
    ap.add_argument("--regime", type=Path, default=DEFAULT_REGIME)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        return check_artifact(output_path=args.output)

    payload = build_engm_payload(
        timeline=_load(args.timeline),
        disagreement=_load(args.disagreement),
        semantic_scores=_load(args.semantic_scores),
        signals=_load(args.signals),
        regime=_load(args.regime),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    print(f"[ok] wrote {args.output.relative_to(REPO_ROOT)} ({len(payload.get('events') or {})} event(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
