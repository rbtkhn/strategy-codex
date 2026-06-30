"""Shared prediction event registry, note parsing, and artifact builders."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
EVENT_REGISTRY_PATH = REPO_ROOT / "statecraft" / "data" / "event-registry.json"
PREDICTIONS_DIR = REPO_ROOT / "statecraft" / "notes" / "predictions"

STANCES = frozenset({"yes", "no", "conditional", "uncertain"})
CONFIDENCES = frozenset({"low", "medium", "high"})
EVENT_STATUSES = frozenset({"open", "resolved", "void", "deprecated"})
PREDICTION_STATUSES = frozenset({"pending", "resolved"})
RESOLVED_EVENT_OUTCOMES = frozenset({"yes", "no"})
TERMINAL_EVENT_STATUSES = frozenset({"resolved", "void", "deprecated"})
STANCE_KEYS = ("yes", "no", "conditional", "uncertain")
MAX_GINI = 0.75
SHIFT_TYPES = frozenset({"flip", "qualification_shift", "certainty_shift", "stance_change"})
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

EVENT_ID_RE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
FENCED_YAML_RE = re.compile(r"```yaml\r?\n(.*?)```", re.DOTALL | re.IGNORECASE)

PREDICTION_REQUIRED_FIELDS = ("event_id", "speaker", "date_made", "stance", "source", "status")
REGISTRY_PREDICTION_FIELDS = (
    "file",
    "speaker",
    "event_id",
    "stance",
    "confidence",
    "date_made",
    "source",
    "prediction_status",
    "event_status",
    "event_outcome",
)

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from yaml_compat import safe_load_text  # noqa: E402

@dataclass
class PredictionNote:
    file: str
    path: Path
    event_id: str
    speaker: str
    date_made: str
    stance: str
    source: str
    confidence: str | None = None
    speech_act: str | None = None

def repo_relative(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix().replace("\\", "/")

def _coerce_stance(value: Any) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value or "").strip()

def normalize_prediction_frontmatter(data: dict[str, Any]) -> dict[str, Any]:
    """Coerce YAML quirks before JSON Schema validation."""
    out = dict(data)
    if "stance" in out:
        out["stance"] = _coerce_stance(out.get("stance"))
    if "date_made" in out and out["date_made"] is not None:
        out["date_made"] = str(out["date_made"])
    if "status" in out and out["status"] is not None:
        out["status"] = str(out["status"]).strip()
    return out

def parse_frontmatter_dict(text: str, *, feature: str) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    fm = FRONTMATTER_RE.match(text.lstrip("\ufeff"))
    if fm:
        block = safe_load_text(fm.group(1), feature=feature)
        if isinstance(block, dict):
            merged.update(block)
    fence = FENCED_YAML_RE.search(text)
    if fence:
        block = safe_load_text(fence.group(1), feature=f" fenced yaml {feature}")
        if isinstance(block, dict):
            for key, value in block.items():
                if key not in merged or merged[key] in (None, "", []):
                    merged[key] = value
    return merged

def load_event_registry(path: Path | None = None) -> dict[str, dict[str, Any]]:
    registry_path = path or EVENT_REGISTRY_PATH
    if not registry_path.is_file():
        raise FileNotFoundError(f"missing event registry: {repo_relative(registry_path)}")
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("event registry must be a JSON object")
    return data

def validate_event(event_id: str, event: Any) -> list[str]:
    issues: list[str] = []
    if not EVENT_ID_RE.fullmatch(event_id):
        issues.append(f"{event_id}: invalid event_id format (lowercase snake_case required)")
    if not isinstance(event, dict):
        issues.append(f"{event_id}: event must be an object")
        return issues

    for field in ("question", "resolution_criteria", "status"):
        val = event.get(field)
        if val is None or not str(val).strip():
            issues.append(f"{event_id}: missing required field `{field}`")

    status = str(event.get("status") or "").strip()
    if status and status not in EVENT_STATUSES:
        issues.append(f"{event_id}: invalid status `{status}`")

    outcome = event.get("outcome")
    if status == "resolved":
        if outcome not in RESOLVED_EVENT_OUTCOMES:
            issues.append(f"{event_id}: resolved event requires outcome yes or no")
    elif outcome is not None:
        issues.append(f"{event_id}: outcome must be null unless status is resolved")

    return issues

def expected_prediction_status(event_status: str) -> str:
    if event_status == "open":
        return "pending"
    if event_status in TERMINAL_EVENT_STATUSES:
        return "resolved"
    return "pending"

def validate_prediction_fields(
    data: dict[str, Any],
    rel: str,
    *,
    events: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    issues: list[str] = []
    note_type = str(data.get("note_type") or "").strip()
    if note_type != "prediction":
        return issues

    for field in PREDICTION_REQUIRED_FIELDS:
        val = data.get(field)
        if val is None or not str(val).strip():
            issues.append(f"{rel}: missing required field `{field}`")

    status = str(data.get("status") or "").strip()
    if status and status not in PREDICTION_STATUSES:
        issues.append(f"{rel}: invalid status `{status}`")

    stance = _coerce_stance(data.get("stance"))
    if stance and stance not in STANCES:
        issues.append(f"{rel}: invalid stance `{stance}`")

    confidence = data.get("confidence")
    if confidence is not None and str(confidence).strip():
        conf = str(confidence).strip()
        if conf not in CONFIDENCES:
            issues.append(f"{rel}: invalid confidence `{conf}`")

    authority = str(data.get("authority_level") or "").strip()
    if authority == "shelf-native":
        issues.append(f"{rel}: prediction notes must not be shelf-native (explicit review required)")

    essay = data.get("essay_candidate")
    if essay is True or str(essay).strip().lower() == "true":
        issues.append(f"{rel}: prediction notes must not be essay_candidate")

    speech_act = str(data.get("speech_act") or "").strip()
    if speech_act and speech_act not in SPEECH_ACTS:
        issues.append(f"{rel}: invalid speech_act `{speech_act}`")

    if events is not None and status in PREDICTION_STATUSES:
        event_id = str(data.get("event_id") or "").strip()
        event = events.get(event_id)
        if event is None:
            return issues
        event_status = str(event.get("status") or "").strip()
        expected = expected_prediction_status(event_status)
        if status != expected:
            issues.append(
                f"{rel}: status `{status}` inconsistent with event `{event_id}` "
                f"(event status `{event_status}` expects `{expected}`)"
            )
        if status == "resolved" and event_status not in TERMINAL_EVENT_STATUSES:
            issues.append(f"{rel}: resolved prediction requires resolved/void/deprecated event")

    return issues

def iter_prediction_note_paths(*, predictions_dir: Path | None = None) -> list[Path]:
    root = predictions_dir or PREDICTIONS_DIR
    if not root.is_dir():
        return []
    return sorted(root.glob("*.md"))

def parse_prediction_note(path: Path, text: str | None = None) -> PredictionNote | None:
    rel = repo_relative(path)
    body = text if text is not None else path.read_text(encoding="utf-8", errors="replace")
    data = parse_frontmatter_dict(body, feature=rel)
    note_type = str(data.get("note_type") or "").strip()
    if note_type != "prediction":
        return None

    event_id = str(data.get("event_id") or "").strip()
    speaker = str(data.get("speaker") or "").strip()
    date_made = str(data.get("date_made") or "").strip()
    stance = _coerce_stance(data.get("stance"))
    source = str(data.get("source") or "").strip()
    confidence_raw = data.get("confidence")
    confidence = str(confidence_raw).strip() if confidence_raw is not None and str(confidence_raw).strip() else None
    speech_act_raw = data.get("speech_act")
    speech_act = str(speech_act_raw).strip() if speech_act_raw is not None and str(speech_act_raw).strip() else None

    return PredictionNote(
        file=rel,
        path=path,
        event_id=event_id,
        speaker=speaker,
        date_made=date_made,
        stance=stance,
        source=source,
        confidence=confidence,
        speech_act=speech_act,
    )

def collect_prediction_notes(*, predictions_dir: Path | None = None) -> list[PredictionNote]:
    notes: list[PredictionNote] = []
    for path in iter_prediction_note_paths(predictions_dir=predictions_dir):
        parsed = parse_prediction_note(path)
        if parsed is not None:
            notes.append(parsed)
    return notes

def prediction_status_for_event(event_status: str) -> str:
    return expected_prediction_status(event_status)

def join_prediction_to_event(
    note: PredictionNote,
    events: dict[str, dict[str, Any]],
    *,
    note_status: str | None = None,
) -> dict[str, Any]:
    event = events.get(note.event_id, {})
    event_status = str(event.get("status") or "open")
    event_outcome = event.get("outcome")
    derived_status = prediction_status_for_event(event_status)
    prediction_status = note_status if note_status in PREDICTION_STATUSES else derived_status
    row: dict[str, Any] = {
        "file": note.file,
        "speaker": note.speaker,
        "event_id": note.event_id,
        "stance": note.stance,
        "confidence": note.confidence,
        "date_made": note.date_made,
        "source": note.source,
        "prediction_status": prediction_status,
        "event_status": event_status,
        "event_outcome": event_outcome,
    }
    if note.speech_act:
        row["speech_act"] = note.speech_act
    return row

def gini_impurity(counts: dict[str, int]) -> tuple[float, float]:
    total = sum(counts.get(key, 0) for key in STANCE_KEYS)
    if total <= 0:
        return 0.0, 0.0
    raw = 1.0
    for key in STANCE_KEYS:
        share = counts.get(key, 0) / total
        raw -= share * share
    normalized = raw / MAX_GINI if MAX_GINI else 0.0
    return round(raw, 4), round(normalized, 4)

def stance_distribution(rows: list[dict[str, Any]]) -> dict[str, int]:
    dist = {key: 0 for key in STANCE_KEYS}
    for row in rows:
        stance = str(row.get("stance") or "")
        if stance in dist:
            dist[stance] += 1
    return dist

def latest_by_speaker(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in sorted(rows, key=lambda r: (r.get("date_made", ""), r.get("file", ""))):
        speaker = str(row.get("speaker") or "")
        if speaker:
            latest[speaker] = row
    return latest

def classify_shift(from_stance: str, to_stance: str) -> str:
    if from_stance == to_stance:
        raise ValueError("classify_shift requires distinct stances")
    hard = {"yes", "no"}
    if from_stance in hard and to_stance in hard:
        return "flip"
    if (from_stance in hard and to_stance == "conditional") or (
        from_stance == "conditional" and to_stance in hard
    ):
        return "qualification_shift"
    if to_stance == "uncertain" or from_stance == "uncertain":
        return "certainty_shift"
    return "stance_change"

def build_meta(*, source: str) -> dict[str, Any]:
    return {
        "generated": True,
        "do_not_edit": True,
        "source": source,
    }

def build_registry_payload(
    *,
    events_path: Path | None = None,
    predictions_dir: Path | None = None,
) -> dict[str, Any]:
    events = load_event_registry(events_path)
    predictions: list[dict[str, Any]] = []
    errors: list[str] = []

    for note in collect_prediction_notes(predictions_dir=predictions_dir):
        if note.event_id not in events:
            errors.append(f"{note.file}: unknown event_id `{note.event_id}`")
            continue
        text = note.path.read_text(encoding="utf-8", errors="replace")
        data = parse_frontmatter_dict(text, feature=note.file)
        note_status = str(data.get("status") or "").strip() or None
        predictions.append(join_prediction_to_event(note, events, note_status=note_status))

    if errors:
        raise ValueError("\n".join(errors))

    predictions.sort(key=lambda row: (row["event_id"], row["speaker"], row["date_made"], row["file"]))
    return {
        "_meta": build_meta(source="scripts/build_prediction_registry.py"),
        "predictions": predictions,
    }

def score_prediction(row: dict[str, Any], event: dict[str, Any]) -> str | None:
    if str(event.get("status") or "") != "resolved":
        return None
    stance = str(row.get("stance") or "")
    if stance not in {"yes", "no"}:
        return "unscored"
    outcome = event.get("outcome")
    if outcome not in RESOLVED_EVENT_OUTCOMES:
        return "unscored"
    return "correct" if stance == outcome else "incorrect"

def build_metrics_payload(
    registry: dict[str, Any],
    events: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    voices: dict[str, dict[str, Any]] = {}

    for row in registry.get("predictions") or []:
        speaker = str(row.get("speaker") or "")
        if not speaker:
            continue
        bucket = voices.setdefault(
            speaker,
            {
                "total": 0,
                "resolved": 0,
                "scorable": 0,
                "correct": 0,
                "incorrect": 0,
                "unscored": 0,
                "accuracy": None,
            },
        )
        bucket["total"] += 1
        event = events.get(str(row.get("event_id") or ""), {})
        if str(event.get("status") or "") != "resolved":
            continue
        bucket["resolved"] += 1
        result = score_prediction(row, event)
        if result == "correct":
            bucket["scorable"] += 1
            bucket["correct"] += 1
        elif result == "incorrect":
            bucket["scorable"] += 1
            bucket["incorrect"] += 1
        elif result == "unscored":
            bucket["unscored"] += 1

    for bucket in voices.values():
        scorable = bucket["scorable"]
        if scorable > 0:
            bucket["accuracy"] = round(bucket["correct"] / scorable, 4)

    return {
        "_meta": build_meta(source="scripts/build_prediction_metrics.py"),
        "voices": dict(sorted(voices.items())),
    }

def build_disagreement_payload(registry: dict[str, Any]) -> dict[str, Any]:
    by_event: dict[str, list[dict[str, Any]]] = {}
    for row in registry.get("predictions") or []:
        event_id = str(row.get("event_id") or "")
        if event_id:
            by_event.setdefault(event_id, []).append(row)

    events_out: dict[str, Any] = {}
    for event_id in sorted(by_event):
        rows = by_event[event_id]
        pred_dist = stance_distribution(rows)
        pred_raw, pred_norm = gini_impurity(pred_dist)
        latest_rows = list(latest_by_speaker(rows).values())
        voice_dist = stance_distribution(latest_rows)
        voice_raw, voice_norm = gini_impurity(voice_dist)
        events_out[event_id] = {
            "prediction_level": {
                "total_predictions": sum(pred_dist.values()),
                "distribution": pred_dist,
                "disagreement_score_raw": pred_raw,
                "disagreement_score_normalized": pred_norm,
            },
            "latest_voice_level": {
                "total_voices": sum(1 for v in voice_dist.values() if v > 0),
                "distribution": voice_dist,
                "disagreement_score_raw": voice_raw,
                "disagreement_score_normalized": voice_norm,
            },
        }

    return {
        "_meta": build_meta(source="scripts/build_prediction_disagreement.py"),
        "events": events_out,
    }

def build_timeline_payload(registry: dict[str, Any]) -> dict[str, Any]:
    by_event: dict[str, list[dict[str, Any]]] = {}
    for row in registry.get("predictions") or []:
        event_id = str(row.get("event_id") or "")
        if event_id:
            by_event.setdefault(event_id, []).append(row)

    events_out: dict[str, Any] = {}
    for event_id in sorted(by_event):
        rows = sorted(by_event[event_id], key=lambda r: (r.get("date_made", ""), r.get("file", "")))
        entries: list[dict[str, Any]] = []
        for row in rows:
            entry: dict[str, Any] = {
                "date": row["date_made"],
                "speaker": row["speaker"],
                "stance": row["stance"],
                "confidence": row.get("confidence"),
                "file": row["file"],
                "source": row["source"],
            }
            if row.get("speech_act"):
                entry["speech_act"] = row["speech_act"]
            entries.append(entry)

        latest_map: dict[str, dict[str, Any]] = {}
        for speaker, row in latest_by_speaker(rows).items():
            latest_map[speaker] = {
                "date": row["date_made"],
                "stance": row["stance"],
                "confidence": row.get("confidence"),
                "file": row["file"],
                "source": row["source"],
            }

        shifts: dict[str, list[dict[str, Any]]] = {}
        restatements: dict[str, list[dict[str, Any]]] = {}
        reviews: dict[str, list[dict[str, Any]]] = {}
        by_speaker: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            by_speaker.setdefault(str(row["speaker"]), []).append(row)

        for speaker, speaker_rows in by_speaker.items():
            speaker_shifts: list[dict[str, Any]] = []
            speaker_restatements: list[dict[str, Any]] = []
            speaker_reviews: list[dict[str, Any]] = []
            for prev, curr in zip(speaker_rows, speaker_rows[1:]):
                from_stance = str(prev.get("stance") or "")
                to_stance = str(curr.get("stance") or "")
                if from_stance != to_stance:
                    speaker_shifts.append(
                        {
                            "type": classify_shift(from_stance, to_stance),
                            "from": from_stance,
                            "to": to_stance,
                            "from_date": prev.get("date_made"),
                            "to_date": curr.get("date_made"),
                            "from_file": prev.get("file"),
                            "to_file": curr.get("file"),
                        }
                    )
                elif str(curr.get("speech_act") or "") == "restated" or (
                    not curr.get("speech_act") and from_stance == to_stance
                ):
                    speaker_restatements.append(
                        {
                            "from_date": prev.get("date_made"),
                            "to_date": curr.get("date_made"),
                            "stance": to_stance,
                            "from_file": prev.get("file"),
                            "to_file": curr.get("file"),
                            "speech_act": "restated",
                        }
                    )
            for row in speaker_rows:
                act = str(row.get("speech_act") or "")
                if act in REVIEW_SPEECH_ACTS:
                    speaker_reviews.append(
                        {
                            "date": row.get("date_made"),
                            "speech_act": act,
                            "stance": row.get("stance"),
                            "file": row.get("file"),
                            "source": row.get("source"),
                        }
                    )
            if speaker_shifts:
                shifts[speaker] = speaker_shifts
            if speaker_restatements:
                restatements[speaker] = speaker_restatements
            if speaker_reviews:
                reviews[speaker] = speaker_reviews

        events_out[event_id] = {
            "entries": entries,
            "latest_by_speaker": dict(sorted(latest_map.items())),
            "shifts": dict(sorted(shifts.items())),
            "restatements": dict(sorted(restatements.items())),
            "reviews": dict(sorted(reviews.items())),
        }

    return {
        "_meta": build_meta(source="scripts/build_prediction_timeline.py"),
        "events": events_out,
    }

def render_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
