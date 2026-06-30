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

from freeman_prediction_pilot import FREEMAN_PILOT_EVENT_ORDER, JAN_21_CAPTURE  # noqa: E402

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
)
CITATION_REQUIRED = ("title", "channel", "pub_date", "youtube_url", "capture")
FORBIDDEN_HEADING_TERMS = ("event_id", "speech_act", "appearances", "crawl manifest")


def check_json(path: Path) -> list[str]:
    issues: list[str] = []
    if not path.is_file():
        return [f"missing {path.relative_to(REPO_ROOT)}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

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


def run_check(*, json_path: Path, md_path: Path) -> tuple[list[str], list[str]]:
    issues = check_json(json_path)
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
    args = ap.parse_args()

    issues, warnings = run_check(json_path=args.json, md_path=args.md)
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
