#!/usr/bin/env python3
"""Flag known ASR manglings still present in PH-CIV lecture transcript bodies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIRROR_REL = "public/ph-civ"
MIRROR_ROOT = REPO_ROOT / MIRROR_REL
DEFAULT_BLOCKLIST = (
    MIRROR_ROOT / "data/asr-blocklist/volume-ii-pilot.json"
)
PILOT_SLUGS = [f"civ-{n:02d}" for n in range(1, 19)]
TRANSCRIPT_MARKERS = (
    "## Part I: Full transcript",
    "## Full transcript",
)


@dataclass(frozen=True)
class Hit:
    path: Path
    slug: str
    line_no: int
    entry_id: str
    literal: str
    replacement: str
    excerpt: str


def load_blocklist(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def transcript_body(text: str) -> str:
    for marker in TRANSCRIPT_MARKERS:
        if marker in text:
            return text.split(marker, 1)[1]
    return text


def iter_transcripts(root: Path, slugs: list[str] | None) -> list[Path]:
    volume_ii = root / "book/volume-ii"
    if not volume_ii.is_dir():
        return []
    paths: list[Path] = []
    for slug_dir in sorted(volume_ii.iterdir()):
        if not slug_dir.is_dir():
            continue
        slug = slug_dir.name
        if slugs and slug not in slugs:
            continue
        path = slug_dir / f"{slug}-transcript.md"
        if path.is_file():
            paths.append(path)
    return paths


def literal_pattern(literal: str) -> re.Pattern[str]:
    """Match standalone ASR tokens, not substrings inside corrected forms."""
    return re.compile(rf"(?<![A-Za-z0-9]){re.escape(literal)}(?![A-Za-z0-9])")


def line_hits(
    path: Path,
    body: str,
    entries: list[dict],
    allowed_residual_literals: set[str],
) -> list[Hit]:
    slug = path.parent.name
    hits: list[Hit] = []
    lines = body.splitlines()
    for line_no, line in enumerate(lines, start=1):
        for entry in entries:
            literal = entry["literal"]
            entry_slugs = entry.get("slugs")
            if entry_slugs and slug not in entry_slugs:
                continue
            if literal in allowed_residual_literals:
                continue
            match = literal_pattern(literal).search(line)
            if not match:
                continue
            start = max(0, match.start() - 24)
            end = min(len(line), match.end() + 24)
            excerpt = line[start:end].strip()
            hits.append(
                Hit(
                    path=path,
                    slug=slug,
                    line_no=line_no,
                    entry_id=entry["id"],
                    literal=literal,
                    replacement=entry.get("replacement", ""),
                    excerpt=excerpt,
                )
            )
    return hits


def format_report(hits: list[Hit], blocklist_path: Path) -> str:
    lines = [
        "PH-CIV transcript proper-noun blocklist: FAIL",
        f"  Blocklist: {blocklist_path.relative_to(REPO_ROOT)}",
        f"  Hits: {len(hits)}",
        "",
    ]
    for hit in hits:
        rel = hit.path.relative_to(REPO_ROOT)
        lines.append(
            f"  - {rel}:{hit.line_no} [{hit.entry_id}] "
            f'"{hit.literal}" -> "{hit.replacement}"'
        )
        lines.append(f"      …{hit.excerpt}…")
    lines.extend(
        [
            "",
            "Regenerate blocklist after pilot edits:",
            "  python scripts/generate_ph_civ_asr_blocklist.py",
            "Re-run normalization:",
            "  python public/ph-civ/scripts/_pilot_asr_normalize_civ01_civ07.py",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--blocklist",
        type=Path,
        default=DEFAULT_BLOCKLIST,
        help="JSON blocklist path (default: ph-civ/data/asr-blocklist/volume-ii-pilot.json)",
    )
    parser.add_argument(
        "--slug",
        action="append",
        dest="slugs",
        help="Limit to civ slug(s), e.g. civ-08 (repeatable)",
    )
    parser.add_argument(
        "--all-volume-ii",
        action="store_true",
        help="Scan all volume-ii transcripts (default: pilot civ-01..18 only)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON on stdout",
    )
    args = parser.parse_args()

    blocklist_path = args.blocklist.resolve()
    if not blocklist_path.is_file():
        print(f"Blocklist not found: {blocklist_path}", file=sys.stderr)
        return 2

    payload = load_blocklist(blocklist_path)
    entries = payload.get("entries", [])
    allowed_residual_literals = {
        item["literal"] for item in payload.get("allowed_residuals", [])
    }

    if not MIRROR_ROOT.is_dir():
        print(f"PH-CIV mirror not found: {MIRROR_ROOT}", file=sys.stderr)
        return 2

    slugs = args.slugs
    if slugs is None and not args.all_volume_ii:
        slugs = payload.get("pilot_slugs", PILOT_SLUGS)

    all_hits: list[Hit] = []
    for path in iter_transcripts(MIRROR_ROOT, slugs):
        raw = path.read_text(encoding="utf-8")
        body = transcript_body(raw)
        all_hits.extend(
            line_hits(path, body, entries, allowed_residual_literals)
        )

    if args.json:
        print(
            json.dumps(
                [
                    {
                        "path": str(hit.path.relative_to(REPO_ROOT)).replace("\\", "/"),
                        "slug": hit.slug,
                        "line": hit.line_no,
                        "id": hit.entry_id,
                        "literal": hit.literal,
                        "replacement": hit.replacement,
                        "excerpt": hit.excerpt,
                    }
                    for hit in all_hits
                ],
                indent=2,
            )
        )
        return 1 if all_hits else 0

    if all_hits:
        print(format_report(all_hits, blocklist_path), file=sys.stderr)
        return 1

    scope = payload.get("scope", "unknown scope")
    inspected = len(iter_transcripts(MIRROR_ROOT, slugs))
    print(
        f"PH-CIV transcript proper-noun blocklist OK: "
        f"{inspected} transcript(s), {len(entries)} pattern(s), {scope}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
