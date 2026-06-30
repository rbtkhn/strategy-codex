#!/usr/bin/env python3
"""Normalize opening rapport/production banter out of Mario Nawfal statecraft archive transcripts.

Rewrites repo-tracked source-archive/statecraft captures in place when --apply is set.
Default is dry-run. Conservative: trims only clearly separable banter blocks.
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

BANTER_SIGNAL_RE = re.compile(
    r"\b(?:hey man|how are you|good to have you|long time|two weeks|welcome back(?:\s+to\s+reality)?|"
    r"\blisa\b|\bproducer\b|volume is(?:\s+a\s+bit)?\s+low|going live|no jokes|"
    r"\[sighs\]|perfect timing|we booked this|can't complain|that is wild|can't believe that|"
    r"life\.\s+i'll make it after)\b",
    re.IGNORECASE,
)
SUBSTANTIVE_SIGNAL_RE = re.compile(
    r"\b(?:iran|israel|lebanon|hormuz|homos|deal|ceasefire|netanyahu|trump|ukraine|nato|"
    r"missile|strike|war|negotiat|blockade|gaza|beirut|kuwait|sanction|enriched|uranium|"
    r"straight of|substack|before we go into|i want to bring this up first)\b",
    re.IGNORECASE,
)
SIDE_QUEST_ANCHOR_RE = re.compile(
    r"\b(?:before we get into|before we go into|i want to bring this up first)\b",
    re.IGNORECASE,
)
MIXED_CUT_ANCHOR_RE = re.compile(
    r"(?:>>\s*)?(?:Well,|So,)\s+(?:the reality that we're dealing with now|um,?\s+a lot of people|"
    r"before we go into your piece|i want to bring this up first|there's been a roller coaster|"
    r"hi,?\s+larry|well,?\s+you know,?\s+mario|but um let's start with)",
    re.IGNORECASE,
)
SIDE_QUEST_START_RE = re.compile(
    r"\b(?:but um let's start with|but before that i want to|before we go into your piece|"
    r"i want to bring this up first|so, before we go into)\b",
    re.IGNORECASE,
)
PRODUCTION_AUDIO_SIGNAL_RE = re.compile(
    r"\b(?:lisa\b.*(?:volume|audio|level|studio|producer|heads up)|"
    r"\bproducer\b.*(?:hear myself|can't hear)|"
    r"volume is(?:\s+a\s+bit)?\s+low|"
    r"same level(?:\s+now)?|put it up more|now it should be better)\b",
    re.IGNORECASE | re.DOTALL,
)
PRODUCTION_EXIT_ANCHOR_RE = re.compile(
    r"(?:>>\s*)?(?:Yeah\.\s+)?(?:So,?\s+)?(?:Uh,?\s+)?"
    r"(?:a lot of people are talking|"
    r"(?:I'?ll|I will)\s+go through(?:\s+kind of)?\s+the\s+latest)",
    re.IGNORECASE,
)
GUEST_DROPOUT_SIGNAL_RE = re.compile(
    r"\blisa\b.*?(?:internet just cut out|video just cut out|cut out if you could quickly check it in the studio|"
    r"waiting for .+? to join)",
    re.IGNORECASE | re.DOTALL,
)
GUEST_DROPOUT_RETURN_RE = re.compile(
    r"(\w+)\.\s+Did you hear",
    re.IGNORECASE,
)
ORPHAN_OPENING_PREFIX_RE = re.compile(
    r"^>>\s*(?:Um,?\s+)?(?:I\s+I\s+)?heard the last thing.*?"
    r"(?:I'll read it out quick\.?\s*)?(?:It's a quick one\.?\s*)?(?:I'll read it very quickly\.?\s*)?",
    re.IGNORECASE | re.DOTALL,
)
ORPHAN_INSTITUTION_ANCHOR_RE = re.compile(
    r"\b(?:US Navy Central Command|Navy Central Command|Central Command has warned)\b",
    re.IGNORECASE,
)
WRAPPER_LINE_RE = re.compile(
    r"^(?:BREAKING:.*YouTube\s*$|Transcripts:\s*$|Kind:\s*captions\s*$|Language:\s*\S+\s*$)",
    re.IGNORECASE | re.MULTILINE,
)
GUEST_TITLE_PREFIXES = ("amb.", "ambassador", "colonel", "col.", "professor", "prof.", "judge", "dr.", "dr", "lt.")

EDITORIAL_TRIM_NOTE = (
    "Opening rapport/production banter trimmed in place; SSOT body otherwise preserved."
)
EDITORIAL_PRODUCTION_TRIM_NOTE = (
    "Lisa/producer opening audio block trimmed in place; SSOT body otherwise preserved."
)
EDITORIAL_DROPOUT_TRIM_NOTE = (
    "Guest-dropout reconnect filler trimmed in place; SSOT body otherwise preserved."
)
EDITORIAL_ORPHAN_TRIM_NOTE = (
    "Post-trim orphan opening fragment removed in place; SSOT body otherwise preserved."
)

@dataclass(frozen=True)
class FileChange:
    path: Path
    intro_removed: bool
    opening_tier: str
    paragraphs_removed: int
    prefix_trimmed: bool
    production_trimmed: bool = False
    dropout_trimmed: bool = False
    orphan_trimmed: bool = False

def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
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

def guest_paragraph_cues(guest: str) -> set[str]:
    clean = " ".join(guest.split()).strip()
    if not clean:
        return set()
    low = clean.lower()
    cues = {low}
    parts = [part for part in re.split(r"\s+", low) if part]
    if parts:
        cues.add(parts[-1])
    for title in GUEST_TITLE_PREFIXES:
        if low.startswith(title + " "):
            cues.add(low[len(title) + 1 :].strip())
    return {cue for cue in cues if cue}

def is_nawfal_hosted(meta: dict[str, Any], path: Path) -> bool:
    name = path.name.lower()
    if "daniel-davis-deep-dive" in name and "mario-nawfal" in name:
        return False
    channel = str(meta.get("channel_slug") or "").strip().lower()
    if channel in ("mario-nawfal", "nawfal"):
        return True
    show = str(meta.get("show") or meta.get("show_title") or "").strip().lower()
    host = str(meta.get("host") or "").strip().lower()
    if "mario nawfal" in show or "mario nawfal" in host:
        return True
    return name.startswith("source-mario-nawfal-") and not name.startswith(
        "source-daniel-davis"
    )

def split_paragraphs(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    return [chunk.strip() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()]

def join_paragraphs(paragraphs: list[str]) -> str:
    if not paragraphs:
        return ""
    return "\n\n".join(paragraphs).rstrip() + "\n"

def is_banter_paragraph(paragraph: str) -> bool:
    if not BANTER_SIGNAL_RE.search(paragraph):
        return False
    if SUBSTANTIVE_SIGNAL_RE.search(paragraph):
        return False
    return True

def trim_mixed_paragraph_prefix(paragraph: str) -> tuple[str, bool]:
    if not BANTER_SIGNAL_RE.search(paragraph):
        return paragraph, False
    if is_banter_paragraph(paragraph):
        return "", True

    match = MIXED_CUT_ANCHOR_RE.search(paragraph)
    if match:
        trimmed = paragraph[match.start() :].lstrip()
        if trimmed and trimmed != paragraph:
            return trimmed, True

    guest_turn = re.search(r">>\s*(?:Yeah|Yes|No|Well|I think|Um|So,)\b", paragraph, re.IGNORECASE)
    if guest_turn and BANTER_SIGNAL_RE.search(paragraph[: guest_turn.start()]):
        after = paragraph[guest_turn.start() :]
        if re.match(
            r">>\s*(?:Good|Yeah|Yes|Doing well|I'm doing well)\b",
            after,
            re.IGNORECASE,
        ) and SUBSTANTIVE_SIGNAL_RE.search(after[:240]):
            return paragraph, False
        trimmed = after.lstrip()
        if trimmed:
            return trimmed, True

    return paragraph, False

def first_guest_substantive_index(paragraphs: list[str], guest: str) -> int | None:
    cues = guest_paragraph_cues(guest)
    for idx, para in enumerate(paragraphs):
        lower = para.lower()
        if cues and any(cue in lower for cue in cues):
            if SUBSTANTIVE_SIGNAL_RE.search(para) and not is_banter_paragraph(para):
                return idx
        if re.search(r">>\s*(?:Yeah|Yes|No|Well|I think|Um,|So,)\b", para) and SUBSTANTIVE_SIGNAL_RE.search(para):
            if not is_banter_paragraph(para):
                return idx
    return None

def opening_has_separable_production_block(paragraphs: list[str]) -> bool:
    if not paragraphs:
        return False
    window = "\n\n".join(paragraphs[:3])
    production = PRODUCTION_AUDIO_SIGNAL_RE.search(window)
    if not production:
        return False
    substantive = SUBSTANTIVE_SIGNAL_RE.search(window)
    if substantive and substantive.start() < production.start():
        return False
    anchor = PRODUCTION_EXIT_ANCHOR_RE.search(window)
    if not anchor:
        return False
    return anchor.start() > production.start()

def trim_production_audio_block(paragraphs: list[str]) -> tuple[list[str], bool]:
    if not opening_has_separable_production_block(paragraphs):
        return paragraphs, False

    window_paragraphs = paragraphs[:3]
    rest = paragraphs[3:]
    window_text = "\n\n".join(window_paragraphs)
    anchor = PRODUCTION_EXIT_ANCHOR_RE.search(window_text)
    if not anchor:
        return paragraphs, False

    trimmed_window = window_text[anchor.start() :].lstrip()
    if not trimmed_window or trimmed_window == window_text:
        return paragraphs, False
    return split_paragraphs(trimmed_window) + rest, True

def guest_token_matches_cues(token: str, cues: set[str]) -> bool:
    token = token.lower().strip()
    if not token:
        return False
    if token in cues:
        return True
    return any(token in cue or cue.split()[-1] == token for cue in cues)

def opening_has_separable_guest_dropout_block(paragraphs: list[str], guest: str) -> bool:
    if not paragraphs or not guest.strip():
        return False
    window = "\n\n".join(paragraphs[:4])
    dropout = GUEST_DROPOUT_SIGNAL_RE.search(window)
    if not dropout:
        return False
    return_match = GUEST_DROPOUT_RETURN_RE.search(window)
    if not return_match or return_match.start() <= dropout.start():
        return False
    return guest_token_matches_cues(return_match.group(1), guest_paragraph_cues(guest))

def trim_guest_dropout_block(paragraphs: list[str], guest: str) -> tuple[list[str], bool]:
    if not opening_has_separable_guest_dropout_block(paragraphs, guest):
        return paragraphs, False

    window_paragraphs = paragraphs[:4]
    rest = paragraphs[4:]
    window_text = "\n\n".join(window_paragraphs)
    return_match = GUEST_DROPOUT_RETURN_RE.search(window_text)
    if not return_match:
        return paragraphs, False

    trimmed_window = window_text[return_match.start() :].lstrip()
    if not trimmed_window or trimmed_window == window_text:
        return paragraphs, False
    return split_paragraphs(trimmed_window) + rest, True

def opening_has_separable_orphan_fragment(paragraphs: list[str]) -> bool:
    if not paragraphs:
        return False
    first = paragraphs[0].lstrip()
    prefix_match = ORPHAN_OPENING_PREFIX_RE.match(first)
    if not prefix_match:
        return False
    remainder = first[prefix_match.end() :].lstrip()
    if not remainder:
        return False
    return bool(
        SUBSTANTIVE_SIGNAL_RE.search(remainder[:400])
        or ORPHAN_INSTITUTION_ANCHOR_RE.search(remainder[:200])
    )

def trim_orphan_opening_fragment(paragraphs: list[str]) -> tuple[list[str], bool]:
    if not opening_has_separable_orphan_fragment(paragraphs):
        return paragraphs, False
    first = paragraphs[0]
    prefix_match = ORPHAN_OPENING_PREFIX_RE.match(first)
    if not prefix_match:
        return paragraphs, False
    remainder = first[prefix_match.end() :].lstrip()
    if not remainder:
        return paragraphs, False
    paragraphs[0] = remainder
    return paragraphs, True

def trim_side_quest_block(paragraphs: list[str], guest: str) -> tuple[list[str], bool]:
    if not paragraphs:
        return paragraphs, False

    first = paragraphs[0]
    side_match = SIDE_QUEST_START_RE.search(first)
    if side_match and BANTER_SIGNAL_RE.search(first[: side_match.start()]):
        trimmed_first = first[side_match.start() :].lstrip()
        new_paragraphs = [trimmed_first, *paragraphs[1:]] if trimmed_first else paragraphs[1:]
        return new_paragraphs, True

    anchor_idx = next(
        (i for i, p in enumerate(paragraphs) if SIDE_QUEST_ANCHOR_RE.search(p)),
        None,
    )
    if anchor_idx is None or anchor_idx == 0:
        return paragraphs, False
    guest_idx = first_guest_substantive_index(paragraphs, guest)
    if guest_idx is not None and guest_idx <= anchor_idx:
        return paragraphs, False
    new_paragraphs = paragraphs[anchor_idx:]
    return new_paragraphs, True

def classify_opening_tier(
    original_paragraphs: list[str],
    trimmed_paragraphs: list[str],
    intro_removed: bool,
    guest: str,
) -> str:
    if intro_removed:
        return "heavy-banter"
    opening = " ".join(original_paragraphs[:3]).lower()
    if BANTER_SIGNAL_RE.search(opening) and not SUBSTANTIVE_SIGNAL_RE.search(opening):
        return "heavy-banter"
    guest_idx = first_guest_substantive_index(trimmed_paragraphs, guest)
    if guest_idx is None:
        guest_idx = len(trimmed_paragraphs)
    host_words = 0
    for para in trimmed_paragraphs[: max(guest_idx, 1)]:
        host_words += len(para.split())
    if guest_idx <= 1 and host_words < 120:
        return "clean"
    if guest_idx <= 2 and host_words < 200:
        return "clean"
    if host_words >= 120 or guest_idx > 2:
        return "host-monologue"
    return "clean"

def trim_transcript_body(
    body: str, guest: str, include_side_quests: bool
) -> tuple[str, bool, int, bool, bool, bool, bool]:
    paragraphs = split_paragraphs(body)
    if not paragraphs:
        return body, False, 0, False, False, False, False

    removed_count = 0
    prefix_trimmed = False
    production_trimmed = False
    dropout_trimmed = False
    orphan_trimmed = False
    changed = False

    while paragraphs and (
        paragraphs[0].startswith("BREAKING:")
        or paragraphs[0].strip().lower() == "transcripts:"
        or paragraphs[0].strip().lower().startswith("kind: captions")
        or paragraphs[0].strip().lower().startswith("language:")
    ):
        paragraphs.pop(0)
        removed_count += 1
        changed = True

    while paragraphs and is_banter_paragraph(paragraphs[0]):
        paragraphs.pop(0)
        removed_count += 1
        changed = True

    if paragraphs:
        trimmed_first, did_trim = trim_mixed_paragraph_prefix(paragraphs[0])
        if did_trim:
            if trimmed_first:
                paragraphs[0] = trimmed_first
            else:
                paragraphs.pop(0)
                removed_count += 1
            prefix_trimmed = True
            changed = True

    if include_side_quests:
        paragraphs, side_removed = trim_side_quest_block(paragraphs, guest)
        if side_removed:
            changed = True

    paragraphs, production_removed = trim_production_audio_block(paragraphs)
    if production_removed:
        production_trimmed = True
        changed = True

    paragraphs, dropout_removed = trim_guest_dropout_block(paragraphs, guest)
    if dropout_removed:
        dropout_trimmed = True
        changed = True

    paragraphs, orphan_removed = trim_orphan_opening_fragment(paragraphs)
    if orphan_removed:
        orphan_trimmed = True
        changed = True

    if not changed:
        return body, False, removed_count, prefix_trimmed, False, False, False
    new_body = join_paragraphs(paragraphs)
    return new_body, changed, removed_count, prefix_trimmed, production_trimmed, dropout_trimmed, orphan_trimmed

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
    return prefix, "", transcript_body

def merge_body_sections(prefix: str, transcript_header: str, transcript_body: str) -> str:
    if not transcript_header:
        return prefix + transcript_body
    return prefix + transcript_header + transcript_body

def update_editorial_note(meta: dict[str, Any], intro_removed: bool) -> None:
    if not intro_removed:
        return
    note = str(meta.get("editorial_note") or "").strip()
    if EDITORIAL_TRIM_NOTE.lower() in note.lower():
        return
    meta["editorial_note"] = f"{note} {EDITORIAL_TRIM_NOTE}".strip() if note else EDITORIAL_TRIM_NOTE

def update_production_editorial_note(meta: dict[str, Any]) -> None:
    note = str(meta.get("editorial_note") or "").strip()
    if EDITORIAL_PRODUCTION_TRIM_NOTE.lower() in note.lower():
        return
    meta["editorial_note"] = (
        f"{note} {EDITORIAL_PRODUCTION_TRIM_NOTE}".strip() if note else EDITORIAL_PRODUCTION_TRIM_NOTE
    )

def update_dropout_editorial_note(meta: dict[str, Any]) -> None:
    note = str(meta.get("editorial_note") or "").strip()
    if EDITORIAL_DROPOUT_TRIM_NOTE.lower() in note.lower():
        return
    meta["editorial_note"] = (
        f"{note} {EDITORIAL_DROPOUT_TRIM_NOTE}".strip() if note else EDITORIAL_DROPOUT_TRIM_NOTE
    )

def update_orphan_editorial_note(meta: dict[str, Any]) -> None:
    note = str(meta.get("editorial_note") or "").strip()
    if EDITORIAL_ORPHAN_TRIM_NOTE.lower() in note.lower():
        return
    if "orphan" in note.lower() and "fragment" in note.lower():
        return
    meta["editorial_note"] = (
        f"{note} {EDITORIAL_ORPHAN_TRIM_NOTE}".strip() if note else EDITORIAL_ORPHAN_TRIM_NOTE
    )

def normalize_text(
    path: Path,
    text: str,
    *,
    include_side_quests: bool,
    tag_only: bool = False,
) -> tuple[bool, str, FileChange | None]:
    meta, body = split_frontmatter(text)
    if not is_nawfal_hosted(meta, path):
        return False, text, None

    guest = str(meta.get("guest") or "")
    prefix, transcript_header, transcript_body = split_body_sections(body)
    if not transcript_body.strip():
        return False, text, None

    original_paragraphs = split_paragraphs(transcript_body)
    if meta.get("opening_trim_applied") and not tag_only:
        tier = str(meta.get("opening_tier") or "heavy-banter")
        if not meta.get("production_trim_applied"):
            paragraphs = split_paragraphs(transcript_body)
            new_paragraphs, production_removed = trim_production_audio_block(paragraphs)
            if production_removed:
                meta["production_trim_applied"] = True
                update_production_editorial_note(meta)
                new_transcript_body = join_paragraphs(new_paragraphs)
                new_body = merge_body_sections(prefix, transcript_header, new_transcript_body)
                new_text = dump_frontmatter(meta) + new_body
                return (
                    True,
                    new_text,
                    FileChange(
                        path,
                        False,
                        tier,
                        0,
                        True,
                        production_trimmed=True,
                    ),
                )
        if not meta.get("dropout_trim_applied"):
            paragraphs = split_paragraphs(transcript_body)
            new_paragraphs, dropout_removed = trim_guest_dropout_block(paragraphs, guest)
            if dropout_removed:
                meta["dropout_trim_applied"] = True
                update_dropout_editorial_note(meta)
                if tier == "clean":
                    meta["opening_tier"] = "heavy-banter"
                    tier = "heavy-banter"
                new_transcript_body = join_paragraphs(new_paragraphs)
                new_body = merge_body_sections(prefix, transcript_header, new_transcript_body)
                new_text = dump_frontmatter(meta) + new_body
                return (
                    True,
                    new_text,
                    FileChange(
                        path,
                        False,
                        tier,
                        0,
                        False,
                        production_trimmed=False,
                        dropout_trimmed=True,
                    ),
                )
        if not meta.get("orphan_trim_applied"):
            paragraphs = split_paragraphs(transcript_body)
            new_paragraphs, orphan_removed = trim_orphan_opening_fragment(paragraphs)
            if orphan_removed:
                meta["orphan_trim_applied"] = True
                update_orphan_editorial_note(meta)
                new_transcript_body = join_paragraphs(new_paragraphs)
                new_body = merge_body_sections(prefix, transcript_header, new_transcript_body)
                new_text = dump_frontmatter(meta) + new_body
                return (
                    True,
                    new_text,
                    FileChange(
                        path,
                        False,
                        tier,
                        0,
                        False,
                        dropout_trimmed=False,
                        orphan_trimmed=True,
                    ),
                )
        if tier != "heavy-banter":
            meta["opening_tier"] = "heavy-banter"
            new_text = dump_frontmatter(meta) + body
            return (
                new_text != text,
                new_text,
                FileChange(path, False, "heavy-banter", 0, False),
            )
        return False, text, FileChange(path, False, tier, 0, False)

    if tag_only:
        if meta.get("opening_trim_applied"):
            tier = "heavy-banter"
        else:
            tier = classify_opening_tier(original_paragraphs, original_paragraphs, False, guest)
        if meta.get("opening_tier") != tier:
            meta["opening_tier"] = tier
            new_text = dump_frontmatter(meta) + body
            return new_text != text, new_text, FileChange(path, False, tier, 0, False)
        return False, text, None

    (
        new_transcript_body,
        changed,
        removed_count,
        prefix_trimmed,
        production_trimmed,
        dropout_trimmed,
        orphan_trimmed,
    ) = trim_transcript_body(
        transcript_body,
        guest,
        include_side_quests,
    )
    trimmed_paragraphs = split_paragraphs(new_transcript_body)
    intro_removed = changed
    tier = (
        "heavy-banter"
        if intro_removed
        else classify_opening_tier(original_paragraphs, trimmed_paragraphs, intro_removed, guest)
    )

    meta["opening_tier"] = tier
    if intro_removed:
        meta["opening_trim_applied"] = True
        update_editorial_note(meta, True)
    if production_trimmed:
        meta["production_trim_applied"] = True
        update_production_editorial_note(meta)
    if dropout_trimmed:
        meta["dropout_trim_applied"] = True
        update_dropout_editorial_note(meta)
    if orphan_trimmed:
        meta["orphan_trim_applied"] = True
        update_orphan_editorial_note(meta)

    new_body = merge_body_sections(prefix, transcript_header, new_transcript_body)
    new_text = dump_frontmatter(meta) + new_body
    file_change = FileChange(
        path=path,
        intro_removed=intro_removed,
        opening_tier=tier,
        paragraphs_removed=removed_count,
        prefix_trimmed=prefix_trimmed,
        production_trimmed=production_trimmed,
        dropout_trimmed=dropout_trimmed,
        orphan_trimmed=orphan_trimmed,
    )
    return new_text != text, new_text, file_change

def candidate_paths(root: Path, explicit: list[Path] | None = None) -> list[Path]:
    if explicit:
        return sorted({p.resolve() for p in explicit})
    paths: list[Path] = []
    for path in root.rglob("*.md"):
        if ".cleaned." in path.name:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        meta, _ = split_frontmatter(text)
        if is_nawfal_hosted(meta, path):
            paths.append(path)
    return sorted(set(paths))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ARCHIVE_ROOT)
    parser.add_argument("--path", type=Path, action="append", default=[], help="Explicit archive file(s).")
    parser.add_argument("--apply", action="store_true", help="Write changes in place.")
    parser.add_argument(
        "--tag-only",
        action="store_true",
        help="Only set opening_tier metadata; do not trim body.",
    )
    parser.add_argument(
        "--include-side-quests",
        action="store_true",
        help="Also trim Mario-only side quests before announced main topic.",
    )
    args = parser.parse_args()

    explicit = [REPO_ROOT / p if not p.is_absolute() else p for p in args.path] if args.path else None
    paths = candidate_paths(args.root, explicit)
    changes: list[FileChange] = []
    skipped = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        changed, new_text, file_change = normalize_text(
            path,
            text,
            include_side_quests=args.include_side_quests,
            tag_only=args.tag_only,
        )
        if file_change is None:
            skipped += 1
            continue
        if changed:
            changes.append(file_change)
            if args.apply:
                path.write_text(new_text, encoding="utf-8")

    mode = "Applied" if args.apply else "Dry-run"
    print(f"{mode}: {len(changes)} Mario Nawfal transcript file(s) would change; {skipped} skipped.")
    for change in changes:
        flags = []
        if change.intro_removed:
            flags.append("intro")
        if change.prefix_trimmed:
            flags.append("prefix")
        if change.production_trimmed:
            flags.append("production")
        if change.dropout_trimmed:
            flags.append("dropout")
        if change.orphan_trimmed:
            flags.append("orphan")
        if change.paragraphs_removed:
            flags.append(f"-{change.paragraphs_removed}p")
        joined = ", ".join(flags) if flags else "metadata"
        rel = change.path.relative_to(REPO_ROOT).as_posix()
        print(f"- {rel} [{joined}] tier={change.opening_tier}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
