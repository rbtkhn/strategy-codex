#!/usr/bin/env python3
"""Calibrate auto-file scoring against hand-audited (non-auto_file) prediction notes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "runtime" / "artifacts" / "freeman-prediction-auto-file-calibration.json"
PREDICTIONS_DIR = REPO_ROOT / "statecraft" / "notes" / "predictions"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from freeman_prediction_auto_file import (  # noqa: E402
    ScoredCandidate,
    build_register_index,
    collect_auto_file_candidates,
    group_key,
    iter_freeman_captures,
    load_auto_file_config,
    load_thesis_map,
    pick_group_winner,
    read_capture_meta,
    score_capture_for_event,
)
from freeman_prediction_pilot import FREEMAN_PILOT_EVENT_ORDER, FREEMAN_SPEAKER, iso_now  # noqa: E402
from prediction_lib import collect_prediction_notes, render_json  # noqa: E402

AUTO_FILE_RE = re.compile(r"^auto_file:\s*true\s*$", re.M)

def load_gold_labels(*, event_id: str, manual_only: bool = True) -> dict[str, Any]:
    gold_sources: set[str] = set()
    gold_dates: dict[str, str] = {}
    notes_meta: list[dict[str, str]] = []
    for note in collect_prediction_notes():
        if note.speaker != FREEMAN_SPEAKER or note.event_id != event_id:
            continue
        body = note.path.read_text(encoding="utf-8", errors="replace")
        is_auto = bool(AUTO_FILE_RE.search(body))
        if manual_only and is_auto:
            continue
        src = note.source.replace("\\", "/")
        gold_sources.add(src)
        gold_dates[note.date_made] = src
        notes_meta.append(
            {
                "date_made": note.date_made,
                "source": src,
                "file": note.file,
                "auto_file": str(is_auto).lower(),
            }
        )
    return {
        "event_id": event_id,
        "manual_only": manual_only,
        "gold_count": len(notes_meta),
        "gold_sources": gold_sources,
        "gold_dates": gold_dates,
        "notes": sorted(notes_meta, key=lambda n: n["date_made"]),
    }

def score_all_captures(*, event_id: str, auto_cfg: dict[str, Any]) -> list[ScoredCandidate]:
    thesis = load_thesis_map()
    register_index = build_register_index(thesis, auto_cfg)
    event_auto = (auto_cfg.get("events") or {}).get(event_id) or {}
    thesis_cfg = thesis.get(event_id) or {}
    scored: list[ScoredCandidate] = []

    for pub, path, meta in iter_freeman_captures():
        source = path.relative_to(REPO_ROOT).as_posix()
        title = str(meta.get("title") or path.name)
        body = path.read_text(encoding="utf-8", errors="replace")
        cap_meta = read_capture_meta(path)
        row = score_capture_for_event(
            event_id=event_id,
            source=source,
            pub_date=pub,
            title=title,
            body=body,
            meta=cap_meta,
            thesis_cfg=thesis_cfg,
            event_auto_cfg=event_auto,
            auto_cfg=auto_cfg,
            register_sources=register_index.get(event_id) or set(),
        )
        if row is not None:
            scored.append(row)
    return scored

def filing_predictions(candidates: list[ScoredCandidate]) -> dict[str, ScoredCandidate]:
    grouped: dict[tuple, list[ScoredCandidate]] = {}
    for candidate in candidates:
        grouped.setdefault(group_key(candidate), []).append(candidate)
    out: dict[str, ScoredCandidate] = {}
    for (_event_id, pub_date), group in grouped.items():
        out[pub_date] = pick_group_winner(group)
    return out

def prf(*, hits: int, predicted: int, gold: int) -> dict[str, float | None]:
    precision = hits / predicted if predicted else None
    recall = hits / gold if gold else None
    f1 = None
    if precision is not None and recall is not None and (precision + recall) > 0:
        f1 = 2 * precision * recall / (precision + recall)
    return {"precision": precision, "recall": recall, "f1": f1, "hits": hits, "predicted": predicted, "gold": gold}

def calibrate_event(*, event_id: str, manual_only: bool = True) -> dict[str, Any]:
    auto_cfg = load_auto_file_config()
    gold = load_gold_labels(event_id=event_id, manual_only=manual_only)
    gold_sources: set[str] = gold["gold_sources"]
    gold_dates: dict[str, str] = gold["gold_dates"]

    all_scored = score_all_captures(event_id=event_id, auto_cfg=auto_cfg)
    scored_sources = {c.source for c in all_scored}
    filings = filing_predictions(all_scored)

    source_hits = len(gold_sources & scored_sources)
    source_metrics = prf(hits=source_hits, predicted=len(scored_sources), gold=len(gold_sources))

    pred_dates = set(filings.keys())
    gold_date_set = set(gold_dates.keys())
    date_hits = len(pred_dates & gold_date_set)
    date_metrics = prf(hits=date_hits, predicted=len(pred_dates), gold=len(gold_date_set))

    filing_source_hits = sum(
        1 for d, src in gold_dates.items() if d in filings and filings[d].source == src
    )
    filing_metrics = prf(
        hits=filing_source_hits,
        predicted=len(filings),
        gold=len(gold_dates),
    )

    false_negative_dates = sorted(gold_date_set - pred_dates)
    false_positive_dates = sorted(pred_dates - gold_date_set)
    false_negative_sources = sorted(gold_sources - scored_sources)

    false_positive_filings = [
        {
            "pub_date": d,
            "source": filings[d].source,
            "score": filings[d].score,
            "reasons": filings[d].reasons,
            "quote_preview": filings[d].quote[:100],
        }
        for d in sorted(false_positive_dates)
    ]
    false_negative_detail = [
        {
            "pub_date": d,
            "expected_source": gold_dates[d],
            "file": next(
                (n["file"] for n in gold["notes"] if n["date_made"] == d),
                "",
            ),
        }
        for d in false_negative_dates
    ]

    gold_scores = [c.score for c in all_scored if c.source in gold_sources]
    non_gold_scores = [c.score for c in all_scored if c.source not in gold_sources]

    production_candidates = collect_auto_file_candidates(auto_cfg=auto_cfg, event_id_filter=event_id)

    return {
        "_meta": {
            "source": "scripts/calibrate_auto_file.py",
            "generated_at": iso_now(),
            "event_id": event_id,
            "gold_label": "manual_only (auto_file != true)" if manual_only else "all notes",
        },
        "gold": {
            "count": gold["gold_count"],
            "dates": sorted(gold_dates.keys()),
        },
        "metrics": {
            "source_level": source_metrics,
            "date_level_filing": date_metrics,
            "date_overlap": date_metrics,
            "source_in_scored_set": source_metrics,
            "filing_source_match": filing_metrics,
        },
        "counts": {
            "scored_capture_rows": len(all_scored),
            "filing_rows": len(filings),
            "production_auto_file_new": len(production_candidates),
        },
        "score_distribution": {
            "gold_mean": sum(gold_scores) / len(gold_scores) if gold_scores else None,
            "non_gold_mean": sum(non_gold_scores) / len(non_gold_scores) if non_gold_scores else None,
            "gold_min": min(gold_scores) if gold_scores else None,
            "gold_max": max(gold_scores) if gold_scores else None,
        },
        "false_negatives": {
            "dates": false_negative_detail,
            "sources_not_scored": [
                {"source": s, "basename": Path(s).name} for s in false_negative_sources
            ],
        },
        "false_positives_filing": false_positive_filings,
    }

def calibrate_all_events(*, manual_only: bool = True) -> dict[str, Any]:
    reports: dict[str, Any] = {}
    for event_id in FREEMAN_PILOT_EVENT_ORDER:
        reports[event_id] = calibrate_event(event_id=event_id, manual_only=manual_only)
    return {
        "_meta": {
            "source": "scripts/calibrate_auto_file.py",
            "generated_at": iso_now(),
            "mode": "all_events",
            "gold_label": "manual_only (auto_file != true)" if manual_only else "all notes",
        },
        "events": reports,
    }

def print_report(report: dict[str, Any]) -> None:
    event_id = report["_meta"]["event_id"]
    gold_n = report["gold"]["count"]
    print(f"=== Auto-file calibration — `{event_id}` ===")
    print(f"Gold labels: {gold_n} hand-audited notes (auto_file != true)")
    print()

    def line(name: str, block: dict[str, Any]) -> None:
        p = block.get("precision")
        r = block.get("recall")
        f1 = block.get("f1")
        if p is None:
            print(f"  {name}: n/a")
            return
        print(
            f"  {name}: precision={p:.1%} recall={r:.1%} f1={f1:.1%} "
            f"(hits={block['hits']}/{block['gold']} gold, {block['predicted']} predicted)"
        )

    print("Metrics:")
    line("Source in scored set", report["metrics"]["source_level"])
    line("Filing date overlap", report["metrics"]["date_level_filing"])
    line("Filing source match (date + same capture)", report["metrics"]["filing_source_match"])
    print()
    dist = report["score_distribution"]
    non_gold = dist["non_gold_mean"]
    non_gold_s = f"{non_gold:.3f}" if non_gold is not None else "n/a"
    print(
        f"Score distribution: gold mean={dist['gold_mean']:.3f} "
        f"(min={dist['gold_min']}, max={dist['gold_max']}) · "
        f"non-gold mean={non_gold_s}"
    )
    print(
        f"Production pipeline would add {report['counts']['production_auto_file_new']} new note(s) "
        f"(skips existing notes on disk)."
    )
    print()

    fn = report["false_negatives"]
    if fn["dates"]:
        print("False negative dates (gold but scorer would not file):")
        for row in fn["dates"]:
            print(f"  - {row['pub_date']} · {Path(row['expected_source']).name}")
    else:
        print("False negative dates: none")

    if fn["sources_not_scored"]:
        print("Gold sources never scored positive:")
        for row in fn["sources_not_scored"]:
            print(f"  - {row['basename']}")

    fp = report["false_positives_filing"]
    if fp:
        print(f"\nFalse positive filing dates ({len(fp)} — scorer files, not in gold):")
        for row in fp[:12]:
            print(
                f"  - {row['pub_date']} score={row['score']} "
                f"{Path(row['source']).name[:50]}"
            )
        if len(fp) > 12:
            print(f"  … ({len(fp) - 12} more)")
    else:
        print("\nFalse positive filing dates: none")

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--event-id",
        default="israel_self_destruction_trajectory",
        help="Pilot event to calibrate (default: Israel trajectory)",
    )
    ap.add_argument(
        "--all-events",
        action="store_true",
        help="Calibrate every Freeman pilot event; writes combined summary JSON",
    )
    ap.add_argument("--include-auto-file-notes", action="store_true")
    ap.add_argument("--output", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.all_events:
        report = calibrate_all_events(manual_only=not args.include_auto_file_notes)
        out = args.output
        if out == DEFAULT_OUT:
            out = REPO_ROOT / "runtime" / "artifacts" / "freeman-prediction-auto-file-calibration-all.json"
        if not args.quiet:
            print("=== Auto-file calibration — all Freeman pilot events ===")
            for event_id, ev in report["events"].items():
                m = ev["metrics"]["filing_source_match"]
                gold_n = ev["gold"]["count"]
                if gold_n == 0:
                    print(f"  {event_id}: no manual gold notes")
                    continue
                prec = m["precision"]
                rec = m["recall"]
                f1 = m["f1"]
                prec_s = f"{prec:.0%}" if prec is not None else "n/a"
                rec_s = f"{rec:.0%}" if rec is not None else "n/a"
                f1_s = f"{f1:.0%}" if f1 is not None else "n/a"
                print(
                    f"  {event_id}: filing P/R/F1="
                    f"{prec_s}/{rec_s}/{f1_s} "
                    f"({m['hits']}/{gold_n} gold, {len(ev['false_positives_filing'])} FP dates)"
                )
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_json(report), encoding="utf-8")
        if not args.quiet:
            print(f"\n[ok] wrote {out.relative_to(REPO_ROOT)}")
        return 0

    report = calibrate_event(
        event_id=args.event_id,
        manual_only=not args.include_auto_file_notes,
    )
    if not args.quiet:
        print_report(report)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(report), encoding="utf-8")
    if not args.quiet:
        print(f"\n[ok] wrote {args.output.relative_to(REPO_ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
