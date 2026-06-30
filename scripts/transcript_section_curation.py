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
    for key in ("kind", "source_form", "source_type", "source_url", "channel_slug", "guest", "host"):
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

ABBREV_GUARDS: tuple[str, ...] = (
    "U.S.",
    "U.K.",
    "Mr.",
    "Mrs.",
    "Ms.",
    "Dr.",
    "etc.",
    "i.e.",
    "e.g.",
    "Fab",
    "MoU",
    "No.",
    "vs.",
    "St.",
    "Gen.",
    "Col.",
    "Jr.",
    "Sr.",
)

DISCOURSE_PIVOTS: tuple[str, ...] = (
    "Now,",
    "Anyway,",
    "So anyway,",
    "So,",
    "But,",
    "Meanwhile,",
    "Incidentally,",
    "And of course,",
    "By the way,",
    "This, by the way,",
    "Just saying.",
    "For the last",
    "In the meantime,",
    "There's been, by the way,",
)

_SECTION_HEADING_LINE = re.compile(r"^### .+$", re.M)
_SPEAKER_LINE = re.compile(r"^\*\*.+:\*\*", re.M)
_SPEAKER_LABEL_LINE = re.compile(r"^(\*\*.+:\*\*)(?:\s+(.*))?$", re.DOTALL)
_TURN_MARKER = re.compile(r"^>>", re.M)
_WORD_RE = re.compile(r"\b\w+\b")

def count_words(text: str) -> int:
    return len(_WORD_RE.findall(text))

def _paragraph_word_counts(text: str) -> list[int]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    return [count_words(p) for p in paras]

def _starts_with_discourse_pivot(sentence: str) -> bool:
    stripped = sentence.lstrip()
    return any(stripped.startswith(pivot) for pivot in DISCOURSE_PIVOTS)

def _normalize_runon_whitespace(text: str) -> str:
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    return re.sub(r" +", " ", text).strip()

def _protect_abbreviations(text: str) -> tuple[str, dict[str, str]]:
    placeholders: dict[str, str] = {}
    protected = text
    for idx, abbr in enumerate(ABBREV_GUARDS):
        token = f"__ABBR{idx}__"
        if abbr in protected:
            placeholders[token] = abbr
            protected = protected.replace(abbr, token)
    return protected, placeholders

def _restore_abbreviations(text: str, placeholders: dict[str, str]) -> str:
    restored = text
    for token, abbr in placeholders.items():
        restored = restored.replace(token, abbr)
    return restored

def split_sentences(text: str) -> list[str]:
    """Conservative sentence split for spoken transcript reflow."""
    normalized = _normalize_runon_whitespace(text)
    if not normalized:
        return []
    protected, placeholders = _protect_abbreviations(normalized)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'*])", protected)
    sentences = [_restore_abbreviations(p.strip(), placeholders) for p in parts if p.strip()]
    return sentences

def pack_sentences_into_paragraphs(
    sentences: Sequence[str],
    *,
    target_para_words: int = 80,
    soft_max_para_words: int = 120,
    hard_max_para_words: int = 150,
) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    current_words = 0

    for sentence in sentences:
        sentence_words = count_words(sentence)
        if (
            current
            and _starts_with_discourse_pivot(sentence)
            and current_words >= int(target_para_words * 0.6)
        ):
            paragraphs.append(" ".join(current))
            current = [sentence]
            current_words = sentence_words
            continue

        if current and current_words + sentence_words > hard_max_para_words:
            paragraphs.append(" ".join(current))
            current = [sentence]
            current_words = sentence_words
            continue

        if current and current_words + sentence_words > soft_max_para_words:
            paragraphs.append(" ".join(current))
            current = [sentence]
            current_words = sentence_words
            continue

        current.append(sentence)
        current_words += sentence_words

    if current:
        paragraphs.append(" ".join(current))
    return paragraphs

