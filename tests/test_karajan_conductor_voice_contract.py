from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONDUCTOR_SKILL = REPO_ROOT / ".cursor" / "skills" / "conductor" / "SKILL.md"


def _conductor_text() -> str:
    return CONDUCTOR_SKILL.read_text(encoding="utf-8")


def _section(heading: str, next_heading: str) -> str:
    text = _conductor_text()
    start = text.index(heading)
    end = text.index(next_heading, start)
    return text[start:end]


def _karajan_section() -> str:
    return _section("## Karajan conductor voice prototype", "## Kleiber conductor voice prototype")


def _bernstein_section() -> str:
    return _section("## Bernstein rehearsal voice prototype", "## Karajan conductor voice prototype")


def test_karajan_voice_is_scoped_to_karajan() -> None:
    section = _karajan_section()

    assert "This prototype applies only when resolved `conductor=karajan`" in section
    assert "It does not change `toscanini`, `furtwangler`, `kleiber`, or `bernstein` behavior" in section
    assert "not companion Voice" in section
    assert "not Record authority" in section


def test_karajan_contract_requires_controlled_conductor_orientation() -> None:
    section = _karajan_section()

    required_phrases = [
        "2-4 sentence orientation",
        "first-person conductor mask",
        "controlled authority",
        "concise elegance",
        "technical focus",
        "direct ensemble address",
        "Use \"we\" sparingly and purposefully",
        "one operator-facing next action",
        "the next decision",
        "Conductor action MCQ",
    ]
    for phrase in required_phrases:
        assert phrase in section


def test_karajan_musicology_is_sound_architecture_and_specificity() -> None:
    section = _karajan_section()

    for term in (
        "line",
        "balance",
        "architecture",
        "rhythm",
        "texture",
        "blend",
        "proportion",
        "silence",
        "finish",
        "control",
        "continuity",
        "sonority",
        "hierarchy",
        "long arc",
    ):
        assert term in section

    assert "If the work is mechanical, state the operational point plainly" in section
    assert "Karajan failure mode: elegance without specificity" in section
    assert "Avoid ornamental grandeur" in section


def test_karajan_is_distinct_from_bernstein_function() -> None:
    section = _karajan_section()
    bernstein = _bernstein_section()

    assert "Bernstein = music as argument, language, drama, transformation, discovery" in section
    assert "Karajan = music as controlled total form, continuity, sonority, hierarchy, finish" in section
    assert 'Bernstein asks: "What is the stake?"' in section
    assert 'Karajan asks: "What shape must the whole work have?"' in section
    assert "Bernstein makes the next action meaningful" in section
    assert "Karajan makes the next action inevitable" in section
    assert "3-5 sentence orientation" in bernstein
    assert "2-4 sentence orientation" not in bernstein


def test_karajan_guardrails_reject_biographical_caricature() -> None:
    section = _karajan_section()

    guardrails = [
        "Borrow the conducting lens, not accent, ethnicity, speech tics, fake quotes, or biographical imitation",
        "Do not claim exact historical authenticity",
        "every sensory or architectural metaphor must sharpen operational judgment",
        "Do not let Karajan become Bernstein in darker colors",
    ]
    for phrase in guardrails:
        assert phrase in section


def test_karajan_examples_pin_three_contexts_and_four_movement_options() -> None:
    section = _karajan_section()

    assert "**Technical/code example**" in section
    assert "**Documentation/governance example**" in section
    assert "**Strategy/workflow example**" in section
    assert section.count("**Conductor action MCQ - Reply A-D for this `karajan` pass**") == 3
    assert section.count("\nA. Allegro: ") == 3
    assert section.count("\nB. Andante: ") == 3
    assert section.count("\nC. Scherzo: ") == 3
    assert section.count("\nD. Finale: ") == 3


def test_non_prototype_conductor_shape_hints_remain_concise() -> None:
    text = _conductor_text()

    unchanged_rows = {
        "toscanini": "Verify the seam, pin the receipt, and force the claim back to the archive/placeholders/evidence",
        "furtwangler": "Hold the tension open, resist false closure",
        "kleiber": "Pick one hotspot, falsify it fast",
    }
    for slug, phrase in unchanged_rows.items():
        assert f"| **{slug}** | {phrase}" in text

    assert "| **karajan** | Shape the long arc so the whole line lands cleanly" in text
    assert "| **bernstein** | Make the stake legible in one line" in text
