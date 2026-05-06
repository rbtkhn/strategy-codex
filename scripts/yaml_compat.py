"""Small compatibility layer for optional PyYAML usage in repo scripts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml as _yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - dependency fallback
    _yaml = None


def has_yaml() -> bool:
    return _yaml is not None


def require_yaml(feature: str) -> None:
    if _yaml is None:
        raise RuntimeError(f"PyYAML is required for {feature}")


def safe_load_text(text: str, *, feature: str) -> Any:
    require_yaml(feature)
    return _yaml.safe_load(text)


def safe_load_path(path: Path, *, feature: str) -> Any:
    return safe_load_text(path.read_text(encoding="utf-8"), feature=feature)


def safe_dump(data: Any, *, feature: str, **kwargs: Any) -> str:
    require_yaml(feature)
    return _yaml.safe_dump(data, **kwargs)
