#!/usr/bin/env python3
"""Write prediction notes from approved freeman-prediction-crawl manifest rows."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "runtime" / "artifacts" / "freeman-prediction-crawl.json"
PREDICTIONS_DIR = REPO_ROOT / "statecraft" / "notes" / "predictions"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_freeman_index import parse_head  # noqa: E402
from freeman_prediction_pilot import FREEMAN_SPEAKER, load_thesis_map, patterns_match  # noqa: E402
from prediction_lib import expected_prediction_status, load_event_registry  # noqa: E402

_EVENT_REGISTRY: dict[str, dict[str, Any]] | None = None

def _prediction_status(event_id: str) -> str:
    global _EVENT_REGISTRY
    if _EVENT_REGISTRY is None:
        _EVENT_REGISTRY = load_event_registry()
    event_status = str(_EVENT_REGISTRY.get(event_id, {}).get("status") or "open")
    return expected_prediction_status(event_status)

EVENT_SLUG: dict[str, str] = {
    "israel_self_destruction_trajectory": "israel-self-destruction",
    "ukraine_escalation_russian_capitulation": "ukraine-kellogg-capitulation",
    "gaza_hostage_deal_jan_2025": "gaza-hostage-deal",
    "gaza_ceasefire_holds_2025": "gaza-ceasefire-holds",
    "us_israel_iran_war_preparation_2025": "us-israel-iran-prep",
    "iran_great_power_direct_war_entry": "iran-great-power-backup",
    "china_tariff_capitulation_2025": "china-tariff-capitulation",
}

EVENT_LABEL: dict[str, str] = {
    "israel_self_destruction_trajectory": "Israel self-destruction",
    "ukraine_escalation_russian_capitulation": "Ukraine Kellogg / capitulation",
    "gaza_hostage_deal_jan_2025": "Gaza hostage deal",
    "gaza_ceasefire_holds_2025": "Gaza ceasefire hold",
    "us_israel_iran_war_preparation_2025": "US–Israel Iran war prep",
    "iran_great_power_direct_war_entry": "Iran great-power backup",
    "china_tariff_capitulation_2025": "China tariff capitulation",
}

FRONTMATTER_RE = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
YOUTUBE_ID_RE = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube_id:\s*[\"']?)([A-Za-z0-9_-]{6,})",
    re.I,
)
INTRO_SKIP = re.compile(
    r"^(hi everyone|hi everybody|okay\.|kind:|language:|# |judge andrew|today is |today's )",
    re.I,
)

EXTRA_META_KEYS = (
    "source_url",
    "youtube_id",
    "cross_host_alias",
    "source_note",
    "channel_slug",
    "thread",
)

def body_without_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text.lstrip("\ufeff"), count=1)

def read_capture_meta(path: Path) -> dict[str, Any]:
    meta = parse_head(path) if path.is_file() else {}
    if not path.is_file():
        return meta
    head = path.read_text(encoding="utf-8", errors="replace")[:8000]
    for key in EXTRA_META_KEYS:
        m = re.search(rf"^{key}:\s*(.+)$", head, re.M)
        if m:
            meta[key] = m.group(1).strip().strip('"').strip("'")
    return meta

def youtube_id_from_meta(meta: dict[str, Any], body: str) -> str | None:
    explicit = str(meta.get("youtube_id") or "").strip()
    if explicit:
        return explicit
    for hay in (str(meta.get("source_url") or ""), body[:4000]):
        m = YOUTUBE_ID_RE.search(hay)
        if m:
            return m.group(1)
    return None

def episode_group_key(event_id: str, pub_date: str, source: str, meta: dict[str, Any], body: str) -> tuple:
    yt = youtube_id_from_meta(meta, body)
    if yt:
        return (event_id, pub_date, yt)
    return (event_id, pub_date, source.replace("\\", "/"))

def canonical_rank(*, source: str, meta: dict[str, Any], body: str) -> tuple[int, str]:
    """Lower rank wins (preferred canonical capture for materialize)."""
    s = source.replace("\\", "/").casefold()
    note = str(meta.get("source_note") or "").casefold()
    slug = str(meta.get("channel_slug") or "").casefold()
    rank = 0
    if "glenn-diesen" in s or slug == "glenn-diesen":
        rank -= 20
    if "source-glenn-diesen" in s:
        rank -= 10
    if "dialogue-works" in s and ("mis-attributed" in note or "mis-attributed host" in note):
        rank += 30
    if "cross_host_alias" in meta and "dialogue-works" in str(meta.get("cross_host_alias")).casefold():
        rank -= 5
    if "judging-freedom" in s or slug == "judging-freedom":
        rank -= 3
    if "india-global-left" in s:
        rank -= 2
    return (rank, s)

def pick_canonical_row(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scored: list[tuple[tuple[int, str], dict[str, Any]]] = []
    for row in rows:
        source = str(row.get("source") or "").replace("\\", "/")
        cap_path = REPO_ROOT / source
        body = cap_path.read_text(encoding="utf-8", errors="replace") if cap_path.is_file() else ""
        meta = read_capture_meta(cap_path)
        scored.append((canonical_rank(source=source, meta=meta, body=body), row))
    scored.sort(key=lambda item: item[0])
    return scored[0][1]

def note_slug(event_id: str, pub_date: str) -> str:
    slug = EVENT_SLUG.get(event_id)
    if not slug:
        raise ValueError(f"unknown event_id for slug: {event_id}")
    return f"{slug}-freeman-{pub_date}.md"

def extract_quote(
    *,
    body: str,
    title: str,
    patterns: list[str],
    exclude: list[str],
) -> str:
    hay = body_without_frontmatter(body)
    sentences = [s.strip() for s in SENTENCE_SPLIT.split(hay) if s.strip()]
    for sentence in sentences:
        if len(sentence) < 40 or len(sentence) > 320:
            continue
        if INTRO_SKIP.search(sentence):
            continue
        if "freeman" in sentence.casefold() and sentence.count(":") == 1 and len(sentence) < 120:
            continue
        if exclude and patterns_match(sentence, exclude):
            continue
        if patterns_match(sentence, patterns):
            return sentence[:240]
    for sentence in sentences:
        if len(sentence) < 40 or len(sentence) > 320:
            continue
        if INTRO_SKIP.search(sentence):
            continue
        if exclude and patterns_match(sentence, exclude):
            continue
        if patterns_match(sentence, patterns[:3] if len(patterns) > 3 else patterns):
            return sentence[:240]
    if title.strip() and not INTRO_SKIP.search(title.strip()):
        return title.strip()[:240]
    return "(audit quote — review capture)"

def alias_tier3_lines(
    *,
    canonical_source: str,
    alias_sources: list[str],
    canonical_meta: dict[str, Any],
) -> list[str]:
    if not alias_sources:
        return []
    yt = youtube_id_from_meta(canonical_meta, "")
    yt_tag = f" `{yt}`" if yt else ""
    lines = ["## Tier-3 context (audit — not stance)", ""]
    for alias in alias_sources:
        alias_meta = read_capture_meta(REPO_ROOT / alias)
        note = str(alias_meta.get("source_note") or "")
        hint = "mis-file alias"
        if "mis-attributed" in note.casefold():
            hint = "Dialogue Works mis-file"
        lines.append(
            f"Alias capture (same episode{yt_tag}): `{alias}` — {hint}; "
            f"canonical host capture is `{canonical_source}`."
        )
    lines.append("")
    return lines

def render_note(
    *,
    event_id: str,
    pub_date: str,
    stance: str,
    speech_act: str,
    source: str,
    quote: str,
    alias_sources: list[str] | None = None,
    canonical_meta: dict[str, Any] | None = None,
    confidence: str = "high",
) -> str:
    label = EVENT_LABEL.get(event_id, event_id.replace("_", " "))
    rel_source = source.replace("\\", "/")
    parts = [
        "---",
        "note_type: prediction",
        f"event_id: {event_id}",
        f"speaker: {FREEMAN_SPEAKER}",
        f"date_made: {pub_date}",
        f"stance: {stance}",
        f"confidence: {confidence}",
        f"source: {rel_source}",
        f"speech_act: {speech_act}",
        f"status: {_prediction_status(event_id)}",
        "---",
        "",
        f"# Freeman — {label} ({pub_date})",
        "",
        "## Quote (audit)",
        "",
        quote,
        "",
    ]
    if alias_sources:
        parts.extend(
            alias_tier3_lines(
                canonical_source=rel_source,
                alias_sources=alias_sources,
                canonical_meta=canonical_meta or {},
            )
        )
    return "\n".join(parts).rstrip() + "\n"

def group_approved_rows(
    rows: list[dict[str, Any]],
    *,
    event_id_filter: str | None,
) -> dict[tuple, list[dict[str, Any]]]:
    groups: dict[tuple, list[dict[str, Any]]] = {}
    for row in rows:
        if str(row.get("audit_status") or "") != "approved":
            continue
        event_id = str(row.get("event_id") or "")
        if event_id_filter and event_id != event_id_filter:
            continue
        pub_date = str(row.get("pub_date") or "")
        source = str(row.get("source") or "").replace("\\", "/")
        if not (event_id and pub_date and source):
            continue
        cap_path = REPO_ROOT / source
        body = cap_path.read_text(encoding="utf-8", errors="replace") if cap_path.is_file() else ""
        meta = read_capture_meta(cap_path)
        key = episode_group_key(event_id, pub_date, source, meta, body)
        groups.setdefault(key, []).append(row)
    return groups

def materialize_manifest(
    *,
    manifest_path: Path,
    dry_run: bool = False,
    force: bool = False,
    event_id_filter: str | None = None,
) -> tuple[int, int, int]:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    thesis = load_thesis_map()
    written = linked = skipped = 0
    groups = group_approved_rows(payload.get("rows") or [], event_id_filter=event_id_filter)

    for _key, group_rows in groups.items():
        canonical = pick_canonical_row(group_rows)
        event_id = str(canonical.get("event_id") or "")
        pub_date = str(canonical.get("pub_date") or "")
        stance = str(canonical.get("audit_stance") or "")
        speech_act = str(canonical.get("audit_speech_act") or "")
        canonical_source = str(canonical.get("source") or "").replace("\\", "/")
        alias_sources = sorted(
            {
                str(r.get("source") or "").replace("\\", "/")
                for r in group_rows
                if str(r.get("source") or "").replace("\\", "/") != canonical_source
            }
        )

        fname = note_slug(event_id, pub_date)
        note_path = PREDICTIONS_DIR / fname
        rel_note = f"statecraft/notes/predictions/{fname}"

        for row in group_rows:
            row["note_file"] = rel_note

        if note_path.is_file() and not force:
            linked += len(group_rows)
            skipped += 1
            continue

        if not (stance and speech_act and canonical_source):
            continue

        cfg = thesis.get(event_id) or {}
        patterns = list(cfg.get("title_patterns") or [])
        exclude = list(cfg.get("exclude_patterns") or [])
        cap_path = REPO_ROOT / canonical_source
        meta = read_capture_meta(cap_path)
        title = str(meta.get("title") or cap_path.name)
        body = cap_path.read_text(encoding="utf-8", errors="replace") if cap_path.is_file() else ""
        quote = extract_quote(body=body, title=title, patterns=patterns, exclude=exclude)
        text = render_note(
            event_id=event_id,
            pub_date=pub_date,
            stance=stance,
            speech_act=speech_act,
            source=canonical_source,
            quote=quote,
            alias_sources=alias_sources,
            canonical_meta=meta,
        )

        if dry_run:
            label = "would write"
            if alias_sources:
                label += f" (+{len(alias_sources)} alias link(s))"
            print(f"[dry-run] {label} {rel_note} from {Path(canonical_source).name}")
            written += 1
            continue

        PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
        note_path.write_text(text, encoding="utf-8")
        written += 1
        linked += len(group_rows)

    if not dry_run:
        manifest_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    return written, linked, skipped

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--event-id", default=None, help="Materialize one event only")
    args = ap.parse_args()
    if not args.manifest.is_file():
        print(f"error: missing {args.manifest.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    written, linked, skipped = materialize_manifest(
        manifest_path=args.manifest,
        dry_run=args.dry_run,
        force=args.force,
        event_id_filter=args.event_id,
    )
    mode = "dry-run" if args.dry_run else "wrote"
    print(
        f"[ok] materialize_freeman_predictions: {mode} {written} note(s), "
        f"linked {linked} manifest row(s), skipped {skipped} existing group(s)"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
