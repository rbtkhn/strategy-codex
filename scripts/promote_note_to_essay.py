#!/usr/bin/env python3
"""Promote a shelf-native statecraft note to repo-root essays/ (stub law)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_ROOT = REPO_ROOT / "statecraft" / "notes"
ESSAYS_ROOT = REPO_ROOT / "essays"

STUB_HEADER = """---
promotion_status: promoted_to_essay
promoted_at: {date}
canonical: essays/{slug}.md
---

Deprecated compatibility stub — canonical essay: [essays/{slug}.md](../../essays/{slug}.md).

"""

def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Promote statecraft/notes/<slug>.md to essays/<slug>.md. "
            "Phase 4 stub: validates paths and prints promotion checklist; "
            "does not move files until operator confirms with --apply."
        )
    )
    ap.add_argument("note", help="Note path under statecraft/notes/ or bare slug.md")
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Perform move and write stub (default: dry-run checklist only)",
    )
    ap.add_argument("--promoted-at", default="", help="YYYY-MM-DD for stub frontmatter")
    args = ap.parse_args()

    note_path = Path(args.note)
    if not note_path.is_absolute():
        if note_path.parent == Path("."):
            note_path = NOTES_ROOT / note_path.name
        else:
            note_path = REPO_ROOT / note_path

    if not note_path.is_file():
        print(f"note not found: {note_path}", file=sys.stderr)
        return 2

    try:
        note_path.relative_to(NOTES_ROOT)
    except ValueError:
        print("note must live under statecraft/notes/", file=sys.stderr)
        return 2

    slug = note_path.stem
    essay_path = ESSAYS_ROOT / f"{slug}.md"

    print(f"Source: {note_path.relative_to(REPO_ROOT)}")
    print(f"Target: {essay_path.relative_to(REPO_ROOT)}")
    print("Checklist:")
    print("- Run: python3 scripts/check_statecraft_notes.py --verify on source note")
    print("- Confirm essay voice per docs/essay-voice.md and docs/prose-index.md")
    print("- Update essays/README.md cluster entry if load-bearing")
    print("- Stub source note with promotion_status: promoted_to_essay")

    if not args.apply:
        print("Dry run only. Re-run with --apply to execute promotion.")
        return 0

    if essay_path.exists():
        print(f"essay already exists: {essay_path}", file=sys.stderr)
        return 1

    promoted_at = args.promoted_at or "YYYY-MM-DD"
    body = note_path.read_text(encoding="utf-8", errors="replace")
    essay_path.write_text(body, encoding="utf-8")
    stub = STUB_HEADER.format(date=promoted_at, slug=slug) + body
    note_path.write_text(stub, encoding="utf-8")
    print(f"promote_note_to_essay: wrote {essay_path.relative_to(REPO_ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