def _split_hard_segments(text: str) -> list[str]:
    """Split section text on paragraph breaks, speaker labels, and turn markers."""
    segments: list[str] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        block = block.strip()
        if not block:
            continue
        parts = re.split(r"(?=^\*\*.+:\*\*)|(?=^>>)", block, flags=re.M)
        for part in parts:
            part = part.strip()
            if part:
                segments.append(part)
    return segments or ([text.strip()] if text.strip() else [])

def _reflow_text_segment(
    text: str,
    *,
    target_para_words: int,
    soft_max_para_words: int,
    hard_max_para_words: int,
) -> str:
    text = text.strip()
    if not text:
        return ""

    label_prefix = ""
    speaker_match = _SPEAKER_LABEL_LINE.match(text)
    if speaker_match:
        label, rest = speaker_match.group(1), (speaker_match.group(2) or "").strip()
        if not rest:
            return text
        label_prefix = f"{label} "
        text = rest
    else:
        turn_match = re.match(r"^(>>\s*)(.+)$", text, re.DOTALL)
        if turn_match:
            marker, rest = turn_match.group(1), turn_match.group(2).strip()
            if not rest:
                return text
            label_prefix = marker
            text = rest

    sentences = split_sentences(text)
    if not sentences:
        return label_prefix.rstrip() if label_prefix else text
    if len(sentences) == 1 and count_words(sentences[0]) <= hard_max_para_words:
        body = sentences[0]
        return f"{label_prefix}{body}" if label_prefix else body
    paragraphs = pack_sentences_into_paragraphs(
        sentences,
        target_para_words=target_para_words,
        soft_max_para_words=soft_max_para_words,
        hard_max_para_words=hard_max_para_words,
    )
    if label_prefix:
        paragraphs[0] = f"{label_prefix}{paragraphs[0]}"
    return "\n\n".join(paragraphs)

def _reflow_section_chunk(
    chunk: str,
    *,
    target_para_words: int,
    soft_max_para_words: int,
    hard_max_para_words: int,
) -> str:
    chunk = chunk.strip()
    if not chunk:
        return ""
    para_counts = _paragraph_word_counts(chunk)
    if len(para_counts) >= 2 and all(w <= hard_max_para_words for w in para_counts):
        return chunk

    reflowed_segments: list[str] = []
    for segment in _split_hard_segments(chunk):
        reflowed_segments.append(
            _reflow_text_segment(
                segment,
                target_para_words=target_para_words,
                soft_max_para_words=soft_max_para_words,
                hard_max_para_words=hard_max_para_words,
            )
        )
    return "\n\n".join(s for s in reflowed_segments if s)

def reflow_section_paragraphs(
    body: str,
    *,
    target_para_words: int = 80,
    soft_max_para_words: int = 120,
    hard_max_para_words: int = 150,
) -> str:
    """Insert markdown paragraph breaks within each ``###`` section (words unchanged)."""
    if not body.strip():
        return body

    if not _SECTION_HEADING_LINE.search(body):
        return _reflow_section_chunk(
            body,
            target_para_words=target_para_words,
            soft_max_para_words=soft_max_para_words,
            hard_max_para_words=hard_max_para_words,
        )

    parts = re.split(r"(^### .+$)", body, flags=re.M)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("### "):
            out.append(part)
            continue
        reflowed = _reflow_section_chunk(
            part,
            target_para_words=target_para_words,
            soft_max_para_words=soft_max_para_words,
            hard_max_para_words=hard_max_para_words,
        )
        if reflowed:
            out.append(reflowed)
    return "\n\n".join(out)

