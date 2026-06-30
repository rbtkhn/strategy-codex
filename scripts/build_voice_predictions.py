#!/usr/bin/env python3
"""Build voice prediction record — colocated JSON + public markdown on the voice shelf."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_freeman_index import host_short, parse_head, pub_date_key  # noqa: E402
from prediction_lib import (  # noqa: E402
    REPO_ROOT as LIB_ROOT,
    load_event_registry,
)
from voice_prediction_pilot import (  # noqa: E402
    VoiceConfig,
    derive_record,
    get_voice_config,
    load_capture_map,
    load_public_map,
    parse_capture_frontmatter,
    select_anchor_appearance,
    shorten_quote,
    source_citation,
    validate_capture_row,
)

assert LIB_ROOT == REPO_ROOT


def appearance_label(citation: dict[str, str], *, date: str | None = None) -> str:
    pub = str(date or citation.get("pub_date") or "")
    channel = str(citation.get("channel") or "")
    host = host_short({"channel": channel, "host": channel}, Path(citation["capture"]))
    return f"{pub} {host}".strip()


def format_exact_words_cell(app: dict[str, Any]) -> str:
    quote = (
        app["public_excerpt_short"]
        if len(app["public_excerpt"]) > 120
        else app["public_excerpt"]
    )
    note = str(app.get("context_note") or "").strip()
    if note:
        return f'{note} — "{quote}"'
    return f'"{quote}"'


def build_appearances_for_event(
    rows: list[dict[str, Any]],
    public_event: dict[str, Any],
    *,
    anchor_capture: str | None,
    default_channel: str,
) -> list[dict[str, Any]]:
    appearances: list[dict[str, Any]] = []
    for row in rows:
        capture_path = REPO_ROOT / str(row["capture"]).replace("\\", "/")
        text = capture_path.read_text(encoding="utf-8")
        _, body = parse_capture_frontmatter(text)
        is_anchor = str(row.get("capture") or "") == str(anchor_capture or "")
        errors = validate_capture_row(
            row,
            body,
            public_event,
            is_anchor=is_anchor,
        )
        if errors:
            raise ValueError(
                f"{row['event_id']} @ {row['capture']}: " + "; ".join(errors)
            )
        citation = source_citation(capture_path, default_channel=default_channel)
        excerpt = str(row["public_excerpt"])
        appearance_date = str(row.get("appearance_date") or citation["pub_date"] or "")
        appearances.append(
            {
                "date": appearance_date,
                "speech_act": row["speech_act"],
                "stance": row["stance"],
                "public_excerpt": excerpt,
                "public_excerpt_short": shorten_quote(excerpt),
                "capture": row["capture"],
                "citation": citation,
                "appearance_label": appearance_label(citation, date=appearance_date),
                "context_note": row.get("context_note"),
            }
        )
    appearances.sort(key=lambda a: (a["date"], a["capture"]))
    return appearances


def load_timeline(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"events": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def format_public_position(
    event_public: dict[str, Any],
    appearances: list[dict[str, Any]],
    shifts: list[dict[str, Any]],
) -> str:
    explicit = str(event_public.get("public_position") or "").strip()
    if explicit and not shifts:
        return explicit
    if not appearances:
        return explicit or "—"
    latest = str(appearances[-1]["stance"])
    if shifts:
        first = str(appearances[0]["stance"])
        if first != latest:
            return f"{first.capitalize()} → {latest}"
    if explicit:
        return explicit
    return latest.capitalize() if latest else "—"


def format_status(event: dict[str, Any]) -> str:
    status = str(event.get("status") or "open")
    if status == "resolved":
        outcome = event.get("outcome")
        if outcome == "yes":
            return "Resolved — yes"
        if outcome == "no":
            return "Resolved — no"
        return f"Resolved — {outcome}"
    return "Open"


def render_citation_line(citation: dict[str, str], *, speaker_display_name: str) -> str:
    title = citation.get("title") or "Source"
    channel = citation.get("channel") or "Source"
    pub_date = citation.get("pub_date") or ""
    youtube_url = str(citation.get("youtube_url") or "").strip()
    if youtube_url:
        title_part = f'[{title}]({youtube_url})'
    else:
        title_part = title
    return f"— {speaker_display_name}, **{channel}**, {title_part}, **{pub_date}**"


def build_voice_prediction_payload(
    config: VoiceConfig,
    *,
    timeline_path: Path,
    public_map_path: Path,
    capture_map_path: Path,
) -> dict[str, Any]:
    events = load_event_registry()
    public_map = load_public_map(public_map_path, event_order=config.pilot_event_order)
    capture_rows = load_capture_map(capture_map_path)
    timeline = load_timeline(timeline_path)

    by_event: dict[str, list[dict[str, Any]]] = {}
    for row in capture_rows:
        by_event.setdefault(str(row["event_id"]), []).append(row)

    event_payloads: list[dict[str, Any]] = []
    shifted_count = 0
    resolved_count = 0
    open_count = 0
    appearance_count = 0

    for event_id in config.pilot_event_order:
        registry_event = events.get(event_id, {})
        event_public = public_map[event_id]
        event_rows = by_event.get(event_id, [])
        if not event_rows:
            raise ValueError(f"capture map has no rows for event {event_id}")
        appearances = build_appearances_for_event(
            event_rows,
            event_public,
            anchor_capture=str(event_public.get("anchor_capture") or "") or None,
            default_channel=config.default_channel,
        )
        appearance_count += len(appearances)
        block = timeline.get("events", {}).get(event_id, {})
        shifts = list((block.get("shifts") or {}).get(config.speaker, []))
        reviews = list((block.get("reviews") or {}).get(config.speaker, []))

        review_objects: list[dict[str, Any]] = []
        for review in reviews:
            review_date = str(review.get("date") or "")
            quote = ""
            for app in appearances:
                if app["date"] == review_date:
                    quote = str(app["public_excerpt"])
                    break
            review_objects.append(
                {
                    "date": review.get("date"),
                    "speech_act": review.get("speech_act"),
                    "public_excerpt": quote,
                }
            )

        record, record_label = derive_record(
            event=registry_event,
            event_public=event_public,
            touchpoints=appearances,
            shifts=shifts,
            reviews=review_objects,
        )
        anchor = select_anchor_appearance(appearances, event_public)
        anchor_excerpt = str(anchor.get("public_excerpt") or "").strip()
        if not anchor_excerpt:
            raise ValueError(f"missing anchor excerpt for event {event_id}")
        anchor_citation = dict(anchor["citation"])
        anchor_context_note = str(anchor.get("context_note") or "").strip() or None

        status = str(registry_event.get("status") or "open")
        if status == "resolved":
            resolved_count += 1
        else:
            open_count += 1
        if shifts:
            shifted_count += 1

        stub = config.wire_stubs.get(event_id)
        resolution_note = stub if stub and (REPO_ROOT / stub).is_file() else None

        latest = appearances[-1] if appearances else None
        event_payloads.append(
            {
                "event_id": event_id,
                "public_title": event_public["public_title"],
                "technical_question": registry_event.get("question", ""),
                "status": status,
                "outcome": registry_event.get("outcome"),
                "latest_stance": latest["stance"] if latest else None,
                "latest_date": latest["date"] if latest else None,
                "record": record,
                "record_label": record_label,
                "scoring_policy": event_public["scoring_policy"],
                "event_kind": event_public["event_kind"],
                "anchor_excerpt": anchor_excerpt,
                "anchor_citation": anchor_citation,
                "anchor_context_note": anchor_context_note,
                "public_position": format_public_position(event_public, appearances, shifts),
                "public_summary": event_public["public_summary"],
                "why_it_matters": event_public["why_it_matters"],
                "resolution_note": resolution_note,
                "appearances": appearances,
                "shifts": shifts,
                "reviews": review_objects,
            }
        )

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_voice_predictions.py",
            "speaker": config.speaker,
            "schema": config.schema,
        },
        "speaker": config.speaker,
        "summary": {
            "events_tracked": len(config.pilot_event_order),
            "appearances": appearance_count,
            "resolved_events": resolved_count,
            "open_events": open_count,
            "shifted_events": shifted_count,
        },
        "events": event_payloads,
    }


def render_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def format_position_line(position: str) -> str:
    text = str(position).strip()
    if text.endswith("."):
        return text
    return f"{text}." if text else "—"


def md_escape_cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def render_public_markdown(payload: dict[str, Any], config: VoiceConfig) -> str:
    summary = payload["summary"]
    intro_name = config.speaker_display_name
    capture_map_name = config.capture_map_path.name
    lines = [
        f"<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. build_voice_predictions.py -->",
        "",
        config.page_title,
        "",
        f"This page tracks major falsifiable predictions and strategic judgments made by "
        f"{intro_name} across the Statecraft archive.",
        "",
        f"Each section asks one concrete question, shows {intro_name}'s own words, and tracks "
        "whether later events confirmed, challenged, or complicated the claim.",
        "",
        "## How to Read This Page",
        "",
        "Use **At a Glance** for a compact overview. Each numbered section is one prediction "
        f"or strategic judgment. {intro_name}'s exact words appear in blockquotes; the collapsible "
        "**Source trail** lists every archived appearance with stance and excerpt.",
        "",
        "## At a Glance",
        "",
        "| Question | Position | Status | Record |",
        "| --- | --- | --- | --- |",
    ]

    for event in payload["events"]:
        lines.append(
            "| "
            f"{md_escape_cell(event['public_title'])} | "
            f"{md_escape_cell(event['public_position'])} | "
            f"{format_status({'status': event['status'], 'outcome': event['outcome']})} | "
            f"{event['record_label']} |"
        )

    lines.append("")

    for index, event in enumerate(payload["events"], start=1):
        event_id = event["event_id"]
        anchor_cite = event["anchor_citation"]
        anchor_context = str(event.get("anchor_context_note") or "").strip()
        block_lines = [
                f"## {index}. {event['public_title']} {{#{event_id}}}",
                "",
                f"**Position:** {format_position_line(event['public_position'])}  ",
                f"**Status:** {format_status({'status': event['status'], 'outcome': event['outcome']})}.  ",
                f"**Record:** {event['record_label']}.",
                "",
        ]
        if anchor_context:
            block_lines.append(anchor_context)
            block_lines.append("")
        block_lines.extend(
            [
                f"> \"{event['anchor_excerpt']}\"",
                "",
                render_citation_line(anchor_cite, speaker_display_name=config.speaker_display_name),
                "",
                f"{event['public_summary']}",
                "",
                "**Why it matters:**  ",
                event["why_it_matters"],
                "",
                "<details>",
                "<summary>Source trail</summary>",
                "",
                "| Date | Appearance | Stance | Exact words |",
                "| --- | --- | --- | --- |",
            ]
        )
        lines.extend(block_lines)
        for app in event["appearances"]:
            lines.append(
                "| "
                f"{app['date']} | "
                f"{md_escape_cell(app['appearance_label'])} | "
                f"{app['stance']} | "
                f"{md_escape_cell(format_exact_words_cell(app))} |"
            )
        lines.extend(["", "</details>", ""])

    lines.extend(
        [
            "## Method",
            "",
            "This page is generated from curated capture rows in "
            f"`statecraft/data/{capture_map_name}`, joined to shared events in "
            "`statecraft/data/event-registry.json`. YouTube links appear when the underlying "
            "archive capture carries a watch URL; otherwise the episode title is shown without a link.",
            "",
            "The structured data companion lives beside this page:",
            "",
            f"`statecraft/voices/{config.speaker}/{config.speaker}-predictions.json`",
            "",
            f"_Generated companion — {summary['events_tracked']} events, "
            f"{summary['appearances']} appearances. Rebuild: "
            f"`{config.builder_script}`_",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(
    payload: dict[str, Any],
    *,
    config: VoiceConfig,
    json_out: Path,
    md_out: Path,
    json_only: bool = False,
    md_only: bool = False,
) -> None:
    if not md_only:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(render_json(payload), encoding="utf-8", newline="\n")
        print(f"[ok] wrote {json_out.relative_to(REPO_ROOT)}")
    if not json_only:
        md_out.parent.mkdir(parents=True, exist_ok=True)
        md_out.write_text(render_public_markdown(payload, config), encoding="utf-8", newline="\n")
        print(f"[ok] wrote {md_out.relative_to(REPO_ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--speaker",
        default="freeman",
        help="Voice slug (see voice_prediction_pilot.list_voice_speakers())",
    )
    ap.add_argument("--json-output", type=Path, default=None)
    ap.add_argument("--md-output", type=Path, default=None)
    ap.add_argument("--public-map", type=Path, default=None)
    ap.add_argument("--capture-map", type=Path, default=None)
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json-only", action="store_true")
    ap.add_argument("--md-only", action="store_true")
    args = ap.parse_args()

    try:
        config = get_voice_config(args.speaker)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    json_out = args.json_output or config.predictions_json_path
    md_out = args.md_output or config.predictions_md_path
    public_map_path = args.public_map or config.public_map_path
    capture_map_path = args.capture_map or config.capture_map_path

    try:
        payload = build_voice_prediction_payload(
            config,
            timeline_path=args.timeline,
            public_map_path=public_map_path,
            capture_map_path=capture_map_path,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    rendered_json = render_json(payload)
    rendered_md = render_public_markdown(payload, config)

    if args.check:
        rc = 0
        if not args.md_only:
            if not json_out.is_file():
                print(
                    f"error: missing {json_out.relative_to(REPO_ROOT)}",
                    file=sys.stderr,
                )
                rc = 1
            elif json_out.read_text(encoding="utf-8") != rendered_json:
                print(
                    f"error: {json_out.relative_to(REPO_ROOT)} is out of date; "
                    f"run {config.builder_script}",
                    file=sys.stderr,
                )
                rc = 1
        if not args.json_only:
            if not md_out.is_file():
                print(
                    f"error: missing {md_out.relative_to(REPO_ROOT)}",
                    file=sys.stderr,
                )
                rc = 1
            elif md_out.read_text(encoding="utf-8") != rendered_md:
                print(
                    f"error: {md_out.relative_to(REPO_ROOT)} is out of date; "
                    f"run {config.builder_script}",
                    file=sys.stderr,
                )
                rc = 1
        if rc == 0:
            print(f"[ok] {config.speaker} predictions match generator output")
        return rc

    write_outputs(
        payload,
        config=config,
        json_out=json_out,
        md_out=md_out,
        json_only=args.json_only,
        md_only=args.md_only,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
