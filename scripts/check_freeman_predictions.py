#!/usr/bin/env python3
"""Validate Freeman prediction JSON + public markdown shape and cross-links."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.json"
DEFAULT_MD = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.md"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from freeman_prediction_pilot import (  # noqa: E402
    ALLOWED_PUBLIC_EXCEPTIONS,
    FREEMAN_CAPTURE_MAP,
    FREEMAN_PILOT_EVENT_ORDER,
    FREEMAN_PREDICTIONS_JSON,
    JAN_21_CAPTURE,
    contains_prediction_object,
    is_complete_sentence,
    load_capture_map,
    load_public_map,
    parse_capture_frontmatter,
    resolve_prediction_object_terms,
    validate_capture_row,
    validate_excerpt_quality,
    word_count,
)

EVENT_REQUIRED = (
    "event_id",
    "public_title",
    "technical_question",
    "status",
    "latest_stance",
    "record",
    "record_label",
    "anchor_excerpt",
    "anchor_citation",
    "anchor_context_note",
    "public_summary",
    "why_it_matters",
    "event_kind",
    "scoring_policy",
    "appearances",
)
APPEARANCE_REQUIRED = (
    "date",
    "speech_act",
    "stance",
    "public_excerpt",
    "public_excerpt_short",
    "capture",
    "citation",
    "appearance_label",
    "context_note",
)
CITATION_REQUIRED = ("title", "channel", "pub_date", "youtube_url", "capture")
FORBIDDEN_HEADING_TERMS = ("event_id", "speech_act", "appearances", "crawl manifest")
DISALLOWED_EXCERPT_EXCEPTIONS = frozenset(
    {"under_30_verified", "summary_grade_capture", "stub_capture", "rhetorical_analogy"}
)
DEFAULT_CAPTURE_MAP = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-capture-map.json"
DEFAULT_PUBLIC_MAP = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-public-map.json"


def capture_map_lookup(path: Path) -> dict[tuple[str, str], dict]:
    rows = load_capture_map(path)
    return {(str(r["event_id"]), str(r["capture"])): r for r in rows}


def check_capture_map(
    capture_map_path: Path,
    public_map_path: Path,
) -> list[str]:
    issues: list[str] = []
    try:
        public_map = load_public_map(public_map_path)
        rows = load_capture_map(capture_map_path)
    except (FileNotFoundError, ValueError) as exc:
        return [str(exc)]

    anchors = {
        event_id: str(public_map[event_id].get("anchor_capture") or "")
        for event_id in FREEMAN_PILOT_EVENT_ORDER
    }

    for row in rows:
        event_id = str(row.get("event_id") or "")
        exception = row.get("excerpt_exception")
        if exception in DISALLOWED_EXCERPT_EXCEPTIONS:
            issues.append(f"{event_id}: disallowed excerpt_exception {exception!r}")
        if exception and exception not in ALLOWED_PUBLIC_EXCEPTIONS:
            issues.append(f"{event_id}: unsupported excerpt_exception {exception!r}")

        cap_path = REPO_ROOT / str(row.get("capture") or "").replace("\\", "/")
        if not cap_path.is_file():
            issues.append(f"{event_id}: missing capture {row.get('capture')}")
            continue
        _, body = parse_capture_frontmatter(cap_path.read_text(encoding="utf-8"))
        public_event = public_map.get(event_id, {})
        is_anchor = str(row.get("capture") or "") == anchors.get(event_id, "")
        label = f"{event_id} @ {row.get('capture')}"
        for err in validate_capture_row(row, body, public_event, is_anchor=is_anchor):
            issues.append(f"{label}: {err}")

    return issues


def check_json(
    path: Path,
    *,
    public_map_path: Path,
    capture_map_path: Path,
) -> list[str]:
    issues: list[str] = []
    if not path.is_file():
        return [f"missing {path.relative_to(REPO_ROOT)}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        public_map = load_public_map(public_map_path)
        row_lookup = capture_map_lookup(capture_map_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]

    meta = data.get("_meta") or {}
    if meta.get("generated") is not True:
        issues.append("_meta.generated must be true")
    if meta.get("speaker") != "freeman":
        issues.append("_meta.speaker must be freeman")
    if data.get("speaker") != "freeman":
        issues.append("speaker must be freeman")

    events = data.get("events")
    if not isinstance(events, list) or not events:
        issues.append("events must be a non-empty list")
        return issues

    event_ids = [e.get("event_id") for e in events if isinstance(e, dict)]
    if event_ids != list(FREEMAN_PILOT_EVENT_ORDER):
        issues.append(f"expected event order {list(FREEMAN_PILOT_EVENT_ORDER)!r}; got {event_ids!r}")

    jan21_events: set[str] = set()

    for event in events:
        if not isinstance(event, dict):
            issues.append("each event must be an object")
            continue
        event_id = str(event.get("event_id") or "")
        for field in EVENT_REQUIRED:
            if field not in event:
                issues.append(f"{event_id or '?'}: missing field {field}")
        if not str(event.get("anchor_excerpt") or "").strip():
            issues.append(f"{event_id}: empty anchor_excerpt")
        public_event = public_map.get(event_id, {})
        anchor_capture = str(public_event.get("anchor_capture") or "")
        anchor_row = row_lookup.get((event_id, anchor_capture), {})
        anchor_terms = resolve_prediction_object_terms(anchor_row, public_event)
        issues.extend(
            validate_excerpt_quality(
                event_id=event_id,
                excerpt=str(event.get("anchor_excerpt") or ""),
                min_words=40,
                exception=anchor_row.get("excerpt_exception"),
                context_note=event.get("anchor_context_note"),
                object_terms=anchor_terms,
                is_anchor=True,
            )
        )
        anchor_citation = event.get("anchor_citation")
        if not isinstance(anchor_citation, dict):
            issues.append(f"{event_id}: anchor_citation must be an object")
        else:
            for field in CITATION_REQUIRED:
                if field not in anchor_citation:
                    issues.append(f"{event_id}: anchor_citation missing {field}")
        appearances = event.get("appearances")
        if not isinstance(appearances, list):
            issues.append(f"{event_id}: appearances must be a list")
            continue
        for app in appearances:
            if not isinstance(app, dict):
                issues.append(f"{event_id}: appearance must be object")
                continue
            for field in APPEARANCE_REQUIRED:
                if field not in app:
                    issues.append(f"{event_id}: appearance missing {field}")
            if not str(app.get("public_excerpt") or "").strip():
                issues.append(f"{event_id}: appearance missing public_excerpt text")
            capture = str(app.get("capture") or "")
            app_row = row_lookup.get((event_id, capture), {})
            app_terms = resolve_prediction_object_terms(app_row, public_event)
            issues.extend(
                validate_excerpt_quality(
                    event_id=event_id,
                    excerpt=str(app.get("public_excerpt") or ""),
                    min_words=30,
                    exception=app_row.get("excerpt_exception"),
                    context_note=app.get("context_note"),
                    object_terms=app_terms,
                    is_anchor=False,
                )
            )
            if capture.endswith(JAN_21_CAPTURE.split("/")[-1]):
                jan21_events.add(event_id)
            citation = app.get("citation")
            if isinstance(citation, dict):
                for field in CITATION_REQUIRED:
                    if field not in citation:
                        issues.append(f"{event_id}: citation missing {field}")

    if len(jan21_events) < 2:
        issues.append("Jan 21 capture must appear in at least 2 event appearances")

    return issues


def check_markdown(path: Path, *, public_titles: list[str]) -> list[str]:
    issues: list[str] = []
    if not path.is_file():
        return [f"missing {path.relative_to(REPO_ROOT)}"]
    text = path.read_text(encoding="utf-8")

    required_strings = [
        "# Chas Freeman Prediction Record",
        "## At a Glance",
        "## Method",
        "<details>",
        "<summary>Source trail</summary>",
        "freeman-prediction-capture-map.json",
        "— Chas Freeman,",
    ]
    for needle in required_strings:
        if needle not in text:
            issues.append(f"markdown missing {needle!r}")

    if not re.search(r"^>\s+\"", text, re.M):
        issues.append("markdown missing blockquote")

    for title in public_titles:
        if title not in text:
            issues.append(f"markdown missing public title: {title!r}")

    for line in text.splitlines():
        if line.startswith("## ") and not line.startswith("## At a Glance") and line != "## Method":
            if line.startswith("## How to Read"):
                continue
            lowered = line.casefold()
            for term in FORBIDDEN_HEADING_TERMS:
                if term in lowered:
                    issues.append(f"forbidden machine term in heading: {line}")

    return issues


def run_check(
    *,
    json_path: Path,
    md_path: Path,
    capture_map_path: Path = DEFAULT_CAPTURE_MAP,
    public_map_path: Path = DEFAULT_PUBLIC_MAP,
) -> tuple[list[str], list[str]]:
    issues = check_capture_map(capture_map_path, public_map_path)
    issues.extend(
        check_json(
            json_path,
            public_map_path=public_map_path,
            capture_map_path=capture_map_path,
        )
    )
    public_titles: list[str] = []
    if json_path.is_file():
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            public_titles = [
                str(e.get("public_title") or "")
                for e in data.get("events", [])
                if isinstance(e, dict)
            ]
        except json.JSONDecodeError:
            pass
    issues.extend(check_markdown(md_path, public_titles=public_titles))
    return issues, []


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", type=Path, default=DEFAULT_JSON)
    ap.add_argument("--md", type=Path, default=DEFAULT_MD)
    ap.add_argument("--capture-map", type=Path, default=DEFAULT_CAPTURE_MAP)
    ap.add_argument("--public-map", type=Path, default=DEFAULT_PUBLIC_MAP)
    args = ap.parse_args()

    issues, warnings = run_check(
        json_path=args.json,
        md_path=args.md,
        capture_map_path=args.capture_map,
        public_map_path=args.public_map,
    )
    for line in warnings:
        print(f"[warn] {line}")
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"check_freeman_predictions: {len(issues)} violation(s)", file=sys.stderr)
        return 1
    print("[ok] freeman predictions valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