def write_paragraph_reflow_capture(
    capture_path: Path,
    *,
    body_marker: str | None = None,
    target_para_words: int = 80,
    soft_max_para_words: int = 120,
    hard_max_para_words: int = 150,
) -> None:
    """Paragraph reflow only — preserve existing section map."""
    doc = capture_path.read_text(encoding="utf-8")
    marker = body_marker or detect_body_marker(doc)
    head, body = doc.split(marker, 1)
    if not body.lstrip().startswith("### "):
        raise ValueError("paragraph reflow only applies to sectioned captures")
    body = reflow_section_paragraphs(
        body.strip(),
        target_para_words=target_para_words,
        soft_max_para_words=soft_max_para_words,
        hard_max_para_words=hard_max_para_words,
    )
    today = date.today().isoformat()
    receipt = f"paragraph reflow pass {today}"
    if receipt not in head:
        if re.search(r"^editorial_note:", head, flags=re.M):
            head = re.sub(
                r'^(editorial_note: "?)(.*?)"?\s*$',
                rf'\1\2 · {receipt}."',
                head,
                count=1,
                flags=re.M,
            )
    doc = f"{head}{marker}\n\n{body}\n"
    capture_path.write_text(doc, encoding="utf-8", newline="\n")
    print(f"wrote {capture_path} (paragraph reflow, {len(body.split()):,} words)")

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

def body_has_interview_speaker_labels(body: str) -> bool:
    return bool(
        re.search(r"^\*\*Larry Johnson:\*\*", body, re.M)
        and re.search(r"^\*\*Nima Alkhorshid:\*\*", body, re.M)
    )

def normalize_dialogue_works_asr_turns(text: str) -> str:
    """Collapse common YouTube ASR false ``>>`` splits (not speaker turns)."""
    text = re.sub(r"\s>>\s+on\s>>\s+", " on ", text, flags=re.I)
    text = re.sub(r"\s>>\s+off\s>>\s+", " off ", text, flags=re.I)
    # Broken mid-sentence guest continuation (e.g. "Jordan. The >> people").
    text = re.sub(r"\.\sThe\s>>\s+", ". The ", text)
    return text

# Host lines ASR sometimes merges into the prior guest ``>>`` chunk without a marker.
DIALOGUE_WORKS_HOST_TURN_SPLITS: tuple[str, ...] = (
    "My understanding today, Larry",
)

# Section anchors can swallow ``>>``; inject before relabel when a new section opens mid-turn.
DIALOGUE_WORKS_GUEST_SECTION_OPENERS: tuple[str, ...] = (
    "Nima these are really good questions",
    "Nemo these are really good questions",
    "what's what's left of what's left of that place",
    "I mean, let's just last night's attacks",
    "Well, you know, the US is not responding",
    "You know, I really, for the life of me",
    "The concept on the part of Iranian",
    "What's so amazing to me that MOU",
    "Look they stopped the the United States has been breaking the MOU",
    "Well, the assembly the assembly of experts issued that",
)

DIALOGUE_WORKS_HOST_SECTION_OPENERS: tuple[str, ...] = (
    "Yeah. My understanding is that Iran has doesn't feel",
    "Yeah. The question is Rey",
    "Yeah. The question is Ray",
    "Before wrapping up, my understanding of Russia",
    "Right. Before wrapping up, my understanding of Russia",
    "the communication line that JD Vance was talking about",
    "Today I talk with David Pyne",
    "The whole I think it's it's the outcome of the Marco Rubio's visit",
    "I don't know if Larry the case of Lebanon is complicating",
    "Yeah. You see the flag of Hezbollah in the crowd",
    "Their argument is this Larry",
    "Here is no reports, Larry",
    "Larry, do you do you think that Europe",
    "take out all the air tankers of Ben Gurion for starter",
)

def inject_section_open_turn_markers(body: str) -> str:
    """Insert ``>>`` when a ``###`` section opens on a known host/guest line without a marker."""
    parts = re.split(r"(^### .+$)", body, flags=re.M)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("### "):
            out.append(part.rstrip() + "\n\n")
            continue
        chunk = part.lstrip("\n")
        if not chunk.strip():
            continue
        stripped = chunk.lstrip()
        if not stripped.startswith(">>"):
            for opener in DIALOGUE_WORKS_GUEST_SECTION_OPENERS + DIALOGUE_WORKS_HOST_SECTION_OPENERS:
                if stripped.startswith(opener):
                    chunk = f">> {stripped}"
                    break
        out.append(chunk.rstrip() + "\n\n")
    return "".join(out)

