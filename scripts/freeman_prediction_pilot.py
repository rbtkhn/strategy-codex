"""Freeman prediction pilot — shared constants and helpers."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
THESIS_MAP_PATH = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-thesis-map.json"
FREEMAN_PREDICTIONS_OUT = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.md"
CRAWL_ARTIFACT = REPO_ROOT / "runtime" / "artifacts" / "freeman-prediction-crawl.json"
FREEMAN_SPEAKER = "freeman"

FREEMAN_PILOT_EVENT_ORDER: tuple[str, ...] = (
    "israel_self_destruction_trajectory",
    "ukraine_escalation_russian_capitulation",
    "gaza_hostage_deal_jan_2025",
    "gaza_ceasefire_holds_2025",
    "us_israel_iran_war_preparation_2025",
    "iran_great_power_direct_war_entry",
    "china_tariff_capitulation_2025",
)

SPEECH_ACTS = frozenset(
    {
        "initial",
        "restated",
        "iterated",
        "self_acknowledged_correct",
        "self_acknowledged_incorrect",
        "outcome_commentary",
    }
)
REVIEW_SPEECH_ACTS = frozenset(
    {
        "self_acknowledged_correct",
        "self_acknowledged_incorrect",
        "outcome_commentary",
    }
)

ARCHIVE_LINK_RE = re.compile(
    r"source-archive/statecraft/\d{4}-\d{2}-\d{2}/source-[^\s)\]]+\.md"
)

JAN_21_CAPTURE = (
    "source-archive/statecraft/2025-01-21/"
    "source-judging-freedom-amb-chas-freeman-a-ceasefire-or-a-pause-2025-01-21.md"
)

def load_thesis_map(path: Path | None = None) -> dict[str, dict[str, Any]]:
    target = path or THESIS_MAP_PATH
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("thesis map must be a JSON object")
    return data

def pilot_event_sort_key(event_id: str) -> tuple[int, str]:
    try:
        return (FREEMAN_PILOT_EVENT_ORDER.index(event_id), event_id)
    except ValueError:
        return (999, event_id)

def match_text(haystack: str, pattern: str) -> bool:
    return pattern.casefold() in haystack.casefold()

def patterns_match(text: str, patterns: list[str]) -> bool:
    return any(match_text(text, pat) for pat in patterns)

def parse_register_capture_paths(register_path: Path) -> list[str]:
    if not register_path.is_file():
        return []
    text = register_path.read_text(encoding="utf-8", errors="replace")
    return sorted(set(ARCHIVE_LINK_RE.findall(text)))

def extract_quote_stub(note_text: str) -> str:
    lines = note_text.splitlines()
    in_quote = False
    chunks: list[str] = []
    for line in lines:
        if line.strip().lower().startswith("## quote"):
            in_quote = True
            continue
        if in_quote:
            if line.startswith("## "):
                break
            stripped = line.strip()
            if stripped:
                chunks.append(stripped)
    return " ".join(chunks)[:240] if chunks else ""

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
