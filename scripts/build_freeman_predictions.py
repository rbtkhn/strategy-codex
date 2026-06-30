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
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_freeman_index import host_short, parse_head, pub_date_key  # noqa: E402
from freeman_prediction_pilot import (  # noqa: E402
    FREEMAN_PILOT_EVENT_ORDER,
    FREEMAN_PREDICTIONS_JSON,
    FREEMAN_PREDICTIONS_OUT,
    FREEMAN_SPEAKER,
    REVIEW_SPEECH_ACTS,
    derive_record,
    extract_quote,
    load_public_map,
    pilot_event_sort_key,
    require_quote,
    select_anchor_quote,
    shorten_quote,
)
from prediction_lib import (  # noqa: E402
    REPO_ROOT as LIB_ROOT,
    collect_prediction_notes,
    load_event_registry,
    parse_prediction_note,
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


def derive_speech_act(row: dict[str, Any], prior: dict[str, Any] | None) -> str:
    act = str(row.get("speech_act") or "").strip()
    if act:
        return act
    if prior is None:
        return "initial"
    if str(prior.get("stance") or "") != str(row.get("stance") or ""):
        return "iterated"
    return "restated"


def appearance_label(source: str) -> str:
    path = REPO_ROOT / source.replace("\\", "/")
    if not path.is_file():
        return source.split("/")[-1]
    meta = parse_head(path)
    pub = pub_date_key(meta, path)
    host = host_short(meta, path)
    return f"{pub} {host}"


def load_freeman_pilot_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for note in collect_prediction_notes():
        if note.speaker != FREEMAN_SPEAKER:
            continue
        if note.event_id not in FREEMAN_PILOT_EVENT_ORDER:
            continue
        body = note.path.read_text(encoding="utf-8", errors="replace")
        if parse_prediction_note(note.path, body) is None:
            continue
        quote = extract_quote(body)
        require_quote(note.path, quote)
        rows.append(
            {
                "event_id": note.event_id,
                "date_made": note.date_made,
                "stance": note.stance,
                "source": note.source,
                "file": note.file,
                "speech_act": note.speech_act,
                "quote": quote,
                "quote_short": shorten_quote(quote),
            }
        )
    rows.sort(key=lambda r: (pilot_event_sort_key(str(r["event_id"])), r["date_made"], r["file"]))
    return rows


def load_timeline(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"events": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def format_public_position(
    event_public: dict[str, Any],
    touchpoints: list[dict[str, Any]],
    shifts: list[dict[str, Any]],
) -> str:
    explicit = str(event_public.get("public_position") or "").strip()
    if explicit and not shifts:
        return explicit
    if not touchpoints:
        return explicit or "—"
    latest = str(touchpoints[-1]["stance"])
    if shifts:
        first = str(touchpoints[0]["stance"])
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


def build_touchpoints_for_event(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    touchpoints: list[dict[str, Any]] = []
    prior: dict[str, Any] | None = None
    for row in rows:
        act = derive_speech_act(row, prior)
        touchpoints.append(
            {
                "date": row["date_made"],
                "speech_act": act,
                "stance": row["stance"],
                "quote": row["quote"],
                "quote_short": row["quote_short"],
                "capture": row["source"],
                "note": row["file"],
                "appearance_label": appearance_label(str(row["source"])),
            }
        )
        prior = row
    return touchpoints


def build_freeman_prediction_payload(
    *,
    timeline_path: Path,
    public_map_path: Path,
) -> dict[str, Any]:
    events = load_event_registry()
    public_map = load_public_map(public_map_path)
    rows = load_freeman_pilot_rows()
    timeline = load_timeline(timeline_path)

    by_event: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_event.setdefault(str(row["event_id"]), []).append(row)

    event_payloads: list[dict[str, Any]] = []
    shifted_count = 0
    resolved_count = 0
    open_count = 0

    for event_id in FREEMAN_PILOT_EVENT_ORDER:
        registry_event = events.get(event_id, {})
        event_public = public_map[event_id]
        event_rows = by_event.get(event_id, [])
        touchpoints = build_touchpoints_for_event(event_rows)
        block = timeline.get("events", {}).get(event_id, {})
        shifts = list((block.get("shifts") or {}).get(FREEMAN_SPEAKER, []))
        reviews = list((block.get("reviews") or {}).get(FREEMAN_SPEAKER, []))

        review_objects: list[dict[str, Any]] = []
        for review in reviews:
            note_path = str(review.get("file") or "")
            quote = ""
            for tp in touchpoints:
                if tp["note"] == note_path:
                    quote = str(tp["quote"])
                    break
            review_objects.append(
                {
                    "date": review.get("date"),
                    "speech_act": review.get("speech_act"),
                    "quote": quote,
                    "note": note_path,
                }
            )

        record, record_label = derive_record(
            event=registry_event,
            event_public=event_public,
            touchpoints=touchpoints,
            shifts=shifts,
            reviews=review_objects,
        )
        anchor_quote = select_anchor_quote(event_public, touchpoints)
        if not anchor_quote.strip():
            raise ValueError(f"missing anchor quote for event {event_id}")

        status = str(registry_event.get("status") or "open")
        if status == "resolved":
            resolved_count += 1
        else:
            open_count += 1
        if shifts:
            shifted_count += 1

        stub = WIRE_STUBS.get(event_id)
        resolution_note = stub if stub and (REPO_ROOT / stub).is_file() else None

        latest = touchpoints[-1] if touchpoints else None
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
                "anchor_quote": anchor_quote,
                "public_position": format_public_position(event_public, touchpoints, shifts),
                "public_summary": event_public["public_summary"],
                "why_it_matters": event_public["why_it_matters"],
                "resolution_note": resolution_note,
                "touchpoints": touchpoints,
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
        },
        "speaker": FREEMAN_SPEAKER,
        "summary": {
            "events_tracked": len(FREEMAN_PILOT_EVENT_ORDER),
            "touchpoints": len(rows),
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
        "**Source trail** lists every archived appearance with stance and quote.",
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
        lines.extend(
            [
                f"## {index}. {event['public_title']} {{#{event_id}}}",
                "",
                f"**Freeman's position:** {format_position_line(event['public_position'])}  ",
                f"**Status:** {format_status({'status': event['status'], 'outcome': event['outcome']})}.  ",
                f"**Record:** {event['record_label']}.",
                "",
                f"> \"{event['anchor_quote']}\"",
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
        for tp in event["touchpoints"]:
            quote_cell = tp["quote_short"] if len(tp["quote"]) > 120 else tp["quote"]
            lines.append(
                "| "
                f"{tp['date']} | "
                f"{md_escape_cell(tp['appearance_label'])} | "
                f"{tp['stance']} | "
                f"\"{md_escape_cell(quote_cell)}\" |"
            )
        lines.extend(["", "</details>", ""])

    lines.extend(
        [
            "## Method",
            "",
            "This page is generated from source-backed prediction notes in "
            "`statecraft/notes/predictions/`, joined to shared events in "
            "`statecraft/data/event-registry.json`.",
            "",
            "The structured data companion lives beside this page:",
            "",
            "`statecraft/voices/freeman/freeman-predictions.json`",
            "",
            f"_Generated companion — {summary['events_tracked']} events, "
            f"{summary['touchpoints']} appearances. Rebuild: "
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
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json-only", action="store_true")
    ap.add_argument("--md-only", action="store_true")
    args = ap.parse_args()

    try:
        payload = build_freeman_prediction_payload(
            timeline_path=args.timeline,
            public_map_path=args.public_map,
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