def restore_turn_markers_from_speaker_labels(
    body: str,
    *,
    host: str = "Nima Alkhorshid",
    guest: str = "Larry Johnson",
) -> str:
    """Convert ``**Speaker:**`` turn labels back to ``>>`` for idempotent relabel passes."""
    for name in (host, guest):
        body = re.sub(rf"\*\*{re.escape(name)}:\*\* ", ">> ", body)
    return body

def inject_dialogue_works_missing_turn_markers(text: str) -> str:
    """Insert ``>>`` before host lines glued onto a guest turn (no marker in source)."""
    for cue in DIALOGUE_WORKS_HOST_TURN_SPLITS:
        if f">> {cue}" in text or f">>{cue}" in text:
            continue
        text = re.sub(
            rf"(?<=[.!?]\s){re.escape(cue)}",
            rf" >> {cue}",
            text,
        )
    text = re.sub(r"\s*>>\s*>>\s+", " >> ", text)
    return text

def _guess_dialogue_works_host(piece: str) -> bool | None:
    opening = piece.lstrip()[:160].lower()
    if opening.startswith(
        (
            "nima these are really good",
            "nemo these are really good",
            "what's what's left of what's left",
            "in a jocular mood",
            "now uh in a jocular",
            "yeah. and oman is really",
            "exactly. because when you don't",
        )
    ):
        return False
    if opening.startswith(
        (
            "yeah. the question is rey",
            "yeah. the question is ray",
            "before wrapping up, my understanding",
            "right. before wrapping up, my understanding",
        )
    ):
        return True
    if opening.startswith(
        (
            "i think i think",
            "i i think i think",
            "i mean,",
            "well, you know",
            "well,",
            "look they stopped",
            "correct.",
            "i'm told",
            "i anticipate",
            "either way,",
            "maybe uh",
        )
    ):
        return False
    if opening.startswith(("uh yeah", "yeah. yeah. no, i think")):
        return False
    if opening.startswith(
        (
            "yeah, they've already they already",
            "yeah. they've already",
            "yeah. one of the us officials",
            "yeah. but again, all i'm saying",
            "yeah. who",
            "hi everybody",
        )
    ):
        return True
    if opening.startswith(
        (
            "so yeah, they're not that",
            "yeah, bahrain was reported",
            "people they've already",
            "do you you know who",
        )
    ):
        return False

    lower = piece[:500].lower()
    host_cues = (
        "larry,",
        " Larry",
        "my understanding today, lar",
        "the problem lar",
        "here is no reports",
        "i don't know if lar",
        "what has happened in lebanon",
        "yeah. you see the flag",
        "their argument is this lar",
        "i talked with mar",
        "today i talk with david",
        "the communication line that jd vance",
        "there is no communication lar",
        "who's giving them the basis",
        "yeah. but again, all i'm saying",
        "the whole i think it's it's the outcome of the marco rubio's visit",
        "did did he did he issue",
        "was it was it was it the ayatollah",
        "yeah. my the reason that i said",
        "yeah. the iranian media",
        "how much pressure do they receive",
        "to the point of sanctions, lar",
        "do you think that he's going to",
        "jd vance, he went on",
        "he he he told me yesterday",
    )
    guest_cues = (
        "i really, for the life of me",
        "i don't know because it was nobody",
    )
    host_score = sum(1 for cue in host_cues if cue in lower)
    guest_score = sum(1 for cue in guest_cues if cue in lower)
    if host_score > guest_score:
        return True
    if guest_score > host_score:
        return False
    return None

def remove_empty_speaker_turns(body: str) -> str:
    """Drop ``**Speaker:**`` lines with no spoken content (section-boundary artifacts)."""
    blocks = re.split(r"(\n\s*\n)", body.strip())
    kept: list[str] = []
    for block in blocks:
        if re.fullmatch(r"\*\*.+:\*\*", block.strip()):
            continue
        kept.append(block)
    return "".join(kept)

