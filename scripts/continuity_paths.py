#!/usr/bin/env python3
"""Resolve canonical continuity-layer root (dual-path: continuity/ or legacy codex/)."""

from __future__ import annotations

from pathlib import Path

CANONICAL_CONTINUITY_DIR = "continuity"
LEGACY_CODEX_DIR = "codex"


def continuity_root(repo_root: Path) -> Path:
    """Return continuity/ when present, else legacy codex/."""
    canonical = repo_root / CANONICAL_CONTINUITY_DIR
    legacy = repo_root / LEGACY_CODEX_DIR
    if canonical.is_dir():
        return canonical
    return legacy


def continuity_subpath(repo_root: Path, *parts: str) -> Path:
    """Path under the resolved continuity root."""
    return continuity_root(repo_root).joinpath(*parts)
