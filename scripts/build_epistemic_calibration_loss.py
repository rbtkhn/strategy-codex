#!/usr/bin/env python3
"""Generate runtime/artifacts/epistemic-calibration-loss.json (ENGM PR2 advisory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENGM = REPO_ROOT / "runtime" / "artifacts" / "epistemic-generative-state.json"
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
DEFAULT_SIGNALS = REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
DEFAULT_REGIME = REPO_ROOT / "runtime" / "artifacts" / "prediction-regime-summary.json"
DEFAULT_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "epistemic-calibration-loss.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.epistemic_loss import build_calibration_payload  # noqa: E402
from prediction_lib import render_json  # noqa: E402


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _eval_date_from_artifact(path: Path) -> str | None:
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    meta = payload.get("_meta") if isinstance(payload, dict) else {}
    if isinstance(meta, dict) and meta.get("eval_date"):
        return str(meta["eval_date"])
    return None


def check_artifact(*, output_path: Path, eval_date: str | None = None) -> int:
    if not output_path.is_file():
        print(f"error: missing {output_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    pinned = eval_date or _eval_date_from_artifact(output_path)
    expected = render_json(
        build_calibration_payload(
            engm=_load(DEFAULT_ENGM),
            timeline=_load(DEFAULT_TIMELINE),
            signals=_load(DEFAULT_SIGNALS),
            regime=_load(DEFAULT_REGIME),
            eval_date=pinned,
        )
    )
    current = output_path.read_text(encoding="utf-8")
    if current != expected:
        print(
            f"error: {output_path.relative_to(REPO_ROOT)} is out of date; "
            "run build_epistemic_calibration_loss.py",
            file=sys.stderr,
        )
        return 1
    print("[ok] epistemic calibration loss artifact matches generator output")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--engm", type=Path, default=DEFAULT_ENGM)
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument("--signals", type=Path, default=DEFAULT_SIGNALS)
    ap.add_argument("--regime", type=Path, default=DEFAULT_REGIME)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--eval-date", default=None, help="ISO eval date (default: today)")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        return check_artifact(output_path=args.output, eval_date=args.eval_date)

    payload = build_calibration_payload(
        engm=_load(args.engm),
        timeline=_load(args.timeline),
        signals=_load(args.signals),
        regime=_load(args.regime),
        eval_date=args.eval_date,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    print(
        f"[ok] wrote {args.output.relative_to(REPO_ROOT)} "
        f"(total_loss={payload.get('total_loss')}, events={len(payload.get('events') or {})})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
