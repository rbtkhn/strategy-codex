#!/usr/bin/env python3
"""Post-land hook: Dialogue Works opening scaffold normalize for one statecraft capture.

Usage:
    python scripts/post_land_dialogue_works_opening_normalize.py --path <landed-file>
    python scripts/post_land_dialogue_works_opening_normalize.py --path <landed-file> --dry-run
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

from normalize_dialogue_works_opening_scaffold import (  # noqa: E402
    ARCHIVE_ROOT,
    is_dialogue_works_capture,
    normalize_text,
    split_frontmatter,
)

@dataclass(frozen=True)
class PostLandResult:
    path: Path
    status: str
    applied: bool
    flags: str
    opening_tier: str

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

def post_land_dialogue_works_opening_normalize(
    path: Path,
    *,
    dry_run: bool = False,
    tag_only: bool = False,
) -> PostLandResult:
    landed = _resolve_landed_path(path)
    text = landed.read_text(encoding="utf-8")
    meta, _ = split_frontmatter(text)
    if not is_dialogue_works_capture(meta, landed):
        return PostLandResult(
            path=landed,
            status="skipped-not-dialogue-works",
            applied=False,
            flags="",
            opening_tier=str(meta.get("opening_tier") or ""),
        )

    changed, new_text, file_change = normalize_text(landed, text, tag_only=tag_only)
    if file_change is None or not changed:
        tier = str(meta.get("opening_tier") or (file_change.opening_tier if file_change else ""))
        return PostLandResult(
            path=landed,
            status="no-op",
            applied=False,
            flags="",
            opening_tier=tier,
        )

    flags: list[str] = []
    if file_change.mid_substack_trimmed:
        flags.append("mid_substack")
    if file_change.book_interrupt_trimmed:
        flags.append("book_interrupt")
    if file_change.close_substack_trimmed:
        flags.append("close_substack")
    if file_change.leading_noise_trimmed:
        flags.append("leading_noise")
    if file_change.paragraphs_removed:
        flags.append(f"-{file_change.paragraphs_removed}p")
    joined = ", ".join(flags) if flags else "metadata"

    if not dry_run:
        landed.write_text(new_text, encoding="utf-8")

    return PostLandResult(
        path=landed,
        status="dry-run" if dry_run else "applied",
        applied=not dry_run,
        flags=joined,
        opening_tier=file_change.opening_tier,
    )

def _format_flags(result: PostLandResult) -> str:
    rel = result.path.relative_to(REPO_ROOT).as_posix()
    if result.status == "skipped-not-dialogue-works":
        return f"skip {rel} (not Dialogue Works / Alkhorshid)"
    if result.status == "no-op":
        tier = f" tier={result.opening_tier}" if result.opening_tier else ""
        return f"no-op {rel}{tier}"
    mode = "would-change" if result.status == "dry-run" else "applied"
    return f"{mode} {rel} [{result.flags}] tier={result.opening_tier}"

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--tag-only", action="store_true")
    args = parser.parse_args()

    try:
        result = post_land_dialogue_works_opening_normalize(
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
