#!/usr/bin/env python3
"""Crawl Freeman archive captures for prediction thesis-map hits."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = REPO_ROOT / "source-archive" / "statecraft"
DEFAULT_OUT = REPO_ROOT / "runtime" / "artifacts" / "freeman-prediction-crawl.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from build_freeman_index import parse_head, pub_date_key  # noqa: E402
from freeman_prediction_pilot import (  # noqa: E402
    FREEMAN_SPEAKER,
    load_thesis_map,
    parse_register_capture_paths,
    patterns_match,
    iso_now,
)
from prediction_lib import collect_prediction_notes, render_json  # noqa: E402

REST_RE = re.compile(
    r"\b(as I said|I['']ve argued|still believe|I was wrong|I misread|I was right|as I predicted)\b",
    re.I,
)


def iter_freeman_captures() -> list[tuple[str, Path, dict[str, Any]]]:
    rows: list[tuple[str, Path, dict[str, Any]]] = []
    for path in iter_archive_captures_for_shelf("freeman", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8", errors="replace")[:8000]
        if shelf_utils.shelf_capture_excluded("freeman", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows


def build_register_index(thesis: dict[str, dict[str, Any]]) -> dict[str, list[tuple[str, str]]]:
    out: dict[str, list[tuple[str, str]]] = {}
    for event_id, cfg in thesis.items():
        for rel in cfg.get("register_notes") or []:
            reg_path = REPO_ROOT / str(rel).replace("\\", "/")
            for source in parse_register_capture_paths(reg_path):
                out.setdefault(source, []).append((event_id, str(rel)))
    return out


def suggested_speech_act_heuristic(body: str) -> str | None:
    m = REST_RE.search(body)
    if not m:
        return None
    phrase = m.group(1).casefold()
    if "wrong" in phrase or "misread" in phrase:
        return "self_acknowledged_incorrect"
    if "right" in phrase or "predicted" in phrase or "as i said" in phrase:
        return "self_acknowledged_correct"
    return "restated"


def prior_stance(notes_by_event: dict[str, list[str]], event_id: str) -> str | None:
    notes = notes_by_event.get(event_id) or []
    return notes[-1] if notes else None


def crawl(*, body_chars: int = 8000) -> dict[str, Any]:
    thesis = load_thesis_map()
    register_index = build_register_index(thesis)
    approved_notes = [
        n
        for n in collect_prediction_notes()
        if n.speaker == FREEMAN_SPEAKER and n.event_id in thesis
    ]
    notes_by_event: dict[str, list[str]] = {}
    existing_pairs: set[tuple[str, str]] = set()
    for note in sorted(approved_notes, key=lambda n: (n.event_id, n.date_made, n.file)):
        notes_by_event.setdefault(note.event_id, []).append(note.stance)
        existing_pairs.add((note.source.replace("\\", "/"), note.event_id))

    rows: list[dict[str, Any]] = []
    for pub, path, meta in iter_freeman_captures():
        source = path.relative_to(REPO_ROOT).as_posix()
        title = str(meta.get("title") or path.name)
        slug = path.name
        hay_title_slug = f"{title} {slug}"
        body = path.read_text(encoding="utf-8", errors="replace")[:body_chars]

        for event_id, cfg in thesis.items():
            gate = cfg.get("close_date_gate")
            if gate and pub > str(gate):
                continue
            exclude = cfg.get("exclude_patterns") or []
            if patterns_match(hay_title_slug, exclude) or patterns_match(body[:2000], exclude):
                continue
            match_method = None
            match_detail = None
            title_patterns = cfg.get("title_patterns") or []
            if patterns_match(hay_title_slug, title_patterns):
                match_method = "title"
            elif patterns_match(body, title_patterns):
                match_method = "body_keyword"
            elif source in register_index:
                for reg_event, reg_note in register_index[source]:
                    if reg_event == event_id:
                        match_method = "register"
                        match_detail = reg_note
                        break
            if not match_method:
                continue
            key = (source, event_id)
            if key in existing_pairs:
                continue
            existing_pairs.add(key)
            rows.append(
                {
                    "source": source,
                    "pub_date": pub,
                    "event_id": event_id,
                    "match_method": match_method,
                    "match_detail": match_detail,
                    "suggested_speech_act": suggested_speech_act_heuristic(body),
                    "suggested_stance": None,
                    "prior_freeman_stance": prior_stance(notes_by_event, event_id),
                    "quote_candidates": [],
                    "needs_human": True,
                    "audit_status": "pending",
                    "audit_stance": None,
                    "audit_speech_act": None,
                    "note_file": None,
                    "reject_reason": None,
                }
            )

    rows.sort(key=lambda r: (r["event_id"], r["pub_date"], r["source"]))
    return {
        "_meta": {
            "source": "scripts/crawl_freeman_predictions.py",
            "generated_at": iso_now(),
            "capture_count": len(list(iter_freeman_captures())),
            "row_count": len(rows),
        },
        "rows": rows,
    }


AUDIT_PRESERVE_FIELDS = (
    "audit_status",
    "audit_stance",
    "audit_speech_act",
    "note_file",
    "reject_reason",
    "needs_human",
)


def merge_audit_from_existing(payload: dict[str, Any], manifest_path: Path) -> int:
    """Carry operator audit fields forward when re-crawling after thesis-map edits."""
    if not manifest_path.is_file():
        return 0
    old = json.loads(manifest_path.read_text(encoding="utf-8"))
    prior: dict[tuple[str, str], dict[str, Any]] = {}
    for row in old.get("rows") or []:
        if not isinstance(row, dict):
            continue
        source = str(row.get("source") or "").replace("\\", "/")
        event_id = str(row.get("event_id") or "")
        if source and event_id:
            prior[(source, event_id)] = row
    merged = 0
    for row in payload.get("rows") or []:
        key = (str(row.get("source") or "").replace("\\", "/"), str(row.get("event_id") or ""))
        prev = prior.get(key)
        if not prev:
            continue
        for field in AUDIT_PRESERVE_FIELDS:
            if field in prev and prev[field] is not None:
                row[field] = prev[field]
        merged += 1
    return merged


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--body-chars", type=int, default=8000)
    ap.add_argument(
        "--no-preserve-audit",
        action="store_true",
        help="Do not merge audit_* / note_file from existing manifest (default: preserve)",
    )
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    payload = crawl(body_chars=args.body_chars)
    if not args.no_preserve_audit:
        merged = merge_audit_from_existing(payload, args.output)
        if merged and not args.check:
            print(f"[ok] preserved audit fields on {merged} row(s) from prior manifest")
    rendered = render_json(payload)

    if args.check:
        if not args.output.is_file():
            print(f"error: missing {args.output.relative_to(REPO_ROOT)}", file=sys.stderr)
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(
                f"error: {args.output.relative_to(REPO_ROOT)} is out of date; "
                "run crawl_freeman_predictions.py",
                file=sys.stderr,
            )
            return 1
        print("[ok] freeman-prediction-crawl.json matches generator output")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"[ok] wrote {args.output.relative_to(REPO_ROOT)} ({payload['_meta']['row_count']} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
