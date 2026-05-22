#!/usr/bin/env python3
"""Normalize ad and promo copy out of Napolitano/Judging Freedom raw transcripts.

This script rewrites repo-tracked raw-input transcript files in place.
It is intended for deterministic readability cleanup of Judging Freedom /
Napolitano transcripts only.
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

RAW_INPUT_ROOT = REPO_ROOT / "codex" / "years" / "2026" / "raw-input"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
MUSIC_ONLY_RE = re.compile(r"^(?:\s*(?:\[music\]|heat\.|>>\s*\[music\]|>>\s*\[clears throat\])\s*)+$", re.IGNORECASE)
INTRO_SPLIT_RE = re.compile(r"(But first,?\s*this(?:[,.\s]*my friends)?\.?)", re.IGNORECASE)
OUTRO_CUE_RE = re.compile(
    r"\b(?:And\s+)?Coming up(?: later today| at \d| today\b| this afternoon\b| this morning\b)?"
    r"|\b(?:A busy and full day|Dark days coming my friends, but also coming today)\b"
    r"|\bJudge\s+(?:Andrew\s+)?N?pa?lit[a-z]*\s+(?:weekly|for)\s+Judging Freedom\b"
    r"|\bIf you haven't seen it yet\b"
    r"|\bIf you want to hear my thoughts on personal liberty\b",
    re.IGNORECASE,
)
AD_SIGNAL_RE = re.compile(
    r"Lear Capital|leerjudg|8005114620|800511-4620|my Patriot Supply|Patriot Preparedness|"
    r"Expat Money|expatmoneysummit|promo code judge|gold and silver|precious metals|"
    r"financial freedom|wealth|IRA|401k|bonus gold|bonus silver",
    re.IGNORECASE,
)
METADATA_LINE_RE = re.compile(r"^\s*(?:Kind:\s*captions|Language:\s*\S+)\s*$", re.IGNORECASE | re.MULTILINE)
INLINE_NOISE_RE = re.compile(
    r"\s*(?:>>\s*)?\[(?:music|clears throat(?: and cough)?|applause|laughter)\]\s*",
    re.IGNORECASE,
)
SPEAKER_MARKER_RE = re.compile(r"\s*>>\s*")
LEADING_SHOW_NOISE_RE = re.compile(
    r"^(?:\s*(?:\[music\]|heat\.|>>\s*\[music\]|>>\s*\[clears throat\])\s*)+(?=hi everyone\b|good morning\b)",
    re.IGNORECASE,
)
UPDATED_QUALITY_NOTE = "Normalized to remove sponsor/promo copy and transcript noise; minor artifacts may remain."


@dataclass(frozen=True)
class FileChange:
    path: Path
    intro_removed: bool
    outro_removed: bool
    quality_note_updated: bool


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    raw = match.group(1)
    body = text[match.end() :]
    return parse_simple_frontmatter(raw), body


def dump_frontmatter(data: dict[str, Any]) -> str:
    raw = dump_simple_frontmatter(data).rstrip()
    return f"---\n{raw}\n---\n\n"


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


def candidate_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*.md"):
        if ".cleaned." in path.name:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        meta, _ = split_frontmatter(text)
        show = str(meta.get("show") or "").strip().lower()
        host = str(meta.get("host") or "").strip().lower()
        if (
            path.name.startswith("transcript-napolitano-")
            or path.name.startswith("judging-freedom-")
            or show == "judging freedom"
            or "napolitano" in host
        ):
            paths.append(path)
    return sorted(set(paths))


def trim_intro_paragraphs(paragraphs: list[str], guest: str) -> tuple[list[str], bool]:
    full_text = join_paragraphs(paragraphs)
    trimmed_text, removed = trim_intro_text(full_text, guest)
    if removed:
        return split_paragraphs(trimmed_text), True

    fallback_trimmed, fallback_removed = trim_leading_ad_paragraphs(paragraphs, guest)
    if fallback_removed:
        return fallback_trimmed, True

    lowered = [p.lower() for p in paragraphs]
    start_idx = -1
    for idx, para in enumerate(paragraphs):
        if INTRO_SPLIT_RE.search(para):
            start_idx = idx
            break
    if start_idx == -1:
        return paragraphs, False

    guest_cues = guest_paragraph_cues(guest)
    end_idx = -1
    for idx in range(start_idx + 1, len(paragraphs)):
        para = paragraphs[idx]
        lower = lowered[idx]
        if guest_cues and any(cue in lower for cue in guest_cues):
            end_idx = idx
            break
        if idx == start_idx + 1 and not AD_SIGNAL_RE.search(para):
            return paragraphs, False
        if idx > start_idx and ("welcome here" in lower or "good day to you" in lower or "thank you for joining us" in lower):
            end_idx = idx
            break
    if end_idx == -1 or end_idx <= start_idx:
        return paragraphs, False

    first = paragraphs[start_idx]
    match = INTRO_SPLIT_RE.search(first)
    if not match:
        return paragraphs, False
    preserved = first[: match.start()].rstrip()
    new_paragraphs = paragraphs[:start_idx]
    if preserved:
        new_paragraphs.append(preserved)
    new_paragraphs.extend(paragraphs[end_idx:])
    return new_paragraphs, True


def trim_intro_text(text: str, guest: str) -> tuple[str, bool]:
    match = INTRO_SPLIT_RE.search(text)
    if not match:
        return text, False

    after_intro = text[match.end() :]
    if not AD_SIGNAL_RE.search(after_intro):
        return text, False

    cut_pos = first_guest_cue_offset(after_intro, guest)
    if cut_pos is None:
        return text, False

    before = text[: match.start()].rstrip()
    after = after_intro[cut_pos:].lstrip()
    if not before:
        new_text = after
    elif not after:
        new_text = before
    else:
        new_text = before + "\n\n" + after
    return new_text, True


def guest_paragraph_cues(guest: str) -> set[str]:
    clean = " ".join(guest.split()).strip()
    if not clean:
        return set()
    low = clean.lower()
    cues = {low}
    parts = [part for part in re.split(r"\s+", low) if part]
    if parts:
        cues.add(parts[-1])
    for title in ("amb.", "ambassador", "colonel", "col.", "professor", "judge", "dr.", "dr"):
        if low.startswith(title + " "):
            cues.add(low[len(title) + 1 :].strip())
    return {cue for cue in cues if cue}


def first_guest_cue_offset(text: str, guest: str) -> int | None:
    candidates: list[int] = []
    lower = text.lower()
    for cue in guest_paragraph_cues(guest):
        idx = lower.find(cue)
        if idx != -1:
            candidates.append(idx)

    generic_patterns = (
        re.compile(r"\b(?:Ambassador|Professor|Colonel|General|Dr\.?|Doctor)\b[^.\n]{0,140}\b(?:welcome|good day|thank you for joining)\b", re.IGNORECASE),
        re.compile(r"\bwelcome here\b", re.IGNORECASE),
        re.compile(r"\bgood day to you\b", re.IGNORECASE),
        re.compile(r"\bthank you for joining us\b", re.IGNORECASE),
    )
    for pattern in generic_patterns:
        match = pattern.search(text)
        if match:
            candidates.append(match.start())

    return min(candidates) if candidates else None


def trim_leading_ad_paragraphs(paragraphs: list[str], guest: str) -> tuple[list[str], bool]:
    guest_idx = first_guest_paragraph_index(paragraphs, guest)
    if guest_idx is None:
        return paragraphs, False

    ad_idx = None
    for idx in range(guest_idx + 1):
        if AD_SIGNAL_RE.search(paragraphs[idx]):
            ad_idx = idx
            break
    if ad_idx is None:
        return paragraphs, False

    new_paragraphs = list(paragraphs[:ad_idx])
    if ad_idx == guest_idx:
        cue_offset = first_guest_cue_offset(paragraphs[guest_idx], guest)
        if cue_offset is None:
            return paragraphs, False
        kept = paragraphs[guest_idx][cue_offset:].lstrip(" ,.-\n")
        if kept:
            new_paragraphs.append(kept)
        new_paragraphs.extend(paragraphs[guest_idx + 1 :])
        return new_paragraphs, True

    new_paragraphs.extend(paragraphs[guest_idx:])
    return new_paragraphs, True


def first_guest_paragraph_index(paragraphs: list[str], guest: str) -> int | None:
    guest_cues = guest_paragraph_cues(guest)
    for idx, para in enumerate(paragraphs):
        lower = para.lower()
        if para.lstrip().startswith("#"):
            continue
        if lower.startswith("kind: captions") or lower.startswith("language: "):
            continue
        if "will be with us" in lower or "here with us in just a moment" in lower or "will be here with us" in lower:
            if "today is" in lower:
                continue
        if guest_cues and any(cue in lower for cue in guest_cues):
            return idx
        if (
            "welcome here" in lower
            or "good day to you" in lower
            or "thank you for joining us" in lower
            or "thank you for accommodating" in lower
        ):
            return idx
    return None


def trim_outro_paragraphs(paragraphs: list[str]) -> tuple[list[str], bool]:
    new_paragraphs = list(paragraphs)
    removed = False
    cut_idx = -1
    cut_offset = -1
    for idx, para in enumerate(new_paragraphs):
        match = OUTRO_CUE_RE.search(para)
        if match:
            cut_idx = idx
            cut_offset = match.start()
            break
    if cut_idx != -1:
        kept = new_paragraphs[cut_idx][:cut_offset].rstrip(" -,\n")
        new_paragraphs = new_paragraphs[:cut_idx]
        if kept:
            new_paragraphs.append(kept)
        removed = True

    while new_paragraphs and is_noise_paragraph(new_paragraphs[-1]):
        new_paragraphs.pop()
        removed = True
    return new_paragraphs, removed


def clean_transcript_noise(paragraphs: list[str]) -> tuple[list[str], bool]:
    cleaned: list[str] = []
    changed = False
    for idx, paragraph in enumerate(paragraphs):
        updated = paragraph

        without_meta = METADATA_LINE_RE.sub("", updated)
        if without_meta != updated:
            updated = without_meta
            changed = True

        without_inline_noise = INLINE_NOISE_RE.sub(" ", updated)
        if without_inline_noise != updated:
            updated = without_inline_noise
            changed = True

        without_speaker_markers = SPEAKER_MARKER_RE.sub(" ", updated)
        if without_speaker_markers != updated:
            updated = without_speaker_markers
            changed = True

        normalized = " ".join(updated.split()).strip()
        if idx == 0:
            without_leading_show_noise = LEADING_SHOW_NOISE_RE.sub("", normalized).strip()
            if without_leading_show_noise != normalized:
                normalized = without_leading_show_noise
                changed = True

        if normalized != paragraph.strip():
            changed = True

        if normalized:
            cleaned.append(normalized)
        else:
            changed = True

    intro_idx = next((idx for idx, para in enumerate(cleaned) if re.search(r"\b(?:hi everyone|good morning)\b", para, re.IGNORECASE)), None)
    if intro_idx is not None:
        new_cleaned: list[str] = []
        for idx, para in enumerate(cleaned):
            if idx < intro_idx and is_noise_paragraph(para):
                changed = True
                continue
            new_cleaned.append(para)
        cleaned = new_cleaned

    return cleaned, changed


def is_noise_paragraph(paragraph: str) -> bool:
    compact = " ".join(paragraph.split()).strip()
    if not compact:
        return True
    return bool(MUSIC_ONLY_RE.fullmatch(compact))


def split_paragraphs(body: str) -> list[str]:
    text = body.strip()
    if not text:
        return []
    return [chunk.strip() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()]


def join_paragraphs(paragraphs: list[str]) -> str:
    return "\n\n".join(paragraphs).rstrip() + "\n"


def normalize_file(path: Path) -> FileChange | None:
    text = path.read_text(encoding="utf-8")
    changed, new_text, file_change = normalize_text(path, text)
    if not changed:
        return None
    path.write_text(new_text, encoding="utf-8")
    return file_change


def normalize_text(path: Path, text: str) -> tuple[bool, str, FileChange]:
    meta, body = split_frontmatter(text)
    paragraphs = split_paragraphs(body)
    guest = str(meta.get("guest") or "")

    cleaned_paragraphs, noise_removed = clean_transcript_noise(paragraphs)
    trimmed_intro, intro_removed = trim_intro_paragraphs(cleaned_paragraphs, guest)
    trimmed_body, outro_removed = trim_outro_paragraphs(trimmed_intro)

    quality_note_before = str(meta.get("quality_note") or "")
    quality_note_updated = False
    if (
        intro_removed
        or outro_removed
        or noise_removed
        or "ad copy" in quality_note_before.lower()
        or "sponsor" in quality_note_before.lower()
        or "promo" in quality_note_before.lower()
        or "transcript noise" in quality_note_before.lower()
    ):
        if quality_note_before != UPDATED_QUALITY_NOTE:
            meta["quality_note"] = UPDATED_QUALITY_NOTE
            quality_note_updated = True

    new_body = join_paragraphs(trimmed_body)
    new_text = dump_frontmatter(meta) + new_body
    file_change = FileChange(
        path=path,
        intro_removed=intro_removed,
        outro_removed=outro_removed,
        quality_note_updated=quality_note_updated,
    )
    return new_text != text, new_text, file_change


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=RAW_INPUT_ROOT,
        help="Root directory to scan for Napolitano/Judging Freedom raw transcripts.",
    )
    args = parser.parse_args()

    changes: list[FileChange] = []
    for path in candidate_paths(args.root):
        change = normalize_file(path)
        if change is not None:
            changes.append(change)

    print(f"Normalized {len(changes)} Napolitano/Judging Freedom transcript file(s).")
    for change in changes:
        flags: list[str] = []
        if change.intro_removed:
            flags.append("intro")
        if change.outro_removed:
            flags.append("outro")
        if change.quality_note_updated:
            flags.append("quality_note")
        joined = ", ".join(flags) if flags else "metadata"
        print(f"- {change.path.relative_to(REPO_ROOT).as_posix()} [{joined}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
