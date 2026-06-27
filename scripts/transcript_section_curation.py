#!/usr/bin/env python3
"""Shared helpers for source transcript section curation (solo / interview captures)."""
from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from datetime import date
from pathlib import Path

BODY_MARKERS: tuple[str, ...] = (
    "## Transcript\n",
    "## Part I: Full transcript\n",
    "## Cleaned Transcript\n",
)
UNICODE_APOSTROPHE = r"['\u2019]"

AUTHORED_KINDS = frozenset({"substack-post", "newsletter", "x-post-text", "paste-bundle"})
AUTHORED_FORMS = frozenset({"newsletter", "article", "post", "roundup"})


def parse_capture_eligibility_meta(head: str) -> dict[str, str]:
    """Minimal frontmatter parse for source-section eligibility checks."""
    fm = head
    if "---" in head:
        parts = head.split("---", 2)
        if len(parts) >= 2:
            fm = parts[1]
    out: dict[str, str] = {}
    for key in ("kind", "source_form", "source_type", "source_url", "channel_slug", "guest"):
        m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    return out


def is_source_section_eligible(meta: dict[str, str], *, guest: bool | None = None) -> bool:
    """True for YouTube channel transcript captures; false for authored essays/posts."""
    kind = (meta.get("kind") or "").lower()
    form = (meta.get("source_form") or "").lower()
    if kind in AUTHORED_KINDS or form in AUTHORED_FORMS:
        return False
    if guest is False:
        return False
    if form in ("interview", "solo"):
        return True
    if (meta.get("source_type") or "").lower() == "youtube":
        return True
    if meta.get("channel_slug"):
        return True
    if "youtube.com" in (meta.get("source_url") or "").lower():
        return True
    if meta.get("guest"):
        return True
    return guest is True


def detect_body_marker(doc: str) -> str:
    for marker in BODY_MARKERS:
        if marker in doc:
            return marker
    raise ValueError(
        f"missing transcript body marker (expected one of: {', '.join(repr(m) for m in BODY_MARKERS)})"
    )


def split_transcript_document(doc: str) -> tuple[str, str, str]:
    marker = detect_body_marker(doc)
    head, body = doc.split(marker, 1)
    return head, marker, body


