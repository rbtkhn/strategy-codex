#!/usr/bin/env python3
"""Normalize Daniel Davis Deep Dive archive scaffold in place.

Conservative lanes (mirrors Nawfal/Napolitano close_promo pattern):
  1. close_promo — subscribe/like, next-episode tease, noon lineup, travel close
  2. wrapper — fix glued ``## Transcript`` header (missing newline after heading)

Default is dry-run. Host news tease / guest substantive setup is preserved.
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
    merge_body_sections,
    split_body_sections,
    split_frontmatter,
)

TAIL_SEARCH_CHARS = 8000

CLOSE_PROMO_ANCHOR_RES: list[tuple[str, re.Pattern[str]]] = [
    (
        "subscribe-like",
        re.compile(
            r"Subscribe,?\s+hit that like button",
            re.IGNORECASE,
        ),
    ),
    (
        "subscribe-like-send",
        re.compile(
            r"Subscribe,\s*like,\s*and send this to somebody",
            re.IGNORECASE,
        ),
    ),
    (
        "like-subscribe-way-out",
        re.compile(
            r"Be sure(?:\s+and|\s+to)\s+like and subscribe if you haven't",
            re.IGNORECASE,
        ),
    ),
    (
        "gold-stock-cta",
        re.compile(
            r"You know,?\s+I don't try to talk you into buying gold",
            re.IGNORECASE,
        ),
    ),
    (
        "next-episode",
        re.compile(
            r"Look forward to seeing you on the next episode of the Daniel Davis",
            re.IGNORECASE,
        ),
    ),
    (
        "see-you-next-time",
        re.compile(
            r"I(?:'ll| will) see you next time on the Daniel Davis",
            re.IGNORECASE,
        ),
    ),
    (
        "noon-lineup",
        re.compile(
            r"we'll see you then at noon",
            re.IGNORECASE,
        ),
    ),
    (
        "tune-in-lineup",
        re.compile(
            r"Be sure and tune in at \d",
            re.IGNORECASE,
        ),
    ),
    (
        "later-today-lineup",
        re.compile(
            r"And we will see you guys(?:\s+uh)? later on today at \d",
            re.IGNORECASE,
        ),
    ),
    (
        "see-you-then-show",
        re.compile(
            r"(?:(?:we'll|we will)\s+)?See you then on the Daniel Davis(?:\s+(?:team|deep))?(?:\s+dive)?",
            re.IGNORECASE,
        ),
    ),
    (
        "thanks-folks-close",
        re.compile(
            r"Thanks very much,?\s+folks",
            re.IGNORECASE,
        ),
    ),
    (
        "look-forward-guest",
        re.compile(
            r"(?<!we'll )(?<!we will )(?:>>\s*)?Look forward to seeing you(?:\s+[\w.-]+)? on the next episode",
            re.IGNORECASE,
        ),
    ),
    (
        "grateful-guest-outro",
        re.compile(
            r"And as always, we're very, very grateful for you coming in",
            re.IGNORECASE,
        ),
    ),
    (
        "travel-schedule",
        re.compile(
            r"I am back on some travels",
            re.IGNORECASE,
        ),
    ),
    (
        "see-you-next-davis",
        re.compile(
            r"we'll see you next on the Daniel Davis(?:\s+\w+)?",
            re.IGNORECASE,
        ),
    ),
    (
        "appreciate-you-guys-close",
        re.compile(
            r">> And we appreciate you guys, too",
            re.IGNORECASE,
        ),
    ),
    (
        "podcast-tell-friends",
        re.compile(
            r"Don't forget to tell your friends",
            re.IGNORECASE,
        ),
    ),
]

EDITORIAL_CLOSE_NOTE = (
    "Routine closing lineup/subscribe promo trimmed in place; SSOT body otherwise preserved."
)
EDITORIAL_WRAPPER_NOTE = (
    "Transcript section wrapper normalized in place; SSOT body otherwise preserved."
)

TRANSCRIPT_GLUE_RE = re.compile(r"(^## Transcript)(?=[A-Za-z\"'])", re.MULTILINE)

@dataclass(frozen=True)
class DavisChange:
    path: Path
    close_promo_trimmed: bool = False
    wrapper_trimmed: bool = False
    anchor: str = ""
    chars_removed: int = 0

def is_davis_capture(meta: dict[str, Any], path: Path) -> bool:
    name = path.name.lower()
    if not name.startswith("source-daniel-davis"):
        return False
    show = str(meta.get("show") or meta.get("show_title") or "").strip().lower()
    host = str(meta.get("host") or "").strip().lower()
    channel = str(meta.get("channel_name") or "").strip().lower()
    return (
        "daniel davis" in show
        or "daniel davis" in host
        or "daniel davis" in channel
        or "daniel-davis" in name
    )

def append_editorial_note(meta: dict[str, Any], note: str) -> None:
    existing = str(meta.get("editorial_note") or "").strip()
    if note.lower() in existing.lower():
        return
    meta["editorial_note"] = f"{existing} {note}".strip() if existing else note

def find_close_promo_cut(full_text: str) -> tuple[int, str] | None:
    search_window = full_text[-TAIL_SEARCH_CHARS:] if len(full_text) > TAIL_SEARCH_CHARS else full_text
    window_offset = len(full_text) - len(search_window)
    candidates: list[tuple[int, str]] = []
    for name, pattern in CLOSE_PROMO_ANCHOR_RES:
        for match in pattern.finditer(search_window):
            abs_start = window_offset + match.start()
            candidates.append((abs_start, name))
    if not candidates:
        return None
    best = min(candidates, key=lambda item: item[0])
    return best[0], best[1]

def trim_close_promo_text(text: str) -> tuple[str, bool, str, int]:
    trimmed = text.rstrip()
    found = find_close_promo_cut(trimmed)
    if not found:
        return text, False, "", 0
    cut_at, anchor = found
    new_text = trimmed[:cut_at].rstrip()
    if not new_text or new_text == trimmed:
        return text, False, "", 0
    if not new_text.endswith("\n"):
        new_text += "\n"
    return new_text, True, anchor, len(trimmed) - len(new_text)

def fix_transcript_wrapper(body: str) -> tuple[str, bool]:
    if not TRANSCRIPT_GLUE_RE.search(body):
        return body, False
    return TRANSCRIPT_GLUE_RE.sub(r"\1\n\n", body, count=1), True

def normalize_davis(
    path: Path,
    text: str,
    *,
    apply: bool = False,
    allow_close: bool = True,
    allow_wrapper: bool = True,
    force_close: bool = False,
) -> tuple[bool, str, DavisChange | None]:
    meta, body = split_frontmatter(text)
    if not is_davis_capture(meta, path):
        return False, text, None

    changed = False
    chars_removed = 0
    anchor = ""
    close_trimmed = False
    wrapper_trimmed = False

    prefix, transcript_header, transcript_body = split_body_sections(body)

    if allow_wrapper and not meta.get("davis_wrapper_trim_applied"):
        merged = prefix + (transcript_header or "") + transcript_body
        fixed, did = fix_transcript_wrapper(merged)
        if did:
            prefix, transcript_header, transcript_body = split_body_sections(fixed)
            meta["davis_wrapper_trim_applied"] = True
            append_editorial_note(meta, EDITORIAL_WRAPPER_NOTE)
            wrapper_trimmed = True
            changed = True

    if (
        allow_close
        and (force_close or not meta.get("davis_close_promo_trim_applied"))
        and transcript_body.strip()
    ):
        new_body, did, anchor, removed = trim_close_promo_text(transcript_body)
        if did:
            transcript_body = new_body
            meta["davis_close_promo_trim_applied"] = True
            append_editorial_note(meta, EDITORIAL_CLOSE_NOTE)
            close_trimmed = True
            chars_removed = removed
            changed = True

    if not changed:
        return False, text, None

    new_body = merge_body_sections(prefix, transcript_header, transcript_body)
    new_text = dump_frontmatter(meta) + new_body
    change = DavisChange(
        path=path,
        close_promo_trimmed=close_trimmed,
        wrapper_trimmed=wrapper_trimmed,
        anchor=anchor,
        chars_removed=chars_removed,
    )
    if apply:
        path.write_text(new_text, encoding="utf-8")
    return True, new_text, change

def candidate_paths(root: Path, explicit: list[Path] | None = None) -> list[Path]:
    if explicit:
        return sorted({p.resolve() for p in explicit})
    paths: list[Path] = []
    for path in root.rglob("source-daniel-davis*.md"):
        if ".cleaned." in path.name:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        meta, _ = split_frontmatter(text)
        if is_davis_capture(meta, path):
            paths.append(path)
    return sorted(set(paths))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ARCHIVE_ROOT)
    parser.add_argument("--path", type=Path, action="append", default=[])
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--no-close", action="store_true")
    parser.add_argument("--no-wrapper", action="store_true")
    parser.add_argument(
        "--force-close",
        action="store_true",
        help="Re-run close promo trim even when davis_close_promo_trim_applied is set",
    )
    args = parser.parse_args()

    explicit = (
        [(REPO_ROOT / p if not p.is_absolute() else p).resolve() for p in args.path]
        if args.path
        else None
    )
    paths = candidate_paths(args.root, explicit)
    changes: list[DavisChange] = []
    skipped = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        changed, _, change = normalize_davis(
            path,
            text,
            apply=args.apply,
            allow_close=not args.no_close,
            allow_wrapper=not args.no_wrapper,
            force_close=args.force_close,
        )
        if change is None:
            skipped += 1
            continue
        if changed:
            changes.append(change)

    mode = "Applied" if args.apply else "Dry-run"
    print(f"{mode}: {len(changes)} Davis file(s); {skipped} skipped/no-op.")
    for change in changes:
        rel = change.path.relative_to(REPO_ROOT).as_posix()
        flags = []
        if change.close_promo_trimmed:
            flags.append(f"close={change.anchor}")
        if change.wrapper_trimmed:
            flags.append("wrapper")
        if change.chars_removed:
            flags.append(f"-{change.chars_removed}c")
        print(f"- {rel} [{', '.join(flags)}]")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
