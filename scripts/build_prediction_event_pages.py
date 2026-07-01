#!/usr/bin/env python3
"""Generate cross-voice prediction event pages and stance matrix from SSOT artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "statecraft" / "data" / "event-registry.json"
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
DEFAULT_DISAGREEMENT = REPO_ROOT / "runtime" / "artifacts" / "prediction-disagreement.json"
EVENTS_DIR = REPO_ROOT / "statecraft" / "predictions" / "events"
MATRIX_PATH = REPO_ROOT / "statecraft" / "predictions" / "cross-voice-matrix.md"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import load_event_registry  # noqa: E402
from voice_prediction_pilot import VOICE_REGISTRY, get_voice_config  # noqa: E402


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_voice_shelves() -> dict[str, dict[str, Any]]:
    shelves: dict[str, dict[str, Any]] = {}
    for speaker in VOICE_REGISTRY:
        config = get_voice_config(speaker)
        if not config.predictions_json_path.is_file():
            continue
        shelves[speaker] = json.loads(config.predictions_json_path.read_text(encoding="utf-8"))
    return shelves


def event_voice_row(
    event_id: str,
    speaker: str,
    shelf: dict[str, Any],
) -> dict[str, Any] | None:
    for event in shelf.get("events") or []:
        if str(event.get("event_id")) == event_id:
            return {
                "speaker": speaker,
                "position": event.get("public_position"),
                "first_seen": event.get("first_seen"),
                "latest_seen": event.get("latest_seen"),
                "record_label": event.get("record_label"),
                "status": event.get("status"),
            }
    return None


def render_event_page(
    event_id: str,
    registry_event: dict[str, Any],
    *,
    voice_rows: list[dict[str, Any]],
    disagreement: dict[str, Any] | None,
) -> str:
    question = registry_event.get("question") or event_id
    lines = [
        "<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. build_prediction_event_pages.py -->",
        "",
        f"# Event: {question}",
        "",
        f"**Event ID:** `{event_id}`  ",
        f"**Registry status:** {registry_event.get('status')}  ",
        "",
        "## Cross-voice summary",
        "",
        "| Speaker | Position | First seen | Latest seen | Record |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in voice_rows:
        lines.append(
            "| "
            f"{row['speaker']} | "
            f"{row.get('position') or '—'} | "
            f"{row.get('first_seen') or '—'} | "
            f"{row.get('latest_seen') or '—'} | "
            f"{row.get('record_label') or '—'} |"
        )
    if disagreement:
        latest = disagreement.get("latest_voice_level") or {}
        lines.extend(
            [
                "",
                "## Disagreement (latest voice level)",
                "",
                f"- **Voices tracked:** {latest.get('total_voices', 0)}",
                f"- **Distribution:** {latest.get('distribution')}",
                f"- **Score (normalized):** {latest.get('disagreement_score_normalized')}",
            ]
        )
    lines.extend(["", "## Registry", "", f"- **Falsifier:** {registry_event.get('falsifier') or '—'}", ""])
    return "\n".join(lines)


def render_matrix(
    registry: dict[str, dict[str, Any]],
    shelves: dict[str, dict[str, Any]],
) -> str:
    speakers = sorted(shelves.keys())
    lines = [
        "<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. build_prediction_event_pages.py -->",
        "",
        "# Cross-voice prediction matrix",
        "",
        "Generated from event registry + voice shelf JSON companions.",
        "",
        "| Event | " + " | ".join(speakers) + " |",
        "| --- | " + " | ".join(["---"] * len(speakers)) + " |",
    ]
    for event_id in sorted(registry.keys()):
        if not isinstance(registry.get(event_id), dict):
            continue
        cells = []
        for speaker in speakers:
            shelf = shelves.get(speaker) or {}
            row = event_voice_row(event_id, speaker, shelf)
            cells.append(str((row or {}).get("position") or "—"))
        short_q = str(registry[event_id].get("question") or event_id)[:80]
        lines.append(f"| {short_q} | " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def build_outputs(
    *,
    registry_path: Path,
    timeline_path: Path,
    disagreement_path: Path,
    event_filter: str | None = None,
) -> tuple[dict[str, str], str]:
    registry = load_event_registry(registry_path)
    disagreement_doc = load_json(disagreement_path).get("events") or {}
    shelves = load_voice_shelves()

    event_pages: dict[str, str] = {}
    for event_id, registry_event in sorted(registry.items()):
        if event_filter and event_id != event_filter:
            continue
        voice_rows = []
        for speaker, shelf in sorted(shelves.items()):
            row = event_voice_row(event_id, speaker, shelf)
            if row:
                voice_rows.append(row)
        if not voice_rows and event_filter:
            voice_rows = []
        event_pages[event_id] = render_event_page(
            event_id,
            registry_event,
            voice_rows=voice_rows,
            disagreement=disagreement_doc.get(event_id),
        )

    matrix = render_matrix(registry, shelves)
    return event_pages, matrix


def check_outputs(
    *,
    registry_path: Path,
    timeline_path: Path,
    disagreement_path: Path,
    events_dir: Path,
    matrix_path: Path,
) -> int:
    expected_pages, expected_matrix = build_outputs(
        registry_path=registry_path,
        timeline_path=timeline_path,
        disagreement_path=disagreement_path,
    )
    errors = 0
    for event_id, content in expected_pages.items():
        path = events_dir / f"{event_id}.md"
        if not path.is_file():
            print(f"error: missing {path.relative_to(REPO_ROOT)}", file=sys.stderr)
            errors += 1
            continue
        if path.read_text(encoding="utf-8") != content:
            print(f"error: stale {path.relative_to(REPO_ROOT)}", file=sys.stderr)
            errors += 1
    if matrix_path.is_file():
        if matrix_path.read_text(encoding="utf-8") != expected_matrix:
            print(f"error: stale {matrix_path.relative_to(REPO_ROOT)}", file=sys.stderr)
            errors += 1
    else:
        print(f"error: missing {matrix_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        errors += 1
    if errors:
        return 1
    print("[ok] prediction event pages match generator output")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument("--disagreement", type=Path, default=DEFAULT_DISAGREEMENT)
    ap.add_argument("--events-dir", type=Path, default=EVENTS_DIR)
    ap.add_argument("--matrix", type=Path, default=MATRIX_PATH)
    ap.add_argument("--event", help="build single event page only")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        return check_outputs(
            registry_path=args.registry,
            timeline_path=args.timeline,
            disagreement_path=args.disagreement,
            events_dir=args.events_dir,
            matrix_path=args.matrix,
        )

    pages, matrix = build_outputs(
        registry_path=args.registry,
        timeline_path=args.timeline,
        disagreement_path=args.disagreement,
        event_filter=args.event,
    )
    args.events_dir.mkdir(parents=True, exist_ok=True)
    for event_id, content in pages.items():
        out = args.events_dir / f"{event_id}.md"
        out.write_text(content, encoding="utf-8")
    args.matrix.parent.mkdir(parents=True, exist_ok=True)
    args.matrix.write_text(matrix, encoding="utf-8")
    print(f"[ok] wrote {len(pages)} event page(s) and {args.matrix.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
