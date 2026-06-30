#!/usr/bin/env python3
"""Build Freeman prediction record — colocated JSON + public markdown on the voice shelf."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MD_OUT = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.md"
DEFAULT_JSON_OUT = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.json"
DEFAULT_PUBLIC_MAP = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-public-map.json"
DEFAULT_CAPTURE_MAP = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-capture-map.json"
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_freeman_index import host_short, parse_head, pub_date_key  # noqa: E402
from freeman_prediction_pilot import (  # noqa: E402
    FREEMAN_CAPTURE_MAP,
    FREEMAN_PILOT_EVENT_ORDER,
    FREEMAN_PREDICTIONS_JSON,
    FREEMAN_PREDICTIONS_OUT,
    FREEMAN_SPEAKER,
    derive_record,
    load_capture_map,
    load_public_map,
    parse_capture_frontmatter,
    select_anchor_appearance,
    shorten_quote,
    source_citation,
    validate_capture_row,
)
from prediction_lib import (  # noqa: E402
    REPO_ROOT as LIB_ROOT,
    load_event_registry,
)

assert LIB_ROOT == REPO_ROOT

WIRE_STUBS: dict[str, str] = {
    "israel_self_destruction_trajectory": (
        "statecraft/notes/wire/prediction-resolution-israel-self-destruction-trajectory.md"
    ),
    "gaza_ceasefire_holds_2025": "statecraft/notes/wire/prediction-resolution-gaza-ceasefire-holds-2025.md",
    "us_israel_iran_war_preparation_2025": (
        "statecraft/notes/wire/prediction-resolution-us-israel-iran-war-preparation-2025.md"
    ),
    "iran_great_power_direct_war_entry": (
        "statecraft/notes/wire/prediction-resolution-iran-great-power-direct-war-entry.md"
    ),
    "china_tariff_capitulation_2025": (
        "statecraft/notes/wire/prediction-resolution-china-tariff-capitulation-2025.md"
    ),
    "gaza_hostage_deal_jan_2025": "statecraft/notes/wire/prediction-resolution-gaza-hostage-deal-jan-2025.md",
    "ukraine_escalation_russian_capitulation": (
        "statecraft/notes/wire/prediction-resolution-ukraine-escalation-russian-capitulation.md"
    ),
}


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
        citation = source_citation(capture_path)
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


def render_citation_line(citation: dict[str, str]) -> str:
    title = citation.get("title") or "Source"
    channel = citation.get("channel") or "Source"
    pub_date = citation.get("pub_date") or ""
    youtube_url = str(citation.get("youtube_url") or "").strip()
    if youtube_url:
        title_part = f'[{title}]({youtube_url})'
    else:
        title_part = title
    return f"— Chas Freeman, **{channel}**, {title_part}, **{pub_date}**"


def build_freeman_prediction_payload(
    *,
    timeline_path: Path,
    public_map_path: Path,
    capture_map_path: Path,
) -> dict[str, Any]:
    events = load_event_registry()
    public_map = load_public_map(public_map_path)
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

    for event_id in FREEMAN_PILOT_EVENT_ORDER:
        registry_event = events.get(event_id, {})
        event_public = public_map[event_id]
        event_rows = by_event.get(event_id, [])
        if not event_rows:
            raise ValueError(f"capture map has no rows for event {event_id}")
        appearances = build_appearances_for_event(
            event_rows,
            event_public,
            anchor_capture=str(event_public.get("anchor_capture") or "") or None,
        )
        appearance_count += len(appearances)
        block = timeline.get("events", {}).get(event_id, {})
        shifts = list((block.get("shifts") or {}).get(FREEMAN_SPEAKER, []))
        reviews = list((block.get("reviews") or {}).get(FREEMAN_SPEAKER, []))

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

        stub = WIRE_STUBS.get(event_id)
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
            "source": "scripts/build_freeman_predictions.py",
            "speaker": FREEMAN_SPEAKER,
            "schema": "freeman-predictions-v2",
        },
        "speaker": FREEMAN_SPEAKER,
        "summary": {
            "events_tracked": len(FREEMAN_PILOT_EVENT_ORDER),
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


def render_public_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. build_freeman_predictions.py -->",
        "",
        "# Chas Freeman Prediction Record",
        "",
        "This page tracks major falsifiable predictions and strategic judgments made by "
        "Ambassador Chas Freeman across the Statecraft archive.",
        "",
        "Each section asks one concrete question, shows Freeman's own words, and tracks "
        "whether later events confirmed, challenged, or complicated the claim.",
        "",
        "## How to Read This Page",
        "",
        "Use **At a Glance** for a compact overview. Each numbered section is one prediction "
        "or strategic judgment. Freeman's exact words appear in blockquotes; the collapsible "
        "**Source trail** lists every archived appearance with stance and excerpt.",
        "",
        "## At a Glance",
        "",
        "| Question | Freeman's position | Status | Record |",
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
                f"**Freeman's position:** {format_position_line(event['public_position'])}  ",
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
                render_citation_line(anchor_cite),
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
            "`statecraft/data/freeman-prediction-capture-map.json`, joined to shared events in "
            "`statecraft/data/event-registry.json`. YouTube links appear when the underlying "
            "archive capture carries a watch URL; otherwise the episode title is shown without a link.",
            "",
            "The structured data companion lives beside this page:",
            "",
            "`statecraft/voices/freeman/freeman-predictions.json`",
            "",
            f"_Generated companion — {summary['events_tracked']} events, "
            f"{summary['appearances']} appearances. Rebuild: "
            "`python3 scripts/build_freeman_predictions.py`_",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(
    payload: dict[str, Any],
    *,
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
        md_out.write_text(render_public_markdown(payload), encoding="utf-8", newline="\n")
        print(f"[ok] wrote {md_out.relative_to(REPO_ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUT)
    ap.add_argument("--md-output", type=Path, default=DEFAULT_MD_OUT)
    ap.add_argument("--public-map", type=Path, default=DEFAULT_PUBLIC_MAP)
    ap.add_argument("--capture-map", type=Path, default=DEFAULT_CAPTURE_MAP)
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json-only", action="store_true")
    ap.add_argument("--md-only", action="store_true")
    args = ap.parse_args()

    try:
        payload = build_freeman_prediction_payload(
            timeline_path=args.timeline,
            public_map_path=args.public_map,
            capture_map_path=args.capture_map,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    rendered_json = render_json(payload)
    rendered_md = render_public_markdown(payload)

    if args.check:
        rc = 0
        if not args.md_only:
            if not args.json_output.is_file():
                print(
                    f"error: missing {args.json_output.relative_to(REPO_ROOT)}",
                    file=sys.stderr,
                )
                rc = 1
            elif args.json_output.read_text(encoding="utf-8") != rendered_json:
                print(
                    f"error: {args.json_output.relative_to(REPO_ROOT)} is out of date; "
                    "run build_freeman_predictions.py",
                    file=sys.stderr,
                )
                rc = 1
        if not args.json_only:
            if not args.md_output.is_file():
                print(
                    f"error: missing {args.md_output.relative_to(REPO_ROOT)}",
                    file=sys.stderr,
                )
                rc = 1
            elif args.md_output.read_text(encoding="utf-8") != rendered_md:
                print(
                    f"error: {args.md_output.relative_to(REPO_ROOT)} is out of date; "
                    "run build_freeman_predictions.py",
                    file=sys.stderr,
                )
                rc = 1
        if rc == 0:
            print("[ok] freeman predictions match generator output")
        return rc

    write_outputs(
        payload,
        json_out=args.json_output,
        md_out=args.md_output,
        json_only=args.json_only,
        md_only=args.md_only,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