def normalize_for_anchor(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2014", "-").replace("\u2013", "-")
    return text.lower()


def find_anchor_pos(flat: str, anchor: str, start: int) -> int:
    hay = normalize_for_anchor(flat)
    needle = normalize_for_anchor(anchor)
    pos = hay.find(needle, start)
    if pos == -1:
        raise ValueError(f"anchor not found: {anchor!r} (from pos {start})")
    return pos


def insert_sections(
    body: str,
    section_titles: Sequence[str],
    section_anchors: Sequence[str],
    *,
    asr_cleanup_fn: Callable[[str], str] | None = None,
    anchor_slice: slice | None = None,
) -> str:
    """Split flat transcript body into Title Case ``###`` sections.

    Uses N−1 anchors for N sections. Final section runs to EOF.
    """
    if len(section_titles) != len(section_anchors) + 1 and anchor_slice is None:
        raise ValueError(
            f"expected {len(section_titles) - 1} anchors for "
            f"{len(section_titles)} sections, got {len(section_anchors)}"
        )

    flat = asr_cleanup_fn(body) if asr_cleanup_fn else body
    anchors = (
        section_anchors[anchor_slice]
        if anchor_slice is not None
        else section_anchors
    )
    if len(section_titles) != len(anchors) + 1:
        raise ValueError(
            f"after anchor_slice, expected {len(section_titles) - 1} anchors, "
            f"got {len(anchors)}"
        )

    positions = [0]
    cursor = 0
    for anchor in anchors:
        pos = find_anchor_pos(flat, anchor, cursor)
        positions.append(pos)
        cursor = pos + len(normalize_for_anchor(anchor))
    positions.append(len(flat))

    parts: list[str] = []
    for i, heading in enumerate(section_titles):
        end = len(flat) if i == len(section_titles) - 1 else positions[i + 1]
        chunk = flat[positions[i] : end].strip()
        parts.append(f"### {heading}\n\n{chunk}")
    return "\n\n".join(parts)


def common_asr_cleanup(
    text: str,
    *,
    replacements: dict[str, str] | None = None,
) -> str:
    text = text.replace("Professor Dieng.", "Professor Jiang.")
    text = text.replace("Professor Dieng,", "Professor Jiang,")
    text = text.replace("Professor Dieng", "Professor Jiang")
    for old, new in (replacements or {}).items():
        text = text.replace(old, new)
    text = re.sub(r"\bThe The\b", "The", text)
    text = re.sub(r"\bIt It\b", "It", text)
    text = re.sub(r"\bTrump Trump\b", "Trump", text)
    text = re.sub(r"\bdemystify all of all of\b", "demystify all of", text)
    text = re.sub(r"\bMiddle Middle East\b", "Middle East", text)
    text = re.sub(r"\bof of\b", "of", text)
    text = re.sub(r"\bthe the\b", "the", text, flags=re.I)
    text = re.sub(r"\bhave has\b", "have", text, flags=re.I)
    return text


def strip_speakers_before_section_headings(body: str, speaker_pattern: str) -> str:
    return re.sub(
        rf"\n\n\*\*(?:{speaker_pattern}):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )


def prepend_speaker_at_section_opens(
    body: str,
    fixes: Sequence[tuple[str, str, str]],
) -> str:
    """Each fix: (section title without ###, speaker label, opener regex)."""
    for section, speaker, opener in fixes:
        pattern = (
            rf"(### {re.escape(section)}\n\n)"
            rf"(?!\*\*{re.escape(speaker)}:\*\*)"
            rf"({opener})"
        )
        body = re.sub(pattern, rf"\1**{speaker}:** \2", body, count=1)
    return body


def apply_slug_to_title_headings(
    body: str,
    slug_headings: Sequence[tuple[str, str]],
) -> str:
    out = body
    for slug, heading in slug_headings:
        old = f"### {slug}"
        new = f"### {heading}"
        if old not in out and new in out:
            continue
        if old not in out:
            raise ValueError(f"missing section slug: {slug}")
        out = out.replace(old, new, 1)
    return out


def mark_sectioned_frontmatter(head: str, *, section_count: int) -> str:
    today = date.today().isoformat()
    receipt = f"source-section pass {today} ({section_count} sections)"
    if re.search(r"^transcript_curation:", head, flags=re.M):
        head = re.sub(
            r"^transcript_curation:.*$",
            "transcript_curation: curated_sectioned",
            head,
            count=1,
            flags=re.M,
        )
    else:
        head = head.replace("\n---\n", f"\ntranscript_curation: curated_sectioned\n---\n", 1)
    if re.search(r"^editorial_note:", head, flags=re.M):
        if receipt not in head:
            head = re.sub(
                r"^(editorial_note: \"?)(.*?)\"?\s*$",
                rf'\1\2 · {receipt}."',
                head,
                count=1,
                flags=re.M,
            )
    elif re.search(r"^source_note:", head, flags=re.M):
        head = re.sub(
            r"^(source_note: \"?)(.*?)\"?\s*$",
            rf'\1\2 · {receipt}."',
            head,
            count=1,
            flags=re.M,
        )
    return head


def write_sectioned_capture(
    capture_path: Path,
    section_titles: Sequence[str],
    section_anchors: Sequence[str],
    *,
    asr_cleanup_fn: Callable[[str], str] | None = None,
    speaker_cleanup_fn: Callable[[str], str] | None = None,
    anchor_slice: slice | None = None,
    reject_if_sectioned: bool = True,
    body_marker: str | None = None,
) -> None:
    doc = capture_path.read_text(encoding="utf-8")
    marker = body_marker or detect_body_marker(doc)
    if marker not in doc:
        raise ValueError(f"missing body marker: {marker!r}")

    head, body = doc.split(marker, 1)
    if not is_source_section_eligible(parse_capture_eligibility_meta(head)):
        raise ValueError(
            "source-section applies to YouTube channel transcripts (solo/interview) only; "
            "authored texts (Substack, newsletter, article) are out of scope"
        )
    if reject_if_sectioned and body.lstrip().startswith("### "):
        raise ValueError("transcript already sectioned")

    head = mark_sectioned_frontmatter(head, section_count=len(section_titles))
    body = insert_sections(
        body.strip(),
        section_titles,
        section_anchors,
        asr_cleanup_fn=asr_cleanup_fn,
        anchor_slice=anchor_slice,
    )
    if speaker_cleanup_fn:
        body = speaker_cleanup_fn(body)

    doc = f"{head}{marker}\n\n{body}\n"
    capture_path.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {capture_path} "
        f"({len(body.split()):,} words, {len(section_titles)} sections)"
    )


def write_slug_retitle_capture(
    capture_path: Path,
    slug_headings: Sequence[tuple[str, str]],
    *,
    asr_cleanup_fn: Callable[[str], str] | None = None,
    body_marker: str | None = None,
) -> None:
    doc = capture_path.read_text(encoding="utf-8")
    marker = body_marker or detect_body_marker(doc)
    head, body = doc.split(marker, 1)
    if asr_cleanup_fn:
        body = asr_cleanup_fn(body)
    body = apply_slug_to_title_headings(body, slug_headings)
    head = mark_sectioned_frontmatter(head, section_count=len(slug_headings))
    doc = f"{head}{marker}{body}"
    capture_path.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {capture_path} "
        f"({len(body.split()):,} words, {len(slug_headings)} sections)"
    )
