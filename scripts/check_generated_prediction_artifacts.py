#!/usr/bin/env python3
"""Verify committed prediction artifacts match freshly computed generator output."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import build_epistemic_generative_state  # noqa: E402
import build_prediction_disagreement  # noqa: E402
import build_prediction_metrics  # noqa: E402
import build_prediction_registry  # noqa: E402
import build_prediction_regime_summary  # noqa: E402
import build_prediction_signals  # noqa: E402
import build_prediction_timeline  # noqa: E402

def main() -> int:
    rc = build_prediction_registry.check_artifact(
        output_path=build_prediction_registry.DEFAULT_OUTPUT
    )
    rc |= build_prediction_metrics.check_artifact(
        output_path=build_prediction_metrics.DEFAULT_OUTPUT,
        registry_path=build_prediction_metrics.DEFAULT_REGISTRY,
    )
    rc |= build_prediction_disagreement.check_artifact(
        output_path=build_prediction_disagreement.DEFAULT_OUTPUT,
        registry_path=build_prediction_disagreement.DEFAULT_REGISTRY,
    )
    rc |= build_prediction_timeline.check_artifact(
        output_path=build_prediction_timeline.DEFAULT_OUTPUT,
        registry_path=build_prediction_timeline.DEFAULT_REGISTRY,
    )
    rc |= build_prediction_signals.check_artifact(
        output_path=build_prediction_signals.DEFAULT_OUTPUT,
    )
    rc |= build_prediction_regime_summary.check_artifact(
        output_path=build_prediction_regime_summary.DEFAULT_OUTPUT,
        signals_path=build_prediction_regime_summary.DEFAULT_SIGNALS,
    )
    rc |= build_epistemic_generative_state.check_artifact(
        output_path=build_epistemic_generative_state.DEFAULT_OUTPUT,
    )

    if rc == 0:
        print("[ok] generated prediction artifacts are fresh")
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
