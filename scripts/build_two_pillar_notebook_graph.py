#!/usr/bin/env python3
"""Build a polyphonic cognition-stream graph for strategy-codex.

This is a WORK-only strategy-codex derived artifact. It consumes the public
YouTube crawl indices already present on disk, folds them into one graph, and
emits a JSON graph plus a Markdown companion view focused on a count-neutral
lattice of cognition streams. The current lattice has eight streams:

- Nima (`nima`)
- Diesen (`diesen`)
- Davis (`davis`)
- Mercouris (`mercouris_duran`)
- Crooke (`crooke`)
- Parsi (`parsi`)
- Pape (`pape`)
- Ritter (`ritter`)

The file keeps a legacy module name for compatibility. The public artifact
language treats streams as interpretive voices first, with source/channel
provenance carried separately.

The graph is intentionally richer than the historical-expert-context rollups:
it carries episode routing, guest normalization, stream bridges, chronology
edges, and episode-level theme tags while staying compact enough for notebook
inspection.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_DW_INDEX = REPO_ROOT / ".codex-tmp" / "dialogue-works-full-latest" / "index.json"
DEFAULT_DIESEN_INDEX = REPO_ROOT / ".codex-tmp" / "diesen-january" / "index.json"
DEFAULT_DAVIS_INDEX = REPO_ROOT / ".codex-tmp" / "davis-january" / "index.json"
DEFAULT_RAW_INPUT_ROOT = (
    REPO_ROOT / "codex" / "2026" / "raw-input"
)
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "skill-work" / "work-strategy" / "interview-graph"
DEFAULT_OUT_JSON = DEFAULT_OUT_DIR / "cognition-streams-graph.json"
DEFAULT_OUT_MD = DEFAULT_OUT_DIR / "cognition-streams-graph.md"

WINDOW_START = date(2025, 5, 1)
WINDOW_END = date(2026, 5, 1)

PILLARS = {
    "nima": {
        "pillar_id": "nima",
        "stream_id": "nima",
        "stream_kind": "host_channel",
        "display_name": "Nima",
        "axis_label": "Synthesis",
        "voice_note": "Synthesis through long-form cross-guest interviews.",
        "host_id": "nima",
        "host_name": "Nima Alkorshid",
        "host_thread": "thread:nima",
        "channel_url": "https://www.youtube.com/@dialogueworks01/videos",
        "source_channels": ["@dialogueworks01"],
        "source_label": "Dialogue Works; dialogue-works-full-latest/index.json",
    },
    "diesen": {
        "pillar_id": "diesen",
        "stream_id": "diesen",
        "stream_kind": "host_channel",
        "display_name": "Diesen",
        "axis_label": "Order",
        "voice_note": "Order through civilizational, multipolar, and institutional transition.",
        "host_id": "diesen",
        "host_name": "Glenn Diesen",
        "host_thread": "thread:diesen",
        "channel_url": "https://www.youtube.com/@GDiesen1/videos",
        "source_channels": ["@GDiesen1"],
        "source_label": "diesen-january/index.json",
    },
    "davis": {
        "pillar_id": "davis",
        "stream_id": "davis",
        "stream_kind": "host_channel",
        "display_name": "Davis",
        "axis_label": "Conflict",
        "voice_note": "Conflict through military feasibility, battlefield dynamics, and policy risk.",
        "host_id": "davis",
        "host_name": "Daniel Davis",
        "host_thread": "thread:davis",
        "channel_url": "https://www.youtube.com/@DanielDavisDeepDive/videos",
        "source_channels": ["@DanielDavisDeepDive"],
        "source_label": "davis-january/index.json",
    },
    "mercouris_duran": {
        "pillar_id": "mercouris_duran",
        "stream_id": "mercouris_duran",
        "stream_kind": "host_channel",
        "display_name": "Mercouris",
        "axis_label": "Statecraft",
        "voice_note": "Statecraft through diplomatic sequence, elite maneuver, and daily geopolitical narrative.",
        "host_id": "mercouris",
        "host_name": "Alexander Mercouris",
        "host_thread": "thread:mercouris",
        "channel_url": "https://www.youtube.com/@TheDuran/videos",
        "source_channels": ["@AlexMercouris", "@TheDuran"],
        "source_label": "Alexander Mercouris / The Duran; raw-input/mercouris-duran",
    },
}

EXPERT_LENS_STREAMS = {
    "crooke": {
        "stream_id": "crooke",
        "stream_kind": "expert_lens",
        "display_name": "Crooke",
        "axis_label": "Process",
        "voice_note": "Process through civilizational motive, institutional memory, and revolutionary statecraft.",
        "host_id": None,
        "host_name": "Alastair Crooke",
        "host_thread": "thread:crooke",
        "channel_url": None,
        "source_channels": [],
        "source_label": "strategy-codex raw-input and historical expert context",
    },
    "parsi": {
        "stream_id": "parsi",
        "stream_kind": "expert_lens",
        "display_name": "Parsi",
        "axis_label": "Scope",
        "voice_note": "Scope through diplomatic possibility space, regional constraints, and negotiation framing.",
        "host_id": None,
        "host_name": "Trita Parsi",
        "host_thread": "thread:parsi",
        "channel_url": None,
        "source_channels": [],
        "source_label": "strategy-codex raw-input and historical expert context",
    },
    "pape": {
        "stream_id": "pape",
        "stream_kind": "expert_lens",
        "display_name": "Pape",
        "axis_label": "Escalation",
        "voice_note": "Escalation through formal mechanisms, coercion clocks, and strategic choice points.",
        "host_id": None,
        "host_name": "Robert Pape",
        "host_thread": "thread:pape",
        "channel_url": None,
        "source_channels": [],
        "source_label": "strategy-codex raw-input and historical expert context",
    },
    "ritter": {
        "stream_id": "ritter",
        "stream_kind": "expert_lens",
        "display_name": "Ritter",
        "axis_label": "Mechanics",
        "voice_note": "Mechanics through military-technical claims, operational constraints, and inspection detail.",
        "host_id": None,
        "host_name": "Scott Ritter",
        "host_thread": "thread:ritter",
        "channel_url": None,
        "source_channels": [],
        "source_label": "strategy-codex raw-input and historical expert context",
    },
}

COGNITION_STREAMS = {**PILLARS, **EXPERT_LENS_STREAMS}
HOST_STREAM_IDS = tuple(PILLARS)

HUMAN_TITLE_RE = re.compile(
    r"^(?:col|amb|prof|dr|lt\.?\s*col|gen|mr|mrs|ms)\.?\s+",
    re.IGNORECASE,
)
NOISE_TITLE_TOKENS = {
    "breaking",
    "breaking news",
    "exclusive",
    "eu",
    "live",
    "news",
    "report",
    "special",
    "trump",
    "update",
    "watch",
}
PERSON_LIKE_RE = re.compile(
    r"^(?:[A-Z][a-z]+(?:[ '\-][A-Z][a-z]+)*|[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4})$"
)
PAREN_RE = re.compile(r"\([^)]*\)")
WHITESPACE_RE = re.compile(r"\s+")
WATCH_URL_RE = re.compile(r"https?://(?:www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]+)")
SHORTS_URL_RE = re.compile(r"https?://(?:www\.)?youtube\.com/shorts/([A-Za-z0-9_-]+)")
YOUTU_BE_RE = re.compile(r"https?://youtu\.be/([A-Za-z0-9_-]+)")

GUEST_ALIAS_CANONICAL: dict[str, str] = {
    "larry c johnson": "Larry Johnson",
    "col larry c johnson": "Larry Johnson",
    "col larry johnson": "Larry Johnson",
    "larry johnson": "Larry Johnson",
    "larry c. johnson": "Larry Johnson",
    "col larry c. johnson": "Larry Johnson",
    "amb chas freeman": "Charles Freeman",
    "amb. chas freeman": "Charles Freeman",
    "chas freeman": "Charles Freeman",
    "charles freeman": "Charles Freeman",
    "prof ted postol": "Theodore Postol",
    "prof. ted postol": "Theodore Postol",
    "ted postol": "Theodore Postol",
    "theodore postol": "Theodore Postol",
    "seyed m marandi": "Seyed Mohammad Marandi",
    "seyed m. marandi": "Seyed Mohammad Marandi",
    "mohammad marandi": "Seyed Mohammad Marandi",
    "seyed mohammad marandi": "Seyed Mohammad Marandi",
    "col larry wilkerson": "Lawrence Wilkerson",
    "col. larry wilkerson": "Lawrence Wilkerson",
    "larry wilkerson": "Lawrence Wilkerson",
    "lawrence wilkerson": "Lawrence Wilkerson",
    "richard d wolff": "Richard Wolff",
    "richard wolff": "Richard Wolff",
    "warwick powell": "Warwick Powell",
    "anatol lieven": "Anatol Lieven",
    "karin kneissl": "Karin Kneissl",
    "saeed khatibzadeh": "Saeed Khatibzadeh",
    "vladimir putin": "Vladimir Putin",
    "president putin": "Vladimir Putin",
    "jeffrey sachs": "Jeffrey Sachs",
    "douglas macgregor": "Douglas Macgregor",
    "scott ritter": "Scott Ritter",
    "alastair crooke": "Alastair Crooke",
    "andrei martyanov": "Andrei Martyanov",
    "alex krainer": "Alex Krainer",
    "max blumenthal": "Max Blumenthal",
    "michael hudson": "Michael Hudson",
    "pepe escobar": "Pepe Escobar",
    "john mearsheimer": "John Mearsheimer",
    "daniel davis": "Daniel Davis",
    "jacques baud": "Jacques Baud",
    "george beebe": "George Beebe",
    "brian berletic": "Brian Berletic",
    "aaron mate": "Aaron Maté",
    "aaron maté": "Aaron Maté",
    "richard sakwa": "Richard Sakwa",
}

THEME_RULES: list[tuple[str, str]] = [
    ("iran", "iran"),
    ("hormuz", "iran"),
    ("tehran", "iran"),
    ("nuclear", "nuclear"),
    ("ukraine", "ukraine"),
    ("nato", "nato"),
    ("europe", "europe"),
    ("eu ", "europe"),
    (" european", "europe"),
    ("multipolar", "multipolarity"),
    ("brics", "multipolarity"),
    ("china", "china"),
    ("taiwan", "china"),
    ("venezuela", "venezuela"),
    ("dollar", "dollar"),
    ("petrodollar", "dollar"),
    ("treasury", "dollar"),
    ("israel", "middle-east"),
    ("gaza", "middle-east"),
    ("palestine", "middle-east"),
    ("russia", "russia"),
    ("empire", "us-empire"),
    ("unipolar", "us-empire"),
    ("american power", "us-empire"),
]

HOST_LOOKUP_KEYS = {
    "nima": {"nima", "alkorshid", "alkhorshid", "nima alkhorshid", "nima alkorshid"},
    "diesen": {"glenn", "diesen", "glenn diesen"},
    "davis": {"daniel", "davis", "daniel davis", "lt col daniel davis", "lt. col. daniel davis"},
    "mercouris_duran": {
        "alexander mercouris",
        "mercouris",
        "the duran",
        "alex mercouris",
        "alexandrer mercouris",
        "alex christoforou",
        "christoforou",
    },
}

COHOST_LOOKUP_KEYS = {
    "mercouris_duran": {"alex christoforou", "christoforou"},
}

DISPLAY_NAME_OVERRIDES = {
    "nima alkhorshid": "Nima Alkorshid",
    "nima alkorshid": "Nima Alkorshid",
    "glenn diesen": "Glenn Diesen",
    "daniel davis": "Daniel Davis",
    "lt col daniel davis": "Daniel Davis",
    "lt. col. daniel davis": "Daniel Davis",
    "alex christoforou": "Alex Christoforou",
    "larry c johnson": "Larry Johnson",
    "col larry c johnson": "Larry Johnson",
    "col larry johnson": "Larry Johnson",
    "larry johnson": "Larry Johnson",
    "chas freeman": "Charles Freeman",
    "amb chas freeman": "Charles Freeman",
    "amb. chas freeman": "Charles Freeman",
    "charles freeman": "Charles Freeman",
    "ted postol": "Theodore Postol",
    "prof ted postol": "Theodore Postol",
    "prof. ted postol": "Theodore Postol",
    "theodore postol": "Theodore Postol",
    "seyed m marandi": "Seyed Mohammad Marandi",
    "seyed m. marandi": "Seyed Mohammad Marandi",
    "mohammad marandi": "Seyed Mohammad Marandi",
    "seyed mohammad marandi": "Seyed Mohammad Marandi",
    "richard d wolff": "Richard Wolff",
    "richard wolff": "Richard Wolff",
    "warwick powell": "Warwick Powell",
    "anatol lieven": "Anatol Lieven",
    "karin kneissl": "Karin Kneissl",
    "saeed khatibzadeh": "Saeed Khatibzadeh",
    "vladimir putin": "Vladimir Putin",
    "president putin": "Vladimir Putin",
    "lawrence wilkerson": "Lawrence Wilkerson",
    "larry wilkerson": "Lawrence Wilkerson",
    "col larry wilkerson": "Lawrence Wilkerson",
    "col. larry wilkerson": "Lawrence Wilkerson",
}


@dataclass(frozen=True)
class SourceRow:
    episode_id: str
    pillar_id: str
    pub_date: str
    title: str
    guest_raw: str
    guest_aliases: dict[str, list[str]]
    guest_ids: list[str]
    guest_names: list[str]
    cohost_ids: list[str]
    cohost_names: list[str]
    status: str
    themes: list[str]
    routing: dict[str, object]
    source: dict[str, object]


def _normalize_space(text: str) -> str:
    return WHITESPACE_RE.sub(" ", (text or "")).strip()


def _normalize_date(raw: str | None) -> str | None:
    text = _normalize_space(raw or "")
    if not text:
        return None
    if re.fullmatch(r"\d{8}", text):
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return text
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def _extract_video_id(value: str) -> str | None:
    text = (value or "").strip()
    if not text:
        return None
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", text):
        return text
    for pattern in (WATCH_URL_RE, SHORTS_URL_RE, YOUTU_BE_RE):
        m = pattern.search(text)
        if m:
            return m.group(1)
    return None


def _is_canonical_youtube_video_id(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{11}", _extract_video_id(value) or ""))


def _canonical_watch_url(value: str) -> str | None:
    video_id = _extract_video_id(value)
    if not video_id:
        return None
    return f"https://www.youtube.com/watch?v={video_id}"


def _ascii_slugify(text: str, *, max_len: int = 80) -> str:
    normalized = unicodedata.normalize("NFKD", text or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower().strip()
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text)
    ascii_text = re.sub(r"-+", "-", ascii_text).strip("-")
    ascii_text = ascii_text[:max_len].rstrip("-")
    return ascii_text or "item"


def _display_clean(text: str) -> str:
    out = html.unescape(text or "")
    out = out.replace("“", '"').replace("”", '"').replace("’", "'")
    out = PAREN_RE.sub("", out)
    out = HUMAN_TITLE_RE.sub("", out)
    out = _normalize_space(out)
    out = out.strip(" ,;:-|")
    return out


def _looks_like_person_name(text: str) -> bool:
    cleaned = _display_clean(text)
    if not cleaned:
        return False
    key = _lookup_key(cleaned)
    if not key or key in NOISE_TITLE_TOKENS:
        return False
    if len(cleaned) <= 3 and cleaned.isupper():
        return False
    if cleaned.upper() == cleaned and len(cleaned.split()) <= 4:
        return False
    words = cleaned.split()
    if len(words) < 2 or len(words) > 6:
        return False
    return bool(PERSON_LIKE_RE.fullmatch(cleaned))


def _best_person_fragment(text: str) -> str:
    candidate = _display_clean(text)
    if not candidate:
        return ""
    if _looks_like_person_name(candidate):
        return candidate
    fragments = [
        part.strip()
        for part in re.split(r"\s*(?:/|[-â€”â€“:|])\s*", candidate)
        if part.strip()
    ]
    person_fragments = [fragment for fragment in fragments if _looks_like_person_name(fragment)]
    if person_fragments:
        return max(person_fragments, key=lambda item: (len(item.split()), len(item)))
    return ""


def _lookup_key(text: str) -> str:
    out = _display_clean(text)
    out = unicodedata.normalize("NFKD", out)
    out = "".join(ch for ch in out if not unicodedata.combining(ch))
    out = out.lower().replace(".", "")
    out = re.sub(r"[^a-z0-9]+", " ", out)
    return _normalize_space(out)


def _canonicalize_guest_name(raw_name: str) -> str:
    key = _lookup_key(raw_name)
    if not key:
        return ""
    if key in DISPLAY_NAME_OVERRIDES:
        return DISPLAY_NAME_OVERRIDES[key]
    if key in GUEST_ALIAS_CANONICAL:
        return GUEST_ALIAS_CANONICAL[key]
    if len(key.split()) < 2:
        return ""
    return _display_clean(raw_name)


def _scan_title_for_known_guest(title: str) -> str | None:
    title_key = _lookup_key(title)
    if not title_key:
        return None
    candidate_pairs = list({**DISPLAY_NAME_OVERRIDES, **GUEST_ALIAS_CANONICAL}.items())
    candidate_pairs.sort(key=lambda item: (-len(item[0]), item[0]))
    for alias_key, canonical in candidate_pairs:
        if alias_key and alias_key in title_key:
            return canonical
    return None


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _synthetic_video_id(seed: str) -> str:
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:11]


def _parse_frontmatter_value(raw: str) -> object:
    text = _normalize_space(raw)
    if not text:
        return ""
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        items = [item.strip().strip('"').strip("'") for item in inner.split(",")]
        return [item for item in items if item]
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return text[1:-1]
    return text


def _parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    idx = 1
    front: dict[str, object] = {}
    while idx < len(lines):
        line = lines[idx]
        if line.strip() == "---":
            idx += 1
            break
        if ":" in line:
            key, raw_value = line.split(":", 1)
            front[key.strip()] = _parse_frontmatter_value(raw_value)
        idx += 1
    body = "\n".join(lines[idx:])
    return front, body


def _first_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return _normalize_space(line[2:])
    return ""


def _load_crawl_rows(
    *,
    index_path: Path,
    pillar_id: str,
    window_start: date,
    window_end: date,
) -> list[dict[str, str]]:
    payload = _load_json(index_path)
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for video in payload.get("videos") or []:
        upload_date = _normalize_date(str(video.get("upload_date") or ""))
        if not upload_date:
            continue
        pub = date.fromisoformat(upload_date)
        if pub < window_start or pub > window_end:
            continue
        video_id = _extract_video_id(str(video.get("video_id") or "")) or _extract_video_id(
            str(video.get("url") or "")
        )
        if not video_id or video_id in seen:
            continue
        seen.add(video_id)
        title = _normalize_space(str(video.get("title") or ""))
        rows.append(
            {
                "episode_id": f"https://www.youtube.com/watch?v={video_id}",
                "pillar_id": pillar_id,
                "pub_date": upload_date,
                "title": title,
                "video_id": video_id,
                "source_channel": PILLARS[pillar_id]["source_channels"][0],
                "source_index_path": str(index_path.relative_to(REPO_ROOT).as_posix())
                if index_path.is_relative_to(REPO_ROOT)
                else str(index_path),
            }
        )
    rows.sort(key=lambda row: (row["pub_date"], row["title"], row["video_id"]))
    return rows


def _build_raw_input_index(raw_root: Path) -> tuple[set[str], set[str]]:
    video_ids: set[str] = set()
    urls: set[str] = set()
    if not raw_root.is_dir():
        return video_ids, urls

    for path in raw_root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        head = text[:12_000]
        for match in WATCH_URL_RE.finditer(head):
            video_ids.add(match.group(1))
            urls.add(f"https://www.youtube.com/watch?v={match.group(1)}")
        for match in SHORTS_URL_RE.finditer(head):
            video_ids.add(match.group(1))
            urls.add(f"https://www.youtube.com/watch?v={match.group(1)}")
        for match in YOUTU_BE_RE.finditer(head):
            video_ids.add(match.group(1))
            urls.add(f"https://www.youtube.com/watch?v={match.group(1)}")
    return video_ids, urls


def _date_from_path(path: Path) -> str | None:
    for part in reversed(path.parts):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", part):
            return part
    return None


def _count_lens_raw_inputs(raw_root: Path) -> dict[str, dict[str, object]]:
    stats = {
        stream_id: {"raw_inputs": 0, "first_seen": None, "last_seen": None}
        for stream_id in EXPERT_LENS_STREAMS
    }
    if not raw_root.is_dir():
        return stats

    for path in raw_root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        front, _body = _parse_frontmatter(text)
        thread_values = {_lookup_key(value) for value in _frontmatter_values(front, "thread")}
        path_key = _lookup_key(path.as_posix())
        for stream_id in EXPERT_LENS_STREAMS:
            if stream_id not in thread_values and stream_id not in path_key:
                continue
            date_text = _normalize_date(str(front.get("pub_date") or "")) or _date_from_path(path)
            stat = stats[stream_id]
            stat["raw_inputs"] = int(stat["raw_inputs"]) + 1
            if date_text:
                if stat["first_seen"] is None or date_text < str(stat["first_seen"]):
                    stat["first_seen"] = date_text
                if stat["last_seen"] is None or date_text > str(stat["last_seen"]):
                    stat["last_seen"] = date_text
    return stats


def _load_thread_id_map() -> dict[str, str]:
    path = (
        REPO_ROOT / "codex" / "strategy-commentator-threads.md"
    )
    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.startswith("| expert_id | Name | Role"):
            start = idx + 2
            break
    if start is None:
        return {}

    thread_map: dict[str, str] = {}
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        expert_id = cells[0].strip("` ")
        name = cells[1]
        if not expert_id or expert_id == "expert_id":
            continue
        key = _lookup_key(name)
        if key:
            thread_map[key] = expert_id
    return thread_map


def _frontmatter_values(front: dict[str, object], key: str) -> list[str]:
    value = front.get(key)
    if value is None:
        return []
    if isinstance(value, list):
        items = [str(item) for item in value]
    elif isinstance(value, str) and value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        items = [part.strip().strip('"').strip("'") for part in inner.split(",")] if inner else []
    elif isinstance(value, str) and "," in value:
        items = [part.strip() for part in value.split(",")]
    else:
        items = [str(value)]
    return [_normalize_space(item) for item in items if _normalize_space(item)]


def _extract_people_from_body(text: str) -> tuple[list[str], list[str]]:
    guests: list[str] = []
    cohosts: list[str] = []
    for line in text.splitlines()[:80]:
        raw = line.strip()
        if not raw:
            continue
        cleaned = re.sub(r"^\*+\s*", "", raw)
        cleaned = re.sub(r"\s*\*+$", "", cleaned)
        lowered = cleaned.lower()
        if lowered.startswith("participants:") or lowered.startswith("speakers:"):
            _, value = cleaned.split(":", 1)
            for person in re.split(r"\s*,\s*", _normalize_space(value)):
                if not person:
                    continue
                key = _lookup_key(person)
                if key in COHOST_LOOKUP_KEYS["mercouris_duran"]:
                    if "Alex Christoforou" not in cohosts:
                        cohosts.append("Alex Christoforou")
                    continue
                if key in HOST_LOOKUP_KEYS["mercouris_duran"]:
                    continue
                canonical = _canonicalize_guest_name(person)
                if canonical and canonical not in guests:
                    guests.append(canonical)
        elif lowered.startswith("speaker:"):
            _, value = cleaned.split(":", 1)
            person = _normalize_space(value)
            if person:
                key = _lookup_key(person)
                if key in COHOST_LOOKUP_KEYS["mercouris_duran"]:
                    if "Alex Christoforou" not in cohosts:
                        cohosts.append("Alex Christoforou")
                elif key not in HOST_LOOKUP_KEYS["mercouris_duran"]:
                    canonical = _canonicalize_guest_name(person)
                    if canonical and canonical not in guests:
                        guests.append(canonical)
    return guests, cohosts


def _mercouris_source_channel(front: dict[str, object], path: Path, title: str, body: str) -> str:
    front_show = _lookup_key(str(front.get("show") or ""))
    front_host = _lookup_key(str(front.get("host") or ""))
    path_text = _lookup_key(f"{path.name} {path.stem}")
    title_key = _lookup_key(title)
    body_key = _lookup_key(body[:400])
    if "the duran" in front_show or "the duran" in path_text or "the duran" in title_key:
        return "@TheDuran"
    if "christoforou" in body_key:
        return "@TheDuran"
    if "alexander mercouris" in front_host and "the duran" not in front_show:
        return "@AlexMercouris"
    return "@TheDuran"


def _mercouris_episode_id(front: dict[str, object], path: Path, title: str, pub_date: str) -> tuple[str, str]:
    raw_candidates = [
        str(front.get("source_url") or ""),
        str(front.get("canonical_url") or ""),
    ]
    for raw in raw_candidates:
        video_id = _extract_video_id(raw)
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}", video_id
    seed = f"{path.as_posix()}|{pub_date}|{title}"
    video_id = _synthetic_video_id(seed)
    return f"https://www.youtube.com/watch?v={video_id}", video_id


def _is_mercouris_source(path: Path, front: dict[str, object], title: str, body: str) -> bool:
    haystack = " ".join(
        [
            path.name,
            path.stem,
            title,
            body[:1000],
            str(front.get("show") or ""),
            str(front.get("host") or ""),
            str(front.get("thread") or ""),
        ]
    ).lower()
    return any(token in haystack for token in ("mercouris", "the duran", "christoforou"))


def _guess_guest_block(title: str, *, pillar_id: str) -> str | None:
    text = _normalize_space(title)
    if not text:
        return None

    low = text.lower()
    if pillar_id == "mercouris_duran":
        for marker in (" w/ ", " w/", " with ", " featuring ", " feat. ", " ft. "):
            marker_idx = low.find(marker)
            if marker_idx >= 0:
                candidate = text[marker_idx + len(marker) :].strip()
                candidate = _best_person_fragment(candidate)
                if candidate:
                    return candidate
        return None
    if pillar_id == "nima" and low.startswith("nima x "):
        candidate = text[7:].strip()
        candidate = _best_person_fragment(candidate)
        if candidate and _lookup_key(candidate) not in HOST_LOOKUP_KEYS["nima"]:
            return candidate
    if pillar_id == "davis" and "daniel davis" in low:
        host_idx = low.find("daniel davis")
        if host_idx >= 0:
            for marker in (" & ", " and ", " with "):
                marker_idx = low.find(marker, host_idx + len("daniel davis"))
                if marker_idx >= 0:
                    candidate = text[marker_idx + len(marker) :].strip()
                    candidate = _best_person_fragment(candidate)
                    if candidate:
                        return candidate

    candidates: list[str] = []

    def add_parts(parts: list[str]) -> None:
        for part in parts:
            part = _best_person_fragment(part)
            if part:
                candidates.append(part)

    if "|" in text:
        parts = text.split("|")
        add_parts([parts[0], parts[-1]])
    if ":" in text:
        parts = text.split(":")
        add_parts([parts[0], parts[-1]])
    for sep in ("—", "–", " - ", " | "):
        if sep in text:
            parts = text.split(sep)
            add_parts([parts[0], parts[-1]])

    def score(candidate: str) -> int:
        key = _lookup_key(candidate)
        if not key:
            return -10
        score_value = 0
        low_key = key
        if any(token in low_key for token in (" and ", " & ", ", ")):
            score_value += 3
        if re.search(r"\b(?:col|amb|prof|dr|gen|lt col)\b", low_key):
            score_value += 2
        if any(
            token in low_key
            for token in (
                "johnson",
                "ritter",
                "freeman",
                "marandi",
                "macgregor",
                "sachs",
                "diesen",
                "wilkerson",
                "crooke",
                "baud",
                "mearsheimer",
                "hudson",
                "wolff",
                "krainer",
                "martyanov",
                "postol",
                "escobar",
                "blumenthal",
                "davis",
                "mate",
                "beebe",
                "berletic",
                "guerot",
                "galloway",
            )
        ):
            score_value += 4
        words = key.split()
        if 1 <= len(words) <= 6:
            score_value += 3
        elif len(words) > 8:
            score_value -= 2
        if any(
            token in low_key
            for token in (
                "iran",
                "ukraine",
                "nato",
                "europe",
                "china",
                "russia",
                "venezuela",
                "war",
                "collapse",
                "dollar",
                "empire",
                "gaza",
                "palestine",
            )
        ):
            score_value -= 2
        return score_value

    best = max(((score(c), c) for c in candidates), default=(-10, ""))
    if best[0] >= 3:
        candidate = _best_person_fragment(best[1])
        if not candidate:
            return None
        if not re.search(r"\s*(?:&| and |,|;|\+|\bx\b)\s*", candidate, flags=re.IGNORECASE):
            trimmed = _scan_title_for_known_guest(candidate)
            if trimmed:
                return trimmed
        return candidate
    fallback = _scan_title_for_known_guest(text)
    if fallback:
        return fallback
    return None


def _split_guest_block(guest_block: str) -> list[str]:
    text = _normalize_space(guest_block)
    if not text:
        return []
    parts = re.split(r"\s*(?:&| and |,|;|\+|\bx\b)\s*", text, flags=re.IGNORECASE)
    out: list[str] = []
    for part in parts:
        cleaned = _display_clean(part)
        if cleaned:
            out.append(cleaned)
    return out


def _extract_themes(title: str, guest_raw: str) -> list[str]:
    haystack = f"{title} {guest_raw}".lower()
    tags: list[str] = []
    seen: set[str] = set()
    for needle, tag in THEME_RULES:
        if needle in haystack and tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return tags


def _build_rows(
    *,
    index_path: Path,
    pillar_id: str,
    window_start: date,
    window_end: date,
    raw_video_ids: set[str],
    raw_urls: set[str],
    thread_map: dict[str, str],
) -> list[SourceRow]:
    rows: list[SourceRow] = []
    pillar = PILLARS[pillar_id]
    host_lookup = {_lookup_key(item) for item in HOST_LOOKUP_KEYS[pillar_id] | {pillar["host_name"]}}
    host_lookup = {item for item in host_lookup if item}

    for row in _load_crawl_rows(
        index_path=index_path,
        pillar_id=pillar_id,
        window_start=window_start,
        window_end=window_end,
    ):
        guest_block = _guess_guest_block(row["title"], pillar_id=pillar_id) or ""
        guest_names: list[str] = []
        guest_ids: list[str] = []
        guest_threads: list[str] = []
        guest_aliases: dict[str, list[str]] = defaultdict(list)

        for raw_name in _split_guest_block(guest_block):
            if _lookup_key(raw_name) in host_lookup:
                continue
            canonical = _canonicalize_guest_name(raw_name)
            if not canonical:
                continue
            guest_id = _ascii_slugify(canonical)
            if guest_id not in guest_ids:
                guest_ids.append(guest_id)
                guest_names.append(canonical)
            if _lookup_key(raw_name) != _lookup_key(canonical) and raw_name not in guest_aliases[guest_id]:
                guest_aliases[guest_id].append(raw_name)
            thread_id = thread_map.get(_lookup_key(canonical))
            if thread_id and f"thread:{thread_id}" not in guest_threads:
                guest_threads.append(f"thread:{thread_id}")

        themes = _extract_themes(row["title"], guest_block)
        status = "mirrored" if (row["video_id"] in raw_video_ids or row["episode_id"] in raw_urls) else "needs_capture"
        if not guest_ids:
            status = "provisional"

        routing = {
            "host_thread": pillar["host_thread"],
            "guest_threads": guest_threads,
        }
        source = {
            "index_path": row["source_index_path"],
            "video_id": row["video_id"],
            "channel_url": pillar["channel_url"],
            "source_channel": pillar["source_channels"][0],
        }
        rows.append(
            SourceRow(
                episode_id=row["episode_id"],
                pillar_id=pillar_id,
                pub_date=row["pub_date"],
                title=row["title"],
                guest_raw=guest_block,
                guest_aliases={guest_id: aliases[:] for guest_id, aliases in guest_aliases.items()},
                guest_ids=guest_ids,
                guest_names=guest_names,
                cohost_ids=[],
                cohost_names=[],
                status=status,
                themes=themes,
                routing=routing,
                source=source,
            )
        )

    return rows


def _load_mercouris_rows(
    *,
    raw_root: Path,
    window_start: date,
    window_end: date,
    raw_video_ids: set[str],
    raw_urls: set[str],
    thread_map: dict[str, str],
) -> list[SourceRow]:
    rows: list[SourceRow] = []
    if not raw_root.is_dir():
        return rows

    for path in sorted(raw_root.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        front, body = _parse_frontmatter(text)
        title = _normalize_space(
            str(front.get("title") or _first_h1(text) or _first_h1(body) or path.stem.replace("-", " "))
        )
        if not _is_mercouris_source(path, front, title, body):
            continue

        pub_raw = str(front.get("pub_date") or front.get("aired") or "")
        pub_date = _normalize_date(pub_raw)
        if not pub_date:
            folder_match = re.search(r"(20\d{2}-\d{2}-\d{2})", str(path.parent.name))
            if folder_match:
                pub_date = folder_match.group(1)
        if not pub_date:
            continue
        pub = date.fromisoformat(pub_date)
        if pub < window_start or pub > window_end:
            continue

        episode_id, video_id = _mercouris_episode_id(front, path, title, pub_date)
        source_channel = _mercouris_source_channel(front, path, title, body)
        host_lookup = HOST_LOOKUP_KEYS["mercouris_duran"]
        cohost_lookup = COHOST_LOOKUP_KEYS["mercouris_duran"]

        guest_names: list[str] = []
        guest_ids: list[str] = []
        guest_threads: list[str] = []
        guest_aliases: dict[str, list[str]] = defaultdict(list)
        cohost_names: list[str] = []
        cohost_ids: list[str] = []

        people = _frontmatter_values(front, "participants") or _frontmatter_values(front, "speakers")
        if not people:
            people, body_cohosts = _extract_people_from_body(body)
            cohost_names.extend(body_cohosts)

        for raw_name in people:
            key = _lookup_key(raw_name)
            if key in cohost_lookup:
                if "Alex Christoforou" not in cohost_names:
                    cohost_names.append("Alex Christoforou")
                continue
            if not key or key in host_lookup:
                continue
            canonical = _canonicalize_guest_name(raw_name)
            if not canonical:
                continue
            guest_id = _ascii_slugify(canonical)
            if guest_id not in guest_ids:
                guest_ids.append(guest_id)
                guest_names.append(canonical)
            if _lookup_key(raw_name) != _lookup_key(canonical) and raw_name not in guest_aliases[guest_id]:
                guest_aliases[guest_id].append(raw_name)
            thread_id = thread_map.get(_lookup_key(canonical))
            if thread_id and f"thread:{thread_id}" not in guest_threads:
                guest_threads.append(f"thread:{thread_id}")

        if not guest_names:
            guest_block = _guess_guest_block(title, pillar_id="mercouris_duran") or ""
            for raw_name in _split_guest_block(guest_block):
                key = _lookup_key(raw_name)
                if key in host_lookup or key in cohost_lookup:
                    continue
                canonical = _canonicalize_guest_name(raw_name)
                if not canonical:
                    continue
                guest_id = _ascii_slugify(canonical)
                if guest_id not in guest_ids:
                    guest_ids.append(guest_id)
                    guest_names.append(canonical)
                if _lookup_key(raw_name) != _lookup_key(canonical) and raw_name not in guest_aliases[guest_id]:
                    guest_aliases[guest_id].append(raw_name)
                thread_id = thread_map.get(_lookup_key(canonical))
                if thread_id and f"thread:{thread_id}" not in guest_threads:
                    guest_threads.append(f"thread:{thread_id}")
        else:
            guest_block = " & ".join(guest_names)

        for raw_name in list(cohost_names):
            canonical = _canonicalize_guest_name(raw_name)
            if canonical and canonical not in cohost_names:
                cohost_names.append(canonical)
        for raw_name in cohost_names:
            if _lookup_key(raw_name) in cohost_lookup:
                cohost_id = _ascii_slugify("Alex Christoforou")
                if cohost_id not in cohost_ids:
                    cohost_ids.append(cohost_id)

        themes = _extract_themes(title, guest_block or title)
        raw_source_url = str(front.get("source_url") or front.get("canonical_url") or "")
        has_raw_source_id = _is_canonical_youtube_video_id(raw_source_url)
        source_url = raw_source_url
        if has_raw_source_id:
            canonical_source_url = _canonical_watch_url(source_url) or source_url
        else:
            canonical_source_url = episode_id
        status = "mirrored" if (video_id in raw_video_ids or episode_id in raw_urls) else "needs_capture"
        if not guest_ids:
            status = "provisional"

        routing = {
            "host_thread": "thread:mercouris",
            "guest_threads": guest_threads,
            "cohost_threads": [],
        }
        source = {
            "index_path": str(path.relative_to(REPO_ROOT).as_posix()) if path.is_relative_to(REPO_ROOT) else str(path),
            "video_id": video_id,
            "channel_url": PILLARS["mercouris_duran"]["channel_url"],
            "source_channel": source_channel,
            "source_url": canonical_source_url,
            "source_url_is_synthetic": not has_raw_source_id,
            "source_url_status": "provisional" if not has_raw_source_id else "canonical",
        }
        rows.append(
            SourceRow(
                episode_id=episode_id,
                pillar_id="mercouris_duran",
                pub_date=pub_date,
                title=title,
                guest_raw=guest_block,
                guest_aliases={guest_id: aliases[:] for guest_id, aliases in guest_aliases.items()},
                guest_ids=guest_ids,
                guest_names=guest_names,
                cohost_ids=cohost_ids,
                cohost_names=cohost_names,
                status=status,
                themes=themes,
                routing=routing,
                source=source,
            )
        )

    rows.sort(key=lambda row: (row.pub_date, row.title, row.episode_id))
    return rows


def _gap_days(left: str, right: str) -> int:
    return (date.fromisoformat(right) - date.fromisoformat(left)).days


def build_graph(
    *,
    dialogue_index: Path,
    diesen_index: Path,
    davis_index: Path,
    raw_input_root: Path,
    window_start: date = WINDOW_START,
    window_end: date = WINDOW_END,
) -> dict:
    raw_video_ids, raw_urls = _build_raw_input_index(raw_input_root)
    lens_raw_input_stats = _count_lens_raw_inputs(raw_input_root)
    thread_map = _load_thread_id_map()

    rows_by_pillar = {
        "nima": _build_rows(
            index_path=dialogue_index,
            pillar_id="nima",
            window_start=window_start,
            window_end=window_end,
            raw_video_ids=raw_video_ids,
            raw_urls=raw_urls,
            thread_map=thread_map,
        ),
        "diesen": _build_rows(
            index_path=diesen_index,
            pillar_id="diesen",
            window_start=window_start,
            window_end=window_end,
            raw_video_ids=raw_video_ids,
            raw_urls=raw_urls,
            thread_map=thread_map,
        ),
        "davis": _build_rows(
            index_path=davis_index,
            pillar_id="davis",
            window_start=window_start,
            window_end=window_end,
            raw_video_ids=raw_video_ids,
            raw_urls=raw_urls,
            thread_map=thread_map,
        ),
        "mercouris_duran": _load_mercouris_rows(
            raw_root=raw_input_root,
            window_start=window_start,
            window_end=window_end,
            raw_video_ids=raw_video_ids,
            raw_urls=raw_urls,
            thread_map=thread_map,
        ),
    }

    nodes: list[dict] = []
    edges: list[dict] = []
    seen_node_ids: set[str] = set()

    def add_node(node: dict) -> None:
        node_id = node["id"]
        if node_id in seen_node_ids:
            return
        seen_node_ids.add(node_id)
        nodes.append(node)

    for stream_id, stream in COGNITION_STREAMS.items():
        add_node(
            {
                "type": "stream",
                "id": f"stream:{stream_id}",
                "stream_id": stream_id,
                "stream_kind": stream["stream_kind"],
                "pillar_id": stream_id if stream_id in PILLARS else None,
                "display_name": stream["display_name"],
                "axis_label": stream["axis_label"],
                "voice_note": stream["voice_note"],
                "host_id": stream["host_id"],
                "host_name": stream["host_name"],
                "host_thread": stream["host_thread"],
                "channel_url": stream["channel_url"],
                "source_channels": stream["source_channels"],
                "source_label": stream["source_label"],
                "raw_input_count": lens_raw_input_stats.get(stream_id, {}).get("raw_inputs", 0),
                "first_seen": lens_raw_input_stats.get(stream_id, {}).get("first_seen"),
                "last_seen": lens_raw_input_stats.get(stream_id, {}).get("last_seen"),
            }
        )

    episode_nodes_by_pillar: dict[str, list[dict]] = {}
    guest_episode_ids: dict[str, list[str]] = defaultdict(list)
    guest_aliases: dict[str, set[str]] = defaultdict(set)
    guest_counts_by_pillar: dict[str, Counter[str]] = defaultdict(Counter)
    guest_display_names: dict[str, str] = {}
    guest_thread_ids: dict[str, set[str]] = defaultdict(set)
    cohost_episode_ids: dict[str, list[str]] = defaultdict(list)
    cohost_counts_by_pillar: dict[str, Counter[str]] = defaultdict(Counter)
    cohost_display_names: dict[str, str] = {}
    theme_counter: Counter[str] = Counter()
    episode_status_counter: Counter[str] = Counter()
    episode_lookup: dict[str, dict[str, str]] = {}

    for pillar_id, rows in rows_by_pillar.items():
        sorted_rows = sorted(rows, key=lambda r: (r.pub_date, r.title, r.episode_id))
        episode_nodes_by_pillar[pillar_id] = []
        for row in sorted_rows:
            node_id = f"episode:{row.episode_id}"
            add_node(
                {
                    "type": "episode",
                    "id": node_id,
                    "episode_id": row.episode_id,
                    "stream_id": row.pillar_id,
                    "pillar_id": row.pillar_id,
                    "pub_date": row.pub_date,
                    "title": row.title,
                    "guest_raw": row.guest_raw,
                    "guest_aliases": row.guest_aliases,
                    "guest_ids": row.guest_ids,
                    "guest_names": row.guest_names,
                    "cohost_ids": row.cohost_ids,
                    "cohost_names": row.cohost_names,
                    "status": row.status,
                    "themes": row.themes,
                    "routing": row.routing,
                    "source": row.source,
                }
            )
            episode_nodes_by_pillar[pillar_id].append({"id": row.episode_id, "pub_date": row.pub_date})
            episode_lookup[row.episode_id] = {"pillar_id": pillar_id, "pub_date": row.pub_date}
            episode_status_counter[row.status] += 1
            for theme in row.themes:
                theme_counter[theme] += 1

            edges.append(
                {
                    "from": node_id,
                    "to": f"stream:{pillar_id}",
                    "type": "in_stream",
                }
            )

            for guest_id, guest_name in zip(row.guest_ids, row.guest_names):
                edges.append(
                    {
                        "from": node_id,
                        "to": f"guest:{guest_id}",
                        "type": "features_guest",
                    }
                )
                guest_episode_ids[guest_id].append(row.episode_id)
                guest_aliases[guest_id].update(row.guest_aliases.get(guest_id, []))
                guest_counts_by_pillar[guest_id][pillar_id] += 1
                guest_display_names.setdefault(guest_id, guest_name)
                for thread_id in row.routing.get("guest_threads") or []:
                    guest_thread_ids[guest_id].add(thread_id)

            for cohost_id, cohost_name in zip(row.cohost_ids, row.cohost_names):
                edges.append(
                    {
                        "from": node_id,
                        "to": f"cohost:{cohost_id}",
                        "type": "features_cohost",
                    }
                )
                cohost_episode_ids[cohost_id].append(row.episode_id)
                cohost_counts_by_pillar[cohost_id][pillar_id] += 1
                cohost_display_names.setdefault(cohost_id, cohost_name)

        for left, right in zip(sorted_rows, sorted_rows[1:]):
            edges.append(
                {
                    "from": f"episode:{left.episode_id}",
                    "to": f"episode:{right.episode_id}",
                    "type": "chronology_next",
                    "gap_days": _gap_days(left.pub_date, right.pub_date),
                }
            )

    bridge_nodes: list[dict] = []
    for guest_id, episode_ids in sorted(guest_episode_ids.items()):
        pillar_ids = sorted(
            pillar for pillar, counts in guest_counts_by_pillar[guest_id].items() if counts > 0
        )
        if not pillar_ids:
            continue
        display_name = guest_display_names.get(guest_id, guest_id.replace("-", " ").title())
        episode_ids_sorted = sorted(
            set(episode_ids),
            key=lambda episode_id: (
                episode_lookup.get(episode_id, {}).get("pub_date", "9999-99-99"),
                episode_id,
            ),
        )
        guest_node = {
            "type": "guest",
            "id": f"guest:{guest_id}",
            "guest_id": guest_id,
            "display_name": display_name,
            "aliases": sorted(
                {
                    alias
                    for alias in guest_aliases[guest_id]
                    if _normalize_space(alias) and _lookup_key(alias) != _lookup_key(display_name)
                }
            ),
            "pillar_ids": pillar_ids,
            "episode_ids": episode_ids_sorted,
            "episode_count": len(episode_ids_sorted),
            "counts_by_pillar": {pid: guest_counts_by_pillar[guest_id][pid] for pid in pillar_ids},
            "thread_ids": sorted(guest_thread_ids.get(guest_id, set())),
            "is_bridge": len(pillar_ids) > 1,
            "first_seen": episode_lookup.get(episode_ids_sorted[0], {}).get("pub_date"),
            "last_seen": episode_lookup.get(episode_ids_sorted[-1], {}).get("pub_date"),
        }
        add_node(guest_node)

        if len(pillar_ids) > 1:
            bridge_id = f"bridge:{guest_id}"
            bridge_node = {
                "type": "bridge",
                "id": bridge_id,
                "guest_id": guest_id,
                "display_name": display_name,
                "pillar_ids": pillar_ids,
                "episode_counts_by_pillar": {
                    pid: guest_counts_by_pillar[guest_id][pid] for pid in pillar_ids
                },
                "episode_ids_by_pillar": {
                    pid: sorted(
                        {
                            episode_id
                            for episode_id in episode_ids_sorted
                            if episode_lookup.get(episode_id, {}).get("pillar_id") == pid
                        },
                        key=lambda episode_id: (
                            episode_lookup.get(episode_id, {}).get("pub_date", "9999-99-99"),
                            episode_id,
                        ),
                    )
                    for pid in pillar_ids
                },
            }
            bridge_nodes.append(bridge_node)
            add_node(bridge_node)
            edges.append(
                {
                    "from": f"guest:{guest_id}",
                    "to": bridge_id,
                    "type": "shared_guest_bridge",
                }
            )
            for pillar_id in pillar_ids:
                edges.append(
                    {
                        "from": bridge_id,
                        "to": f"stream:{pillar_id}",
                        "type": "spans_stream",
                    }
                )

    for cohost_id, episode_ids in sorted(cohost_episode_ids.items()):
        pillar_ids = sorted(
            pillar for pillar, counts in cohost_counts_by_pillar[cohost_id].items() if counts > 0
        )
        display_name = cohost_display_names.get(cohost_id, cohost_id.replace("-", " ").title())
        episode_ids_sorted = sorted(
            set(episode_ids),
            key=lambda episode_id: (
                episode_lookup.get(episode_id, {}).get("pub_date", "9999-99-99"),
                episode_id,
            ),
        )
        add_node(
            {
                "type": "cohost",
                "id": f"cohost:{cohost_id}",
                "cohost_id": cohost_id,
                "display_name": display_name,
                "pillar_ids": pillar_ids,
                "episode_ids": episode_ids_sorted,
                "episode_count": len(episode_ids_sorted),
                "counts_by_pillar": {pid: cohost_counts_by_pillar[cohost_id][pid] for pid in pillar_ids},
                "first_seen": episode_lookup.get(episode_ids_sorted[0], {}).get("pub_date")
                if episode_ids_sorted
                else None,
                "last_seen": episode_lookup.get(episode_ids_sorted[-1], {}).get("pub_date")
                if episode_ids_sorted
                else None,
            }
        )

    per_pillar_episode_counts = {
        pillar_id: len(episode_nodes_by_pillar.get(pillar_id, [])) for pillar_id in PILLARS
    }
    per_pillar_guest_counts = {
        pillar_id: len(
            {
                guest_id
                for guest_id, counts in guest_counts_by_pillar.items()
                if counts.get(pillar_id, 0) > 0
            }
        )
        for pillar_id in PILLARS
    }
    per_pillar_cohost_counts = {
        pillar_id: len(
            {
                cohost_id
                for cohost_id, counts in cohost_counts_by_pillar.items()
                if counts.get(pillar_id, 0) > 0
            }
        )
        for pillar_id in PILLARS
    }
    bridge_guest_ids = sorted(
        guest_id
        for guest_id, counts in guest_counts_by_pillar.items()
        if sum(1 for pillar_id in PILLARS if counts.get(pillar_id, 0) > 0) > 1
    )
    raw_inputs_by_stream = {
        stream_id: int(lens_raw_input_stats.get(stream_id, {}).get("raw_inputs", 0))
        for stream_id in EXPERT_LENS_STREAMS
    }
    stream_manifest = {
        stream_id: {
            "display_name": stream["display_name"],
            "stream_kind": stream["stream_kind"],
            "axis_label": stream["axis_label"],
            "voice_note": stream["voice_note"],
            "source_label": stream["source_label"],
        }
        for stream_id, stream in COGNITION_STREAMS.items()
    }

    graph = {
        "schema_version": "2.0.0-cognition-streams-graph",
        "deprecated_schema_aliases": ["1.0.0-four-pillar-notebook-graph"],
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "title": "Polyphonic Cognition Streams",
        "stream_model": {
            "description": "Count-neutral lattice of cognition streams; current shape has eight streams but may change.",
            "analysis_mode": "contrapuntal comparison",
            "streams": stream_manifest,
            "compatibility_note": "Legacy pillar fields remain only for older strategy-codex compatibility wiring.",
        },
        "window": {
            "start": window_start.isoformat(),
            "end": window_end.isoformat(),
        },
        "sources": {
            "nima": {
                "index_path": str(dialogue_index.relative_to(REPO_ROOT))
                if dialogue_index.is_relative_to(REPO_ROOT)
                else str(dialogue_index),
                "channel_url": PILLARS["nima"]["channel_url"],
                "source_label": PILLARS["nima"]["source_label"],
                "axis_label": PILLARS["nima"]["axis_label"],
            },
            "diesen": {
                "index_path": str(diesen_index.relative_to(REPO_ROOT))
                if diesen_index.is_relative_to(REPO_ROOT)
                else str(diesen_index),
                "channel_url": PILLARS["diesen"]["channel_url"],
                "source_label": PILLARS["diesen"]["source_label"],
                "axis_label": PILLARS["diesen"]["axis_label"],
            },
            "davis": {
                "index_path": str(davis_index.relative_to(REPO_ROOT))
                if davis_index.is_relative_to(REPO_ROOT)
                else str(davis_index),
                "channel_url": PILLARS["davis"]["channel_url"],
                "source_label": PILLARS["davis"]["source_label"],
                "axis_label": PILLARS["davis"]["axis_label"],
            },
            "mercouris_duran": {
                "raw_input_root": str(raw_input_root.relative_to(REPO_ROOT))
                if raw_input_root.is_relative_to(REPO_ROOT)
                else str(raw_input_root),
                "source_channels": PILLARS["mercouris_duran"]["source_channels"],
                "channel_url": PILLARS["mercouris_duran"]["channel_url"],
                "source_label": PILLARS["mercouris_duran"]["source_label"],
                "axis_label": PILLARS["mercouris_duran"]["axis_label"],
            },
        },
        "summary": {
            "episodes_total": sum(per_pillar_episode_counts.values()),
            "guests_total": len(guest_episode_ids),
            "cohosts_total": len(cohost_episode_ids),
            "bridge_guests_total": len(bridge_guest_ids),
            "episodes_by_pillar": per_pillar_episode_counts,
            "guests_by_pillar": per_pillar_guest_counts,
            "cohosts_by_pillar": per_pillar_cohost_counts,
            "episodes_by_stream": per_pillar_episode_counts
            | {stream_id: 0 for stream_id in EXPERT_LENS_STREAMS},
            "raw_inputs_by_stream": raw_inputs_by_stream,
            "status_counts": dict(sorted(episode_status_counter.items())),
            "top_themes": theme_counter.most_common(12),
        },
        "nodes": nodes,
        "edges": edges,
        "derived": {
            "bridge_guest_ids": bridge_guest_ids,
            "bridge_nodes": bridge_nodes,
        },
    }
    return graph


def _build_table(headers: list[str], rows: list[list[str]]) -> str:
    def esc(text: str) -> str:
        return text.replace("|", "\\|")

    table = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("-" * max(3, len(h)) for h in headers) + " |",
    ]
    for row in rows:
        table.append("| " + " | ".join(esc(cell) for cell in row) + " |")
    return "\n".join(table)


def _episode_links(episode_ids: list[str], limit: int = 3) -> str:
    if not episode_ids:
        return "-"
    shown = episode_ids[:limit]
    links = [f"[{ep}]({ep})" for ep in shown]
    if len(episode_ids) > limit:
        links.append(f"... (+{len(episode_ids) - limit})")
    return ", ".join(links)


def render_markdown(graph: dict) -> str:
    nodes = graph["nodes"]
    guests = [node for node in nodes if node["type"] == "guest"]
    bridges = [node for node in nodes if node["type"] == "bridge"]
    cohosts = [node for node in nodes if node["type"] == "cohost"]
    episodes = [node for node in nodes if node["type"] == "episode"]
    streams = [node for node in nodes if node["type"] == "stream"]
    summary = graph["summary"]

    stream_names = {node["stream_id"]: node["display_name"] for node in streams}
    stream_axes = {node["stream_id"]: node["axis_label"] for node in streams}
    stream_notes = {node["stream_id"]: node.get("voice_note", "") for node in streams}
    stream_source_labels = {node["stream_id"]: node.get("source_label", "") for node in streams}
    stream_order = list(COGNITION_STREAMS)
    pillar_theme_counts: dict[str, Counter[str]] = defaultdict(Counter)
    mercouris_synthetic_sources = 0
    for episode in episodes:
        for theme in episode.get("themes") or []:
            pillar_theme_counts[episode["pillar_id"]][theme] += 1
        if episode["pillar_id"] == "mercouris_duran" and episode.get("source", {}).get("source_url_is_synthetic"):
            mercouris_synthetic_sources += 1

    bridge_roles: list[dict[str, str]] = []
    for node in sorted(
        bridges,
        key=lambda item: (-sum(item.get("episode_counts_by_pillar", {}).values()), item["display_name"].lower()),
    ):
        total_episodes = sum(node.get("episode_counts_by_pillar", {}).values())
        span = len(node.get("pillar_ids") or [])
        if span >= 4:
            role = "cross-stream hub"
        elif span == 3:
            role = "multi-stream bridge"
        elif total_episodes >= 6:
            role = "recurring bridge"
        else:
            role = "bridge"
        bridge_roles.append(
            {
                "guest": node["display_name"],
                "role": role,
                "streams": ", ".join(stream_names.get(pid, pid) for pid in (node.get("pillar_ids") or [])),
                "episodes": str(total_episodes),
                "first": node.get("first_seen") or "-",
                "last": node.get("last_seen") or "-",
            }
        )

    lines: list[str] = []
    lines.append("# Polyphonic Cognition Streams")
    lines.append("")
    lines.append("WORK only; not Record.")
    lines.append(
        "This is a count-neutral lattice of cognition streams. The current shape has eight streams: "
        + ", ".join(stream_names[stream_id] for stream_id in stream_order)
        + "."
    )
    lines.append(
        "Each stream is treated as an interpretive voice. The default analysis mode is contrapuntal comparison: "
        "surface tensions, harmonies, bridges, and differences without forcing synthesis."
    )
    lines.append(f"Window: {graph['window']['start']} to {graph['window']['end']}.")
    lines.append(
        "Deprecated compatibility note: legacy four-pillar filenames and pillar fields may appear in old wiring only; "
        "public strategy-codex language should use streams."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(
        f"- Episodes: {summary['episodes_total']} total | "
        + " | ".join(
            f"{stream_names[stream_id]} {summary['episodes_by_stream'].get(stream_id, 0)}"
            for stream_id in stream_order
        )
    )
    lines.append(
        f"- Guests: {summary['guests_total']} total | "
        + " | ".join(
            f"{stream_names[stream_id]} {summary['guests_by_pillar'].get(stream_id, 0)}"
            for stream_id in HOST_STREAM_IDS
        )
        + " | "
        + f"Bridge guests {summary['bridge_guests_total']}"
    )
    lines.append(
        f"- Cohosts: {summary['cohosts_total']} total | "
        f"{stream_names['mercouris_duran']} {summary['cohosts_by_pillar']['mercouris_duran']}"
    )
    if summary.get("raw_inputs_by_stream"):
        lines.append(
            "- Expert-lens raw inputs: "
            + " | ".join(
                f"{stream_names[stream_id]} {summary['raw_inputs_by_stream'].get(stream_id, 0)}"
                for stream_id in EXPERT_LENS_STREAMS
            )
        )
    lines.append(
        "- Automation readiness: future daily stream input would need reliable source discovery, provenance capture, "
        "dedupe, raw-input normalization, stream routing, and human review. No scheduler or automatic strategy-codex mutation exists here."
    )
    if summary.get("status_counts"):
        lines.append(
            "- Status mix: "
            + ", ".join(f"{k}={v}" for k, v in summary["status_counts"].items())
        )
    if summary.get("top_themes"):
        lines.append(
            "- Top themes: "
            + ", ".join(f"{tag}={count}" for tag, count in summary["top_themes"])
        )
    lines.append("")
    lines.append("## Stream Notes")
    lines.append("")
    for pillar_id in stream_order:
        top_theme = pillar_theme_counts.get(pillar_id, Counter()).most_common(1)
        theme_text = top_theme[0][0] if top_theme else "none"
        if pillar_id in HOST_STREAM_IDS:
            note = (
                f"- {stream_names[pillar_id]} ({stream_axes[pillar_id]}): "
                f"{summary['episodes_by_pillar'][pillar_id]} episodes, "
                f"{summary['guests_by_pillar'][pillar_id]} guests, top theme {theme_text}. "
                f"Voice: {stream_notes[pillar_id]}"
            )
        else:
            note = (
                f"- {stream_names[pillar_id]} ({stream_axes[pillar_id]}): "
                f"{summary['raw_inputs_by_stream'].get(pillar_id, 0)} raw inputs currently visible to this builder. "
                f"Voice: {stream_notes[pillar_id]}"
            )
        if pillar_id == "mercouris_duran":
            note += (
                f" Source channels: {', '.join(PILLARS[pillar_id]['source_channels'])}."
                f" Cohost lane keeps Alex Christoforou visible without counting him as a guest."
                f" {mercouris_synthetic_sources} episodes use provisional source URLs where the raw-input corpus lacked a canonical link."
            )
        lines.append(note)
    lines.append("")
    lines.append("## Roster")
    lines.append("")
    roster_rows: list[list[str]] = []
    for rank, guest in enumerate(
        sorted(guests, key=lambda node: (-node["episode_count"], node["display_name"].lower())),
        start=1,
    ):
        roster_rows.append(
            [
                str(rank),
                guest["display_name"],
                str(guest["episode_count"]),
                str(guest["counts_by_pillar"].get("nima", 0)),
                str(guest["counts_by_pillar"].get("diesen", 0)),
                str(guest["counts_by_pillar"].get("davis", 0)),
                str(guest["counts_by_pillar"].get("mercouris_duran", 0)),
                "yes" if guest["is_bridge"] else "no",
                guest.get("first_seen") or "-",
                guest.get("last_seen") or "-",
            ]
        )
    lines.append(
        _build_table(
            ["#", "Guest", "Episodes", "Nima", "Diesen", "Davis", "Mercouris", "Bridge", "First", "Last"],
            roster_rows,
        )
    )
    lines.append("")
    lines.append("## Bridge Map")
    lines.append("")
    if bridges:
        bridge_rows: list[list[str]] = []
        for bridge in sorted(
            bridges,
            key=lambda node: (
                -sum(node["episode_counts_by_pillar"].values()),
                node["display_name"].lower(),
            ),
        ):
            counts = bridge["episode_counts_by_pillar"]
            bridge_rows.append(
                [
                    bridge["display_name"],
                    str(counts.get("nima", 0)),
                    str(counts.get("diesen", 0)),
                    str(counts.get("davis", 0)),
                    str(counts.get("mercouris_duran", 0)),
                    ", ".join(stream_names.get(pid, pid) for pid in bridge["pillar_ids"]),
                    _episode_links(bridge["episode_ids_by_pillar"].get("nima", [])),
                    _episode_links(bridge["episode_ids_by_pillar"].get("diesen", [])),
                    _episode_links(bridge["episode_ids_by_pillar"].get("davis", [])),
                    _episode_links(bridge["episode_ids_by_pillar"].get("mercouris_duran", [])),
                ]
            )
        lines.append(
            _build_table(
                [
                    "Guest",
                    "Nima",
                    "Diesen",
                    "Davis",
                    "Mercouris",
                    "Streams",
                    "Nima episodes",
                    "Diesen episodes",
                    "Davis episodes",
                    "Mercouris episodes",
                ],
                bridge_rows,
            )
        )
    else:
        lines.append("- No shared guests in the selected window.")
    lines.append("")
    lines.append("## Cohosts")
    lines.append("")
    cohost_rows: list[list[str]] = []
    for rank, cohost in enumerate(
        sorted(cohosts, key=lambda node: (-node["episode_count"], node["display_name"].lower())),
        start=1,
    ):
        cohost_rows.append(
            [
                str(rank),
                cohost["display_name"],
                str(cohost["episode_count"]),
                ", ".join(stream_names.get(pid, pid) for pid in (cohost.get("pillar_ids") or [])),
                cohost.get("first_seen") or "-",
                cohost.get("last_seen") or "-",
            ]
        )
    if cohost_rows:
        lines.append(_build_table(["#", "Cohost", "Episodes", "Streams", "First", "Last"], cohost_rows))
    else:
        lines.append("- No cohosts in the selected window.")
    lines.append("")
    lines.append("## Motif Clusters")
    lines.append("")
    motif_rows: list[list[str]] = []
    for tag, count in summary.get("top_themes", [])[:8]:
        touched_pillars = sorted(
            stream_names[pillar_id]
            for pillar_id in PILLARS
            if pillar_theme_counts.get(pillar_id, Counter()).get(tag, 0) > 0
        )
        motif_rows.append([tag, str(count), ", ".join(touched_pillars) if touched_pillars else "-"])
    if motif_rows:
        lines.append(_build_table(["Theme", "Episodes", "Streams"], motif_rows))
    else:
        lines.append("- No motif clusters in the selected window.")
    lines.append("")
    lines.append("## Contrapuntal Notes")
    lines.append("")
    lines.append("- Harmony: shared guests and themes indicate where streams are hearing the same strategic material.")
    lines.append("- Tension: stream-specific absences matter; an empty count is a routing signal, not a lower rank.")
    lines.append("- Bridge: recurring guests connect interpretive voices without collapsing them into one synthesis.")
    lines.append("")
    lines.append("## Bridge Roles")
    lines.append("")
    if bridge_roles:
        lines.append(
            _build_table(
                ["Guest", "Role", "Streams", "Episodes", "First", "Last"],
                [[item["guest"], item["role"], item["streams"], item["episodes"], item["first"], item["last"]] for item in bridge_roles[:12]],
            )
        )
    else:
        lines.append("- No bridge roles in the selected window.")
    lines.append("")
    lines.append("## Stream Balance")
    lines.append("")
    for pillar_id in stream_order:
        lines.append(
            f"- {stream_names[pillar_id]} ({stream_axes[pillar_id]}): "
            f"{summary['episodes_by_stream'].get(pillar_id, 0)} episodes, "
            f"{summary['guests_by_pillar'].get(pillar_id, 0)} guests, "
            f"{summary['raw_inputs_by_stream'].get(pillar_id, 0)} expert-lens raw inputs"
        )
    lines.append("")
    lines.append("## Source Provenance")
    lines.append("")
    for stream_id in stream_order:
        lines.append(f"- {stream_names[stream_id]}: {stream_source_labels[stream_id]}")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Themes stay episode-level only in this first pass; bridge relationships are guest-based.")
    lines.append("- The JSON graph carries the full node and edge set; this markdown view is the quick roster, bridge map, and slow-context notes.")
    lines.append("- Cohosts stay separate from guests so the Mercouris stream remains structurally accurate without changing bridge logic.")
    lines.append("")
    lines.append("## Build")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scripts/build_two_pillar_notebook_graph.py")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _print_rel(path: Path) -> None:
    try:
        print(str(path.relative_to(REPO_ROOT)))
    except ValueError:
        print(str(path))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dialogue-index", type=Path, default=DEFAULT_DW_INDEX)
    parser.add_argument("--diesen-index", type=Path, default=DEFAULT_DIESEN_INDEX)
    parser.add_argument("--davis-index", type=Path, default=DEFAULT_DAVIS_INDEX)
    parser.add_argument("--raw-input-root", type=Path, default=DEFAULT_RAW_INPUT_ROOT)
    parser.add_argument("--window-start", type=str, default=WINDOW_START.isoformat())
    parser.add_argument("--window-end", type=str, default=WINDOW_END.isoformat())
    parser.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    dialogue_index = args.dialogue_index.resolve()
    diesen_index = args.diesen_index.resolve()
    davis_index = args.davis_index.resolve()
    raw_input_root = args.raw_input_root.resolve()
    if not dialogue_index.is_file():
        print(f"error: dialogue-index not found: {dialogue_index}", file=sys.stderr)
        return 1
    if not diesen_index.is_file():
        print(f"error: diesen-index not found: {diesen_index}", file=sys.stderr)
        return 1
    if not davis_index.is_file():
        print(f"error: davis-index not found: {davis_index}", file=sys.stderr)
        return 1
    if not raw_input_root.is_dir():
        print(f"error: raw-input-root not found: {raw_input_root}", file=sys.stderr)
        return 1

    window_start = date.fromisoformat(args.window_start)
    window_end = date.fromisoformat(args.window_end)
    graph = build_graph(
        dialogue_index=dialogue_index,
        diesen_index=diesen_index,
        davis_index=davis_index,
        raw_input_root=raw_input_root,
        window_start=window_start,
        window_end=window_end,
    )
    md = render_markdown(graph)

    out_json = args.out_json.resolve()
    out_md = args.out_md.resolve()
    _ensure_parent(out_json)
    _ensure_parent(out_md)
    out_json.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out_md.write_text(md, encoding="utf-8")

    _print_rel(out_json)
    _print_rel(out_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
