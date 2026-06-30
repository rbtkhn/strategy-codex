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
FREEMAN_PREDICTIONS_JSON = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.json"
FREEMAN_PUBLIC_MAP = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-public-map.json"
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

PUBLIC_MAP_REQUIRED_FIELDS = (
    "public_title",
    "public_summary",
    "why_it_matters",
    "event_kind",
    "scoring_policy",
)

RECORD_LABELS: dict[str, str] = {
    "correct": "Correct",
    "incorrect": "Incorrect",
    "consistent": "Consistent",
    "shifted": "Shifted",
    "later_reviewed_correct": "Later reviewed as correct",
    "later_reviewed_incorrect": "Later reviewed as incorrect",
    "unscored_trajectory": "Unscored trajectory",
    "diagnostic": "Diagnostic",
}


def extract_quote(note_text: str) -> str:
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
            if stripped.startswith(">"):
                stripped = stripped.lstrip(">").strip()
            if stripped:
                chunks.append(stripped)
    text = " ".join(chunks).strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        text = text[1:-1].strip()
    return text


def shorten_quote(quote: str, max_chars: int = 240) -> str:
    text = quote.strip()
    if len(text) <= max_chars:
        return text
    cut = text[: max_chars - 1].rsplit(" ", 1)[0]
    return (cut or text[: max_chars - 3]).rstrip() + "…"


def require_quote(note_path: Path, quote: str) -> None:
    if not quote.strip():
        raise ValueError(f"missing quote in {note_path}")


def extract_quote_stub(note_text: str) -> str:
    return shorten_quote(extract_quote(note_text))


def load_public_map(path: Path | None = None) -> dict[str, dict[str, Any]]:
    target = path or FREEMAN_PUBLIC_MAP
    if not target.is_file():
        raise FileNotFoundError(f"missing public map: {target.relative_to(REPO_ROOT)}")
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("public map must be a JSON object")
    for event_id in FREEMAN_PILOT_EVENT_ORDER:
        if event_id not in data:
            raise ValueError(f"public map missing event: {event_id}")
        entry = data[event_id]
        if not isinstance(entry, dict):
            raise ValueError(f"public map entry must be object: {event_id}")
        for field in PUBLIC_MAP_REQUIRED_FIELDS:
            if not str(entry.get(field) or "").strip():
                raise ValueError(f"public map {event_id}.{field} is required")
    return data


def select_anchor_quote(
    event_public: dict[str, Any],
    touchpoints: list[dict[str, Any]],
) -> str:
    override = str(event_public.get("anchor_quote_override") or "").strip()
    if override:
        return override
    initial = [t for t in touchpoints if t.get("speech_act") == "initial" and t.get("quote")]
    if initial:
        return str(initial[0]["quote"])
    quoted = [t for t in touchpoints if t.get("quote")]
    if quoted:
        return str(quoted[0]["quote"])
    if touchpoints:
        return str(touchpoints[-1].get("quote") or "")
    return ""


def derive_record(
    *,
    event: dict[str, Any],
    event_public: dict[str, Any],
    touchpoints: list[dict[str, Any]],
    shifts: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
) -> tuple[str, str]:
    override = str(event_public.get("public_record_label") or "").strip()
    if override:
        slug = override.lower().replace(" ", "_")
        return slug, override

    status = str(event.get("status") or "open")
    scoring_policy = str(event_public.get("scoring_policy") or "")
    event_kind = str(event_public.get("event_kind") or "")

    review_acts = {str(r.get("speech_act") or "") for r in reviews}
    if status == "open" and "self_acknowledged_correct" in review_acts:
        return "later_reviewed_correct", RECORD_LABELS["later_reviewed_correct"]
    if status == "open" and "self_acknowledged_incorrect" in review_acts:
        return "later_reviewed_incorrect", RECORD_LABELS["later_reviewed_incorrect"]

    if status == "resolved" and scoring_policy == "yes_no":
        outcome = str(event.get("outcome") or "")
        latest_stance = str(touchpoints[-1]["stance"]) if touchpoints else ""
        if latest_stance and outcome and latest_stance == outcome:
            return "correct", RECORD_LABELS["correct"]
        if latest_stance and outcome:
            return "incorrect", RECORD_LABELS["incorrect"]

    if status == "open" and event_kind == "trajectory":
        return "unscored_trajectory", RECORD_LABELS["unscored_trajectory"]
    if status == "open" and event_kind == "diagnostic":
        return "diagnostic", RECORD_LABELS["diagnostic"]
    if status == "open" and shifts:
        return "shifted", RECORD_LABELS["shifted"]
    if status == "open":
        return "consistent", RECORD_LABELS["consistent"]

    return "consistent", RECORD_LABELS["consistent"]

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
