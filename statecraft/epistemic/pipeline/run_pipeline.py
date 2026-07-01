"""Epistemic audit pipeline orchestration."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from observation.loader import (
    DEFAULT_OUT,
    DEFAULT_VOICE_DIR,
    REPO_ROOT,
    load_voice_captures,
    write_observations,
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Run epistemic observation layer (PR2)")
    parser.add_argument(
        "--voice-dir",
        type=Path,
        default=DEFAULT_VOICE_DIR,
        help="Directory containing voice_captures/<voice>/*.md",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="Output observations.json path",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse captures without writing observations.json",
    )
    args = parser.parse_args()

    observations = run_observation_layer(
        voice_dir=args.voice_dir,
        out_path=args.out,
        repo_root=REPO_ROOT,
        write=not args.dry_run,
    )

    if args.dry_run:
        print(f"observations: {len(observations)} (dry run, no write)")
    else:
        print(f"observations: {len(observations)} -> {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
