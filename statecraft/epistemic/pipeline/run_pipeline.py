"""Epistemic audit pipeline orchestration."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from analysis.engine import (
    DEFAULT_ANALYSIS_OUT,
    DEFAULT_STRUCTURED_IN as ANALYSIS_STRUCTURED_IN,
    analyze_all,
    load_structured_predictions as load_structured_for_analysis,
    write_analysis,
)
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
from temporal.temporal_engine import (
    DEFAULT_OBSERVATIONS_IN as TEMPORAL_OBSERVATIONS_IN,
    DEFAULT_STRUCTURED_IN as TEMPORAL_STRUCTURED_IN,
    DEFAULT_TEMPORAL_OUT,
    build_temporal_view,
    load_structured_predictions as load_structured_for_temporal,
    write_temporal_view,
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

def run_analysis_layer(
    structured: list[dict[str, Any]] | None = None,
    *,
    structured_path: Path | None = None,
    out_path: Path | None = None,
    write: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    preds = (
        structured
        if structured is not None
        else load_structured_for_analysis(path=structured_path or ANALYSIS_STRUCTURED_IN)
    )
    analysis_by_event, summary = analyze_all(preds)
    if write:
        write_analysis(
            analysis_by_event,
            summary,
            out_path=out_path or DEFAULT_ANALYSIS_OUT,
            structured_path=structured_path or ANALYSIS_STRUCTURED_IN,
        )
    return analysis_by_event, summary

def run_temporal_layer(
    structured: list[dict[str, Any]] | None = None,
    observations: list[dict[str, Any]] | None = None,
    *,
    structured_path: Path | None = None,
    observations_path: Path | None = None,
    out_path: Path | None = None,
    write: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    preds = (
        structured
        if structured is not None
        else load_structured_for_temporal(path=structured_path or TEMPORAL_STRUCTURED_IN)
    )
    obs = (
        observations
        if observations is not None
        else load_observations(path=observations_path or TEMPORAL_OBSERVATIONS_IN)
    )
    temporal_by_event, summary = build_temporal_view(preds, obs)
    if write:
        write_temporal_view(
            temporal_by_event,
            summary,
            out_path=out_path or DEFAULT_TEMPORAL_OUT,
            structured_path=structured_path or TEMPORAL_STRUCTURED_IN,
            observations_path=observations_path or TEMPORAL_OBSERVATIONS_IN,
        )
    return temporal_by_event, summary

def run_all_layers(
    *,
    voice_dir: Path | None = None,
    observations_out: Path | None = None,
    observations_in: Path | None = None,
    registry_path: Path | None = None,
    structured_out: Path | None = None,
    structured_in: Path | None = None,
    analysis_out: Path | None = None,
    temporal_out: Path | None = None,
    repo_root: Path | None = None,
    write: bool = True,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
    list[dict[str, Any]],
    dict[str, Any],
]:
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
    analysis_by_event, analysis_summary = run_analysis_layer(
        structured,
        structured_path=structured_in or structured_out or ANALYSIS_STRUCTURED_IN,
        out_path=analysis_out or DEFAULT_ANALYSIS_OUT,
        write=write,
    )
    temporal_by_event, temporal_summary = run_temporal_layer(
        structured,
        observations,
        structured_path=structured_in or structured_out or TEMPORAL_STRUCTURED_IN,
        observations_path=observations_in or observations_out or TEMPORAL_OBSERVATIONS_IN,
        out_path=temporal_out or DEFAULT_TEMPORAL_OUT,
        write=write,
    )
    return (
        observations,
        structured,
        analysis_by_event,
        analysis_summary,
        temporal_by_event,
        temporal_summary,
    )

def main() -> int:
    parser = argparse.ArgumentParser(description="Run epistemic audit pipeline layers")
    parser.add_argument(
        "--layer",
        choices=("observation", "structuring", "analysis", "temporal", "all"),
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
        help="Input observations.json path for structuring/temporal",
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
        "--structured-in",
        type=Path,
        default=ANALYSIS_STRUCTURED_IN,
        help="Input structured_predictions.json path for analysis/temporal",
    )
    parser.add_argument(
        "--analysis-out",
        type=Path,
        default=DEFAULT_ANALYSIS_OUT,
        help="Output analysis.json path",
    )
    parser.add_argument(
        "--temporal-out",
        type=Path,
        default=DEFAULT_TEMPORAL_OUT,
        help="Output temporal.json path",
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

    if args.layer == "analysis":
        analysis_by_event, summary = run_analysis_layer(
            structured_path=args.structured_in,
            out_path=args.analysis_out,
            write=write,
        )
        if args.dry_run:
            print(
                f"analysis: events={len(analysis_by_event)} "
                f"divergence_events={len(summary['cross_voice_divergence'])} "
                "(dry run, no write)"
            )
        else:
            print(
                f"analysis: events={len(analysis_by_event)} "
                f"divergence_events={len(summary['cross_voice_divergence'])} "
                f"-> {args.analysis_out}"
            )
        return 0

    if args.layer == "temporal":
        temporal_by_event, summary = run_temporal_layer(
            structured_path=args.structured_in,
            observations_path=args.observations_in,
            out_path=args.temporal_out,
            write=write,
        )
        if args.dry_run:
            print(
                f"temporal: events={len(temporal_by_event)} "
                f"event_count={summary['event_count']} "
                "(dry run, no write)"
            )
        else:
            print(
                f"temporal: events={len(temporal_by_event)} "
                f"event_count={summary['event_count']} "
                f"-> {args.temporal_out}"
            )
        return 0

    (
        observations,
        structured,
        analysis_by_event,
        analysis_summary,
        temporal_by_event,
        temporal_summary,
    ) = run_all_layers(
        voice_dir=args.voice_dir,
        observations_out=args.out,
        observations_in=args.observations_in,
        registry_path=args.registry,
        structured_out=args.structured_out,
        structured_in=args.structured_in,
        analysis_out=args.analysis_out,
        temporal_out=args.temporal_out,
        repo_root=REPO_ROOT,
        write=write,
    )
    if args.dry_run:
        print(
            f"all: observations={len(observations)} structured={len(structured)} "
            f"analysis_events={len(analysis_by_event)} "
            f"divergence_events={len(analysis_summary['cross_voice_divergence'])} "
            f"temporal_events={len(temporal_by_event)} "
            f"event_count={temporal_summary['event_count']} "
            "(dry run, no write)"
        )
    else:
        print(
            f"all: observations={len(observations)} -> {args.out}; "
            f"structured={len(structured)} -> {args.structured_out}; "
            f"analysis_events={len(analysis_by_event)} "
            f"divergence_events={len(analysis_summary['cross_voice_divergence'])} "
            f"-> {args.analysis_out}; "
            f"temporal_events={len(temporal_by_event)} "
            f"event_count={temporal_summary['event_count']} "
            f"-> {args.temporal_out}"
        )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
