"""Tests for scripts/transcript_section_curation.py."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    _guess_dialogue_works_host,
    apply_interview_turn_speaker_labels,
    detect_body_marker,
    inject_dialogue_works_missing_turn_markers,
    inject_section_open_turn_markers,
    insert_sections,
    mark_sectioned_frontmatter,
    normalize_dialogue_works_host_label_suffix,
    normalize_for_anchor,
    reflow_section_paragraphs,
    split_sentences,
    split_transcript_document,
    count_words,
    pack_sentences_into_paragraphs,
    write_sectioned_capture,
    flatten_sectioned_body,
    apply_interview_section_body,
    apply_manual_asr_substitutions,
    validate_section_anchors,
    write_interview_section_patch_capture,
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


def test_reflow_splits_long_labeled_speaker_turn():
    runon = (
        "**Ray McGovern:** First sentence here with enough words. "
        "Second sentence follows with more words. "
        "Now, a third sentence opens a pivot. "
        "Fourth wraps the block with additional words."
    )
    body = f"### One — Topic\n\n{runon}"
    out = reflow_section_paragraphs(body, soft_max_para_words=8, hard_max_para_words=12)
    chunk = out.split("### One — Topic\n\n", 1)[1]
    assert chunk.startswith("**Ray McGovern:**")
    assert chunk.count("\n\n") >= 1
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
    assert ">> My understanding today, Larry" in injected


def test_inject_section_open_turn_marker_for_johnson_guest_opener():
    body = (
        "### Military Theater — Test\n\n"
        "I mean, let's just last night's attacks were what I call military political theater."
    )
    out = inject_section_open_turn_markers(body)
    assert ">> I mean, let's just last night's attacks" in out


def test_inject_section_open_turn_marker_for_guest_opener():
    body = (
        "### Forked Tongue — Test\n\n"
        "Nima these are really good questions. Now uh in a jocular mood."
    )
    out = inject_section_open_turn_markers(body)
    assert ">> Nima these are really good questions" in out


def test_guest_opener_guess_mcgovern_forked_tongue():
    assert _guess_dialogue_works_host("Nima these are really good questions.") is False
    assert _guess_dialogue_works_host("Yeah. The question is Rey, is the United States") is True


def test_apply_interview_section_body_section_boundary_guest_opener():
    body = (
        "Host asks a long question about the strait and what do you make of it right now? "
        ">> Nima these are really good questions. Now uh in a jocular mood I would simply say that uh "
        "Rubio had courage. >> Yeah. My understanding is that Iran has doesn't feel that they're in a rush."
    )
    out, turns = apply_interview_section_body(
        body,
        ["Open", "Forked Tongue", "Strait Control"],
        [
            "Nima these are really good questions.",
            "Yeah. My understanding is that Iran has doesn't feel that they're in a rush",
        ],
        host="Nima Alkhorshid",
        guest="Ray McGovern",
    )
    assert "### Forked Tongue" in out
    assert "**Ray McGovern:** Nima these are really good questions." in out
    assert "**Nima Alkhorshid:** Yeah. My understanding" in out
    assert turns >= 2


def test_write_sectioned_capture_interview_reflow_after_labels():
    work = ROOT / ".codex-tmp" / "pytest-section-curation"
    work.mkdir(parents=True, exist_ok=True)
    capture = work / "interview.md"
    capture.write_text(
        "---\nsource_form: interview\nhost: Nima Alkhorshid\nguest: Ray McGovern\n"
        "source_type: youtube\n---\n# Title\n\n## Transcript\n\n"
        "Hi everybody welcome. >> Thank you Nima for inviting me. >> "
        "Nima these are really good questions. Now uh in a jocular mood I would simply say that uh "
        "Rubio visited Bahrain. >> Yeah. My understanding is that Iran has doesn't feel that they're in a rush.\n",
        encoding="utf-8",
    )
    write_sectioned_capture(
        capture,
        ["Open", "Forked Tongue", "Strait Control"],
        [
            "Nima these are really good questions.",
            "Yeah. My understanding is that Iran has doesn't feel that they're in a rush",
        ],
    )
    text = capture.read_text(encoding="utf-8")
    assert "transcript_curation: curated_sectioned" in text
    assert "**Ray McGovern:** Nima these are really good questions." in text
    assert "interview speaker-label pass" in text
    assert ">>" not in text.split("## Transcript", 1)[1]
    capture.unlink(missing_ok=True)


def test_write_sectioned_capture_resection_flattens_existing():
    work = ROOT / ".codex-tmp" / "pytest-section-curation"
    work.mkdir(parents=True, exist_ok=True)
    capture = work / "solo.md"
    capture.write_text(
        "---\nsource_form: solo\nsource_type: youtube\n---\n# Title\n\n## Transcript\n\n"
        "### One — First\n\nAlpha sentence here. >> Beta follows.\n\n"
        "### Two — Second\n\nGamma closes the transcript body now.\n",
        encoding="utf-8",
    )
    write_sectioned_capture(
        capture,
        ["First Block", "Second Block"],
        ["Gamma closes"],
        resection=True,
        reject_if_sectioned=False,
    )
    text = capture.read_text(encoding="utf-8")
    assert "### First Block" in text
    assert "### Second Block" in text
    assert "### One — First" not in text
    capture.unlink(missing_ok=True)


def test_flatten_sectioned_body_drops_headings():
    body = "### One — A\n\nLine one.\n\n### Two — B\n\nLine two."
    flat = flatten_sectioned_body(body)
    assert "###" not in flat
    assert "Line one." in flat and "Line two." in flat


def test_normalize_dialogue_works_host_label_suffix():
    raw = (
        "**Nima Alkhorshid (host):** Hi.\n\n"
        "**Nima (host):** Next.\n\n"
        "**Nima Alkorshid (host):** Typo."
    )
    out = normalize_dialogue_works_host_label_suffix(raw)
    assert "(host)" not in out
    assert out.count("**Nima Alkhorshid:**") == 3


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
    assert "**Nima Alkhorshid:** My understanding today, Larry" in labeled
    assert "**Nima Alkhorshid:** Yeah, they've already" in labeled
    assert ">>" not in labeled


def test_apply_manual_asr_substitutions_counts_groups():
    text, n = apply_manual_asr_substitutions(
        "Baharin and Strait of form",
        [("Baharin", "Bahrain"), ("Strait of form", "Strait of Hormuz")],
    )
    assert n == 2
    assert "Bahrain" in text and "Strait of Hormuz" in text


def test_validate_section_anchors_reports_missing():
    body = "Open. First anchor here. Second anchor tail."
    errs = validate_section_anchors(
        body,
        ["Open", "One", "Two"],
        ["first anchor", "missing anchor"],
    )
    assert len(errs) == 1
    assert "missing anchor" in errs[0].lower() or "not found" in errs[0].lower()


def test_write_interview_section_patch_capture_sections_and_receipt():
    work = ROOT / ".codex-tmp" / "pytest-section-curation"
    work.mkdir(parents=True, exist_ok=True)
    capture = work / "patch-interview.md"
    capture.write_text(
        "---\nsource_form: interview\nhost: Nima Alkhorshid\nguest: Ray McGovern\n"
        "source_type: youtube\n---\n# Title\n\n## Transcript\n\n"
        "Hi everybody welcome. >> Thank you Nima for inviting me. >> "
        "Nima these are really good questions. Now uh in a jocular mood. >> "
        "Yeah. My understanding is that Iran has doesn't feel that they're in a rush.\n",
        encoding="utf-8",
    )
    resection_note = " · source-section re-section pass 2026-06-28 (test arc)"
    subs = write_interview_section_patch_capture(
        capture,
        ["Open", "Forked Tongue", "Strait Control"],
        [
            "Nima these are really good questions.",
            "Yeah. My understanding is that Iran has doesn't feel that they're in a rush",
        ],
        manual_asr=[("jocular mood", "jocular mood")],
        manual_asr_spot_fix="test spot-fix",
        resection_note=resection_note,
        interview_host="Nima Alkhorshid",
        interview_guest="Ray McGovern",
    )
    text = capture.read_text(encoding="utf-8")
    assert subs >= 0
    assert "### Open" in text
    assert resection_note in text
    assert "**Ray McGovern:** Nima these are really good questions." in text
    capture.unlink(missing_ok=True)