def merge_orphan_paragraphs_into_prior_turn(body: str) -> str:
    """Attach unlabeled paragraphs to the preceding speaker turn (interview layout)."""
    blocks = re.split(r"\n\s*\n", body.strip())
    merged: list[str] = []
    for block in blocks:
        stripped = block.strip()
        if not stripped:
            continue
        if stripped.startswith("### ") or re.match(r"^\*\*.+:\*\*", stripped):
            merged.append(stripped)
            continue
        if merged and not merged[-1].startswith("### "):
            merged[-1] = merged[-1] + "\n\n" + stripped
        else:
            merged.append(stripped)
    return "\n\n".join(merged) + "\n\n"

def normalize_dialogue_works_host_label_suffix(
    body: str,
    *,
    host: str = "Nima Alkhorshid",
) -> str:
    """Drop legacy ``(host)`` from Dialogue Works Nima speaker labels."""
    for old in (
        f"**{host} (host):**",
        "**Nima Alkhorshid (host):**",
        "**Nima (host):**",
    ):
        body = body.replace(old, f"**{host}:**")
    return body

def apply_interview_turn_speaker_labels(
    body: str,
    *,
    host: str = "Nima Alkhorshid",
    guest: str = "Larry Johnson",
    host_suffix: str = "",
    start_with_host: bool = True,
) -> tuple[str, int]:
    """Replace YouTube ``>>`` turn markers with alternating host/guest speaker labels."""
    host_label = f"**{host}{host_suffix}:**"
    body = normalize_dialogue_works_host_label_suffix(body, host=host)
    if body_has_interview_speaker_labels(body) or ">>" not in body:
        return body, 0
    guest_label = f"**{guest}:**"
    speaker_is_host = start_with_host
    turns_labeled = 0

    sections = re.split(r"(^### .+$)", body, flags=re.M)
    out: list[str] = []
    for part in sections:
        if not part:
            continue
        if part.startswith("### "):
            out.append(part.rstrip() + "\n\n")
            continue
        labeled, speaker_is_host, n = _label_section_turns(
            part,
            host_label=host_label,
            guest_label=guest_label,
            speaker_is_host=speaker_is_host,
        )
        turns_labeled += n
        out.append(labeled)

    result = "".join(out)
    if turns_labeled:
        result = merge_orphan_paragraphs_into_prior_turn(result)
        result = remove_empty_speaker_turns(result)
    return result, turns_labeled

def _label_section_turns(
    text: str,
    *,
    host_label: str,
    guest_label: str,
    speaker_is_host: bool,
) -> tuple[str, bool, int]:
    text = normalize_dialogue_works_asr_turns(text)
    text = inject_dialogue_works_missing_turn_markers(text)
    pieces = re.split(r"\s*>>\s*", text)
    blocks: list[str] = []
    count = 0

    leading = pieces[0].strip() if pieces else ""
    if leading:
        guess = _guess_dialogue_works_host(leading)
        if guess is not None:
            speaker_is_host = guess
        label = host_label if speaker_is_host else guest_label
        blocks.append(f"{label} {leading}")
        count += 1

    for piece in pieces[1:]:
        piece = piece.strip()
        if not piece:
            continue
        speaker_is_host = not speaker_is_host
        guess = _guess_dialogue_works_host(piece)
        if guess is not None:
            speaker_is_host = guess
        label = host_label if speaker_is_host else guest_label
        blocks.append(f"{label} {piece}")
        count += 1

    if not blocks:
        return text, speaker_is_host, 0
    return "\n\n".join(blocks) + "\n\n", speaker_is_host, count

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

def flatten_sectioned_body(body: str) -> str:
    """Join section bodies into one flat transcript (drop ``###`` headings)."""
    chunks: list[str] = []
    current: list[str] = []
    for line in body.splitlines():
        if line.startswith("### "):
            if current:
                chunks.append("\n\n".join(current).strip())
                current = []
            continue
        current.append(line)
    if current:
        chunks.append("\n\n".join(current).strip())
    return "\n\n".join(chunks)

def flat_body_from_doc(doc: str) -> tuple[str, str, str]:
    """Return head, body marker, and flat transcript (drop existing ``###`` headings)."""
    head, marker, body = split_transcript_document(doc)
    if body.lstrip().startswith("### "):
        body = flatten_sectioned_body(body)
    return head, marker, body

