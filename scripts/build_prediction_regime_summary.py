#!/usr/bin/env python3
"""Generate runtime/artifacts/prediction-regime-summary.json (Phase 4.5 advisory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SIGNALS = REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
DEFAULT_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "prediction-regime-summary.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.signal_extraction_engine import build_regime_summary_payload  # noqa: E402
from prediction_lib import render_json  # noqa: E402


def check_artifact(*, output_path: Path, signals_path: Path) -> int:
    if not output_path.is_file():
        print(f"error: missing {output_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    if not signals_path.is_file():
        print(f"error: missing {signals_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    signals_payload = json.loads(signals_path.read_text(encoding="utf-8"))
    expected = render_json(build_regime_summary_payload(signals_payload))
    current = output_path.read_text(encoding="utf-8")
    if current != expected:
        print(
            f"error: {output_path.relative_to(REPO_ROOT)} is out of date; "
            "run build_prediction_regime_summary.py",
            file=sys.stderr,
        )
        return 1
    print("[ok] prediction regime summary artifact matches generator output")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--signals", type=Path, default=DEFAULT_SIGNALS)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        return check_artifact(output_path=args.output, signals_path=args.signals)

    if not args.signals.is_file():
        print(f"error: missing {args.signals.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    signals_payload = json.loads(args.signals.read_text(encoding="utf-8"))
    payload = build_regime_summary_payload(signals_payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    print(f"[ok] wrote {args.output.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
