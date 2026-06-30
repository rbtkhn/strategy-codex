"""Voice prediction record — shared constants, registry, and helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

FREEMAN_PILOT_EVENT_ORDER: tuple[str, ...] = (
    "israel_self_destruction_trajectory",
    "ukraine_escalation_russian_capitulation",
    "gaza_hostage_deal_jan_2025",
    "gaza_ceasefire_holds_2025",
    "us_israel_iran_war_preparation_2025",
    "iran_great_power_direct_war_entry",
    "china_tariff_capitulation_2025",
)

FREEMAN_WIRE_STUBS: dict[str, str] = {
    "israel_self_destruction_trajectory": (
        "statecraft/notes/wire/prediction-resolution-israel-self-destruction-trajectory.md"
    ),
    "gaza_ceasefire_holds_2025": (
        "statecraft/notes/wire/prediction-resolution-gaza-ceasefire-holds-2025.md"
    ),
    "us_israel_iran_war_preparation_2025": (
        "statecraft/notes/wire/prediction-resolution-us-israel-iran-war-preparation-2025.md"
    ),
    "iran_great_power_direct_war_entry": (
        "statecraft/notes/wire/prediction-resolution-iran-great-power-direct-war-entry.md"
    ),
    "china_tariff_capitulation_2025": (
        "statecraft/notes/wire/prediction-resolution-china-tariff-capitulation-2025.md"
    ),
    "gaza_hostage_deal_jan_2025": (
        "statecraft/notes/wire/prediction-resolution-gaza-hostage-deal-jan-2025.md"
    ),
    "ukraine_escalation_russian_capitulation": (
        "statecraft/notes/wire/prediction-resolution-ukraine-escalation-russian-capitulation.md"
    ),
}


@dataclass(frozen=True)
class VoiceConfig:
    speaker: str
    pilot_event_order: tuple[str, ...]
    public_map_path: Path
    capture_map_path: Path
    predictions_json_path: Path
    predictions_md_path: Path
    thesis_map_path: Path
    crawl_artifact_path: Path
    schema: str
    page_title: str
    speaker_display_name: str
    citation_prefix: str
    default_channel: str
    builder_script: str
    checker_script: str
    bootstrap_script: str
    wire_stubs: dict[str, str]
    shared_capture_suffix: str | None = None
    min_events_for_shared_capture: int = 0


def _voice_data_paths(speaker: str) -> tuple[Path, Path, Path, Path, Path, Path]:
    data = REPO_ROOT / "statecraft" / "data"
    voice = REPO_ROOT / "statecraft" / "voices" / speaker
    return (
        data / f"{speaker}-prediction-public-map.json",
        data / f"{speaker}-prediction-capture-map.json",
        voice / f"{speaker}-predictions.json",
        voice / f"{speaker}-predictions.md",
        data / f"{speaker}-prediction-thesis-map.json",
        REPO_ROOT / "runtime" / "artifacts" / f"{speaker}-prediction-crawl.json",
    )


def _freeman_config() -> VoiceConfig:
    public_map, capture_map, json_out, md_out, thesis_map, crawl = _voice_data_paths("freeman")
    return VoiceConfig(
        speaker="freeman",
        pilot_event_order=FREEMAN_PILOT_EVENT_ORDER,
        public_map_path=public_map,
        capture_map_path=capture_map,
        predictions_json_path=json_out,
        predictions_md_path=md_out,
        thesis_map_path=thesis_map,
        crawl_artifact_path=crawl,
        schema="freeman-predictions-v2",
        page_title="# Chas Freeman Prediction Record",
        speaker_display_name="Chas Freeman",
        citation_prefix="— Chas Freeman,",
        default_channel="Judging Freedom",
        builder_script="scripts/build_voice_predictions.py --speaker freeman",
        checker_script="scripts/check_voice_predictions.py --speaker freeman",
        bootstrap_script="scripts/bootstrap_voice_capture_map.py --speaker freeman --check",
        wire_stubs=FREEMAN_WIRE_STUBS,
        shared_capture_suffix=(
            "source-judging-freedom-amb-chas-freeman-a-ceasefire-or-a-pause-2025-01-21.md"
        ),
        min_events_for_shared_capture=2,
    )


VOICE_REGISTRY: dict[str, VoiceConfig] = {
    "freeman": _freeman_config(),
}


def list_voice_speakers() -> list[str]:
    return sorted(VOICE_REGISTRY.keys())


def get_voice_config(speaker: str) -> VoiceConfig:
    key = str(speaker or "").strip().lower()
    if key not in VOICE_REGISTRY:
        known = ", ".join(list_voice_speakers()) or "(none)"
        raise ValueError(f"unknown speaker {speaker!r}; known: {known}")
    return VOICE_REGISTRY[key]


# Freeman compatibility aliases (legacy imports)
FREEMAN_SPEAKER = "freeman"
THESIS_MAP_PATH = VOICE_REGISTRY["freeman"].thesis_map_path
FREEMAN_PREDICTIONS_OUT = VOICE_REGISTRY["freeman"].predictions_md_path
FREEMAN_PREDICTIONS_JSON = VOICE_REGISTRY["freeman"].predictions_json_path
FREEMAN_PUBLIC_MAP = VOICE_REGISTRY["freeman"].public_map_path
FREEMAN_CAPTURE_MAP = VOICE_REGISTRY["freeman"].capture_map_path
CRAWL_ARTIFACT = VOICE_REGISTRY["freeman"].crawl_artifact_path

YOUTUBE_URL_RE = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)"
)
CAPTURE_MAP_REQUIRED = ("event_id", "capture", "stance", "speech_act", "public_excerpt")

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

def pilot_event_sort_key(
    event_id: str,
    event_order: tuple[str, ...] | None = None,
) -> tuple[int, str]:
    order = event_order or FREEMAN_PILOT_EVENT_ORDER
    try:
        return (order.index(event_id), event_id)
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
    "consistent": "Open — consistent",
    "shifted": "Open — shifted",
    "later_reviewed_correct": "Open — later reviewed as correct",
    "later_reviewed_incorrect": "Open — later reviewed as incorrect",
    "unscored_trajectory": "Open — trajectory",
    "diagnostic": "Open — diagnostic",
}

STANCE_VALUES = frozenset({"yes", "no", "uncertain"})

MIN_ANCHOR_WORDS = 40
MIN_APPEARANCE_WORDS = 30
MAX_PUBLIC_EXCERPT_WORDS = 80
ALLOWED_PUBLIC_EXCEPTIONS = frozenset({"short_decisive_sentence"})
BAD_EXCERPT_STARTS = (
    "if this ",
    "if that ",
    "this ",
    "that ",
    "it ",
    "they ",
    "he ",
)


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


def load_public_map(
    path: Path | None = None,
    *,
    event_order: tuple[str, ...] | None = None,
) -> dict[str, dict[str, Any]]:
    target = path or FREEMAN_PUBLIC_MAP
    order = event_order or FREEMAN_PILOT_EVENT_ORDER
    if not target.is_file():
        raise FileNotFoundError(f"missing public map: {target.relative_to(REPO_ROOT)}")
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("public map must be a JSON object")
    for event_id in order:
        if event_id not in data:
            raise ValueError(f"public map missing event: {event_id}")
        entry = data[event_id]
        if not isinstance(entry, dict):
            raise ValueError(f"public map entry must be object: {event_id}")
        for field in PUBLIC_MAP_REQUIRED_FIELDS:
            if not str(entry.get(field) or "").strip():
                raise ValueError(f"public map {event_id}.{field} is required")
        terms = entry.get("prediction_object_terms")
        if not isinstance(terms, list) or not terms:
            raise ValueError(f"public map {event_id}.prediction_object_terms is required")
        if not all(str(t).strip() for t in terms):
            raise ValueError(f"public map {event_id}.prediction_object_terms must be non-empty strings")
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


def normalize_for_match(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2014", "-").replace("\u2013", "-")
    text = re.sub(r"[^\w\s'-]", " ", text)
    text = re.sub(r"\s+", " ", text.strip().lower())
    return text


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def is_complete_sentence(text: str, *, capture_body: str | None = None) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if word_count(stripped) < 4:
        return False
    if stripped[-1] in ".!?":
        return True
    if capture_body and excerpt_in_capture(stripped, capture_body):
        return True
    return False


def is_title_like(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    if stripped.endswith("?") and word_count(stripped) <= 15:
        return True
    if stripped.startswith(("Will ", "Is ", "Does ", "Were ", "Would ")):
        return True
    if word_count(stripped) <= 6 and stripped[0].isupper() and stripped[-1] not in ".!?":
        return True
    if " w/" in stripped or " w/Chas" in stripped:
        return True
    if stripped.startswith("AMB.") or stripped.startswith("Hostage ceasefire"):
        return True
    return False


def extract_youtube_url_from_capture_text(text: str) -> str | None:
    m = YOUTUBE_URL_RE.search(text)
    if not m:
        return None
    return f"https://www.youtube.com/watch?v={m.group(1)}"


def parse_capture_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_block, body = parts[1], parts[2]
    fm: dict[str, str] = {}
    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        val = val.strip().strip('"').strip("'")
        fm[key.strip()] = val
    return fm, body


def source_citation(
    capture_path: Path,
    *,
    default_channel: str = "Judging Freedom",
) -> dict[str, str]:
    text = capture_path.read_text(encoding="utf-8")
    fm, _ = parse_capture_frontmatter(text)
    youtube_url = ""
    for key in ("source_url", "url", "canonical_url"):
        val = fm.get(key, "")
        if val and YOUTUBE_URL_RE.search(val):
            youtube_url = extract_youtube_url_from_capture_text(val) or val
            break
    if not youtube_url:
        youtube_url = extract_youtube_url_from_capture_text(text[:8000]) or ""
    title = fm.get("title") or fm.get("episode_title") or capture_path.stem.replace("source-", "")
    channel = fm.get("channel") or fm.get("source_channel") or default_channel
    pub_date = fm.get("pub_date") or fm.get("source_date") or ""
    if not pub_date:
        m = re.search(r"statecraft[/\\](\d{4}-\d{2}-\d{2})[/\\]", str(capture_path).replace("\\", "/"))
        if m:
            pub_date = m.group(1)
    return {
        "capture": str(capture_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "title": title,
        "channel": channel,
        "pub_date": pub_date,
        "youtube_url": youtube_url,
    }


def excerpt_in_capture(excerpt: str, capture_body: str) -> bool:
    if not excerpt.strip():
        return False
    norm_excerpt = normalize_for_match(excerpt)
    norm_body = normalize_for_match(capture_body)
    return norm_excerpt in norm_body


def excerpt_segments_in_capture(excerpt: str, capture_body: str) -> bool:
    parts = [p.strip() for p in re.split(r"\s*\|\|\|\s*", excerpt) if p.strip()]
    if len(parts) <= 1:
        return excerpt_in_capture(excerpt, capture_body)
    return all(excerpt_in_capture(part, capture_body) for part in parts)


def _find_word_start(body_words: list[str], seed_words: list[str]) -> int | None:
    for n in range(min(12, len(seed_words)), 5, -1):
        prefix = seed_words[:n]
        plen = len(prefix)
        hits = [
            i
            for i in range(len(body_words) - plen + 1)
            if body_words[i : i + plen] == prefix
        ]
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            best_i: int | None = None
            best_m = 0
            for hit in hits:
                matched = _match_word_run(body_words, hit, seed_words)
                if matched > best_m:
                    best_i, best_m = hit, matched
            if best_i is not None and best_m >= min(n, 6):
                return best_i
    return None


def _match_word_run(body_words: list[str], start_i: int, seed_words: list[str]) -> int:
    matched = 0
    for j, seed_word in enumerate(seed_words):
        if start_i + j >= len(body_words):
            break
        if body_words[start_i + j] == seed_word:
            matched = j + 1
        else:
            break
    return matched


def extract_original_word_span(body: str, words: list[str]) -> str:
    if not words:
        return ""
    pattern = r"(?is)" + r"(?:[\W_]+)".join(re.escape(word) for word in words)
    match = re.search(pattern, body)
    if match:
        return match.group(0).strip()
    return " ".join(words)


def align_excerpt_to_capture(
    excerpt: str,
    capture_body: str,
    *,
    min_words: int = 0,
    max_words: int = MAX_PUBLIC_EXCERPT_WORDS,
) -> str:
    stripped = excerpt.strip()
    if excerpt_in_capture(stripped, capture_body):
        return stripped

    trimmed = stripped
    while trimmed and trimmed[-1] in ".!?" and not excerpt_in_capture(trimmed, capture_body):
        trimmed = trimmed[:-1].rstrip()
    if trimmed and excerpt_in_capture(trimmed, capture_body):
        return trimmed

    seed_words = normalize_for_match(stripped).split()
    body_words = normalize_for_match(capture_body).split()
    start_i = _find_word_start(body_words, seed_words)
    if start_i is None:
        return stripped

    matched = _match_word_run(body_words, start_i, seed_words)
    if matched < 8:
        return stripped

    end_i = start_i + matched
    while end_i < len(body_words) and word_count(" ".join(body_words[start_i:end_i])) < min_words:
        next_end = end_i + 1
        if word_count(" ".join(body_words[start_i:next_end])) > max_words:
            break
        end_i = next_end

    return extract_original_word_span(
        capture_body,
        body_words[start_i:end_i],
    ).strip()


def contains_prediction_object(excerpt: str, terms: list[str]) -> bool:
    if not terms:
        return False
    normalized = normalize_for_match(excerpt)
    return any(normalize_for_match(term) in normalized for term in terms if str(term).strip())


def _bad_excerpt_start(excerpt: str) -> bool:
    lowered = normalize_for_match(excerpt)
    return any(lowered.startswith(start) for start in BAD_EXCERPT_STARTS)


def resolve_prediction_object_terms(
    row: dict[str, Any],
    public_event: dict[str, Any],
) -> list[str]:
    row_terms = row.get("prediction_object_terms")
    if isinstance(row_terms, list) and row_terms:
        return [str(t) for t in row_terms if str(t).strip()]
    event_terms = public_event.get("prediction_object_terms") or []
    return [str(t) for t in event_terms if str(t).strip()]


def validate_excerpt_quality(
    *,
    event_id: str,
    excerpt: str,
    min_words: int,
    exception: str | None,
    context_note: str | None,
    object_terms: list[str],
    is_anchor: bool = False,
    capture_body: str | None = None,
) -> list[str]:
    errors: list[str] = []
    text = excerpt.strip()
    if not text:
        errors.append(f"{event_id}: public_excerpt is empty")
        return errors

    if exception and exception not in ALLOWED_PUBLIC_EXCEPTIONS:
        errors.append(f"{event_id}: unsupported public excerpt exception {exception!r}")

    if is_title_like(text) and exception != "short_decisive_sentence":
        errors.append(f"{event_id}: excerpt looks title-like")

    if not is_complete_sentence(text, capture_body=capture_body):
        errors.append(f"{event_id}: excerpt is not complete sentence text")

    has_object = contains_prediction_object(text, object_terms)
    note = str(context_note or "").strip()

    if is_anchor:
        if not has_object:
            errors.append(f"{event_id}: anchor excerpt must identify prediction object in quote")
    elif not has_object and not note:
        errors.append(f"{event_id}: excerpt must identify prediction object or include context_note")

    if _bad_excerpt_start(text) and not has_object:
        errors.append(f"{event_id}: excerpt starts with ambiguous pronoun without prediction object")

    wc = word_count(text)
    if wc > MAX_PUBLIC_EXCERPT_WORDS:
        errors.append(f"{event_id}: excerpt over {MAX_PUBLIC_EXCERPT_WORDS} words ({wc})")

    if wc < min_words:
        if exception != "short_decisive_sentence":
            errors.append(
                f"{event_id}: excerpt under {min_words} words ({wc}) without short_decisive_sentence"
            )
        elif not note:
            errors.append(f"{event_id}: short excerpt requires context_note")
        elif wc < 4:
            errors.append(f"{event_id}: short_decisive_sentence excerpt too short")

    return errors


def validate_capture_row(
    row: dict[str, Any],
    capture_body: str,
    public_event: dict[str, Any],
    *,
    is_anchor: bool = False,
    require_youtube: bool = False,
) -> list[str]:
    event_id = str(row.get("event_id") or "?")
    excerpt = str(row.get("public_excerpt") or "").strip()
    errors: list[str] = []
    if not excerpt:
        return [f"{event_id}: public_excerpt is empty"]

    if not excerpt_segments_in_capture(excerpt, capture_body):
        errors.append(f"{event_id}: public_excerpt not found in capture body")

    object_terms = resolve_prediction_object_terms(row, public_event)
    min_words = MIN_ANCHOR_WORDS if is_anchor else MIN_APPEARANCE_WORDS
    errors.extend(
        validate_excerpt_quality(
            event_id=event_id,
            excerpt=excerpt,
            min_words=min_words,
            exception=row.get("excerpt_exception"),
            context_note=row.get("context_note"),
            object_terms=object_terms,
            is_anchor=is_anchor,
            capture_body=capture_body,
        )
    )

    if require_youtube:
        cap_path = REPO_ROOT / str(row.get("capture", "")).replace("\\", "/")
        if cap_path.is_file():
            cite = source_citation(cap_path)
            if not cite.get("youtube_url"):
                errors.append(f"{event_id}: missing youtube_url in capture (required mode)")

    return errors


def validate_public_excerpt(
    row: dict[str, Any],
    capture_body: str,
    public_event: dict[str, Any] | None = None,
    *,
    is_anchor: bool = False,
    require_youtube: bool = False,
) -> list[str]:
    if public_event is None:
        public_event = {}
    return validate_capture_row(
        row,
        capture_body,
        public_event,
        is_anchor=is_anchor,
        require_youtube=require_youtube,
    )


def load_capture_map(path: Path | None = None) -> list[dict[str, Any]]:
    target = path or FREEMAN_CAPTURE_MAP
    if not target.is_file():
        raise FileNotFoundError(f"Missing capture map: {target.relative_to(REPO_ROOT)}")
    data = json.loads(target.read_text(encoding="utf-8"))
    rows = data.get("rows") or data
    if not isinstance(rows, list):
        raise ValueError("capture map must be a list or {rows: [...]}")
    for row in rows:
        missing = [k for k in CAPTURE_MAP_REQUIRED if k not in row]
        if missing:
            raise ValueError(f"capture map row missing fields {missing}: {row}")
        if row["stance"] not in STANCE_VALUES:
            raise ValueError(f"invalid stance {row['stance']!r} in {row}")
    return rows


def select_anchor_appearance(
    appearances: list[dict[str, Any]],
    public_event: dict[str, Any],
) -> dict[str, Any]:
    anchor_capture = public_event.get("anchor_capture")
    if anchor_capture:
        for app in appearances:
            if app.get("capture") == anchor_capture:
                return app
    for app in appearances:
        if app.get("speech_act") == "initial":
            return app
    dated = [a for a in appearances if a.get("pub_date")]
    if dated:
        return min(dated, key=lambda a: a["pub_date"])
    return appearances[-1]


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_curated_capture_map(
    config: VoiceConfig,
    *,
    capture_map_path: Path | None = None,
    public_map_path: Path | None = None,
) -> tuple[list[str], int]:
    issues: list[str] = []
    cap_path = capture_map_path or config.capture_map_path
    pub_path = public_map_path or config.public_map_path
    public_map = load_public_map(pub_path, event_order=config.pilot_event_order)
    rows = load_capture_map(cap_path)
    anchors = {
        event_id: str(public_map[event_id].get("anchor_capture") or "")
        for event_id in config.pilot_event_order
    }
    for row in rows:
        capture = REPO_ROOT / str(row["capture"]).replace("\\", "/")
        if not capture.is_file():
            issues.append(f"missing capture {row['capture']}")
            continue
        _, body = parse_capture_frontmatter(capture.read_text(encoding="utf-8"))
        event_id = str(row["event_id"])
        is_anchor = str(row.get("capture") or "") == anchors.get(event_id, "")
        label = f"{event_id} @ {row['capture']}"
        for err in validate_capture_row(
            row,
            body,
            public_map[event_id],
            is_anchor=is_anchor,
        ):
            issues.append(f"{label}: {err}")
    return issues, len(rows)
