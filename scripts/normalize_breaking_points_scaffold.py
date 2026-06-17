#!/usr/bin/env python3
"""Normalize Breaking Points archive scaffold in place.

Conservative lanes (mirrors Davis/Nawfal close_promo pattern):
  1. close_promo — breakingpoints.com signup / like-comment CTA tails
  2. wrapper — fix glued ``## Transcript`` header (missing newline after heading)

Default is dry-run. Host tease and guest substance are preserved.
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
    merge_body_sections,
    split_body_sections,
    split_frontmatter,
)

FRONTMATTER_BLOCK_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

TAIL_SEARCH_CHARS = 8000

CLOSE_PROMO_ANCHOR_RES: list[tuple[str, re.Pattern[str]]] = [
    (
        "like-video-cta",
        re.compile(
            r"(?:>>\s*)?Hey, if you like that video",
            re.IGNORECASE,
        ),
    ),
    (
        "breakingpoints-signup",
        re.compile(
            r"(?:>>\s*)?And if you(?:'d| would) like to get the full show ad[- ]free",
            re.IGNORECASE,
        ),
    ),
    (
        "breakingpoints-support",
        re.compile(
            r"(?:>>\s*)?Help support the future of independent media at breakingpoints\.com",
            re.IGNORECASE,
        ),
    ),
    (
        "breakingpoints-get-full-show",
        re.compile(
            r"(?:>>\s*)?That(?:'s| is) right\. Get the full show",
            re.IGNORECASE,
        ),
    ),
]

EDITORIAL_CLOSE_NOTE = (
    "Routine Breaking Points subscribe/like close trimmed in place; SSOT body otherwise preserved."
)
EDITORIAL_WRAPPER_NOTE = (
    "Transcript section wrapper normalized in place; SSOT body otherwise preserved."
)

TRANSCRIPT_GLUE_RE = re.compile(r"(^## Transcript)(?=[A-Za-z\"'])", re.MULTILINE)


@dataclass(frozen=True)
class BreakingPointsChange:
    path: Path
    close_promo_trimmed: bool = False
    wrapper_trimmed: bool = False
    anchor: str = ""
    chars_removed: int = 0


def is_breaking_points_capture(meta: dict[str, Any], path: Path) -> bool:
    name = path.name.lower()
    if "breaking-points" in name:
        return True
    show = str(meta.get("show") or meta.get("show_title") or "").strip().lower()
    channel = str(meta.get("channel_name") or "").strip().lower()
    channel_slug = str(meta.get("channel_slug") or "").strip().lower()
    return (
        show == "breaking points"
        or channel == "breaking points"
        or channel_slug == "breaking-points"
        or "breaking points" in show
    )


def append_editorial_note(meta: dict[str, Any], note: str) -> None:
    existing = str(meta.get("editorial_note") or "").strip()
    if note.lower() in existing.lower():
        return
    meta["editorial_note"] = f"{existing} {note}".strip() if existing else note


def format_frontmatter_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value)
    if text == "" or any(ch in text for ch in ':"#[]{}') or text != text.strip():
        import json

        return json.dumps(text, ensure_ascii=False)
    return text


def patch_frontmatter_block(text: str, meta: dict[str, Any], keys: set[str]) -> str:
    """Rewrite only selected top-level frontmatter keys; preserve YAML lists/blocks."""
    match = FRONTMATTER_BLOCK_RE.match(text)
    if not match:
        return text
    fm_raw = match.group(0)[4:-4]  # strip --- delimiters
    body = text[match.end() :]
    lines = fm_raw.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            out.append(line)
            i += 1
            continue
        if line.startswith(" ") or line.startswith("\t") or line.lstrip().startswith("- "):
            out.append(line)
            i += 1
            continue
        if ":" not in line:
            out.append(line)
            i += 1
            continue
        key = line.split(":", 1)[0].strip()
        if key in keys and key in meta:
            out.append(f"{key}: {format_frontmatter_value(meta[key])}")
            i += 1
            while i < len(lines) and (
                lines[i].startswith(" ") or lines[i].startswith("\t") or lines[i].lstrip().startswith("- ")
            ):
                i += 1
            continue
        out.append(line)
        i += 1
    present = {line.split(":", 1)[0].strip() for line in out if ":" in line and not line.startswith(" ")}
    for key in keys:
        if key in meta and key not in present:
            out.append(f"{key}: {format_frontmatter_value(meta[key])}")
    return f"---\n" + "\n".join(out).rstrip() + "\n---\n\n" + body


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


def normalize_breaking_points(
    path: Path,
    text: str,
    *,
    apply: bool = False,
    allow_close: bool = True,
    allow_wrapper: bool = True,
    force_close: bool = False,
) -> tuple[bool, str, BreakingPointsChange | None]:
    meta, body = split_frontmatter(text)
    if not is_breaking_points_capture(meta, path):
        return False, text, None

    changed = False
    chars_removed = 0
    anchor = ""
    close_trimmed = False
    wrapper_trimmed = False

    prefix, transcript_header, transcript_body = split_body_sections(body)

    if allow_wrapper and not meta.get("breaking_points_wrapper_trim_applied"):
        merged = prefix + (transcript_header or "") + transcript_body
        fixed, did = fix_transcript_wrapper(merged)
        if did:
            prefix, transcript_header, transcript_body = split_body_sections(fixed)
            meta["breaking_points_wrapper_trim_applied"] = True
            append_editorial_note(meta, EDITORIAL_WRAPPER_NOTE)
            wrapper_trimmed = True
            changed = True

    if (
        allow_close
        and (force_close or not meta.get("breaking_points_close_promo_trim_applied"))
        and transcript_body.strip()
    ):
        new_body, did, anchor, removed = trim_close_promo_text(transcript_body)
        if did:
            transcript_body = new_body
            meta["breaking_points_close_promo_trim_applied"] = True
            append_editorial_note(meta, EDITORIAL_CLOSE_NOTE)
            close_trimmed = True
            chars_removed = removed
            changed = True

    if not changed:
        return False, text, None

    new_body = merge_body_sections(prefix, transcript_header, transcript_body)
    patch_keys = {
        "editorial_note",
        "breaking_points_close_promo_trim_applied",
        "breaking_points_wrapper_trim_applied",
    }
    patched = patch_frontmatter_block(text, meta, patch_keys)
    fm_match = FRONTMATTER_BLOCK_RE.match(patched)
    new_text = (fm_match.group(0) if fm_match else "") + new_body
    change = BreakingPointsChange(
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
    for path in root.rglob("*.md"):
        if ".cleaned." in path.name:
            continue
        if not (path.name.startswith("source-breaking-points") or "breaking-points" in path.name):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        meta, _ = split_frontmatter(text)
        if is_breaking_points_capture(meta, path):
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
        help="Re-run close promo trim even when breaking_points_close_promo_trim_applied is set",
    )
    args = parser.parse_args()

    explicit = (
        [(REPO_ROOT / p if not p.is_absolute() else p).resolve() for p in args.path]
        if args.path
        else None
    )
    paths = candidate_paths(args.root, explicit)
    changes: list[BreakingPointsChange] = []
    skipped = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        changed, _, change = normalize_breaking_points(
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
    print(f"{mode}: {len(changes)} Breaking Points file(s); {skipped} skipped/no-op.")
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
