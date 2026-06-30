#!/usr/bin/env python3
"""Post-land hook: cross-family caption/paste wrapper normalize (run before family hooks).

Usage:
    python scripts/post_land_caption_wrapper_normalize.py --path <landed-file>
    python scripts/post_land_caption_wrapper_normalize.py --path <landed-file> --dry-run
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

from normalize_caption_wrapper_residue import (  # noqa: E402
    ARCHIVE_ROOT,
    is_transcript_archive_capture,
    normalize_text,
    split_frontmatter,
)

@dataclass(frozen=True)
class PostLandResult:
    path: Path
    status: str
    applied: bool
    flags: str
    wrapper_tier: str

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

def post_land_caption_wrapper_normalize(
    path: Path,
    *,
    dry_run: bool = False,
    tag_only: bool = False,
) -> PostLandResult:
    landed = _resolve_landed_path(path)
    text = landed.read_text(encoding="utf-8")
    meta, _ = split_frontmatter(text)
    if not is_transcript_archive_capture(meta, landed):
        return PostLandResult(
            path=landed,
            status="skipped-not-transcript",
            applied=False,
            flags="",
            wrapper_tier="",
        )

    changed, new_text, file_change = normalize_text(landed, text, tag_only=tag_only)
    if file_change is None or not changed:
        tier = str(meta.get("transcript_wrapper_tier") or (file_change.wrapper_tier if file_change else "clean"))
        return PostLandResult(
            path=landed,
            status="no-op",
            applied=False,
            flags="",
            wrapper_tier=tier,
        )

    flags: list[str] = []
    if file_change.entities_decoded:
        flags.append("entities")
    if file_change.caption_header_stripped:
        flags.append("caption_header")
    if file_change.transcripts_prefix_stripped:
        flags.append("transcripts_prefix")
    if file_change.leading_music_stripped:
        flags.append("leading_music")
    joined = ", ".join(flags) if flags else "metadata"

    if not dry_run:
        landed.write_text(new_text, encoding="utf-8")

    return PostLandResult(
        path=landed,
        status="dry-run" if dry_run else "applied",
        applied=not dry_run,
        flags=joined,
        wrapper_tier=file_change.wrapper_tier,
    )

def _format_flags(result: PostLandResult) -> str:
    rel = result.path.relative_to(REPO_ROOT).as_posix()
    if result.status == "skipped-not-transcript":
        return f"skip {rel} (not transcript archive capture)"
    if result.status == "no-op":
        tier = f" tier={result.wrapper_tier}" if result.wrapper_tier else ""
        return f"no-op {rel}{tier}"
    mode = "would-change" if result.status == "dry-run" else "applied"
    return f"{mode} {rel} [{result.flags}] tier={result.wrapper_tier}"

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--tag-only", action="store_true")
    args = parser.parse_args()

    try:
        result = post_land_caption_wrapper_normalize(
            args.path,
            dry_run=args.dry_run,
            tag_only=args.tag_only,
        )
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

    print(_format_flags(result))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
