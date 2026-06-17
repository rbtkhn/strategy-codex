#!/usr/bin/env python3
"""Flag known founding-members ASR manglings still present in statecraft transcript bodies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BLOCKLIST = (
    REPO_ROOT
    / "public/ph-civ/data/asr-blocklist/founding-members-pilot.json"
)
DEFAULT_ROOT = REPO_ROOT / "source-archive/statecraft"
TRANSCRIPT_MARKERS = ("## Transcript", "## Full transcript", "## Cleaned Transcript")


@dataclass(frozen=True)
class Hit:
    path: Path
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


def iter_sources(root: Path, glob: str) -> list[Path]:
    return sorted(root.rglob(glob))


def literal_pattern(literal: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z0-9]){re.escape(literal)}(?![A-Za-z0-9])")


def line_hits(
    path: Path,
    body: str,
    entries: list[dict],
    allowed_residual_literals: set[str],
) -> list[Hit]:
    hits: list[Hit] = []
    for line_no, line in enumerate(body.splitlines(), start=1):
        for entry in entries:
            literal = entry["literal"]
            if literal in allowed_residual_literals:
                continue
            if not literal_pattern(literal).search(line):
                continue
            match = literal_pattern(literal).search(line)
            assert match is not None
            start = max(0, match.start() - 24)
            end = min(len(line), match.end() + 24)
            hits.append(
                Hit(
                    path=path,
                    line_no=line_no,
                    entry_id=entry["id"],
                    literal=literal,
                    replacement=entry.get("replacement", ""),
                    excerpt=line[start:end].strip(),
                )
            )
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocklist", type=Path, default=DEFAULT_BLOCKLIST)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--glob",
        default="source-predictive-history-founding-members-*.md",
        help="Glob under --root for transcript sources",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    blocklist_path = args.blocklist.resolve()
    if not blocklist_path.is_file():
        print(f"Blocklist not found: {blocklist_path}", file=sys.stderr)
        return 2

    payload = load_blocklist(blocklist_path)
    entries = payload.get("entries", [])
    allowed = {item["literal"] for item in payload.get("allowed_residuals", [])}

    paths = iter_sources(args.root.resolve(), args.glob)
    all_hits: list[Hit] = []
    for path in paths:
        body = transcript_body(path.read_text(encoding="utf-8"))
        all_hits.extend(line_hits(path, body, entries, allowed))

    if args.json:
        print(
            json.dumps(
                [
                    {
                        "path": str(h.path.relative_to(REPO_ROOT)).replace("\\", "/"),
                        "line": h.line_no,
                        "id": h.entry_id,
                        "literal": h.literal,
                        "replacement": h.replacement,
                        "excerpt": h.excerpt,
                    }
                    for h in all_hits
                ],
                indent=2,
            )
        )
        return 1 if all_hits else 0

    if all_hits:
        print("Statecraft founding-members ASR blocklist: FAIL", file=sys.stderr)
        print(f"  Blocklist: {blocklist_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        for hit in all_hits:
            rel = hit.path.relative_to(REPO_ROOT)
            print(
                f"  - {rel}:{hit.line_no} [{hit.entry_id}] "
                f'"{hit.literal}" -> "{hit.replacement}"',
                file=sys.stderr,
            )
            print(f"      …{hit.excerpt}…", file=sys.stderr)
        print("\nRegenerate: python scripts/generate_founding_members_asr_blocklist.py", file=sys.stderr)
        print("Repair: python scripts/normalize_statecraft_source_asr.py <path> --write", file=sys.stderr)
        return 1

    print(
        f"Statecraft founding-members ASR blocklist OK: "
        f"{len(paths)} source(s), {len(entries)} pattern(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
