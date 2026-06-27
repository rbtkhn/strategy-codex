#!/usr/bin/env python3
"""Build a durable master index for strategy-codex source-archive surfaces.

WORK only. This script reads the statecraft source-archive tree and writes generated
statecraft-side index artifacts plus machine-readable JSON companions. It does
not edit source-archive captures, speaker folders, host shelves, or Record surfaces.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_voice_routing_queue as voice_routing  # noqa: E402


DEFAULT_RAW_ROOT = REPO_ROOT / "source-archive" / "statecraft"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "statecraft" / "sheets"
DATE_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WORD_RE = re.compile(r"\b[\w'-]+\b")
MIN_TRANSCRIPT_WORDS = 75
MIN_TRANSCRIPT_CHARS = 400
PLACEHOLDER_PATTERNS = (
    "transcript pending",
    "caption pending",
    "body absent",
    "placeholder transcript",
    "stub transcript",
    "index-only",
    "listed_only",
    "todo: transcript",
    "no transcript available",
    "paste full transcript",
    "paste transcript body",
    "transcript body was not included here",
)
HELPER_FILE_NAMES = {
    ".pruning-suspended",
    "BACKFILL-SOURCES.md",
    "CAPTURE-TYPES.md",
    "README.md",
    "fetch-sources.example.json",
    "fetch-sources.json",
    "youtube-transcript-queue.md",
}
SPECIAL_SPEAKER_DIRS = {"_templates", "map", "relations"}
ARC_INDEX_PATTERNS = (
    re.compile(r".*arc-threads.*\.md$", re.IGNORECASE),
    re.compile(r".*arc.*index.*\.md$", re.IGNORECASE),
)


@dataclass(frozen=True)
class RawInputRecord:
    scope: str
    pub_date: str
    month: str
    rel_path: str
    file_name: str
    kind: str
    body_profile: str
    title: str
    thread: str
    host: str
    guest: str
    show: str
    source_url: str
    source_type: str
    source_form: str
    transcript_type: str
    evidence_grade: str
    body_words: int
    body_chars: int


def _rel(path: Path, root: Path = REPO_ROOT) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    meta = _parse_simple_frontmatter(match.group(1))
    return meta, text[match.end() :]


def _parse_simple_frontmatter(raw: str) -> dict[str, Any]:
    meta: dict[str, Any] = {}
    current_list_key: str | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        list_match = re.match(r"^\s*-\s+(.*)$", line)
        if list_match and current_list_key:
            meta.setdefault(current_list_key, [])
            assert isinstance(meta[current_list_key], list)
            meta[current_list_key].append(_parse_frontmatter_value(list_match.group(1).strip()))
            continue
        key_match = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not key_match:
            current_list_key = None
            continue
        key = key_match.group(1)
        value = key_match.group(2).strip()
        if not value:
            meta[key] = []
            current_list_key = key
            continue
        meta[key] = _parse_frontmatter_value(value)
        current_list_key = None
    return meta


def _parse_frontmatter_value(value: str) -> Any:
    text = value.strip()
    if not text:
        return ""
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return text[1:-1]
    lowered = text.casefold()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "none"}:
        return ""
    if re.fullmatch(r"-?\d+", text):
        try:
            return int(text)
        except ValueError:
            return text
    if re.fullmatch(r"-?\d+\.\d+", text):
        try:
            return float(text)
        except ValueError:
            return text
    return text


def _first_heading_or_stem(text: str, path: Path) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return path.stem


def _effective_body(body: str) -> str:
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and re.match(r"^\s{0,3}#{1,6}\s+", lines[0]):
        lines.pop(0)
        while lines and not lines[0].strip():
            lines.pop(0)
    return "\n".join(lines).strip()


def _body_metrics(body: str) -> tuple[int, int, str]:
    effective = _effective_body(body)
    return len(WORD_RE.findall(effective)), len(effective), effective.casefold()


def _body_profile(meta: dict[str, Any], body: str) -> str:
    kind = str(meta.get("kind") or "").strip().casefold()
    if kind and kind != "transcript":
        return "non-transcript"

    transcript_type = str(meta.get("transcript_type") or "").strip().casefold()
    source_type = str(meta.get("source_type") or "").strip().casefold()
    if transcript_type == "operator_summary_from_web_transcript" or source_type == "web-transcript-derived-summary":
        return "summary-grade"
    if transcript_type == "unresolved_youtube_scaffold":
        return "unresolved-scaffold"
    if "source_path" in meta:
        return "pointer-only"

    body_words, body_chars, body_lower = _body_metrics(body)
    if "transcript has not yet been captured" in body_lower:
        return "unresolved-scaffold"
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern in body_lower:
            return "missing-body"
    if body_words < MIN_TRANSCRIPT_WORDS or body_chars < MIN_TRANSCRIPT_CHARS:
        return "short-body"
    return "full-transcript-body"


def _record_from_path(path: Path, *, scope: str, raw_root: Path) -> RawInputRecord:
    text = _read_text(path)
    meta, body = _split_frontmatter(text)
    title = str(meta.get("title") or "").strip() or _first_heading_or_stem(body, path)
    pub_date = ""
    if scope == "canonical-date-bucket":
        pub_date = path.parent.name
    elif scope == "aired-pending":
        pub_date = str(meta.get("pub_date") or meta.get("ingest_date") or "").strip()
    else:
        pub_date = str(meta.get("pub_date") or meta.get("ingest_date") or "").strip()
    month = pub_date[:7] if re.fullmatch(r"\d{4}-\d{2}-\d{2}", pub_date) else ""
    kind = str(meta.get("kind") or "").strip()
    profile = _body_profile(meta, body)
    evidence_grade = (
        voice_routing.classify_evidence_grade(meta)
        if kind.casefold() == "transcript"
        else ""
    )
    body_words, body_chars, _ = _body_metrics(body)
    return RawInputRecord(
        scope=scope,
        pub_date=pub_date,
        month=month,
        rel_path=_rel(path, raw_root),
        file_name=path.name,
        kind=kind or "(none)",
        body_profile=profile,
        title=title,
        thread=str(meta.get("thread") or "").strip(),
        host=str(meta.get("host") or "").strip(),
        guest=str(meta.get("guest") or "").strip(),
        show=str(meta.get("show") or "").strip(),
        source_url=str(meta.get("source_url") or "").strip(),
        source_type=str(meta.get("source_type") or "").strip(),
        source_form=str(meta.get("source_form") or "").strip(),
        transcript_type=str(meta.get("transcript_type") or "").strip(),
        evidence_grade=evidence_grade,
        body_words=body_words,
        body_chars=body_chars,
    )


def discover_records(raw_root: Path) -> tuple[list[RawInputRecord], list[RawInputRecord], list[RawInputRecord]]:
    canonical: list[RawInputRecord] = []
    pending: list[RawInputRecord] = []
    helpers: list[RawInputRecord] = []

    if not raw_root.exists():
        return canonical, pending, helpers

    for child in sorted(raw_root.iterdir(), key=lambda p: p.name):
        if child.is_dir() and DATE_DIR_RE.fullmatch(child.name):
            for md in sorted(child.glob("*.md")):
                canonical.append(_record_from_path(md, scope="canonical-date-bucket", raw_root=raw_root))
            continue
        if child.is_dir() and child.name == "_aired-pending":
            for md in sorted(child.glob("*.md")):
                pending.append(_record_from_path(md, scope="aired-pending", raw_root=raw_root))
            continue
        if child.is_dir() and child.name == "snippets":
            for md in sorted(child.glob("*.md")):
                helpers.append(_record_from_path(md, scope="snippet-helper", raw_root=raw_root))
            continue
        if child.is_file() and child.name in HELPER_FILE_NAMES:
            helpers.append(_record_from_path(child, scope="helper-surface", raw_root=raw_root))
            continue
        if child.is_file() and child.suffix == ".md":
            helpers.append(_record_from_path(child, scope="helper-surface", raw_root=raw_root))

    return canonical, pending, helpers


def _counter_table(counter: Counter[str]) -> list[str]:
    lines = ["| class | count |", "|---|---:|"]
    for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{key}` | {count} |")
    return lines


def _month_counts(records: list[RawInputRecord]) -> dict[str, dict[str, int]]:
    grouped: dict[str, dict[str, int]] = defaultdict(lambda: {"files": 0, "transcript": 0, "full_body": 0, "incomplete": 0})
    for record in records:
        if not record.month:
            continue
        row = grouped[record.month]
        row["files"] += 1
        if record.kind.casefold() == "transcript":
            row["transcript"] += 1
            if record.body_profile == "full-transcript-body":
                row["full_body"] += 1
            else:
                row["incomplete"] += 1
    return dict(grouped)


def _day_summary(records: list[RawInputRecord]) -> dict[str, list[RawInputRecord]]:
    grouped: dict[str, list[RawInputRecord]] = defaultdict(list)
    for record in records:
        grouped[record.pub_date].append(record)
    for bucket in grouped.values():
        bucket.sort(key=lambda item: (item.kind, item.file_name))
    return dict(sorted(grouped.items()))


def _speakers_root(raw_root: Path) -> Path:
    del raw_root  # legacy param; voices root is repo-fixed
    return REPO_ROOT / "statecraft" / "voices"


def _speaker_dirs(speakers_root: Path) -> list[Path]:
    if not speakers_root.exists():
        return []
    return [
        path
        for path in sorted(speakers_root.iterdir(), key=lambda item: item.name)
        if path.is_dir() and path.name not in SPECIAL_SPEAKER_DIRS
    ]


def _speaker_index_paths(speakers_root: Path) -> list[Path]:
    return sorted(speakers_root.glob("*/*-raw-input-index.md"))


def _arc_index_candidate_paths(speakers_root: Path) -> list[Path]:
    candidates: list[Path] = []
    for path in speakers_root.rglob("*.md"):
        name = path.name
        if name == "index.md" or name.endswith("-raw-input-index.md"):
            continue
        if any(pattern.fullmatch(name) for pattern in ARC_INDEX_PATTERNS):
            candidates.append(path)
    return sorted(candidates)


def _record_mentions_speaker(record: RawInputRecord, speaker_slug: str) -> bool:
    haystacks = [
        record.file_name,
        record.title,
        record.thread,
        record.host,
        record.guest,
        record.show,
    ]
    lower_slug = speaker_slug.casefold()
    return any(lower_slug in value.casefold() for value in haystacks if value)


def _speaker_signal_counts(
    canonical: list[RawInputRecord],
    speakers_root: Path,
) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    transcript_records = [record for record in canonical if record.kind.casefold() == "transcript"]
    for speaker_dir in _speaker_dirs(speakers_root):
        slug = speaker_dir.name
        stream_dir = speaker_dir / "stream"
        stream_markdown = len(list(stream_dir.glob("*.md"))) if stream_dir.exists() else 0
        local_markdown = len(list(speaker_dir.glob("*.md")))
        transcript_mentions = sum(
            1 for record in transcript_records if _record_mentions_speaker(record, slug)
        )
        counts[slug] = {
            "transcript_mentions": transcript_mentions,
            "stream_markdown": stream_markdown,
            "local_markdown": local_markdown,
        }
    return counts


def build_audit_payload(
    raw_root: Path,
    *,
    canonical: list[RawInputRecord],
    output_root: Path = DEFAULT_OUTPUT_ROOT,
) -> dict[str, Any]:
    speakers_root = _speakers_root(raw_root)
    speaker_indexes = _speaker_index_paths(speakers_root)
    indexed_speakers = {path.parent.name for path in speaker_indexes}
    arc_candidates = _arc_index_candidate_paths(speakers_root)
    signal_counts = _speaker_signal_counts(canonical, speakers_root)

    weak_signals: list[dict[str, Any]] = []
    for path in arc_candidates:
        speaker = path.parent.parent.name if path.parent.name == "stream" else path.parent.name
        signal = {
            "speaker": speaker,
            "path": _rel(path),
            "reason": "index-like arc support surface exists alongside a speaker bench; verify it remains interpretive rather than becoming a duplicate retrieval surface.",
        }
        if speaker in indexed_speakers:
            weak_signals.append(signal)

    missing_bench: list[dict[str, Any]] = []
    for speaker, counts in sorted(signal_counts.items()):
        if speaker in indexed_speakers:
            continue
        transcript_mentions = counts["transcript_mentions"]
        stream_markdown = counts["stream_markdown"]
        local_markdown = counts["local_markdown"]
        if local_markdown < 2:
            continue
        if transcript_mentions >= 3 or stream_markdown >= 2:
            reason_bits = [f"transcript mentions={transcript_mentions}"]
            if stream_markdown:
                reason_bits.append(f"stream markdown={stream_markdown}")
            reason_bits.append(f"speaker markdown={local_markdown}")
            missing_bench.append(
                {
                    "speaker": speaker,
                    "reason": "; ".join(reason_bits),
                }
            )

    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "raw_root": _rel(raw_root),
        "speakers_root": _rel(speakers_root),
        "master_index": {
            "expected_markdown": 1,
            "found_markdown": 1 if (output_root / "source-archive-master-index.md").exists() else 0,
            "expected_json": 1,
            "found_json": 1 if (output_root / "source-archive-master-index.json").exists() else 0,
        },
        "speaker_raw_input_indexes": [
            {"speaker": path.parent.name, "path": _rel(path)} for path in speaker_indexes
        ],
        "candidate_arc_index_surfaces": [
            {"speaker": path.parent.parent.name if path.parent.name == "stream" else path.parent.name, "path": _rel(path)}
            for path in arc_candidates
        ],
        "weak_justification_signals": weak_signals,
        "missing_bench_candidates": missing_bench,
        "speaker_signal_counts": signal_counts,
    }
    payload["summary"] = {
        "speaker_raw_input_index_count": len(payload["speaker_raw_input_indexes"]),
        "candidate_arc_index_surface_count": len(payload["candidate_arc_index_surfaces"]),
        "weak_justification_signal_count": len(weak_signals),
        "missing_bench_candidate_count": len(missing_bench),
    }
    return payload


def render_audit_markdown(
    raw_root: Path,
    *,
    canonical: list[RawInputRecord],
    output_root: Path = DEFAULT_OUTPUT_ROOT,
) -> str:
    payload = build_audit_payload(raw_root, canonical=canonical, output_root=output_root)
    lines = [
        "# Source-Archive index architecture audit",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "WORK only; not Record. This is a heuristic audit over the secondary source-archive analytic layer and speaker routing surfaces.",
        "",
        "Navigation rule: canonical browsing now lives at `source-archive/statecraft/` via the generated day, month, year, thread, and stale-audit indices. This audit remains an analytic helper, not the primary navigation surface.",
        "",
        "## Summary",
        "",
        f"- corpus-wide master indexes expected: `markdown={payload['master_index']['expected_markdown']}`, `json={payload['master_index']['expected_json']}`",
        f"- corpus-wide master indexes found: `markdown={payload['master_index']['found_markdown']}`, `json={payload['master_index']['found_json']}`",
        f"- speaker source-capture indexes present: `{payload['summary']['speaker_raw_input_index_count']}`",
        f"- candidate arc index surfaces: `{payload['summary']['candidate_arc_index_surface_count']}`",
        f"- weak justification signals: `{payload['summary']['weak_justification_signal_count']}`",
        f"- plausible missing benches: `{payload['summary']['missing_bench_candidate_count']}`",
        "",
        "## Speaker source-capture indexes",
        "",
    ]
    for row in payload["speaker_raw_input_indexes"]:
        lines.append(f"- `{row['speaker']}` -> [{Path(row['path']).name}]({row['path']})")

    lines.extend(["", "## Candidate arc index surfaces", ""])
    if payload["candidate_arc_index_surfaces"]:
        for row in payload["candidate_arc_index_surfaces"]:
            lines.append(f"- `{row['speaker']}` -> [{Path(row['path']).name}]({row['path']})")
    else:
        lines.append("- none")

    lines.extend(["", "## Weak justification signals", ""])
    if payload["weak_justification_signals"]:
        for row in payload["weak_justification_signals"]:
            lines.append(f"- `{row['speaker']}` -> [{Path(row['path']).name}]({row['path']}) | {row['reason']}")
    else:
        lines.append("- none")

    lines.extend(["", "## Missing bench candidates", ""])
    if payload["missing_bench_candidates"]:
        for row in payload["missing_bench_candidates"]:
            lines.append(f"- `{row['speaker']}` | {row['reason']}")
    else:
        lines.append("- none")

    lines.extend(["", "## Signal counts", "", "| speaker | transcript mentions | stream markdown | speaker markdown |", "|---|---:|---:|---:|"])
    for speaker, counts in sorted(payload["speaker_signal_counts"].items()):
        lines.append(
            f"| `{speaker}` | {counts['transcript_mentions']} | {counts['stream_markdown']} | {counts['local_markdown']} |"
        )

    lines.append("")
    return "\n".join(lines)


def render_markdown(
    *,
    raw_root: Path,
    canonical: list[RawInputRecord],
    pending: list[RawInputRecord],
    helpers: list[RawInputRecord],
) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    transcript_records = [record for record in canonical if record.kind.casefold() == "transcript"]
    transcript_profiles = Counter(record.body_profile for record in transcript_records)
    kind_counts = Counter(record.kind for record in canonical)
    month_counts = _month_counts(canonical)
    day_records = _day_summary(canonical)

    lines = [
        "# Source-Archive master index",
        "",
        f"Generated: `{generated_at}`",
        "",
        "WORK only; not Record. This file is generated from the on-disk source-archive tree.",
        "",
        "Authority rule: the dated source-archive folders remain authoritative.",
        "",
        "Navigation rule: this is a secondary analytic rollup. Canonical archive navigation now lives at `source-archive/statecraft/` via the generated day, month, year, thread, and stale-audit indices.",
        "",
        "## Scope",
        "",
        f"- canonical date-bucket captures: `{len(canonical)}`",
        f"- `_aired-pending` captures: `{len(pending)}`",
        f"- helper surfaces and inventories: `{len(helpers)}`",
        f"- transcript-kind canonical captures: `{len(transcript_records)}`",
        "",
        "## Canonical counts by kind",
        "",
        *_counter_table(kind_counts),
        "",
        "## Canonical transcript body platform/profile",
        "",
        *_counter_table(transcript_profiles),
        "",
        "## Canonical month summary",
        "",
        "| month | files | transcript kind | full transcript body | incomplete transcript body |",
        "|---|---:|---:|---:|---:|",
    ]
    for month in sorted(month_counts):
        row = month_counts[month]
        lines.append(
            f"| `{month}` | {row['files']} | {row['transcript']} | {row['full_body']} | {row['incomplete']} |"
        )

    current_month = ""
    for pub_date, records in day_records.items():
        month = pub_date[:7]
        if month != current_month:
            current_month = month
            lines.extend(["", f"## {month}", ""])
        lines.extend(["", f"### {pub_date} ({len(records)})", ""])
        for record in records:
            title = record.title.replace("|", "\\|")
            details = [
                f"`kind:{record.kind}`",
                f"`form:{record.source_form or '(none)'}`",
                f"`body:{record.body_profile}`",
            ]
            if record.thread:
                details.append(f"`thread:{record.thread}`")
            if record.host:
                details.append(f"`host:{record.host}`")
            if record.guest:
                details.append(f"`guest:{record.guest}`")
            if record.evidence_grade:
                details.append(f"`grade:{record.evidence_grade}`")
            lines.append(f"- [{record.file_name}]({record.rel_path}) — {title} | " + " | ".join(details))

    if pending:
        lines.extend(["", "## _aired-pending", ""])
        for record in pending:
            title = record.title.replace("|", "\\|")
            details = [f"`kind:{record.kind}`", f"`form:{record.source_form or '(none)'}`", f"`body:{record.body_profile}`"]
            if record.thread:
                details.append(f"`thread:{record.thread}`")
            lines.append(f"- [{record.file_name}]({record.rel_path}) — {title} | " + " | ".join(details))

    if helpers:
        helper_counts = Counter(record.scope for record in helpers)
        lines.extend(["", "## Helper surfaces", ""])
        lines.extend(_counter_table(helper_counts))
        lines.append("")
        for record in helpers:
            title = record.title.replace("|", "\\|")
            lines.append(f"- [{record.file_name}]({record.rel_path}) — {title} | `{record.scope}` | `kind:{record.kind}`")

    lines.append("")
    return "\n".join(lines)


def build_payload(raw_root: Path) -> dict[str, Any]:
    canonical, pending, helpers = discover_records(raw_root)
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "raw_root": _rel(raw_root),
        "canonical": [asdict(record) for record in canonical],
        "aired_pending": [asdict(record) for record in pending],
        "helpers": [asdict(record) for record in helpers],
    }
    payload["summary"] = {
        "canonical_count": len(canonical),
        "aired_pending_count": len(pending),
        "helper_count": len(helpers),
        "canonical_kind_counts": dict(Counter(record.kind for record in canonical)),
        "canonical_transcript_profile_counts": dict(
            Counter(
                record.body_profile
                for record in canonical
                if record.kind.casefold() == "transcript"
            )
        ),
    }
    return payload


def write_outputs(
    raw_root: Path,
    *,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
    index_name: str = "source-archive-master-index",
) -> dict[str, Path]:
    canonical, pending, helpers = discover_records(raw_root)
    markdown = render_markdown(raw_root=raw_root, canonical=canonical, pending=pending, helpers=helpers)
    payload = build_payload(raw_root)
    audit_markdown = render_audit_markdown(raw_root, canonical=canonical, output_root=output_root)
    audit_payload = build_audit_payload(raw_root, canonical=canonical, output_root=output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    md_path = output_root / f"{index_name}.md"
    json_path = output_root / f"{index_name}.json"
    audit_md_path = output_root / "source-archive-index-audit.md"
    audit_json_path = output_root / "source-archive-index-audit.json"
    md_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    audit_md_path.write_text(audit_markdown, encoding="utf-8")
    audit_json_path.write_text(json.dumps(audit_payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return {
        "markdown": md_path,
        "json": json_path,
        "audit_markdown": audit_md_path,
        "audit_json": audit_json_path,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT, help="Statecraft source-archive root to index.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT, help="Statecraft sheets directory for generated outputs.")
    parser.add_argument("--index-name", default="source-archive-master-index", help="Base filename for generated outputs.")
    parser.add_argument("--json", action="store_true", help="Print JSON payload to stdout instead of writing files.")
    parser.add_argument("--markdown", action="store_true", help="Print Markdown index to stdout instead of writing files.")
    parser.add_argument("--audit-json", action="store_true", help="Print the index-architecture audit JSON to stdout.")
    parser.add_argument("--audit-markdown", action="store_true", help="Print the index-architecture audit Markdown to stdout.")
    parser.add_argument("--apply", action="store_true", help="Write the generated index files to disk.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    raw_root = args.raw_root.resolve()
    if args.json:
        print(json.dumps(build_payload(raw_root), indent=2, ensure_ascii=True))
        return 0
    if args.markdown:
        canonical, pending, helpers = discover_records(raw_root)
        print(render_markdown(raw_root=raw_root, canonical=canonical, pending=pending, helpers=helpers), end="")
        return 0
    if args.audit_json:
        canonical, _, _ = discover_records(raw_root)
        print(json.dumps(build_audit_payload(raw_root, canonical=canonical), indent=2, ensure_ascii=True))
        return 0
    if args.audit_markdown:
        canonical, _, _ = discover_records(raw_root)
        print(render_audit_markdown(raw_root, canonical=canonical), end="")
        return 0
    if not args.apply:
        print("raw_input_master_index: pass --apply, --json, --markdown, --audit-json, or --audit-markdown", file=sys.stderr)
        return 2
    outputs = write_outputs(raw_root, output_root=args.output_root.resolve(), index_name=args.index_name)
    print(json.dumps({key: _rel(value) for key, value in outputs.items()}, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
