"""Tests for scripts/transcript_section_curation.py."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    apply_interview_turn_speaker_labels,
    detect_body_marker,
    inject_dialogue_works_missing_turn_markers,
    insert_sections,
    mark_sectioned_frontmatter,
    normalize_for_anchor,
    reflow_section_paragraphs,
    split_sentences,
    split_transcript_document,
    count_words,
    pack_sentences_into_paragraphs,
)


def test_insert_sections_splits_on_anchors_and_last_runs_to_eof():
    body = "Open line. First anchor section one. Second anchor section two tail."
    out = insert_sections(
        body,
        ["Open", "One", "Two"],
        ["first anchor", "second anchor"],
    )
    assert out.startswith("### Open\n\nOpen line.")
    assert "### One\n\nFirst anchor section one." in out
    assert "### Two\n\nSecond anchor section two tail." in out


def test_insert_sections_applies_asr_cleanup_before_split():
    body = "Start. Professor Dieng speaks. Next anchor part."
    out = insert_sections(
        body,
        ["A", "B"],
        ["next anchor"],
        asr_cleanup_fn=lambda t: t.replace("Professor Dieng", "Professor Jiang"),
    )
    assert "Professor Jiang speaks" in out
    assert "Professor Dieng" not in out


def test_normalize_for_anchor_unicode_punctuation():
    assert normalize_for_anchor("Let's — go") == "let's - go"


def test_detect_body_marker_statecraft_transcript():
    doc = "---\ntitle: x\n---\n\n## Transcript\n\nHello."
    assert detect_body_marker(doc) == "## Transcript\n"


def test_detect_body_marker_cleaned_transcript():
    doc = "---\ntitle: x\n---\n\n## Cleaned Transcript\n\nHello."
    assert detect_body_marker(doc) == "## Cleaned Transcript\n"


def test_split_transcript_document_cleaned_transcript():
    doc = "---\n---\n\n## Cleaned Transcript\n\nBody here."
    head, marker, body = split_transcript_document(doc)
    assert marker == "## Cleaned Transcript\n"
    assert body.strip() == "Body here."


def test_split_transcript_document():
    doc = "---\n---\n\n## Transcript\n\nBody here."
    head, marker, body = split_transcript_document(doc)
    assert marker == "## Transcript\n"
    assert body.strip() == "Body here."


def test_mark_sectioned_frontmatter_adds_curation_field():
    head = "---\ntitle: test\nsource_note: \"landed\"\n---\n\n"
    out = mark_sectioned_frontmatter(head, section_count=3)
    assert "transcript_curation: curated_sectioned" in out
    assert "source-section pass" in out
    assert "(3 sections)" in out


def _word_tokens(text: str) -> list[str]:
    import re

    return re.findall(r"\b\w+\b", text)


def _body_tokens_excluding_headings(text: str) -> list[str]:
    import re

    stripped = re.sub(r"^### .+$", "", text, flags=re.M)
    return re.findall(r"\b\w+\b", stripped)


def test_reflow_runon_monologue_creates_paragraph_breaks():
    sentences = [
        "Good day. Today is Saturday.",
        "Now, over the last week we have had threats.",
        "Anyway, Belarus did not take kindly to these threats.",
    ]
    runon = " ".join(sentences * 20)
    body = f"### Show Open — Test\n\n{runon}"
    out = reflow_section_paragraphs(body, hard_max_para_words=40)
    chunk = out.split("### Show Open — Test\n\n", 1)[1]
    assert "\n\n" in chunk
    assert count_words(out) == count_words(body)


def test_reflow_preserves_word_tokens():
    body = (
        "### One — Topic\n\n"
        "First sentence here. Second sentence follows. "
        "Now, a third sentence opens a pivot. Fourth wraps up the block."
    )
    out = reflow_section_paragraphs(body, soft_max_para_words=8, hard_max_para_words=12)
    assert _word_tokens(body) == _word_tokens(out)


def test_reflow_idempotent_when_already_paragraphed():
    body = "### One — Topic\n\nShort opener.\n\nAnother short block."
    once = reflow_section_paragraphs(body)
    twice = reflow_section_paragraphs(once)
    assert once == twice


def test_reflow_preserves_interview_speaker_and_turn_markers():
    body = (
        "### Interview — Open\n\n"
        "**Host:** What do you think?\n\n"
        ">> Guest reply here. It continues for a bit.\n\n"
        "**Guest:** And another turn."
    )
    out = reflow_section_paragraphs(body, soft_max_para_words=5, hard_max_para_words=10)
    assert "**Host:** What do you think?" in out
    assert out.count(">>") >= 1
    assert "**Guest:**" in out
    assert _word_tokens(body) == _word_tokens(out)


def test_insert_sections_plus_reflow_keeps_headings_and_words():
    body = "Open. First anchor middle text. Second anchor tail text."
    sectioned = insert_sections(body, ["A", "B", "C"], ["first anchor", "second anchor"])
    reflowed = reflow_section_paragraphs(sectioned, soft_max_para_words=3, hard_max_para_words=5)
    assert "### A" in reflowed
    assert "### B" in reflowed
    assert "### C" in reflowed
    assert _body_tokens_excluding_headings(sectioned) == _body_tokens_excluding_headings(reflowed)


def test_split_sentences_respects_u_s_abbreviation():
    text = "Strikes hit U.S. bases. Now, Iran responds."
    sents = split_sentences(text)
    assert len(sents) == 2
    assert sents[0].startswith("Strikes hit U.S.")


def test_pack_sentences_prefers_discourse_pivot_break():
    sentences = ["Alpha one two three four five six seven."] + [
        "Now, pivot sentence one two three four five six seven eight nine."
    ] * 3
    paras = pack_sentences_into_paragraphs(
        sentences,
        target_para_words=10,
        soft_max_para_words=15,
        hard_max_para_words=20,
    )
    assert len(paras) >= 2
    assert any(p.strip().startswith("Now,") for p in paras[1:])


def test_inject_dialogue_works_missing_turn_marker_before_host_cue():
    raw = (
        ">> I I think they're out of Jordan. Iran will know where they came from. "
        "My understanding today, Larry, there are reports from Iran."
    )
    injected = inject_dialogue_works_missing_turn_markers(raw)
    assert " >> My understanding today, Larry" in injected


def test_apply_interview_labels_splits_merged_strike_origins_turn():
    raw = (
        ">> I I think I think they're probably coming out of Jordan. "
        "Iran's going to know where they came from. "
        "My understanding today, Larry, there's some reports coming from Iran. "
        ">> Yeah, they've already they already responded uh and hit Bahrain."
    )
    labeled, n = apply_interview_turn_speaker_labels(raw)
    assert n == 3
    assert "**Larry Johnson:** I I think I think" in labeled
    assert "**Nima Alkhorshid (host):** My understanding today, Larry" in labeled
    assert "**Nima Alkhorshid (host):** Yeah, they've already" in labeled
    assert ">>" not in labeled
