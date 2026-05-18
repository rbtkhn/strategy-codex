#!/usr/bin/env python3
"""Shared repository path helpers for strategy-codex WORK tooling."""

from __future__ import annotations

from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def codex_root() -> Path:
    return REPO_ROOT / "codex"


def academy_root() -> Path:
    return codex_root() / "academy"


def speakers_root() -> Path:
    return codex_root() / "speakers"


def year_root(year: int | None = None) -> Path:
    selected_year = year if year is not None else date.today().year
    return codex_root() / str(selected_year)
