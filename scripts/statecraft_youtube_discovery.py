#!/usr/bin/env python3
"""Load statecraft YouTube discovery config (replaces cognition-streams-watchlist.json)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DISCOVERY_CONFIG_PATH = REPO_ROOT / "platform" / "config" / "statecraft_youtube_discovery.json"
LEGACY_WATCHLIST_PATH = REPO_ROOT / "docs" / "skill-work" / "work-strategy" / "cognition-streams-watchlist.json"


def resolve_discovery_config_path() -> Path:
    if DISCOVERY_CONFIG_PATH.exists():
        return DISCOVERY_CONFIG_PATH
    return LEGACY_WATCHLIST_PATH


def load_discovery_payload(path: Path | None = None) -> dict[str, Any]:
    config_path = path or resolve_discovery_config_path()
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if payload.get("_deprecated") and not payload.get("channels"):
        raise FileNotFoundError(
            f"{config_path} is deprecated; use {DISCOVERY_CONFIG_PATH.relative_to(REPO_ROOT)}"
        )
    return payload


def load_slug_aliases(payload: dict[str, Any] | None = None) -> dict[str, str]:
    data = payload or load_discovery_payload()
    raw = data.get("slug_aliases") or {}
    return {str(key): str(value) for key, value in raw.items()}


def load_index_slug_canonical(payload: dict[str, Any] | None = None) -> dict[str, str]:
    data = payload or load_discovery_payload()
    raw = data.get("index_slug_canonical") or {}
    return {str(key): str(value) for key, value in raw.items()}


def canonical_channel_index_slug(slug: str, canonical: dict[str, str] | None = None) -> str:
    mapping = canonical or load_index_slug_canonical()
    current = slug
    seen: set[str] = set()
    while current in mapping and current not in seen:
        seen.add(current)
        current = mapping[current]
    return current


def load_canonical_channel_labels(path: Path | None = None) -> dict[str, str]:
    labels: dict[str, str] = {}
    for row in load_discovery_channels(path):
        key = str(row.get("channel_key") or "").strip()
        if not key:
            continue
        label = str(row.get("channel_name") or row.get("show") or "").strip()
        if label:
            labels[key] = label
    return labels


def load_canonical_channel_urls(path: Path | None = None) -> dict[str, str]:
    urls: dict[str, str] = {}
    for row in load_discovery_channels(path):
        key = str(row.get("channel_key") or "").strip()
        url = str(row.get("handle_url") or "").strip()
        if key and url:
            urls[key] = url
    return urls


def load_host_index_canonical(payload: dict[str, Any] | None = None) -> dict[str, str]:
    data = payload or load_discovery_payload()
    mapping: dict[str, str] = {}
    for row in data.get("channels") or []:
        key = str(row.get("channel_key") or "").strip()
        if not key:
            continue
        for field in ("host", "show", "channel_name"):
            value = str(row.get(field) or "").strip()
            if value:
                mapping[value] = key
    raw = data.get("host_index_canonical") or {}
    mapping.update({str(key): str(value) for key, value in raw.items()})
    return mapping


def resolve_host_index_slug(host: str, host_map: dict[str, str] | None = None) -> str | None:
    mapping = host_map if host_map is not None else load_host_index_canonical()
    host = str(host or "").strip()
    if not host:
        return None
    return mapping.get(host)


def load_filename_prefix_index_canonical(payload: dict[str, Any] | None = None) -> list[tuple[str, str]]:
    data = payload or load_discovery_payload()
    entries: list[tuple[str, str]] = []
    for row in data.get("channels") or []:
        key = str(row.get("channel_key") or "").strip()
        file_prefix = str(row.get("file_prefix") or "").strip()
        if key and file_prefix:
            entries.append((f"{file_prefix}-", key))
    raw = data.get("filename_prefix_index_canonical") or []
    for item in raw:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            entries.append((str(item[0]), str(item[1])))
    deduped: dict[str, str] = {}
    for prefix, slug in entries:
        deduped[prefix] = slug
    return sorted(deduped.items(), key=lambda pair: len(pair[0]), reverse=True)


def resolve_filename_prefix_index_slug(
    filename: str,
    prefix_map: list[tuple[str, str]] | None = None,
) -> str | None:
    name = Path(filename).name.casefold()
    for prefix, slug in prefix_map if prefix_map is not None else load_filename_prefix_index_canonical():
        if name.startswith(prefix.casefold()):
            return slug
    return None


def load_discovery_channels(path: Path | None = None) -> list[dict[str, Any]]:
    return list(load_discovery_payload(path).get("channels") or [])


def load_daily_watchlist_keys(path: Path | None = None) -> set[str]:
    keys: set[str] = set()
    for row in load_discovery_channels(path):
        if row.get("daily_watchlist"):
            key = str(row.get("channel_key") or "").strip()
            if key:
                keys.add(key)
    keys.update(load_slug_aliases())
    keys.update(load_slug_aliases().values())
    return keys


def is_daily_watchlist_slug(slug: str, watchlist_keys: set[str] | None = None) -> bool:
    keys = watchlist_keys if watchlist_keys is not None else load_daily_watchlist_keys()
    if slug in keys:
        return True
    mapped = load_slug_aliases().get(slug)
    return bool(mapped and mapped in keys)
