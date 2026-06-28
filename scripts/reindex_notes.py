#!/usr/bin/env python3
"""Generate statecraft notes registry from note contract metadata."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_ROOT = REPO_ROOT / "statecraft" / "notes"
DEFAULT_OUT = REPO_ROOT / "runtime" / "artifacts" / "statecraft-notes-registry.md"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_statecraft_notes import (  # noqa: E402
    STUB_MARKER,
    classify_tier,
    parse_note_metadata,
)


def collect_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(NOTES_ROOT.rglob("*.md")):
        tier = classify_tier(path)
        if tier not in {"A", "B"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if STUB_MARKER in text:
            continue
        meta = parse_note_metadata(path, text)
        rel = path.relative_to(REPO_ROOT).as_posix()
        rows.append(
            {
                "path": rel,
                "title": path.stem,
                "note_type": meta.note_type or "",
                "authority_level": meta.authority_level or "",
                "essay_candidate": "true" if meta.essay_candidate else "false",
                "source_basis": meta.source_basis or "",
                "tier": tier,
            }
        )
    return rows


def render_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Statecraft notes registry (generated)",
        "",
        "Do not edit by hand. Regenerate:",
        "",
        "```bash",
        "python3 scripts/reindex_notes.py",
        "```",
        "",
        "| title | type | authority | essay_candidate | source_basis | tier | path |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in sorted(rows, key=lambda r: (r["note_type"], r["title"])):
        link = f"[{row['title']}](../../{row['path']})"
        lines.append(
            "| {title} | {note_type} | {authority_level} | {essay_candidate} | "
            "{source_basis} | {tier} | {link} |".format(link=link, **row)
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help="Registry output path (default: runtime/artifacts/statecraft-notes-registry.md)",
    )
    ap.add_argument("--stdout", action="store_true", help="Print registry to stdout only")
    args = ap.parse_args()

    rows = collect_rows()
    text = render_markdown(rows)
    if args.stdout:
        print(text)
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"reindex_notes: wrote {args.output.relative_to(REPO_ROOT)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
