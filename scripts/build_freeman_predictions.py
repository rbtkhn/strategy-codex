#!/usr/bin/env python3
"""Build statecraft/voices/freeman/freeman-predictions.md from Freeman pilot prediction notes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.md"
DEFAULT_MANIFEST = REPO_ROOT / "runtime" / "artifacts" / "freeman-prediction-crawl.json"
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_freeman_index import host_short, parse_head, pub_date_key  # noqa: E402
from freeman_prediction_pilot import (  # noqa: E402
    CRAWL_ARTIFACT,
    FREEMAN_PILOT_EVENT_ORDER,
    FREEMAN_PREDICTIONS_OUT,
    FREEMAN_SPEAKER,
    REVIEW_SPEECH_ACTS,
    extract_quote_stub,
    pilot_event_sort_key,
)
from prediction_lib import (  # noqa: E402
    REPO_ROOT as LIB_ROOT,
    collect_prediction_notes,
    load_event_registry,
    parse_prediction_note,
    repo_relative,
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

def capture_link(source: str) -> str:
    path = REPO_ROOT / source.replace("\\", "/")
    meta = parse_head(path) if path.is_file() else {}
    pub = pub_date_key(meta, path) if path.is_file() else source.split("/")[-2]
    host = host_short(meta, path) if path.is_file() else "Other"
    rel = f"../../../{source}"
    return f"[{pub} {host}]({rel})"

def note_link(note_file: str, label: str | None = None) -> str:
    name = Path(note_file).name
    text = label or name.replace(".md", "")
    return f"[{text}](../../notes/predictions/{name})"

def derive_speech_act(row: dict[str, Any], prior: dict[str, Any] | None) -> str:
    act = str(row.get("speech_act") or "").strip()
    if act:
        return act
    if prior is None:
        return "initial"
    if str(prior.get("stance") or "") != str(row.get("stance") or ""):
        return "iterated"
    return "restated"

def load_freeman_pilot_rows() -> list[dict[str, Any]]:
    events = load_event_registry()
    rows: list[dict[str, Any]] = []
    for note in collect_prediction_notes():
        if note.speaker != FREEMAN_SPEAKER:
            continue
        if note.event_id not in FREEMAN_PILOT_EVENT_ORDER:
            continue
        body = note.path.read_text(encoding="utf-8", errors="replace")
        data = parse_prediction_note(note.path, body)
        if data is None:
            continue
        row = {
            "event_id": note.event_id,
            "date_made": note.date_made,
            "stance": note.stance,
            "source": note.source,
            "file": note.file,
            "speech_act": note.speech_act,
            "quote_stub": extract_quote_stub(body),
        }
        rows.append(row)
    rows.sort(key=lambda r: (pilot_event_sort_key(str(r["event_id"])), r["date_made"], r["file"]))
    return rows

def load_timeline(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"events": {}}
    return json.loads(path.read_text(encoding="utf-8"))

def render_event_section(
    event_id: str,
    event: dict[str, Any],
    table_rows: list[dict[str, Any]],
    timeline: dict[str, Any],
) -> list[str]:
    block = timeline.get("events", {}).get(event_id, {})
    shifts = (block.get("shifts") or {}).get(FREEMAN_SPEAKER, [])
    restatement_count = sum(
        1 for r in table_rows if str(r.get("speech_act") or "") == "restated"
    )
    review_count = sum(
        1 for r in table_rows if str(r.get("speech_act") or "") in REVIEW_SPEECH_ACTS
    )
    latest = table_rows[-1] if table_rows else None
    status = str(event.get("status") or "open")
    outcome = event.get("outcome")
    lines = [
        f"## {event_id}",
        "",
        f"**Question:** {event.get('question', '')}  ",
    ]
    closure = event.get("closure_trigger")
    if closure:
        lines.append(f"**Closure trigger:** {closure}  ")
    elif event.get("horizon_cite"):
        cite = str(event.get("horizon_cite") or "")
        if len(cite) > 140:
            cite = cite[:137] + "..."
        lines.append(f"**Horizon (Freeman):** {cite}  ")
    close = event.get("close_date")
    if close:
        lines.append(f"**Close date:** {close}  ")
    header = f"**Event status:** {status}"
    if outcome is not None:
        header += f" · **Outcome:** {outcome}"
    if latest:
        header += f" · **Freeman latest:** {latest['stance']} ({latest['date_made']})"
    header += (
        f" · **Arc:** {len(table_rows)} touchpoints · {len(shifts)} shifts · "
        f"{restatement_count} restatements · {review_count} reviews"
    )
    lines.append(header)
    stub = WIRE_STUBS.get(event_id)
    if stub and (REPO_ROOT / stub).is_file():
        stub_name = Path(stub).stem
        lines.append("")
        lines.append(
            f"**Resolution stub:** [../../notes/wire/{stub_name}.md](../../notes/wire/{stub_name}.md)"
        )
    lines.extend(["", "| date | speech_act | stance | capture | note |", "| --- | --- | --- | --- | --- |"])
    prior: dict[str, Any] | None = None
    for row in sorted(table_rows, key=lambda r: (r["date_made"], r["file"])):
        act = derive_speech_act(row, prior)
        row["speech_act"] = act
        lines.append(
            f"| {row['date_made']} | {act} | {row['stance']} | "
            f"{capture_link(str(row['source']))} | {note_link(str(row['file']))} |"
        )
        prior = row
    lines.extend(["", "### Shifts", ""])
    if shifts:
        for shift in shifts:
            lines.append(
                f"- **{shift.get('type')}** · {shift.get('from')} → {shift.get('to')} · "
                f"{shift.get('from_date')} → {shift.get('to_date')} · "
                f"{note_link(str(shift.get('to_file') or ''), 'note')}"
            )
    else:
        lines.append("(none)")
    lines.extend(["", "### Reviews", ""])
    review_rows = [r for r in table_rows if str(r.get("speech_act") or "") in REVIEW_SPEECH_ACTS]
    if review_rows:
        for row in review_rows:
            stub = row.get("quote_stub") or "quote TBD"
            lines.append(
                f"- **{row['speech_act']}** · {row['date_made']} · {stub} · "
                f"{note_link(str(row['file']))}"
            )
    else:
        lines.append("(none)")
    lines.append("")
    return lines

def render_document(
    *,
    rows: list[dict[str, Any]],
    events: dict[str, dict[str, Any]],
    timeline: dict[str, Any],
) -> str:
    by_event: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_event.setdefault(str(row["event_id"]), []).append(row)
    lines = [
        "# Freeman predictions",
        "",
        "Purpose: event-first map of Freeman falsifiable stances — restatements, shifts, and self-review across the full freeman-index corpus.",
        "",
        f"- **Events tracked:** {len(FREEMAN_PILOT_EVENT_ORDER)} · **Touchpoints:** {len(rows)} · "
        "**Rebuild:** `python3 scripts/build_freeman_predictions.py`",
        "- **Doctrine:** [event-system.md](../../docs/statecraft/event-system.md) · "
        "**Wire events:** [freeman-prediction-wire-events.md](freeman-prediction-wire-events.md) · "
        "**Crawl manifest:** [freeman-prediction-crawl.json](../../runtime/artifacts/freeman-prediction-crawl.json) · "
        "**Captures:** [freeman-index.md](freeman-index.md)",
        "",
    ]
    for event_id in FREEMAN_PILOT_EVENT_ORDER:
        event = events.get(event_id, {})
        lines.extend(render_event_section(event_id, event, by_event.get(event_id, []), timeline))
    return "\n".join(lines).rstrip() + "\n"

def build_payload(*, timeline_path: Path) -> str:
    events = load_event_registry()
    rows = load_freeman_pilot_rows()
    timeline = load_timeline(timeline_path)
    return render_document(rows=rows, events=events, timeline=timeline)

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    try:
        rendered = build_payload(timeline_path=args.timeline)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if not args.output.is_file():
            print(f"error: missing {args.output.relative_to(REPO_ROOT)}", file=sys.stderr)
            return 1
        current = args.output.read_text(encoding="utf-8")
        if current != rendered:
            print(
                f"error: {args.output.relative_to(REPO_ROOT)} is out of date; "
                "run build_freeman_predictions.py",
                file=sys.stderr,
            )
            return 1
        print("[ok] freeman-predictions.md matches generator output")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"[ok] wrote {args.output.relative_to(REPO_ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
