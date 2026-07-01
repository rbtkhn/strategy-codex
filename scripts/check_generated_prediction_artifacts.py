#!/usr/bin/env python3
"""Verify committed prediction artifacts match freshly computed generator output."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import build_prediction_disagreement  # noqa: E402
import build_prediction_metrics  # noqa: E402
import build_prediction_registry  # noqa: E402
import build_prediction_timeline  # noqa: E402
from prediction.run_pipeline import check_artifacts  # noqa: E402


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
    rc |= check_artifacts()

    if rc == 0:
        print("[ok] generated prediction artifacts are fresh")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
