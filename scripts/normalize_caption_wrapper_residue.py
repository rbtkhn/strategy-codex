#!/usr/bin/env python3
"""Normalize cross-family caption and paste wrapper residue in place.

Lanes (conservative, substance-preserving):
  1. html_entities — decode &gt;&gt;, &amp;, &quot;, &#39;, &nbsp;
  2. caption_header — strip Kind: captions / Language: preamble
  3. transcripts_prefix — strip leading Transcripts: paste wrapper
  4. leading_music — opening-only [Music] / Heat. noise

Default is dry-run. Run before family opening normalizers on intake.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TRANSCRIPT_SECTION_RE = re.compile(r"(^## Transcript\s*\n)(.*)$", re.DOTALL | re.MULTILINE)
CAPTION_HEADER_RE = re.compile(
    r"^Kind:\s*captions\s*\r?\nLanguage:\s*\w+\s*\r?\n+",
    re.IGNORECASE | re.MULTILINE,
)
TRANSCRIPTS_PREFIX_RE = re.compile(r"^Transcripts:\s*\r?\n?", re.IGNORECASE | re.MULTILINE)
LEADING_MUSIC_RE = re.compile(r"^(?:\[Music\]\s*|\[music\]\s*|Heat\.\s*)+", re.IGNORECASE)
ENTITY_MARKERS = ("&gt;", "&amp;", "&quot;", "&#39;", "&nbsp;")

EDITORIAL_NOTE = (
    "Caption/paste wrapper residue normalized in place; SSOT substance preserved."
)


@dataclass(frozen=True)
class FileChange:
    path: Path
    wrapper_tier: str
    entities_decoded: bool = False
    caption_header_stripped: bool = False
    transcripts_prefix_stripped: bool = False
    leading_music_stripped: bool = False


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


def is_transcript_archive_capture(meta: dict[str, Any], path: Path) -> bool:
    if not path.name.startswith("source-") or not path.name.endswith(".md"):
        return False
    if ".cleaned." in path.name:
        return False
    kind = str(meta.get("kind") or "").strip().lower()
    if kind and kind not in {"transcript", "cleaned-transcript"}:
        return False
    return True


def split_body_sections(body: str) -> tuple[str, str, str]:
    match = TRANSCRIPT_SECTION_RE.search(body)
    if match:
        return body[: match.start()], match.group(1), match.group(2)

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
    return "".join(lines[:idx]), "", "".join(lines[idx:])


def merge_body_sections(prefix: str, transcript_header: str, transcript_body: str) -> str:
    if not transcript_header:
        return prefix + transcript_body
    return prefix + transcript_header + transcript_body


def append_editorial_note(meta: dict[str, Any], note: str) -> None:
    existing = str(meta.get("editorial_note") or "").strip()
    if note.lower() in existing.lower():
        return
    meta["editorial_note"] = f"{existing} {note}".strip() if existing else note


def classify_wrapper_tier(
    *,
    entities: bool,
    caption_header: bool,
    transcripts_prefix: bool,
    leading_music: bool,
) -> str:
    if caption_header:
        return "caption-metadata"
    if transcripts_prefix:
        return "paste-prefix"
    if entities:
        return "html-entities"
    if leading_music:
        return "clean"
    return "clean"


def has_html_entities(text: str) -> bool:
    return any(marker in text for marker in ENTITY_MARKERS)


def decode_html_entities(text: str) -> tuple[str, bool]:
    if not has_html_entities(text):
        return text, False
    decoded = html.unescape(text)
    return decoded, decoded != text


def strip_caption_header(text: str) -> tuple[str, bool]:
    stripped = CAPTION_HEADER_RE.sub("", text, count=1)
    return stripped, stripped != text


def strip_transcripts_prefix(text: str) -> tuple[str, bool]:
    stripped = TRANSCRIPTS_PREFIX_RE.sub("", text, count=1)
    return stripped, stripped != text


def strip_leading_music(text: str) -> tuple[str, bool]:
    stripped = LEADING_MUSIC_RE.sub("", text, count=1).lstrip()
    if stripped != text.lstrip():
        return stripped, True
    return text, False


def normalize_transcript_body(
    body: str,
    *,
    allow_entities: bool,
    allow_caption_header: bool,
    allow_transcripts_prefix: bool,
    allow_leading_music: bool,
) -> tuple[str, bool, FileChange]:
    if not body.strip():
        return body, False, FileChange(Path(), "clean")

    text = body
    entities = caption_header = transcripts_prefix = leading_music = False

    if allow_entities:
        text, did = decode_html_entities(text)
        entities = did

    if allow_caption_header:
        text, did = strip_caption_header(text)
        caption_header = did

    if allow_transcripts_prefix:
        text, did = strip_transcripts_prefix(text)
        transcripts_prefix = did

    if allow_leading_music:
        text, did = strip_leading_music(text)
        leading_music = did

    changed = entities or caption_header or transcripts_prefix or leading_music
    tier = classify_wrapper_tier(
        entities=entities,
        caption_header=caption_header,
        transcripts_prefix=transcripts_prefix,
        leading_music=leading_music,
    )
    return (text if changed else body), changed, FileChange(
        Path(),
        tier,
        entities_decoded=entities,
        caption_header_stripped=caption_header,
        transcripts_prefix_stripped=transcripts_prefix,
        leading_music_stripped=leading_music,
    )


def normalize_text(path: Path, text: str, *, tag_only: bool = False) -> tuple[bool, str, FileChange | None]:
    meta, body = split_frontmatter(text)
    if not is_transcript_archive_capture(meta, path):
        return False, text, None

    prefix, transcript_header, transcript_body = split_body_sections(body)
    if not transcript_body.strip():
        return False, text, None

    entities_done = bool(meta.get("caption_entities_decoded"))
    header_done = bool(meta.get("caption_header_strip_applied"))
    prefix_done = bool(meta.get("transcripts_prefix_stripped"))
    music_done = bool(meta.get("caption_leading_music_stripped"))
    wrapper_done = bool(meta.get("caption_wrapper_normalize_applied"))

    if tag_only:
        tier = str(meta.get("transcript_wrapper_tier") or "clean")
        if meta.get("transcript_wrapper_tier") != tier:
            meta["transcript_wrapper_tier"] = tier
            return True, dump_frontmatter(meta) + body, FileChange(path, tier)
        return False, text, None

    if wrapper_done and entities_done and header_done and prefix_done and music_done:
        tier = str(meta.get("transcript_wrapper_tier") or "clean")
        return False, text, FileChange(path, tier)

    new_body, changed, change = normalize_transcript_body(
        transcript_body,
        allow_entities=not entities_done,
        allow_caption_header=not header_done,
        allow_transcripts_prefix=not prefix_done,
        allow_leading_music=not music_done,
    )

    if not changed:
        if not meta.get("transcript_wrapper_tier"):
            meta["transcript_wrapper_tier"] = "clean"
            return True, dump_frontmatter(meta) + body, FileChange(path, "clean")
        return False, text, FileChange(path, str(meta.get("transcript_wrapper_tier")))

    if change.entities_decoded:
        meta["caption_entities_decoded"] = True
    if change.caption_header_stripped:
        meta["caption_header_strip_applied"] = True
    if change.transcripts_prefix_stripped:
        meta["transcripts_prefix_stripped"] = True
    if change.leading_music_stripped:
        meta["caption_leading_music_stripped"] = True
    meta["caption_wrapper_normalize_applied"] = True
    meta["transcript_wrapper_tier"] = change.wrapper_tier
    append_editorial_note(meta, EDITORIAL_NOTE)

    merged = merge_body_sections(prefix, transcript_header, new_body)
    return (
        True,
        dump_frontmatter(meta) + merged,
        FileChange(
            path,
            change.wrapper_tier,
            entities_decoded=change.entities_decoded,
            caption_header_stripped=change.caption_header_stripped,
            transcripts_prefix_stripped=change.transcripts_prefix_stripped,
            leading_music_stripped=change.leading_music_stripped,
        ),
    )


def candidate_paths(root: Path, explicit: list[Path] | None = None) -> list[Path]:
    if explicit:
        return sorted({p.resolve() for p in explicit})
    paths: list[Path] = []
    for path in root.rglob("source-*.md"):
        if ".cleaned." in path.name:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        meta, _ = split_frontmatter(text)
        if is_transcript_archive_capture(meta, path):
            paths.append(path)
    return sorted(set(paths))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ARCHIVE_ROOT)
    parser.add_argument("--path", type=Path, action="append", default=[])
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--tag-only", action="store_true")
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
            wrapper_tier=file_change.wrapper_tier,
            entities_decoded=file_change.entities_decoded,
            caption_header_stripped=file_change.caption_header_stripped,
            transcripts_prefix_stripped=file_change.transcripts_prefix_stripped,
            leading_music_stripped=file_change.leading_music_stripped,
        )
        if changed:
            changes.append(file_change)
            if args.apply:
                path.write_text(new_text, encoding="utf-8")

    mode = "Applied" if args.apply else "Dry-run"
    print(f"{mode}: {len(changes)} transcript file(s) would change; {skipped} skipped.")
    for change in changes:
        flags: list[str] = []
        if change.entities_decoded:
            flags.append("entities")
        if change.caption_header_stripped:
            flags.append("caption_header")
        if change.transcripts_prefix_stripped:
            flags.append("transcripts_prefix")
        if change.leading_music_stripped:
            flags.append("leading_music")
        joined = ", ".join(flags) if flags else "metadata"
        rel = change.path.relative_to(REPO_ROOT).as_posix()
        print(f"- {rel} [{joined}] tier={change.wrapper_tier}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
