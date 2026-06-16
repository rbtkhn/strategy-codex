#!/usr/bin/env python3
"""Apply ph-civ ASR replacement tiers to a statecraft source-archive transcript.

WORK only; not Record. Preserves frontmatter + header; normalizes body below
``## Transcript`` (or ``## Full transcript``). Also runs bounded regex entity
repairs from ``fix_statecraft_common_asr_entities``.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WJ_DIR = REPO_ROOT / "scripts" / "work_jiang"
if str(WJ_DIR) not in sys.path:
    sys.path.insert(0, str(WJ_DIR))
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from asr_light_clean import detect_series, normalize_transcript_text  # noqa: E402
from fix_statecraft_common_asr_entities import apply_replacements as apply_entity_re  # noqa: E402

TRANSCRIPT_HEADINGS = ("## Transcript", "## Full transcript", "## Cleaned Transcript")
FM_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
EDITORIAL_NOTE_RE = re.compile(r'^editorial_note:\s*"?(.+?)"?\s*$', re.DOTALL)
SOURCE_NOTE_RE = re.compile(r"^source_note:\s*(.+)$", re.MULTILINE)
PRESERVE_EDITORIAL_MARKERS = (
    "trimmed",
    "sponsor",
    "stripped",
    "subscribe",
    "cold open",
    "promo",
)


def split_transcript(md: str) -> tuple[str, str | None]:
    for heading in TRANSCRIPT_HEADINGS:
        idx = md.find(heading)
        if idx == -1:
            continue
        nl = md.find("\n", idx)
        if nl == -1:
            return md[: idx + len(heading)] + "\n", ""
        return md[: nl + 1], md[nl + 1 :]
    return md, None


def _parse_quoted_field(line: str) -> str:
    raw = line.split(":", 1)[-1].strip()
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    return raw.strip('"')


def _merge_editorial_note(existing: str | None, sub_count: int) -> str:
    base = (
        f"AI-assisted ASR repair (common + series tiers + statecraft entity pass); "
        f"{sub_count} substitutions; not human-verified verbatim; verify before quotation."
    )
    if not existing:
        return base
    low = existing.lower()
    if any(marker in low for marker in PRESERVE_EDITORIAL_MARKERS):
        return f"{base} Prior provenance: {existing.rstrip('.')}."
    return base


def _append_source_note_asr_pass(fm_block: str, today: str) -> str:
    marker = f"ASR pass {today}"
    if marker in fm_block:
        return fm_block
    match = SOURCE_NOTE_RE.search(fm_block)
    if not match:
        return fm_block
    old = match.group(1).strip().strip('"')
    new_val = f"{old} · {marker}."
    return fm_block[: match.start()] + f'source_note: "{new_val}"' + fm_block[match.end() :]


def patch_frontmatter(fm_block: str, *, sub_count: int, prior_editorial: str | None = None) -> str:
    today = date.today().isoformat()
    lines = fm_block.splitlines()
    body_lines: list[str] = []
    if lines and lines[0].strip() == "---":
        lines = lines[1:]
    if lines and lines[-1].strip() == "---":
        lines = lines[:-1]
    seen_kind = seen_norm = seen_type = seen_edit = seen_quality = False
    captured_editorial: str | None = prior_editorial
    for line in lines:
        if line.startswith("kind:"):
            body_lines.append("kind: cleaned-transcript")
            seen_kind = True
            continue
        if line.startswith("transcript_type:"):
            body_lines.append("transcript_type: ai_assisted_operator_pasted_youtube_transcript")
            seen_type = True
            continue
        if line.startswith("normalization_state:"):
            body_lines.append("normalization_state: ai_assisted_proper_noun_cleanup")
            seen_norm = True
            continue
        if line.startswith("editorial_note:"):
            if captured_editorial is None:
                captured_editorial = _parse_quoted_field(line)
            seen_edit = True
            continue
        if line.startswith("quality_note:"):
            body_lines.append(f'quality_note: "ASR normalization pass {today}; ph-civ replacement SSOT."')
            seen_quality = True
            continue
        body_lines.append(line)
    if not seen_kind:
        body_lines.insert(0, "kind: cleaned-transcript")
    if not seen_type:
        body_lines.insert(1 if not seen_kind else 2, "transcript_type: ai_assisted_operator_pasted_youtube_transcript")
    if not seen_norm:
        body_lines.append("normalization_state: ai_assisted_proper_noun_cleanup")
    merged_edit = _merge_editorial_note(captured_editorial, sub_count)
    body_lines.append(f'editorial_note: "{merged_edit}"')
    if not seen_quality:
        body_lines.append(f'quality_note: "ASR normalization pass {today}; ph-civ replacement SSOT."')
    block = "---\n" + "\n".join(body_lines) + "\n---"
    return _append_source_note_asr_pass(block, today)


def run(path: Path, *, series: str | None, write: bool) -> int:
    raw = path.read_text(encoding="utf-8")
    head, body = split_transcript(raw)
    if body is None:
        print(f"{path}: no transcript heading found", file=sys.stderr)
        return 1

    prior_editorial: str | None = None
    fm_match = FM_RE.match(raw)
    if fm_match:
        for line in fm_match.group(0).splitlines():
            if line.startswith("editorial_note:"):
                prior_editorial = _parse_quoted_field(line)
                break

    series_resolved = detect_series(path) if series == "auto" else series
    new_body, n = normalize_transcript_text(body, series=series_resolved)
    new_body, entity_counts = apply_entity_re(new_body)
    n += sum(entity_counts.values())

    body_changed = new_body != body
    should_patch_fm = write and fm_match is not None

    if n == 0 and not body_changed and not should_patch_fm:
        print(f"{path}: no substitutions (series={series_resolved!r})")
        return 0

    if should_patch_fm:
        new_fm = patch_frontmatter(
            fm_match.group(0).rstrip("\n"),
            sub_count=n,
            prior_editorial=prior_editorial,
        ) + "\n"
        head = new_fm + head[len(fm_match.group(0)) :]

    new_text = head + (new_body if body_changed else body)

    print(
        f"{path}: {n} substitution(s) (series={series_resolved!r}); "
        f"entity={dict(entity_counts)}; body_changed={body_changed}; fm_patched={should_patch_fm}"
    )
    if write:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--series",
        default="auto",
        help="Replacement tier (auto from filename, or e.g. founding-members, game-theory, none).",
    )
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    path = args.path.resolve()
    if not path.is_file():
        print(f"Not a file: {path}", file=sys.stderr)
        return 1
    series = None if args.series == "none" else args.series
    return run(path, series=series, write=args.write)


if __name__ == "__main__":
    raise SystemExit(main())
