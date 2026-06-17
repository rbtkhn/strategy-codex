#!/usr/bin/env python3
"""Shared statecraft capture scaffold router for post-land and dream catch-up."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from normalize_breaking_points_scaffold import (  # noqa: E402
    is_breaking_points_capture,
    normalize_breaking_points,
)
from normalize_davis_deep_dive_scaffold import is_davis_capture, normalize_davis  # noqa: E402
from normalize_dialogue_works_opening_scaffold import is_dialogue_works_capture  # noqa: E402
from normalize_mercouris_close_scaffold import (  # noqa: E402
    is_mercouris_solo_capture,
    normalize_mercouris,
)
from normalize_napolitano_opening_scaffold import (  # noqa: E402
    is_napolitano_capture,
    split_frontmatter,
)
from normalize_nawfal_opening_banter import is_nawfal_hosted  # noqa: E402
from normalize_redacted_scaffold import is_redacted_capture, normalize_redacted  # noqa: E402
from post_land_caption_wrapper_normalize import (  # noqa: E402
    PostLandResult as CaptionResult,
    post_land_caption_wrapper_normalize,
)
from post_land_dialogue_works_opening_normalize import (  # noqa: E402
    PostLandResult as DwResult,
    post_land_dialogue_works_opening_normalize,
)
from post_land_mercouris_close_normalize import (  # noqa: E402
    PostLandResult as MercourisResult,
    post_land_mercouris_close_normalize,
)
from post_land_napolitano_opening_normalize import (  # noqa: E402
    PostLandResult as NapResult,
    post_land_napolitano_opening_normalize,
)
from post_land_nawfal_opening_normalize import (  # noqa: E402
    PostLandResult as NawfalResult,
    post_land_nawfal_opening_normalize,
)


@dataclass
class CaptureScaffoldResult:
    path: Path
    caption: CaptionResult | None = None
    family: str | None = None
    family_status: str = "skipped"
    family_flags: str = ""
    changed: bool = False
    lines: list[str] = field(default_factory=list)


def _format_caption(result: CaptionResult) -> str:
    rel = result.path.relative_to(REPO_ROOT).as_posix()
    if result.status == "skipped-not-transcript":
        return f"skip {rel} (not transcript archive capture)"
    if result.status == "no-op":
        tier = f" tier={result.wrapper_tier}" if result.wrapper_tier else ""
        return f"no-op {rel}{tier}"
    mode = "would-change" if result.status == "dry-run" else "applied"
    return f"{mode} {rel} [{result.flags}] tier={result.wrapper_tier}"


def _format_post_land(result: NapResult | NawfalResult | DwResult | MercourisResult, *, label: str) -> str:
    rel = result.path.relative_to(REPO_ROOT).as_posix()
    if result.status.startswith("skipped"):
        return f"skip {rel} ({label})"
    if result.status == "no-op":
        return f"no-op {rel}"
    mode = "would-change" if result.status == "dry-run" else "applied"
    return f"{mode} {rel} [{result.flags}]"


def _format_inline(path: Path, family: str, *, changed: bool, dry_run: bool, flags: str) -> str:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if not changed:
        return f"no-op {rel} ({family})"
    mode = "would-change" if dry_run else "applied"
    return f"{mode} {rel} [{flags}] ({family})"


def apply_statecraft_capture_scaffold(
    path: Path,
    *,
    dry_run: bool = False,
    force_mercouris_close: bool = False,
) -> CaptureScaffoldResult:
    """Caption wrapper + family scaffold normalize for one capture."""
    out = CaptureScaffoldResult(path=path.resolve())
    caption = post_land_caption_wrapper_normalize(path, dry_run=dry_run)
    out.caption = caption
    out.lines.append(_format_caption(caption))
    if caption.status == "dry-run" or (caption.status == "applied" and not dry_run):
        out.changed = True

    text = path.read_text(encoding="utf-8")
    meta, _ = split_frontmatter(text)

    if is_napolitano_capture(meta, path):
        result = post_land_napolitano_opening_normalize(path, dry_run=dry_run)
        out.family = "napolitano"
        out.family_status = result.status
        out.family_flags = result.flags
        out.lines.append(_format_post_land(result, label="napolitano"))
        if result.status in ("dry-run", "applied"):
            out.changed = True
        return out

    if is_nawfal_hosted(meta, path):
        result = post_land_nawfal_opening_normalize(path, dry_run=dry_run)
        out.family = "nawfal"
        out.family_status = result.status
        out.family_flags = result.flags
        out.lines.append(_format_post_land(result, label="nawfal"))
        if result.status in ("dry-run", "applied"):
            out.changed = True
        return out

    if is_dialogue_works_capture(meta, path):
        result = post_land_dialogue_works_opening_normalize(path, dry_run=dry_run)
        out.family = "dialogue-works"
        out.family_status = result.status
        out.family_flags = result.flags
        out.lines.append(_format_post_land(result, label="dialogue-works"))
        if result.status in ("dry-run", "applied"):
            out.changed = True
        return out

    if is_mercouris_solo_capture(meta, path):
        if force_mercouris_close and dry_run:
            changed, _, change = normalize_mercouris(
                path, text, apply=False, force_close=True
            )
            out.family = "mercouris-solo"
            if changed and change:
                flags = f"force-close,{change.anchor},-{change.chars_removed}c"
                out.family_status = "dry-run"
                out.family_flags = flags
                out.lines.append(_format_inline(path, "mercouris-solo", changed=True, dry_run=True, flags=flags))
                out.changed = True
            else:
                result = post_land_mercouris_close_normalize(path, dry_run=True)
                out.family_status = result.status
                out.family_flags = result.flags
                out.lines.append(_format_post_land(result, label="mercouris-solo"))
            return out
        if force_mercouris_close and not dry_run:
            changed, _, change = normalize_mercouris(
                path, path.read_text(encoding="utf-8"), apply=True, force_close=True
            )
            out.family = "mercouris-solo"
            if changed and change:
                flags = f"force-close,{change.anchor},-{change.chars_removed}c"
                out.family_status = "applied"
                out.family_flags = flags
                out.lines.append(_format_inline(path, "mercouris-solo", changed=True, dry_run=False, flags=flags))
                out.changed = True
            else:
                result = post_land_mercouris_close_normalize(path, dry_run=False)
                out.family_status = result.status
                out.family_flags = result.flags
                out.lines.append(_format_post_land(result, label="mercouris-solo"))
                if result.status == "applied":
                    out.changed = True
            return out
        result = post_land_mercouris_close_normalize(path, dry_run=dry_run)
        out.family = "mercouris-solo"
        out.family_status = result.status
        out.family_flags = result.flags
        out.lines.append(_format_post_land(result, label="mercouris-solo"))
        if result.status in ("dry-run", "applied"):
            out.changed = True
        return out

    if is_davis_capture(meta, path):
        changed, _, change = normalize_davis(path, text, apply=not dry_run)
        out.family = "davis-deep-dive"
        if changed and change:
            flags = change.anchor or "close"
            if change.chars_removed:
                flags += f",-{change.chars_removed}c"
            out.family_status = "dry-run" if dry_run else "applied"
            out.family_flags = flags
            out.lines.append(_format_inline(path, "davis-deep-dive", changed=True, dry_run=dry_run, flags=flags))
            out.changed = True
        else:
            out.family_status = "no-op"
            out.lines.append(_format_inline(path, "davis-deep-dive", changed=False, dry_run=dry_run, flags=""))
        return out

    if is_redacted_capture(meta, path):
        changed, _, change = normalize_redacted(path, text, apply=not dry_run)
        out.family = "redacted"
        if changed and change:
            flags = change.anchor or "close"
            if change.chars_removed:
                flags += f",-{change.chars_removed}c"
            out.family_status = "dry-run" if dry_run else "applied"
            out.family_flags = flags
            out.lines.append(_format_inline(path, "redacted", changed=True, dry_run=dry_run, flags=flags))
            out.changed = True
        else:
            out.family_status = "no-op"
            out.lines.append(_format_inline(path, "redacted", changed=False, dry_run=dry_run, flags=""))
        return out

    if is_breaking_points_capture(meta, path):
        changed, _, change = normalize_breaking_points(path, text, apply=not dry_run)
        out.family = "breaking-points"
        if changed and change:
            flags = change.anchor or "close"
            if change.chars_removed:
                flags += f",-{change.chars_removed}c"
            out.family_status = "dry-run" if dry_run else "applied"
            out.family_flags = flags
            out.lines.append(_format_inline(path, "breaking-points", changed=True, dry_run=dry_run, flags=flags))
            out.changed = True
        else:
            out.family_status = "no-op"
            out.lines.append(_format_inline(path, "breaking-points", changed=False, dry_run=dry_run, flags=""))
        return out

    rel = path.relative_to(REPO_ROOT).as_posix()
    out.lines.append(f"skip-family {rel} (no routed family match)")
    return out
