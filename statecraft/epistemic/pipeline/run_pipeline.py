"""Epistemic audit pipeline orchestration."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from observation.loader import (
    DEFAULT_OUT as DEFAULT_OBSERVATIONS_OUT,
    DEFAULT_VOICE_DIR,
    REPO_ROOT,
    load_voice_captures,
    write_observations,
)
from structuring.normalize import (
    DEFAULT_OBSERVATIONS_IN,
    DEFAULT_REGISTRY,
    DEFAULT_STRUCTURED_OUT,
    load_event_registry,
    load_observations,
    normalize_observations,
    write_structured_predictions,
)


def run_observation_layer(
    *,
    voice_dir: Path | None = None,
    out_path: Path | None = None,
    repo_root: Path | None = None,
    write: bool = True,
) -> list[dict[str, Any]]:
    observations = load_voice_captures(voice_dir=voice_dir, repo_root=repo_root)
    if write:
        write_observations(observations, out_path=out_path)
    return observations


def run_structuring_layer(
    observations: list[dict[str, Any]] | None = None,
    *,
    observations_path: Path | None = None,
    registry_path: Path | None = None,
    out_path: Path | None = None,
    write: bool = True,
) -> list[dict[str, Any]]:
    obs = (
        observations
        if observations is not None
        else load_observations(path=observations_path or DEFAULT_OBSERVATIONS_IN)
    )
    registry = load_event_registry(path=registry_path or DEFAULT_REGISTRY)
    structured = normalize_observations(obs, registry)
    if write:
        write_structured_predictions(
            structured,
            out_path=out_path or DEFAULT_STRUCTURED_OUT,
            registry_path=registry_path or DEFAULT_REGISTRY,
        )
    return structured


def run_all_layers(
    *,
    voice_dir: Path | None = None,
    observations_out: Path | None = None,
    observations_in: Path | None = None,
    registry_path: Path | None = None,
    structured_out: Path | None = None,
    repo_root: Path | None = None,
    write: bool = True,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    observations = run_observation_layer(
        voice_dir=voice_dir,
        out_path=observations_out or DEFAULT_OBSERVATIONS_OUT,
        repo_root=repo_root,
        write=write,
    )
    structured = run_structuring_layer(
        observations,
        observations_path=observations_in,
        registry_path=registry_path,
        out_path=structured_out or DEFAULT_STRUCTURED_OUT,
        write=write,
    )
    return observations, structured


def main() -> int:
    parser = argparse.ArgumentParser(description="Run epistemic audit pipeline layers")
    parser.add_argument(
        "--layer",
        choices=("observation", "structuring", "all"),
        default="observation",
        help="Pipeline layer to run (default: observation)",
    )
    parser.add_argument(
        "--voice-dir",
        type=Path,
        default=DEFAULT_VOICE_DIR,
        help="Directory containing voice_captures/<voice>/*.md",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OBSERVATIONS_OUT,
        help="Output observations.json path",
    )
    parser.add_argument(
        "--observations-in",
        type=Path,
        default=DEFAULT_OBSERVATIONS_IN,
        help="Input observations.json path for structuring",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Event registry JSON path",
    )
    parser.add_argument(
        "--structured-out",
        type=Path,
        default=DEFAULT_STRUCTURED_OUT,
        help="Output structured_predictions.json path",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse without writing artifacts",
    )
    args = parser.parse_args()
    write = not args.dry_run

    if args.layer == "observation":
        observations = run_observation_layer(
            voice_dir=args.voice_dir,
            out_path=args.out,
            repo_root=REPO_ROOT,
            write=write,
        )
        if args.dry_run:
            print(f"observations: {len(observations)} (dry run, no write)")
        else:
            print(f"observations: {len(observations)} -> {args.out}")
        return 0

    if args.layer == "structuring":
        structured = run_structuring_layer(
            observations_path=args.observations_in,
            registry_path=args.registry,
            out_path=args.structured_out,
            write=write,
        )
        if args.dry_run:
            print(f"structured_predictions: {len(structured)} (dry run, no write)")
        else:
            print(f"structured_predictions: {len(structured)} -> {args.structured_out}")
        return 0

    observations, structured = run_all_layers(
        voice_dir=args.voice_dir,
        observations_out=args.out,
        registry_path=args.registry,
        structured_out=args.structured_out,
        repo_root=REPO_ROOT,
        write=write,
    )
    if args.dry_run:
        print(
            f"all: observations={len(observations)} structured={len(structured)} "
            "(dry run, no write)"
        )
    else:
        print(
            f"all: observations={len(observations)} -> {args.out}; "
            f"structured={len(structured)} -> {args.structured_out}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
