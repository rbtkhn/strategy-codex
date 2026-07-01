#!/usr/bin/env python3
"""Generate PR8 Epistemic Intelligence Core artifacts (advisory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MVEL = REPO_ROOT / "runtime" / "artifacts" / "multivoice-extracted-dataset.json"
DEFAULT_SEMANTIC = REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"
DEFAULT_CORE = REPO_ROOT / "runtime" / "artifacts" / "epistemic-intelligence-core.json"
DEFAULT_EVENTS = REPO_ROOT / "runtime" / "artifacts" / "epistemic-intelligence-events.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.epistemic_intelligence_core import build_eic_payload  # noqa: E402
from prediction_lib import render_json  # noqa: E402


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def check_artifact(*, core_path: Path = DEFAULT_CORE) -> int:
    if not core_path.is_file():
        print(f"error: missing {core_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    expected = build_eic_payload(
        mvel_dataset=_load(DEFAULT_MVEL),
        semantic_scores=_load(DEFAULT_SEMANTIC),
    )
    paths = [
        (core_path, expected["core"]),
        (DEFAULT_EVENTS, expected["events_rollup"]),
    ]
    for path, payload in paths:
        if not path.is_file():
            print(f"error: missing {path.relative_to(REPO_ROOT)}", file=sys.stderr)
            return 1
        current = path.read_text(encoding="utf-8")
        rendered = render_json(payload)
        if current != rendered:
            print(
                f"error: {path.relative_to(REPO_ROOT)} is out of date; "
                "run build_epistemic_intelligence_core.py",
                file=sys.stderr,
            )
            return 1

    print("[ok] epistemic intelligence core artifacts match generator output")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mvel-dataset", type=Path, default=DEFAULT_MVEL)
    ap.add_argument("--semantic-scores", type=Path, default=DEFAULT_SEMANTIC)
    ap.add_argument("--core-output", type=Path, default=DEFAULT_CORE)
    ap.add_argument("--events-output", type=Path, default=DEFAULT_EVENTS)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        return check_artifact(core_path=args.core_output)

    bundle = build_eic_payload(
        mvel_dataset=_load(args.mvel_dataset),
        semantic_scores=_load(args.semantic_scores),
    )
    args.core_output.parent.mkdir(parents=True, exist_ok=True)
    args.core_output.write_text(render_json(bundle["core"]), encoding="utf-8")
    args.events_output.write_text(render_json(bundle["events_rollup"]), encoding="utf-8")
    meta = bundle["core"]["_meta"]
    print(
        f"[ok] wrote EIC artifacts (objects={meta['object_count']}, "
        f"high_entropy={meta.get('high_entropy_object_count', 0)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
