"""Grace-Mar-only legacy path helpers (bot, staging, bootstrap)."""

from __future__ import annotations

from pathlib import Path

from grace_mar.repo_io import REPO_ROOT, resolve_repo_path


def bot_dir(*, prefer_existing: bool = True) -> Path:
    """Deprecated Voice runtime — archive/grace-mar-instance/bot with legacy root fallback."""
    return resolve_repo_path("bot", prefer_existing=prefer_existing)


def grace_mar_instance_dir(*, prefer_existing: bool = True) -> Path:
    return resolve_repo_path("grace-mar-instance", prefer_existing=prefer_existing)


def recursion_gate_staging_dir(*, prefer_existing: bool = True) -> Path:
    return resolve_repo_path("recursion-gate-staging", prefer_existing=prefer_existing)
