#!/usr/bin/env python3
"""Read strategy-codex product config (WORK only; not Record)."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _REPO_ROOT / "config" / "strategy_codex.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        from yaml_compat import safe_load_path
    except ImportError:
        from scripts.yaml_compat import safe_load_path  # type: ignore
    data = safe_load_path(path, feature="strategy_codex_config")
    return data if isinstance(data, dict) else {}


@lru_cache(maxsize=1)
def load_strategy_codex_config() -> dict[str, Any]:
    cfg = _load_yaml(_CONFIG_PATH)
    env = os.getenv("STRATEGY_CODEX_RECORD_FROZEN", "").strip().lower()
    if env in {"1", "true", "yes"}:
        cfg = {**cfg, "record_frozen": True}
    elif env in {"0", "false", "no"}:
        cfg = {**cfg, "record_frozen": False}
    return cfg


def record_frozen() -> bool:
    return bool(load_strategy_codex_config().get("record_frozen", False))


def default_operator_user() -> str:
    cfg = load_strategy_codex_config()
    return str(cfg.get("default_operator_user") or "strategy-codex").strip() or "strategy-codex"


def fork_revive_tokens() -> list[str]:
    raw = load_strategy_codex_config().get("fork_revive_tokens") or []
    return [str(x).strip() for x in raw if str(x).strip()]


def interpretive_machine_health_hint() -> str:
    return (
        "Interpretive machine: refresh archive indices if stale; "
        "run validate_statecraft_daily_synthesis; ship receipt before push."
    )
