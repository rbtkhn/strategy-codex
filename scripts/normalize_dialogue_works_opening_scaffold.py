#!/usr/bin/env python3
"""Normalize Dialogue Works / Nima Alkhorshid archive scaffold in place.

Spec (conservative trim lanes):
  1. leading_noise — [music], ## Cleaned Transcript bleed
  2. host_intro — keep Hi everybody + date + guest welcome (dating SSOT)
  3. mid_substack_cta — separable Substack / book / channel promo before first crisis question
  4. book_substack_interrupt — separable book+Substack tangent between host question and guest answer
  5. close_substack_cta — routine closing link laundry

Default is dry-run. Solo monologues: do not trim timezone/date preamble.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TRANSCRIPT_SECTION_RE = re.compile(r"(^## Transcript\s*\n)(.*)$", re.DOTALL | re.MULTILINE)

HOST_ANCHOR_RE = re.compile(r"Hi everybody\.?", re.I)
QUESTION_START_RE = re.compile(
    r"(?:let me start with|I want to start with|let's start with|let me start with what|I want to start)",
    re.I,
)
CTA_SIGNAL_RE = re.compile(
    r"(?:please go (?:right )?below|please go to|before wrapping up,?\s+please go|"
    r"you can go to this book|whoever is interested in learning more|"
    r"\.substack\.com|21st Century Wire|subscribe to (?:this )?(?:channel|Substack))",
    re.I,
)
BOOK_INTERRUPT_RE = re.compile(
    r"(?:We know that you wrote|What is the axis of resistance\?).*?"
    r"(?:\.substack\.com|wrote on your Substack).*?"
    r"(?=\s*(?:>>|&gt;&gt;))",
    re.I | re.DOTALL,
)
CLOSE_START_RE = re.compile(
    r"(?:>>\s*)?Thank you so much,?\s+[\w\s]+,?\s+for being with us(?: today)?",
    re.I,
)
CLOSE_CTA_RE = re.compile(
    r"(?:please go|before wrapping up|\.substack\.com|21st Century Wire|"
    r"description of this video|I'm going to put the links)",
    re.I,
)
LEADING_NOISE_RE = re.compile(
    r"^(?:\[music\]\s*|## Cleaned Transcript\s*)+",
    re.I,
)
CLEANED_HEADER_RE = re.compile(r"^## Cleaned Transcript\s*", re.I)

EDITORIAL_MID_NOTE = (
    "Mid-intro Substack/book CTA trimmed in place; SSOT body otherwise preserved."
)
EDITORIAL_CLOSE_NOTE = (
    "Routine closing Substack/link promo trimmed in place; SSOT body otherwise preserved."
)


@dataclass(frozen=True)
class FileChange:
    path: Path
    opening_tier: str
    mid_substack_trimmed: bool = False
    book_interrupt_trimmed: bool = False
    close_substack_trimmed: bool = False
    leading_noise_trimmed: bool = False
    paragraphs_removed: int = 0


def strip_bom(text: str) -> str:
    if text.startswith("\ufeff"):
        return text[1:]
    return text


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    text = strip_bom(text)
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    return parse_simple_frontmatter(match.group(1)), text[match.end() :]


def parse_simple_frontmatter(raw: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if value.startswith('"') and value.endswith('"'):
            data[key] = json.loads(value)
        elif value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = value
    return data


def dump_simple_frontmatter(data: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            text = str(value)
            if text == "" or any(ch in text for ch in ':"#[]{}') or text != text.strip():
                rendered = json.dumps(text, ensure_ascii=False)
            else:
                rendered = text
        lines.append(f"{key}: {rendered}")
    return "\n".join(lines)


def dump_frontmatter(data: dict[str, Any]) -> str:
    return f"---\n{dump_simple_frontmatter(data).rstrip()}\n---\n\n"


def is_dialogue_works_capture(meta: dict[str, Any], path: Path) -> bool:
    name = path.name.lower()
    if not (name.startswith("source-alkorshid-") or name.startswith("source-nima-alkorshid-")):
        return False
    show = str(meta.get("show") or meta.get("show_title") or "").strip().lower()
    slug = str(meta.get("channel_slug") or "").strip().lower()
    if show and "dialogue works" not in show:
        return False
    if slug and slug != "dialogue-works":
        return False
    return True


def is_solo_capture(meta: dict[str, Any]) -> bool:
    form = str(meta.get("source_form") or "").strip().lower()
    if form == "solo":
        return True
    guest = meta.get("guest") or meta.get("guest_people")
    if guest in (None, "", "[]", []):
        return True
    return False


def split_paragraphs(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    return [chunk.strip() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()]


def join_paragraphs(paragraphs: list[str]) -> str:
    if not paragraphs:
        return ""
    return "\n\n".join(paragraphs).rstrip() + "\n"


def strip_leading_noise(text: str) -> tuple[str, bool]:
    stripped = LEADING_NOISE_RE.sub("", text.lstrip())
    if stripped != text.lstrip():
        return stripped, True
    return text, False


def trim_mid_substack_before_question(text: str) -> tuple[str, bool]:
    question = QUESTION_START_RE.search(text)
    if not question:
        return text, False
    opening = text[: question.start()]
    cta = CTA_SIGNAL_RE.search(opening)
    if not cta:
        return text, False
    before = text[: cta.start()].rstrip()
    after = text[question.start() :].lstrip()
    if not before or not after:
        return text, False
    joiner = "" if before.endswith((".", "!", "?")) else " "
    trimmed = before + joiner + after
    return trimmed, trimmed != text


def trim_book_substack_interrupt(text: str, *, max_scan: int = 12000) -> tuple[str, bool]:
    window = text[:max_scan]
    match = BOOK_INTERRUPT_RE.search(window)
    if not match:
        return text, False
    trimmed = text[: match.start()].rstrip() + " " + text[match.end() :].lstrip()
    return trimmed, trimmed != text


def trim_close_substack_block(paragraphs: list[str]) -> tuple[list[str], bool]:
    if len(paragraphs) < 2:
        return paragraphs, False
    tail = "\n\n".join(paragraphs[-3:])
    close = CLOSE_START_RE.search(tail)
    if not close:
        return paragraphs, False
    if not CLOSE_CTA_RE.search(tail[close.start() :]):
        return paragraphs, False
    cut_at = len("\n\n".join(paragraphs[:-3])) + (2 if len(paragraphs) > 3 else 0) + close.start()
    full_text = "\n\n".join(paragraphs)
    trimmed = full_text[:cut_at].rstrip()
    new_paragraphs = split_paragraphs(trimmed)
    if not new_paragraphs or new_paragraphs == paragraphs:
        return paragraphs, False
    return new_paragraphs, True


def opening_has_cta(text: str, *, limit: int = 8000) -> bool:
    window = text[:limit]
    question = QUESTION_START_RE.search(window)
    if question:
        return bool(CTA_SIGNAL_RE.search(window[: question.start()]))
    return bool(CTA_SIGNAL_RE.search(window))


def classify_opening_tier(
    text: str,
    *,
    meta: dict[str, Any],
    cta_present: bool,
) -> str:
    if is_solo_capture(meta):
        return "solo-brief"
    if cta_present or BOOK_INTERRUPT_RE.search(text[:12000]):
        return "full-scaffold"
    if HOST_ANCHOR_RE.search(text):
        return "host-tease"
    return "clean"


def trim_transcript_body(
    body: str,
    meta: dict[str, Any],
    *,
    allow_mid: bool,
    allow_interrupt: bool,
    allow_close: bool,
    allow_noise: bool,
) -> tuple[str, bool, FileChange]:
    if not body.strip():
        return body, False, FileChange(Path(), "clean")

    solo = is_solo_capture(meta)
    original = body
    changed = False
    mid_trimmed = False
    interrupt_trimmed = False
    close_trimmed = False
    noise_trimmed = False
    removed = 0

    text = body
    if allow_noise:
        new_text, did = strip_leading_noise(text)
        if did:
            text = new_text
            noise_trimmed = True
            changed = True

    cta_present = opening_has_cta(original)

    if not solo and allow_mid:
        new_text, did = trim_mid_substack_before_question(text)
        if did:
            text = new_text
            mid_trimmed = True
            changed = True

    if not solo and allow_interrupt:
        new_text, did = trim_book_substack_interrupt(text)
        if did:
            text = interrupt_trimmed = True
            changed = True
            text = new_text

    paragraphs = split_paragraphs(text)
    if not solo and allow_close:
        new_paragraphs, did = trim_close_substack_block(paragraphs)
        if did:
            removed += max(0, len(paragraphs) - len(new_paragraphs))
            paragraphs = new_paragraphs
            close_trimmed = True
            changed = True
            text = join_paragraphs(paragraphs)

    tier = classify_opening_tier(
        text if changed else original,
        meta=meta,
        cta_present=opening_has_cta(text if changed else original),
    )

    return (
        text if changed else body,
        changed,
        FileChange(
            Path(),
            tier,
            mid_substack_trimmed=mid_trimmed,
            book_interrupt_trimmed=interrupt_trimmed,
            close_substack_trimmed=close_trimmed,
            leading_noise_trimmed=noise_trimmed,
            paragraphs_removed=removed,
        ),
    )


def split_body_sections(body: str) -> tuple[str, str, str]:
    match = TRANSCRIPT_SECTION_RE.search(body)
    if match:
        prefix = body[: match.start()]
        transcript_header = match.group(1)
        transcript_body = match.group(2)
        return prefix, transcript_header, transcript_body

    lines = body.splitlines(keepends=True)
    idx = 0
    while idx < len(lines):
        stripped = lines[idx].strip()
        if stripped == "" or stripped.startswith("#") or stripped.startswith("**"):
            idx += 1
            continue
        break
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    prefix = "".join(lines[:idx])
    transcript_body = "".join(lines[idx:])
    transcript_body = CLEANED_HEADER_RE.sub("", transcript_body, count=1)
    return prefix, "", transcript_body


def merge_body_sections(prefix: str, transcript_header: str, transcript_body: str) -> str:
    if not transcript_header:
        return prefix + transcript_body
    return prefix + transcript_header + transcript_body


def append_editorial_note(meta: dict[str, Any], note: str) -> None:
    existing = str(meta.get("editorial_note") or "").strip()
    if note.lower() in existing.lower():
        return
    meta["editorial_note"] = f"{existing} {note}".strip() if existing else note


def normalize_text(
    path: Path,
    text: str,
    *,
    tag_only: bool = False,
) -> tuple[bool, str, FileChange | None]:
    meta, body = split_frontmatter(text)
    if not is_dialogue_works_capture(meta, path):
        return False, text, None

    prefix, transcript_header, transcript_body = split_body_sections(body)
    prefix = re.sub(r"(?:^|\n)## Cleaned Transcript\s*\r?\n", "\n", prefix, count=1, flags=re.I)
    if not transcript_body.strip():
        return False, text, None

    original = transcript_body
    mid_done = bool(meta.get("dialogue_works_substack_trim_applied"))
    interrupt_done = bool(meta.get("dialogue_works_book_interrupt_trim_applied"))
    close_done = bool(meta.get("dialogue_works_close_substack_trim_applied"))
    noise_done = bool(meta.get("dialogue_works_leading_noise_trim_applied"))

    cta_present = opening_has_cta(original)

    if tag_only:
        tier = classify_opening_tier(original, meta=meta, cta_present=cta_present)
        if meta.get("opening_tier") != tier:
            meta["opening_tier"] = tier
            return True, dump_frontmatter(meta) + body, FileChange(path, tier)
        return False, text, None

    if mid_done and interrupt_done and close_done and noise_done:
        tier = str(meta.get("opening_tier") or "host-tease")
        return False, text, FileChange(path, tier)

    new_body, changed, change = trim_transcript_body(
        transcript_body,
        meta,
        allow_mid=not mid_done,
        allow_interrupt=not interrupt_done,
        allow_close=not close_done,
        allow_noise=not noise_done,
    )

    if not changed:
        if meta.get("opening_tier"):
            return False, text, FileChange(path, str(meta.get("opening_tier")))
        tier = classify_opening_tier(original, meta=meta, cta_present=cta_present)
        meta["opening_tier"] = tier
        return True, dump_frontmatter(meta) + body, FileChange(path, tier)

    if change.mid_substack_trimmed:
        meta["dialogue_works_substack_trim_applied"] = True
        append_editorial_note(meta, EDITORIAL_MID_NOTE)
    if change.book_interrupt_trimmed:
        meta["dialogue_works_book_interrupt_trim_applied"] = True
        append_editorial_note(meta, EDITORIAL_MID_NOTE)
    if change.close_substack_trimmed:
        meta["dialogue_works_close_substack_trim_applied"] = True
        append_editorial_note(meta, EDITORIAL_CLOSE_NOTE)
    if change.leading_noise_trimmed:
        meta["dialogue_works_leading_noise_trim_applied"] = True

    post_tier = classify_opening_tier(
        new_body,
        meta=meta,
        cta_present=opening_has_cta(new_body),
    )
    meta["opening_tier"] = post_tier
    change = FileChange(
        path=change.path,
        opening_tier=post_tier,
        mid_substack_trimmed=change.mid_substack_trimmed,
        book_interrupt_trimmed=change.book_interrupt_trimmed,
        close_substack_trimmed=change.close_substack_trimmed,
        leading_noise_trimmed=change.leading_noise_trimmed,
        paragraphs_removed=change.paragraphs_removed,
    )
    merged = merge_body_sections(prefix, transcript_header, new_body)
    new_text = dump_frontmatter(meta) + merged
    return (
        True,
        new_text,
        FileChange(
            path,
            change.opening_tier,
            mid_substack_trimmed=change.mid_substack_trimmed,
            book_interrupt_trimmed=change.book_interrupt_trimmed,
            close_substack_trimmed=change.close_substack_trimmed,
            leading_noise_trimmed=change.leading_noise_trimmed,
            paragraphs_removed=change.paragraphs_removed,
        ),
    )


def candidate_paths(root: Path, explicit: list[Path] | None = None) -> list[Path]:
    if explicit:
        return sorted({p.resolve() for p in explicit})
    paths: list[Path] = []
    for pattern in ("source-alkorshid-*.md", "source-nima-alkorshid-*.md"):
        for path in root.rglob(pattern):
            if ".cleaned." in path.name:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            meta, _ = split_frontmatter(text)
            if is_dialogue_works_capture(meta, path):
                paths.append(path)
    return sorted(set(paths))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ARCHIVE_ROOT)
    parser.add_argument("--path", type=Path, action="append", default=[], help="Explicit archive file(s).")
    parser.add_argument("--apply", action="store_true", help="Write changes in place.")
    parser.add_argument("--tag-only", action="store_true", help="Only set opening_tier metadata.")
    args = parser.parse_args()

    explicit = [REPO_ROOT / p if not p.is_absolute() else p for p in args.path] if args.path else None
    paths = candidate_paths(args.root, explicit)
    changes: list[FileChange] = []
    skipped = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        changed, new_text, file_change = normalize_text(path, text, tag_only=args.tag_only)
        if file_change is None:
            skipped += 1
            continue
        file_change = FileChange(
            path=path,
            opening_tier=file_change.opening_tier,
            mid_substack_trimmed=file_change.mid_substack_trimmed,
            book_interrupt_trimmed=file_change.book_interrupt_trimmed,
            close_substack_trimmed=file_change.close_substack_trimmed,
            leading_noise_trimmed=file_change.leading_noise_trimmed,
            paragraphs_removed=file_change.paragraphs_removed,
        )
        if changed:
            changes.append(file_change)
            if args.apply:
                path.write_text(new_text, encoding="utf-8")

    mode = "Applied" if args.apply else "Dry-run"
    print(f"{mode}: {len(changes)} Dialogue Works transcript file(s) would change; {skipped} skipped.")
    for change in changes:
        flags: list[str] = []
        if change.mid_substack_trimmed:
            flags.append("mid_substack")
        if change.book_interrupt_trimmed:
            flags.append("book_interrupt")
        if change.close_substack_trimmed:
            flags.append("close_substack")
        if change.leading_noise_trimmed:
            flags.append("leading_noise")
        if change.paragraphs_removed:
            flags.append(f"-{change.paragraphs_removed}p")
        joined = ", ".join(flags) if flags else "metadata"
        rel = change.path.relative_to(REPO_ROOT).as_posix()
        print(f"- {rel} [{joined}] tier={change.opening_tier}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
