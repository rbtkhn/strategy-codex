#!/usr/bin/env python3
"""Fix Nima Alkhorshid display spelling in archive YAML and speaker labels."""
from __future__ import annotations

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"

# Phase 3: frontmatter + title/scaffold — not transcript speaker labels.
REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("host: Nima Alkhorshid", "host: Nima Alkhorshid"),
    ('host: "Nima Alkhorshid"', 'host: "Nima Alkhorshid"'),
    ("guest: Nima Alkhorshid", "guest: Nima Alkhorshid"),
    ("# Nima Alkhorshid", "# Nima Alkhorshid"),
    ("Dialogue Works (Nima Alkhorshid)", "Dialogue Works (Nima Alkhorshid)"),
    ("**Host:** Nima Alkhorshid", "**Host:** Nima Alkhorshid"),
    ("  - Nima Alkhorshid", "  - Nima Alkhorshid"),
)

# Phase 4: curated speaker labels and section-open prose (not verbatim ASR mis-hearings).
SPEAKER_LABEL_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("**Nima Alkhorshid:**", "**Nima Alkhorshid:**"),
    ("Nima Alkhorshid and ", "Nima Alkhorshid and "),
)

def _apply_replacements(text: str, replacements: tuple[tuple[str, str], ...]) -> tuple[str, int]:
    subs = 0
    for old, new in replacements:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            subs += count
    return text, subs

def sweep(*, replacements: tuple[tuple[str, str], ...], dry_run: bool = False) -> tuple[int, int]:
    changed_files = 0
    total_subs = 0
    for path in sorted(ARCHIVE_ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        orig = text
        text, subs = _apply_replacements(text, replacements)
        if text == orig:
            continue
        changed_files += 1
        total_subs += subs
        if not dry_run:
            path.write_text(text, encoding="utf-8", newline="\n")
        rel = path.relative_to(REPO_ROOT)
        print(f"{'would fix' if dry_run else 'fixed'} {subs:3d}  {rel}")
    return changed_files, total_subs

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--speaker-labels",
        action="store_true",
        help="Fix **Nima Alkhorshid:** labels and curated section-open host names only.",
    )
    args = parser.parse_args()
    replacements = SPEAKER_LABEL_REPLACEMENTS if args.speaker_labels else REPLACEMENTS
    n_files, n_subs = sweep(replacements=replacements, dry_run=args.dry_run)
    mode = "speaker-labels" if args.speaker_labels else "meta"
    print(f"summary ({mode}): files={n_files} replacements={n_subs}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
