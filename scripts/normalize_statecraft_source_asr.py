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


def patch_frontmatter(fm_block: str, *, sub_count: int) -> str:
    today = date.today().isoformat()
    lines = fm_block.splitlines()
    body_lines: list[str] = []
    if lines and lines[0].strip() == "---":
        lines = lines[1:]
    if lines and lines[-1].strip() == "---":
        lines = lines[:-1]
    seen_kind = seen_norm = seen_type = seen_edit = seen_quality = False
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
            body_lines.append(
                'editorial_note: "AI-assisted ASR repair (common + series tiers + statecraft entity pass); '
                f"{sub_count} substitutions; not human-verified verbatim; verify before quotation.\""
            )
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
    if not seen_edit:
        body_lines.append(
            'editorial_note: "AI-assisted ASR repair; not human-verified verbatim; verify before quotation."'
        )
    if not seen_quality:
        body_lines.append(f'quality_note: "ASR normalization pass {today}; ph-civ replacement SSOT."')
    return "---\n" + "\n".join(body_lines) + "\n---"


def run(path: Path, *, series: str | None, write: bool) -> int:
    raw = path.read_text(encoding="utf-8")
    head, body = split_transcript(raw)
    if body is None:
        print(f"{path}: no transcript heading found", file=sys.stderr)
        return 1

    series_resolved = detect_series(path) if series == "auto" else series
    new_body, n = normalize_transcript_text(body, series=series_resolved)
    new_body, entity_counts = apply_entity_re(new_body)
    n += sum(entity_counts.values())

    if n == 0:
        print(f"{path}: no substitutions (series={series_resolved!r})")
        return 0

    if head.startswith("---"):
        fm_match = FM_RE.match(head)
        if fm_match:
            new_fm = patch_frontmatter(fm_match.group(0).rstrip("\n"), sub_count=n) + "\n"
            head = new_fm + head[len(fm_match.group(0)) :]

    new_text = head + new_body

    print(
        f"{path}: {n} substitution(s) (series={series_resolved!r}); "
        f"entity={dict(entity_counts)}"
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
