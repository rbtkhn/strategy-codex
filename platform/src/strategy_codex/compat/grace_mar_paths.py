"""
Grace-Mar archive compatibility path helpers.

This module isolates frozen-fork / Voice archaeology path behavior away from
the active strategy-codex repo resolver (scripts/repo_io.py).
"""

from __future__ import annotations

from pathlib import Path

# platform/src/strategy_codex/compat/grace_mar_paths.py -> repo root
_REPO_ROOT = Path(__file__).resolve().parents[4]

GRACE_MAR_INSTANCE_DIR = _REPO_ROOT / "archive" / "grace-mar-instance"
BOT_DIR = GRACE_MAR_INSTANCE_DIR / "bot"
BOOTSTRAP_DIR = GRACE_MAR_INSTANCE_DIR / "bootstrap"
RECURSION_GATE_STAGING_DIR = GRACE_MAR_INSTANCE_DIR / "recursion-gate-staging"


def bot_dir() -> Path:
    """Canonical archive/grace-mar-instance/bot (Voice archaeology)."""
    return BOT_DIR


def bootstrap_dir() -> Path:
    """Canonical archive/grace-mar-instance/bootstrap (fork bootstrap)."""
    return BOOTSTRAP_DIR


def recursion_gate_staging_dir() -> Path:
    """Canonical archive/grace-mar-instance/recursion-gate-staging."""
    return RECURSION_GATE_STAGING_DIR


def grace_mar_instance_dir() -> Path:
    """Canonical archive/grace-mar-instance Record bundle root."""
    return GRACE_MAR_INSTANCE_DIR
