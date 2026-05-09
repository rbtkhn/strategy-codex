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


def _kleiber_section() -> str:
    return _section("## Kleiber conductor voice prototype", "## When to read this")


def _karajan_section() -> str:
    return _section("## Karajan conductor voice prototype", "## Kleiber conductor voice prototype")


def _bernstein_section() -> str:
    return _section("## Bernstein rehearsal voice prototype", "## Karajan conductor voice prototype")


def test_kleiber_voice_is_scoped_to_kleiber() -> None:
    section = _kleiber_section()

    assert "This prototype applies only when resolved `conductor=kleiber`" in section
    assert "It does not change `toscanini`, `furtwangler`, `karajan`, or `bernstein` behavior" in section
    assert "not companion Voice" in section
    assert "not Record authority" in section


def test_kleiber_contract_requires_short_witty_hotspot_orientation() -> None:
    section = _kleiber_section()

    required_phrases = [
        "1-3 sentence orientation",
        "first-person conductor mask",
        "witty precision",
        "exact correction",
        "playful self-awareness",
        "light irreverence",
        "Locate the one live hotspot",
        "falsify fast, and stop",
        "Conductor action MCQ",
    ]
    for phrase in required_phrases:
        assert phrase in section


def test_kleiber_musicology_is_kinetic_and_alive() -> None:
    section = _kleiber_section()

    for term in (
        "movement",
        "danger",
        "sudden starts",
        "cars",
        "theater",
        "physical character",
        "odd everyday images",
        "spring",
        "timing",
        "rehearsal cues",
    ):
        assert term in section

    assert "Kleiber = kinetic character, spring, danger, theatrical timing, local aliveness" in section
    assert 'Kleiber asks: "Where is it not alive yet?"' in section
    assert "Kleiber makes the next action alive" in section
    assert "Kleiber failure mode: whimsy without falsification" in section


def test_kleiber_is_distinct_from_bernstein_and_karajan() -> None:
    section = _kleiber_section()
    bernstein = _bernstein_section()
    karajan = _karajan_section()

    assert "Bernstein = musical meaning, syntax, drama, transformation, felt stakes" in section
    assert "Karajan = total form, continuity, sonority, hierarchy, finish" in section
    assert "Kleiber = kinetic character, spring, danger, theatrical timing, local aliveness" in section
    assert "3-5 sentence orientation" in bernstein
    assert "2-4 sentence orientation" in karajan
    assert "1-3 sentence orientation" not in bernstein
    assert "1-3 sentence orientation" not in karajan


def test_kleiber_guardrails_reject_caricature_and_evasive_whimsy() -> None:
    section = _kleiber_section()

    guardrails = [
        "Do not imitate accent, ethnicity, private biography, speech tics, or exact historical persona",
        "Do not invent quotes or lean on specific cultural references as costume",
        "No whimsy without falsification",
        "Avoid heavy literary allusion in v1",
        "the four A-D movement choices must remain concrete",
    ]
    for phrase in guardrails:
        assert phrase in section


def test_kleiber_examples_pin_three_contexts_and_four_movement_options() -> None:
    section = _kleiber_section()

    assert "**Technical/code example**" in section
    assert "**Documentation/governance example**" in section
    assert "**Strategy/workflow example**" in section
    assert section.count("**Conductor action MCQ - Reply A-D for this `kleiber` pass**") == 3
    assert section.count("\nA. Allegro: ") == 3
    assert section.count("\nB. Andante: ") == 3
    assert section.count("\nC. Scherzo: ") == 3
    assert section.count("\nD. Finale: ") == 3


def test_concise_non_voice_rows_remain_unchanged() -> None:
    text = _conductor_text()

    assert "| **toscanini** | Verify the seam, pin the receipt, and force the claim back to the evidence" in text
    assert "| **furtwangler** | Hold the tension open, resist false closure" in text
    assert "| **kleiber** | Pick one hotspot, falsify it fast" in text
    assert "| **karajan** | Shape the long arc so the whole line lands cleanly" in text
    assert "| **bernstein** | Make the stake legible in one line" in text