def apply_manual_asr_substitutions(
    text: str,
    replacements: Sequence[tuple[str, str]],
) -> tuple[str, int]:
    """Apply ordered substring replacements; return (text, groups_applied)."""
    count = 0
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
            count += 1
    return text, count

def patch_manual_asr_frontmatter(
    head: str,
    *,
    subs: int,
    manual_asr_spot_fix: str,
    pass_date: str | None = None,
) -> str:
    """Add ``manual_asr_spot_fix`` YAML and receipt tails on first manual ASR ship."""
    today = pass_date or date.today().isoformat()
    note_tail = f" · manual ASR spot-fix {today}"
    if "manual_asr_spot_fix:" not in head:
        head = head.replace(
            "\n---\n",
            f'\nmanual_asr_spot_fix: "{manual_asr_spot_fix}"\n---\n',
            1,
        )
    if re.search(r"^source_note:", head, flags=re.M):
        if note_tail.strip() not in head:
            head = re.sub(
                r'^(source_note: ")(.*?)(")\s*$',
                rf"\1\2{note_tail}\3",
                head,
                count=1,
                flags=re.M,
            )
    receipt = (
        f"Manual ASR spot-fix {today} ({subs} substitution groups); "
        "AI-assisted source-clean"
    )
    if re.search(r"^editorial_note:", head, flags=re.M):
        head = re.sub(
            r'^editorial_note: ".*?"\s*$',
            f'editorial_note: "{receipt} · not human-verified verbatim; verify before quotation."',
            head,
            count=1,
            flags=re.M,
        )
    return head

def append_resection_editorial_note(head: str, resection_note: str) -> str:
    """Append or replace dated ``source-section re-section pass`` editorial tail."""
    if not re.search(r"^editorial_note:", head, flags=re.M):
        return head
    head = re.sub(
        r" · source-section re-section pass \d{4}-\d{2}-\d{2} \([^)]+\)",
        "",
        head,
    )
    if resection_note in head:
        return head
    return re.sub(
        r'^(editorial_note: ")(.*?)("\s*$)',
        rf"\1\2{resection_note}\3",
        head,
        count=1,
        flags=re.M,
    )

def finalize_patch_head(path: Path, *, resection_note: str) -> None:
    """Apply patch-specific re-section receipt to frontmatter after body ship."""
    doc = path.read_text(encoding="utf-8")
    head, marker, body = split_transcript_document(doc)
    head = append_resection_editorial_note(head, resection_note)
    path.write_text(f"{head}{marker}\n\n{body.strip()}\n", encoding="utf-8", newline="\n")

def prepare_section_patch_body(
    doc: str,
    *,
    manual_asr: Sequence[tuple[str, str]],
    interview_host: str | None = None,
    interview_guest: str | None = None,
) -> tuple[str, str, str]:
    """Flat body + manual ASR + optional speaker-label restore for anchor validation."""
    head, marker, body = flat_body_from_doc(doc)
    body, _ = apply_manual_asr_substitutions(body.strip(), manual_asr)
    if (
        interview_host
        and interview_guest
        and capture_has_speaker_labels(body, host=interview_host, guest=interview_guest)
    ):
        body = restore_turn_markers_from_speaker_labels(
            body,
            host=interview_host,
            guest=interview_guest,
        )
    return head, marker, body

def validate_section_anchors(
    body: str,
    section_titles: Sequence[str],
    section_anchors: Sequence[str],
) -> list[str]:
    errors: list[str] = []
    if len(section_titles) != len(section_anchors) + 1:
        errors.append(
            f"title/anchor count mismatch: {len(section_titles)} titles, "
            f"{len(section_anchors)} anchors"
        )
    cursor = 0
    for anchor in section_anchors:
        try:
            pos = find_anchor_pos(body, anchor, cursor)
            cursor = pos + 1
        except ValueError as exc:
            errors.append(str(exc))
    return errors

