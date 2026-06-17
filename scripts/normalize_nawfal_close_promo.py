#!/usr/bin/env python3
"""Trim routine Mario Nawfal closing lineup / next-guest promo tails from archive transcripts.

Conservative lane (mirrors Napolitano ``close_promo``): cut from the first separable
Mario lineup anchor in the transcript tail; keep guest sign-off rapport immediately
before the anchor.

Default is dry-run. Use ``--apply`` to write in place.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from normalize_nawfal_opening_banter import (  # noqa: E402
    ARCHIVE_ROOT,
    dump_frontmatter,
    is_nawfal_hosted,
    merge_body_sections,
    split_body_sections,
    split_frontmatter,
    split_paragraphs,
)

TAIL_SEARCH_CHARS = 8000

# Strong Mario lineup anchors — ordered by preference when multiple match in tail.
CLOSE_PROMO_ANCHOR_RES: list[tuple[str, re.Pattern[str]]] = [
    (
        "all-right-guys",
        re.compile(
            r"(?:>>\s*)?(?:Um,?\s+)?All right,?\s+guys\b",
            re.IGNORECASE,
        ),
    ),
    (
        "enjoyed-coverage",
        re.compile(r"I hope you enjoyed the coverage\b", re.IGNORECASE),
    ),
    (
        "we-do-have-joining",
        re.compile(
            r"(?:>>\s*)?(?:Um,?\s+)?We do have\s+[\w\s.'-]{2,60}?\s+joining\b",
            re.IGNORECASE,
        ),
    ),
    (
        "going-live",
        re.compile(
            r"(?:>>\s*)?(?:Um,?\s+)?I(?:'ll| will) be (?:going )?live(?: again)?\b",
            re.IGNORECASE,
        ),
    ),
    (
        "see-you-schedule",
        re.compile(
            r"(?:>>\s*)?(?:Um,?\s+)?I(?:'ll| will) see you (?:guys )?"
            r"(?:in (?:about|less than|a couple|\d+)|soon)\b",
            re.IGNORECASE,
        ),
    ),
]

EDITORIAL_CLOSE_NOTE = (
    "Routine closing lineup promo trimmed in place; SSOT body otherwise preserved."
)


@dataclass(frozen=True)
class ClosePromoChange:
    path: Path
    anchor: str
    chars_removed: int
    kept_tail: str


def append_editorial_note(meta: dict[str, Any], note: str) -> None:
    existing = str(meta.get("editorial_note") or "").strip()
    if note.lower() in existing.lower():
        return
    meta["editorial_note"] = f"{existing} {note}".strip() if existing else note


def find_close_promo_cut(full_text: str) -> tuple[int, str] | None:
    """Return (cut_index, anchor_name) or None."""
    search_window = full_text[-TAIL_SEARCH_CHARS:] if len(full_text) > TAIL_SEARCH_CHARS else full_text
    window_offset = len(full_text) - len(search_window)

    candidates: list[tuple[int, str, int]] = []
    for name, pattern in CLOSE_PROMO_ANCHOR_RES:
        for match in pattern.finditer(search_window):
            abs_start = window_offset + match.start()
            priority = CLOSE_PROMO_ANCHOR_RES.index((name, pattern))
            candidates.append((abs_start, name, priority))

    if not candidates:
        return None

    # Prefer earliest cut in tail among highest-priority anchor family.
    min_priority = min(p for _, _, p in candidates)
    best = min(
        (c for c in candidates if c[2] == min_priority),
        key=lambda item: item[0],
    )
    return best[0], best[1]


def trim_close_promo_text(text: str) -> tuple[str, bool, str, int]:
    trimmed_text = text.rstrip()
    found = find_close_promo_cut(trimmed_text)
    if not found:
        return text, False, "", 0
    cut_at, anchor = found
    new_text = trimmed_text[:cut_at].rstrip()
    if not new_text or new_text == trimmed_text:
        return text, False, "", 0
    if not new_text.endswith("\n"):
        new_text += "\n"
    return new_text, True, anchor, len(trimmed_text) - len(new_text)


def trim_close_promo_paragraphs(paragraphs: list[str]) -> tuple[list[str], bool, str, int]:
    if not paragraphs:
        return paragraphs, False, "", 0
    full_text = "\n\n".join(paragraphs)
    new_text, changed, anchor, removed = trim_close_promo_text(full_text)
    if not changed:
        return paragraphs, False, "", 0
    return split_paragraphs(new_text), True, anchor, removed


def normalize_close_promo(
    path: Path,
    text: str,
    *,
    apply: bool = False,
) -> tuple[bool, str, ClosePromoChange | None]:
    meta, body = split_frontmatter(text)
    if not is_nawfal_hosted(meta, path):
        return False, text, None

    if meta.get("nawfal_close_promo_trim_applied"):
        return False, text, None

    prefix, transcript_header, transcript_body = split_body_sections(body)
    if not transcript_body.strip():
        return False, text, None

    paragraphs = split_paragraphs(transcript_body)
    new_paragraphs, changed, anchor, removed = trim_close_promo_paragraphs(paragraphs)
    if not changed:
        return False, text, None

    kept_tail = new_paragraphs[-1][-220:] if new_paragraphs else ""
    meta["nawfal_close_promo_trim_applied"] = True
    append_editorial_note(meta, EDITORIAL_CLOSE_NOTE)

    new_transcript = "\n\n".join(new_paragraphs).rstrip() + "\n"
    new_body = merge_body_sections(prefix, transcript_header, new_transcript)
    new_text = dump_frontmatter(meta) + new_body

    change = ClosePromoChange(path=path, anchor=anchor, chars_removed=removed, kept_tail=kept_tail)
    if apply:
        path.write_text(new_text, encoding="utf-8")
    return True, new_text, change


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ARCHIVE_ROOT)
    parser.add_argument("--path", type=Path, action="append", default=[], help="Explicit archive file(s).")
    parser.add_argument("--apply", action="store_true", help="Write changes in place.")
    args = parser.parse_args()

    if args.path:
        paths = sorted(
            {
                (REPO_ROOT / p if not p.is_absolute() else p).resolve()
                for p in args.path
            }
        )
    else:
        paths = sorted(args.root.rglob("source-nawfal-*.md"))

    changes: list[ClosePromoChange] = []
    skipped = 0
    for path in paths:
        if not path.is_file():
            print(f"skip missing {path}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8")
        changed, _, change = normalize_close_promo(path, text, apply=args.apply)
        if change is None:
            skipped += 1
            continue
        if changed:
            changes.append(change)

    mode = "Applied" if args.apply else "Dry-run"
    print(f"{mode}: {len(changes)} Nawfal file(s) close_promo trim; {skipped} skipped/no-op.")
    for change in changes:
        rel = change.path.relative_to(REPO_ROOT).as_posix()
        print(f"- {rel} anchor={change.anchor} removed={change.chars_removed}c")
        print(f"  kept_tail: ...{change.kept_tail.replace(chr(10), ' ')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
