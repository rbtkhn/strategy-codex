"""Script-layer re-export of Grace-Mar archive paths (Voice archaeology).

SSOT: ``strategy_codex.compat.grace_mar_paths`` under ``platform/src``.
Fork-revive scripts import from here so ``platform/src`` is on ``sys.path``.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_PLATFORM_SRC = _REPO_ROOT / "platform" / "src"
if str(_PLATFORM_SRC) not in sys.path:
    sys.path.insert(0, str(_PLATFORM_SRC))

from strategy_codex.compat.grace_mar_paths import (  # noqa: E402
    BOT_DIR,
    BOOTSTRAP_DIR,
    GRACE_MAR_INSTANCE_DIR,
    RECURSION_GATE_STAGING_DIR,
    bot_dir,
    bootstrap_dir,
    grace_mar_instance_dir,
    recursion_gate_staging_dir,
)

__all__ = [
    "BOT_DIR",
    "BOOTSTRAP_DIR",
    "GRACE_MAR_INSTANCE_DIR",
    "RECURSION_GATE_STAGING_DIR",
    "bot_dir",
    "bootstrap_dir",
    "grace_mar_instance_dir",
    "recursion_gate_staging_dir",
]
