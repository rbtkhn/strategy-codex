#!/usr/bin/env python3
"""Episystem canonical pipeline — write epistemic_state, signals, regimes artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = REPO_ROOT / "runtime" / "artifacts"
DEFAULT_SEMANTIC = ARTIFACT_DIR / "prediction-semantic-scores.json"
DEFAULT_DISAGREEMENT = ARTIFACT_DIR / "prediction-disagreement.json"

_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.epistemic_core import build_epistemic_payload  # noqa: E402
from prediction.plugins.runner import build_enriched_payload  # noqa: E402
from prediction_lib import render_json  # noqa: E402

def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}

def build_artifacts(
    *,
    semantic_scores: dict | None = None,
    disagreement: dict | None = None,
    include_multivoice: bool = True,
    with_plugins: bool = False,
) -> dict:
    bundle = build_epistemic_payload(
        semantic_scores=semantic_scores or {},
        disagreement=disagreement or {},
        include_multivoice=include_multivoice,
    )
    if with_plugins:
        bundle["epistemic_enriched"] = build_enriched_payload(bundle)
    return bundle

def write_artifacts(
    bundle: dict,
    *,
    artifact_dir: Path = ARTIFACT_DIR,
    include_multivoice: bool = True,
    with_plugins: bool = False,
) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    (artifact_dir / "epistemic_state.json").write_text(
        render_json(bundle["epistemic_state"]),
        encoding="utf-8",
    )
    (artifact_dir / "signals.json").write_text(
        render_json(bundle["signals"]),
        encoding="utf-8",
    )
    (artifact_dir / "regimes.json").write_text(
        render_json(bundle["regimes"]),
        encoding="utf-8",
    )
    if include_multivoice and "multivoice_dataset" in bundle:
        (artifact_dir / "multivoice_dataset.json").write_text(
            render_json(bundle["multivoice_dataset"]),
            encoding="utf-8",
        )
    if with_plugins and "epistemic_enriched" in bundle:
        (artifact_dir / "epistemic_enriched.json").write_text(
            render_json(bundle["epistemic_enriched"]),
            encoding="utf-8",
        )

def check_artifacts(
    *,
    artifact_dir: Path = ARTIFACT_DIR,
    semantic_path: Path = DEFAULT_SEMANTIC,
    disagreement_path: Path = DEFAULT_DISAGREEMENT,
    include_multivoice: bool = True,
) -> int:
    expected = build_artifacts(
        semantic_scores=_load(semantic_path),
        disagreement=_load(disagreement_path),
        include_multivoice=include_multivoice,
        with_plugins=False,
    )
    paths = [
        artifact_dir / "epistemic_state.json",
        artifact_dir / "signals.json",
        artifact_dir / "regimes.json",
    ]
    if include_multivoice:
        paths.append(artifact_dir / "multivoice_dataset.json")

    key_map = {
        "epistemic_state.json": "epistemic_state",
        "signals.json": "signals",
        "regimes.json": "regimes",
        "multivoice_dataset.json": "multivoice_dataset",
    }
    for path in paths:
        if not path.is_file():
            print(f"error: missing {path.relative_to(REPO_ROOT)}", file=sys.stderr)
            return 1

    for path in paths:
        key = key_map[path.name]
        current = path.read_text(encoding="utf-8")
        exp = render_json(expected[key])
        if current != exp:
            print(
                f"error: {path.relative_to(REPO_ROOT)} out of date; "
                "run scripts/prediction/run_pipeline.py --write",
                file=sys.stderr,
            )
            return 1

    print("[ok] episystem artifacts match generator output")
    return 0

def check_enriched_artifacts(
    *,
    artifact_dir: Path = ARTIFACT_DIR,
    semantic_path: Path = DEFAULT_SEMANTIC,
    disagreement_path: Path = DEFAULT_DISAGREEMENT,
    include_multivoice: bool = True,
) -> int:
    path = artifact_dir / "epistemic_enriched.json"
    if not path.is_file():
        print(
            f"error: missing {path.relative_to(REPO_ROOT)}; "
            "run scripts/prediction/run_pipeline.py --write --with-plugins",
            file=sys.stderr,
        )
        return 1

    expected = build_artifacts(
        semantic_scores=_load(semantic_path),
        disagreement=_load(disagreement_path),
        include_multivoice=include_multivoice,
        with_plugins=True,
    )
    current = path.read_text(encoding="utf-8")
    exp = render_json(expected["epistemic_enriched"])
    if current != exp:
        print(
            f"error: {path.relative_to(REPO_ROOT)} out of date; "
            "run scripts/prediction/run_pipeline.py --write --with-plugins",
            file=sys.stderr,
        )
        return 1

    print("[ok] epistemic enriched artifact matches generator output")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="write canonical artifacts")
    ap.add_argument("--check", action="store_true", help="drift check vs generator (core only)")
    ap.add_argument(
        "--check-enriched",
        action="store_true",
        help="drift check for epistemic_enriched.json",
    )
    ap.add_argument(
        "--with-plugins",
        action="store_true",
        help="also write epistemic_enriched.json via plugin layer",
    )
    ap.add_argument("--semantic-scores", type=Path, default=DEFAULT_SEMANTIC)
    ap.add_argument("--disagreement", type=Path, default=DEFAULT_DISAGREEMENT)
    ap.add_argument("--artifact-dir", type=Path, default=ARTIFACT_DIR)
    ap.add_argument("--skip-multivoice-export", action="store_true")
    args = ap.parse_args()

    include_mv = not args.skip_multivoice_export
    if args.check:
        return check_artifacts(
            artifact_dir=args.artifact_dir,
            semantic_path=args.semantic_scores,
            disagreement_path=args.disagreement,
            include_multivoice=include_mv,
        )
    if args.check_enriched:
        return check_enriched_artifacts(
            artifact_dir=args.artifact_dir,
            semantic_path=args.semantic_scores,
            disagreement_path=args.disagreement,
            include_multivoice=include_mv,
        )

    bundle = build_artifacts(
        semantic_scores=_load(args.semantic_scores),
        disagreement=_load(args.disagreement),
        include_multivoice=include_mv,
        with_plugins=args.with_plugins,
    )
    if args.write or (not args.check and not args.check_enriched):
        write_artifacts(
            bundle,
            artifact_dir=args.artifact_dir,
            include_multivoice=include_mv,
            with_plugins=args.with_plugins,
        )
        msg = (
            f"[ok] episystem complete objects={bundle['object_count']} "
            f"trajectories={bundle['trajectory_count']} "
            f"unmatched={bundle['alignment_audit']['stats']['unmatched_count']}"
        )
        if args.with_plugins:
            msg += " enriched=1"
        print(msg)
        return 0

    ap.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
