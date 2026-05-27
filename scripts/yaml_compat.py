"""Small compatibility layer for optional PyYAML usage in repo scripts."""

from __future__ import annotations

import re
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


_SIMPLE_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s+(.*))?$")


def _coerce_scalar(value: str) -> Any:
    text = value.strip()
    if not text:
        return ""
    if text == "[]":
        return []
    if text == "{}":
        return {}
    if text[0] == text[-1] and text[0] in {"'", '"'}:
        return text[1:-1]
    lowered = text.casefold()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None
    if re.fullmatch(r"-?\d+", text):
        try:
            return int(text)
        except ValueError:
            return text
    return text


def _simple_yaml_fallback(text: str, *, feature: str) -> Any:
    """Parse the narrow frontmatter shape used by repo tests when PyYAML is absent."""
    data: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[Any] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current_key is None or current_list is None:
                raise RuntimeError(f"PyYAML is required for {feature}")
            current_list.append(_coerce_scalar(stripped[2:]))
            continue
        match = _SIMPLE_KEY_RE.match(stripped)
        if not match:
            raise RuntimeError(f"PyYAML is required for {feature}")
        key, value = match.groups()
        if value is None or not value.strip():
            current_key = key
            current_list = []
            data[key] = current_list
            continue
        current_key = None
        current_list = None
        data[key] = _coerce_scalar(value)
    return data


def safe_load_text(text: str, *, feature: str) -> Any:
    if _yaml is not None:
        return _yaml.safe_load(text)
    return _simple_yaml_fallback(text, feature=feature)


def safe_load_path(path: Path, *, feature: str) -> Any:
    return safe_load_text(path.read_text(encoding="utf-8"), feature=feature)


def safe_dump(data: Any, *, feature: str, **kwargs: Any) -> str:
    require_yaml(feature)
    return _yaml.safe_dump(data, **kwargs)