def write_interview_section_patch_capture(
    path: Path,
    section_titles: Sequence[str],
    section_anchors: Sequence[str],
    *,
    manual_asr: Sequence[tuple[str, str]],
    manual_asr_spot_fix: str,
    resection_note: str,
    interview_host: str,
    interview_guest: str,
) -> int:
    """Manual ASR + ``write_sectioned_capture`` interview pipeline + re-section receipt."""
    doc = path.read_text(encoding="utf-8")
    head, marker, body = flat_body_from_doc(doc)
    body, asr_subs = apply_manual_asr_substitutions(body.strip(), manual_asr)
    if "manual_asr_spot_fix:" not in head and asr_subs:
        head = patch_manual_asr_frontmatter(
            head,
            subs=asr_subs,
            manual_asr_spot_fix=manual_asr_spot_fix,
        )
    path.write_text(f"{head}{marker}\n\n{body}\n", encoding="utf-8", newline="\n")
    write_sectioned_capture(
        path,
        section_titles,
        section_anchors,
        resection=True,
        reject_if_sectioned=False,
        interview_host=interview_host,
        interview_guest=interview_guest,
    )
    finalize_patch_head(path, resection_note=resection_note)
    return asr_subs

def parse_interview_speaker_names(head: str) -> tuple[str | None, str | None]:
    """Read ``host:`` / ``guest:`` from capture frontmatter when present."""
    meta = parse_capture_eligibility_meta(head)
    host = meta.get("host")
    guest = meta.get("guest")
    if host and guest:
        return host, guest
    return None, None

def capture_has_speaker_labels(body: str, *, host: str, guest: str) -> bool:
    return f"**{host}:**" in body or f"**{guest}:**" in body

def append_interview_speaker_label_receipt(
    head: str,
    *,
    turns: int,
    host: str,
    guest: str,
) -> str:
    today = date.today().isoformat()
    host_short = host.split()[0] if host else "Host"
    guest_short = guest.split()[0] if guest else "Guest"
    note = (
        f" · interview speaker-label pass {today} "
        f"({turns} turns; {host_short}/{guest_short} >> markers)"
    )
    if note in head:
        return head
    head = re.sub(
        r" · interview speaker-label pass \d{4}-\d{2}-\d{2} \(\d+ turns; [^)]+\)",
        "",
        head,
    )
    if re.search(r"^editorial_note:", head, flags=re.M):
        return re.sub(
            r'^(editorial_note: ")(.*?)("\s*$)',
            rf"\1\2{note}\3",
            head,
            count=1,
            flags=re.M,
        )
    if re.search(r"^source_note:", head, flags=re.M):
        return re.sub(
            r'^(source_note: ")(.*?)("\s*$)',
            rf"\1\2{note}\3",
            head,
            count=1,
            flags=re.M,
        )
    return head.replace(
        "\n---\n",
        f'\neditorial_note: "Interview speaker labels.{note.strip()}"\n---\n',
        1,
    )

def apply_interview_section_body(
    body: str,
    section_titles: Sequence[str],
    section_anchors: Sequence[str],
    *,
    host: str,
    guest: str,
    asr_cleanup_fn: Callable[[str], str] | None = None,
    anchor_slice: slice | None = None,
    speaker_cleanup_fn: Callable[[str], str] | None = None,
) -> tuple[str, int]:
    """Insert sections, repair section-boundary ``>>``, label turns, optional legacy cleanup."""
    body = body.strip()
    if asr_cleanup_fn:
        body = asr_cleanup_fn(body)
    if capture_has_speaker_labels(body, host=host, guest=guest):
        body = restore_turn_markers_from_speaker_labels(body, host=host, guest=guest)
    body = insert_sections(
        body,
        section_titles,
        section_anchors,
        anchor_slice=anchor_slice,
    )
    body = inject_section_open_turn_markers(body)
    if capture_has_speaker_labels(body, host=host, guest=guest):
        body = restore_turn_markers_from_speaker_labels(body, host=host, guest=guest)
        body = inject_section_open_turn_markers(body)
    body, turns_labeled = apply_interview_turn_speaker_labels(
        body,
        host=host,
        guest=guest,
    )
    if speaker_cleanup_fn:
        body = speaker_cleanup_fn(body)
    return body, turns_labeled

