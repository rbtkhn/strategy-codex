#!/usr/bin/env python3
"""Create cleaned study derivatives from transcript-bearing raw-input files.
This script preserves source raw-input files and writes
separate cleaned derivatives plus cleanup receipts.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
from repo_io import ARTIFACTS_DIR

from yaml_compat import safe_dump, safe_load_text  # noqa: E402

DEFAULT_RECEIPT_ROOT = ARTIFACTS_DIR / "transcript-cleanup"
WORD_RE = re.compile(r"\b[\w'-]+\b")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

GLOSSARY: dict[str, str] = {
    "Adessa": "Odesa",
    "Ali Larij Jani": "Ali Larijani",
    "Barniel": "Barnea",
    "Chasufiar": "Chasiv Yar",
    "Chasfyar": "Chasiv Yar",
    "Chas of Yar": "Chasiv Yar",
    "Chaz Freeman": "Chas Freeman",
    "Cinping": "Xi Jinping",
    "Cining": "Xi Jinping",
    "Dujiffka": "Druzhkivka",
    "Dujifka": "Druzhkivka",
    "Hin Matal": "Rheinmetall",
    "Jai Shanka": "Jaishankar",
    "Kaakalis": "Kaja Kallas",
    "Kataussk": "Kramatorsk",
    "Katausk": "Kramatorsk",
    "Katossk": "Kramatorsk",
    "Lavro": "Lavrov",
    "Mandi": "Marandi",
    "Manny": "Marandi",
    "Mirandi": "Marandi",
    "Naboo": "NABU",
    "Neper": "Dnieper",
    "Nepro": "Dnipro",
    "Nema": "Nima",
    "Rigul": "Riegel",
    "Shooyu": "Shoigu",
    "Sining": "Xi Jinping",
    "TAD": "THAAD",
    "Tajjikistan": "Tajikistan",
    "Yermach": "Yermak",
    "Zalinski": "Zelensky",
    "Zaporosia": "Zaporizhzhia",
    "Zaporia": "Zaporizhzhia",
    "Zaporoia": "Zaporizhzhia",
    "Zilinski": "Zelensky",
    "chassis missiles": "JASSM missiles",
    "helium sulfate": "highly enriched uranium",
    "non-coaching": "non-coercion",
    "non-exchange": "non-interference",
    "sea of Azorov": "Sea of Azov",
    "tourist missiles": "Taurus missiles",
    "zero someum": "zero-sum",
}

GUEST_GLOSSARY: dict[str, dict[str, str]] = {
    "Andrei Martyanov": {
        "Andre Martiano": "Andrei Martyanov",
        "Andrei Martiano": "Andrei Martyanov",
        "Andre Martyanov": "Andrei Martyanov",
        "Andre": "Andrei",
    },
    "Larry Wilkerson": {
        "Larry Wilkinson": "Larry Wilkerson",
        "Larry Wilkenson": "Larry Wilkerson",
    },
}

PLACEHOLDER_PATTERNS = (
    "transcript pending",
    "caption pending",
    "paste full transcript",
    "paste transcript body",
    "placeholder transcript",
)

@dataclass(frozen=True)
class CleanupResult:
    source_path: Path
    output_path: Path
    status: str
    cleanup_score: int
    cleanup_grade: str
    source_word_count: int
    cleaned_word_count: int
    corrections: dict[str, int]
    components: dict[str, dict[str, Any]]
    residual_noise_terms: list[str]
    receipt_detail_path: Path | None = None

def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()

def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    raw = match.group(1)
    body = text[match.end() :]
    try:
        data = safe_load_text(raw, feature="clean_raw_input_transcript.py")
    except Exception:
        return {}, body
    return (data if isinstance(data, dict) else {}), body

def dump_frontmatter(data: dict[str, Any]) -> str:
    raw = safe_dump(
        data,
        feature="clean_raw_input_transcript.py",
        sort_keys=False,
        allow_unicode=True,
        width=2000,
    ).rstrip()
    return f"---\n{raw}\n---\n\n"

def effective_body_text(body: str) -> str:
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and re.match(r"^\s{0,3}#{1,6}\s+", lines[0]):
        lines.pop(0)
        while lines and not lines[0].strip():
            lines.pop(0)
    return "\n".join(lines).strip()

def output_path_for(source: Path) -> Path:
    if source.name.endswith(".cleaned.md"):
        return source
    return source.with_name(f"{source.stem}.cleaned.md")

def load_raw_input_list(path: Path | None, raw_inputs: list[Path]) -> list[Path]:
    items = list(raw_inputs)
    if not path:
        return items
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        items.append(Path(line))
    return items

def validate_source(meta: dict[str, Any], body: str) -> list[str]:
    errors: list[str] = []
    for key in ("source_url", "pub_date", "title"):
        if not str(meta.get(key) or "").strip():
            errors.append(f"missing source frontmatter: {key}")
    if str(meta.get("kind") or "") not in {"transcript", "cleaned-transcript"}:
        errors.append("source kind is not transcript-like")
    if not str(meta.get("source_type") or "").strip():
        errors.append("missing source_type")
    if not str(meta.get("transcript_type") or "").strip():
        errors.append("missing transcript_type")
    lowered = body.lower()
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern in lowered:
            errors.append(f"placeholder body: {pattern}")
    if len(WORD_RE.findall(body)) < 75:
        errors.append("source body too short")
    return errors

def remove_caption_artifacts(body: str) -> tuple[list[str], int]:
    out: list[str] = []
    removed = 0
    for raw in body.splitlines():
        line = html.unescape(raw).strip()
        line = re.sub(r"\s+", " ", line)
        if not line:
            continue
        if line in {"WEBVTT", "Kind: captions", "Language: en"}:
            removed += 1
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?", line):
            removed += 1
            continue
        if "-->" in line:
            removed += 1
            continue
        out.append(line)
    return out, removed

def collapse_repeated_fragments(lines: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    removed = 0
    previous = ""
    for line in lines:
        if line == previous:
            removed += 1
            continue
        out.append(line)
        previous = line
    return out, removed

def glossary_for(source_meta: dict[str, Any] | None = None) -> dict[str, str]:
    glossary = dict(GLOSSARY)
    if not source_meta:
        return glossary
    guest = str(source_meta.get("guest") or "").strip()
    if guest in GUEST_GLOSSARY:
        glossary.update(GUEST_GLOSSARY[guest])
    return glossary

def apply_glossary(text: str, source_meta: dict[str, Any] | None = None) -> tuple[str, dict[str, int]]:
    corrections: dict[str, int] = {}
    out = text
    glossary = glossary_for(source_meta)
    for bad, good in sorted(glossary.items(), key=lambda item: len(item[0]), reverse=True):
        flags = 0 if any(ch.isupper() for ch in bad) else re.IGNORECASE
        pattern = re.compile(rf"(?<!\w){re.escape(bad)}(?!\w)", flags)
        out, count = pattern.subn(good, out)
        if count:
            corrections[f"{bad} -> {good}"] = count
    return out, corrections

def reflow_lines(lines: list[str]) -> str:
    paragraphs: list[str] = []
    buffer = ""
    for line in lines:
        if line.startswith(">>"):
            if buffer:
                paragraphs.append(buffer.strip())
            buffer = line
        elif not buffer:
            buffer = line
        else:
            buffer = f"{buffer} {line}"
        if len(buffer) > 650 and re.search(r"[.!?][\"')\]]?$", buffer):
            paragraphs.append(buffer.strip())
            buffer = ""
    if buffer:
        paragraphs.append(buffer.strip())
    return "\n\n".join(paragraphs).strip()

def residual_noise_terms(text: str, source_meta: dict[str, Any] | None = None) -> list[str]:
    found: list[str] = []
    for bad in glossary_for(source_meta):
        flags = 0 if any(ch.isupper() for ch in bad) else re.IGNORECASE
        if re.search(rf"(?<!\w){re.escape(bad)}(?!\w)", text, flags):
            found.append(bad)
    return sorted(found, key=str.casefold)

def provenance_issues(source_meta: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    caption_kind = str(source_meta.get("caption_kind") or "").strip().lower()
    source_note = str(source_meta.get("source_note") or "").strip().lower()
    if caption_kind == "manual" and "auto-caption" in source_note:
        issues.append("caption_kind manual conflicts with auto-caption source_note")
    if caption_kind.startswith("auto") and "manual" in source_note:
        issues.append("caption_kind auto conflicts with manual source_note")

    guest = str(source_meta.get("guest") or "").strip()
    host = str(source_meta.get("host") or "").strip()
    if guest and host:
        host_parts = {part.casefold() for part in re.findall(r"[A-Za-z]+", host)}
        guest_parts = {part.casefold() for part in re.findall(r"[A-Za-z]+", guest)}
        if guest_parts and guest_parts.issubset(host_parts):
            issues.append("guest appears to be host-only inference")
    return issues

def compute_components(
    *,
    source_meta: dict[str, Any],
    source_body: str,
    cleaned_body: str,
    artifact_removed_count: int,
    duplicate_removed_count: int,
    corrections: dict[str, int],
    residual_terms: list[str],
) -> dict[str, dict[str, Any]]:
    source_lines = [line for line in source_body.splitlines() if line.strip()]
    cleaned_paragraphs = [para for para in cleaned_body.split("\n\n") if para.strip()]
    source_words = len(WORD_RE.findall(source_body))
    cleaned_words = len(WORD_RE.findall(cleaned_body))
    word_ratio = (cleaned_words / source_words) if source_words else 0.0
    source_had_bad_terms = bool(residual_noise_terms(source_body, source_meta))
    has_guest = bool(str(source_meta.get("guest") or "").strip())
    has_turn_markers = ">>" in cleaned_body or bool(re.search(r"(?m)^[A-Z][A-Za-z .'-]{1,40}:", cleaned_body))
    speaker_score = 10 if (not has_guest or has_turn_markers) else 6
    paragraph_score = 20 if cleaned_paragraphs and len(cleaned_paragraphs) < max(12, len(source_lines) // 3) and word_ratio >= 0.9 else 12
    proper_score = 20 if not residual_terms and (corrections or not source_had_bad_terms) else (14 if not residual_terms else 6)
    residual_score = 10 if not residual_terms else max(0, 10 - min(10, len(residual_terms) * 2))
    frontmatter_score = 10 if all(str(source_meta.get(key) or "").strip() for key in ("source_url", "pub_date", "title")) else 0
    provenance = provenance_issues(source_meta)
    provenance_score = 5 if not provenance else 0
    artifact_score = 15 if not re.search(r"(?m)^(Kind: captions|Language: en|WEBVTT)$", cleaned_body) else 5
    dedupe_score = 10 if duplicate_removed_count or "\n\n" in cleaned_body else 8
    return {
        "frontmatter_integrity": {"score": frontmatter_score, "max": 10, "passed": frontmatter_score == 10},
        "provenance_integrity": {"score": provenance_score, "max": 5, "passed": provenance_score == 5, "issues": provenance},
        "caption_artifact_removal": {"score": artifact_score, "max": 15, "passed": artifact_score == 15, "removed": artifact_removed_count},
        "repeated_fragment_collapse": {"score": dedupe_score, "max": 10, "passed": dedupe_score >= 8, "removed": duplicate_removed_count},
        "paragraph_reflow": {
            "score": paragraph_score,
            "max": 20,
            "passed": paragraph_score >= 16,
            "source_lines": len(source_lines),
            "cleaned_paragraphs": len(cleaned_paragraphs),
        },
        "proper_noun_normalization": {"score": proper_score, "max": 20, "passed": proper_score >= 16, "corrections": corrections},
        "speaker_turns_where_clear": {"score": speaker_score, "max": 10, "passed": speaker_score >= 8, "required": has_guest},
        "residual_noise_scan": {"score": residual_score, "max": 10, "passed": residual_score == 10, "terms": residual_terms},
    }

def score_from_components(components: dict[str, dict[str, Any]]) -> int:
    return int(sum(int(component["score"]) for component in components.values()))

def build_cleaned_content(
    *,
    source_path: Path,
    source_meta: dict[str, Any],
    source_body: str,
    cleaned_body: str,
    result: CleanupResult,
    detail_path: Path,
) -> str:
    cleanup_grade = result.cleanup_grade
    evidence_grade = "cleaned-transcript" if cleanup_grade == "cleaned-transcript-80" else "transcript-grade-cleaned-draft"
    title = str(source_meta.get("title") or source_path.stem)
    meta = {
        "ingest_date": datetime.now(timezone.utc).date().isoformat(),
        "pub_date": str(source_meta.get("pub_date") or source_path.parent.name),
        "kind": "cleaned-transcript",
        "source_type": str(source_meta.get("source_type") or "youtube"),
        "transcript_type": "machine_assisted_caption_cleanup",
        "title": title,
        "source_url": str(source_meta.get("source_url") or ""),
        "source_raw_input": _rel(source_path),
        "cleanup_score": result.cleanup_score,
        "cleanup_grade": cleanup_grade,
        "cleanup_receipt": _rel(detail_path),
        "cleanup_method": "machine-assisted-caption-cleanup",
        "human_review": "spot-check",
        "audio_verified": False,
        "proper_noun_policy": "known-glossary-only",
        "source_note": "Cleaned derivative from subtitle-derived raw-input. Not human-verified verbatim.",
        "editorial_note": "Machine-assisted cleanup removed caption artifacts, reflowed paragraphs, and applied known-glossary-only proper-noun normalization.",
        "evidence_grade": evidence_grade,
        "body_word_count": result.cleaned_word_count,
    }
    for key in ("show", "host", "guest", "thread", "channel_slug", "youtube_id", "caption_language", "caption_kind"):
        value = source_meta.get(key)
        if value not in (None, ""):
            meta[key] = value
    return dump_frontmatter(meta) + f"# {title}\n\n{cleaned_body.rstrip()}\n"

def clean_one(source_path: Path, *, receipt_dir: Path | None, apply: bool) -> tuple[CleanupResult, str | None]:
    text = source_path.read_text(encoding="utf-8", errors="replace")
    source_meta, raw_body = split_frontmatter(text)
    source_body = effective_body_text(raw_body)
    errors = validate_source(source_meta, source_body)
    output_path = output_path_for(source_path)
    detail_path = receipt_dir / "details" / f"{source_path.stem}.cleanup.json" if receipt_dir else None
    if errors:
        components = {
            "source_validation": {"score": 0, "max": 100, "passed": False, "errors": errors}
        }
        result = CleanupResult(
            source_path=source_path,
            output_path=output_path,
            status="failed-source-validation",
            cleanup_score=0,
            cleanup_grade="failed-cleanup",
            source_word_count=len(WORD_RE.findall(source_body)),
            cleaned_word_count=0,
            corrections={},
            components=components,
            residual_noise_terms=[],
            receipt_detail_path=detail_path,
        )
        return result, None

    lines, artifact_removed_count = remove_caption_artifacts(source_body)
    lines, duplicate_removed_count = collapse_repeated_fragments(lines)
    reflowed = reflow_lines(lines)
    cleaned_body, corrections = apply_glossary(reflowed, source_meta)
    residual_terms = residual_noise_terms(cleaned_body, source_meta)
    components = compute_components(
        source_meta=source_meta,
        source_body=source_body,
        cleaned_body=cleaned_body,
        artifact_removed_count=artifact_removed_count,
        duplicate_removed_count=duplicate_removed_count,
        corrections=corrections,
        residual_terms=residual_terms,
    )
    score = score_from_components(components)
    grade = "cleaned-transcript-80" if score >= 80 else "transcript-grade-cleaned-draft"
    result = CleanupResult(
        source_path=source_path,
        output_path=output_path,
        status="cleaned" if apply else "dry-run",
        cleanup_score=score,
        cleanup_grade=grade,
        source_word_count=len(WORD_RE.findall(source_body)),
        cleaned_word_count=len(WORD_RE.findall(cleaned_body)),
        corrections=corrections,
        components=components,
        residual_noise_terms=residual_terms,
        receipt_detail_path=detail_path,
    )
    if not apply:
        return result, None
    assert detail_path is not None
    content = build_cleaned_content(
        source_path=source_path,
        source_meta=source_meta,
        source_body=source_body,
        cleaned_body=cleaned_body,
        result=result,
        detail_path=detail_path,
    )
    output_path.write_text(content, encoding="utf-8")
    return result, content

def result_payload(result: CleanupResult) -> dict[str, Any]:
    return {
        "source_path": _rel(result.source_path),
        "output_path": _rel(result.output_path),
        "status": result.status,
        "cleanup_score": result.cleanup_score,
        "cleanup_grade": result.cleanup_grade,
        "source_word_count": result.source_word_count,
        "cleaned_word_count": result.cleaned_word_count,
        "corrections": result.corrections,
        "residual_noise_terms": result.residual_noise_terms,
        "components": result.components,
        "cleanup_receipt": _rel(result.receipt_detail_path) if result.receipt_detail_path else "",
    }

def write_receipts(results: list[CleanupResult], receipt_dir: Path, *, batch_label: str) -> dict[str, str]:
    receipt_dir.mkdir(parents=True, exist_ok=True)
    details_dir = receipt_dir / "details"
    details_dir.mkdir(parents=True, exist_ok=True)
    ledger = receipt_dir / "cleanup-ledger.jsonl"
    summary = receipt_dir / "cleanup-summary.md"
    for result in results:
        if result.receipt_detail_path:
            result.receipt_detail_path.parent.mkdir(parents=True, exist_ok=True)
            result.receipt_detail_path.write_text(
                json.dumps(result_payload(result), indent=2, ensure_ascii=True) + "\n",
                encoding="utf-8",
            )
    ledger.write_text(
        "".join(json.dumps(result_payload(result), ensure_ascii=True) + "\n" for result in results),
        encoding="utf-8",
    )
    passed = sum(1 for result in results if result.cleanup_grade == "cleaned-transcript-80")
    lines = [
        "# Transcript cleanup summary",
        "",
                "",
        f"- batch: `{batch_label}`",
        f"- cleaned-80: `{passed}` / `{len(results)}`",
        f"- receipt: `{_rel(ledger)}`",
        "",
        "## Files",
        "",
    ]
    for result in results:
        lines.append(
            f"- `{result.cleanup_score}` `{result.cleanup_grade}` - `{_rel(result.output_path)}` from `{_rel(result.source_path)}`"
        )
    summary.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {
        "ledger": str(ledger),
        "summary": str(summary),
        "details_dir": str(details_dir),
    }

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-input", action="append", type=Path, default=[])
    parser.add_argument("--raw-input-list", type=Path, default=None)
    parser.add_argument("--receipt-root", type=Path, default=DEFAULT_RECEIPT_ROOT)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--batch-label", default="transcript-cleanup")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--no-apply", action="store_false", dest="apply")
    parser.set_defaults(apply=False)
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = load_raw_input_list(args.raw_input_list, args.raw_input)
    if not paths:
        print("No raw-input paths provided.", file=sys.stderr)
        return 2
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    receipt_dir = args.receipt_root / run_id if args.apply else None
    results: list[CleanupResult] = []
    for path in paths:
        result, _content = clean_one(path, receipt_dir=receipt_dir, apply=args.apply)
        results.append(result)
    receipts = write_receipts(results, receipt_dir, batch_label=args.batch_label) if args.apply and receipt_dir else {}
    print(json.dumps({"rows": [result_payload(result) for result in results], "receipts": receipts}, indent=2, ensure_ascii=True))
    return 1 if any(result.status.startswith("failed") for result in results) else 0

if __name__ == "__main__":
    raise SystemExit(main())
