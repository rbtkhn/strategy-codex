#!/usr/bin/env python3
"""Post-land hook: Mercouris solo close scaffold normalize for statecraft captures.

Usage:
    python scripts/post_land_mercouris_close_normalize.py --path <landed-file>
    python scripts/post_land_mercouris_close_normalize.py --path <landed-file> --dry-run
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from normalize_mercouris_close_scaffold import (  # noqa: E402
    ARCHIVE_ROOT,
    is_mercouris_solo_capture,
    normalize_mercouris,
    split_frontmatter,
)


@dataclass(frozen=True)
class PostLandResult:
    path: Path
    status: str
    applied: bool
    flags: str


def _resolve_landed_path(path: Path) -> Path:
    resolved = (REPO_ROOT / path).resolve() if not path.is_absolute() else path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"landed file not found: {resolved}")
    try:
        resolved.relative_to(ARCHIVE_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(
            f"path must be under {ARCHIVE_ROOT.relative_to(REPO_ROOT).as_posix()}: {resolved}"
        ) from exc
    return resolved


def post_land_mercouris_close_normalize(
    path: Path,
    *,
    dry_run: bool = False,
) -> PostLandResult:
    """Normalize one landed Mercouris solo capture; apply unless ``dry_run``."""
    landed = _resolve_landed_path(path)
    text = landed.read_text(encoding="utf-8")
    meta, _ = split_frontmatter(text)
    if not is_mercouris_solo_capture(meta, landed):
        return PostLandResult(
            path=landed,
            status="skipped-not-mercouris-solo",
            applied=False,
            flags="",
        )

    changed, _, change = normalize_mercouris(landed, text, apply=not dry_run)
    if change is None or not changed:
        return PostLandResult(path=landed, status="no-op", applied=False, flags="")

    flags: list[str] = []
    if change.close_promo_trimmed:
        flags.append(f"close={change.anchor}")
    if change.wrapper_trimmed:
        flags.append("wrapper")
    if change.chars_removed:
        flags.append(f"-{change.chars_removed}c")
    joined = ", ".join(flags) if flags else "metadata"

    return PostLandResult(
        path=landed,
        status="dry-run" if dry_run else "applied",
        applied=not dry_run,
        flags=joined,
    )


def _format_flags(result: PostLandResult) -> str:
    rel = result.path.relative_to(REPO_ROOT).as_posix()
    if result.status == "skipped-not-mercouris-solo":
        return f"skip {rel} (not Mercouris solo)"
    if result.status == "no-op":
        return f"no-op {rel}"
    mode = "would-change" if result.status == "dry-run" else "applied"
    return f"{mode} {rel} [{result.flags}]"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        type=Path,
        action="append",
        default=[],
        help="Landed capture under source-archive/statecraft/ (repeatable).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview trim only; do not write.")
    args = parser.parse_args()
    if not args.path:
        parser.error("provide at least one --path")

    for raw in args.path:
        try:
            result = post_land_mercouris_close_normalize(raw, dry_run=args.dry_run)
        except (FileNotFoundError, ValueError) as exc:
            print(exc, file=sys.stderr)
            return 1
        print(_format_flags(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