def apply_solo_section_body(
    body: str,
    section_titles: Sequence[str],
    section_anchors: Sequence[str],
    *,
    asr_cleanup_fn: Callable[[str], str] | None = None,
    anchor_slice: slice | None = None,
    speaker_cleanup_fn: Callable[[str], str] | None = None,
    paragraph_reflow: bool = True,
    target_para_words: int = 80,
    soft_max_para_words: int = 120,
    hard_max_para_words: int = 150,
) -> str:
    body = body.strip()
    body = insert_sections(
        body,
        section_titles,
        section_anchors,
        asr_cleanup_fn=asr_cleanup_fn,
        anchor_slice=anchor_slice,
    )
    if paragraph_reflow:
        body = reflow_section_paragraphs(
            body,
            target_para_words=target_para_words,
            soft_max_para_words=soft_max_para_words,
            hard_max_para_words=hard_max_para_words,
        )
    if speaker_cleanup_fn:
        body = speaker_cleanup_fn(body)
    return body

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
    resection: bool = False,
    interview_host: str | None = None,
    interview_guest: str | None = None,
    body_marker: str | None = None,
    paragraph_reflow: bool = True,
    target_para_words: int = 80,
    soft_max_para_words: int = 120,
    hard_max_para_words: int = 150,
) -> None:
    doc = capture_path.read_text(encoding="utf-8")
    marker = body_marker or detect_body_marker(doc)
    if marker not in doc:
        raise ValueError(f"missing body marker: {marker!r}")

    head, body = doc.split(marker, 1)
    meta = parse_capture_eligibility_meta(head)
    if not is_source_section_eligible(meta):
        raise ValueError(
            "source-section applies to YouTube channel transcripts (solo/interview) only; "
            "authored texts (Substack, newsletter, article) are out of scope"
        )
    body = body.strip()
    if body.lstrip().startswith("### "):
        if reject_if_sectioned and not resection:
            raise ValueError("transcript already sectioned")
        if resection:
            body = flatten_sectioned_body(body)

    fm_host, fm_guest = parse_interview_speaker_names(head)
    host = interview_host or fm_host
    guest = interview_guest or fm_guest
    is_interview = (meta.get("source_form") or "").lower() == "interview"
    if interview_host and interview_guest:
        is_interview = True
    if is_interview and (not host or not guest):
        raise ValueError(
            "interview sectioning requires host and guest names "
            "(frontmatter host:/guest: or interview_host=/interview_guest=)"
        )

    head = mark_sectioned_frontmatter(head, section_count=len(section_titles))
    turns_labeled = 0
    if is_interview:
        body, turns_labeled = apply_interview_section_body(
            body,
            section_titles,
            section_anchors,
            host=host,
            guest=guest,
            asr_cleanup_fn=asr_cleanup_fn,
            anchor_slice=anchor_slice,
            speaker_cleanup_fn=speaker_cleanup_fn,
        )
        if turns_labeled:
            head = append_interview_speaker_label_receipt(
                head,
                turns=turns_labeled,
                host=host,
                guest=guest,
            )
        if paragraph_reflow:
            body = reflow_section_paragraphs(
                body,
                target_para_words=target_para_words,
                soft_max_para_words=soft_max_para_words,
                hard_max_para_words=hard_max_para_words,
            )
    else:
        body = apply_solo_section_body(
            body,
            section_titles,
            section_anchors,
            asr_cleanup_fn=asr_cleanup_fn,
            anchor_slice=anchor_slice,
            speaker_cleanup_fn=speaker_cleanup_fn,
            paragraph_reflow=paragraph_reflow,
            target_para_words=target_para_words,
            soft_max_para_words=soft_max_para_words,
            hard_max_para_words=hard_max_para_words,
        )

    doc = f"{head}{marker}\n\n{body}\n"
    capture_path.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {capture_path} "
        f"({len(body.split()):,} words, {len(section_titles)} sections"
        f"{f', {turns_labeled} turns labeled' if turns_labeled else ''})"
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
