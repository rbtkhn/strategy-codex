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


def _toscanini_section() -> str:
    return _section("## Toscanini conductor voice prototype", "## Furtwangler conductor voice prototype")


def _furtwangler_section() -> str:
    return _section("## Furtwangler conductor voice prototype", "## Bernstein rehearsal voice prototype")


def _bernstein_section() -> str:
    return _section("## Bernstein rehearsal voice prototype", "## Karajan conductor voice prototype")


def _karajan_section() -> str:
    return _section("## Karajan conductor voice prototype", "## Kleiber conductor voice prototype")


def _kleiber_section() -> str:
    return _section("## Kleiber conductor voice prototype", "## When to read this")


def test_toscanini_voice_is_scoped_to_toscanini() -> None:
    section = _toscanini_section()

    assert "This prototype applies only when resolved `conductor=toscanini`" in section
    assert "It does not change `furtwangler`, `karajan`, `kleiber`, or `bernstein` behavior" in section
    assert "not companion Voice" in section
    assert "not Record authority" in section


def test_toscanini_contract_requires_fierce_receipt_orientation() -> None:
    section = _toscanini_section()

    required_phrases = [
        "1-3 sentence orientation",
        "first-person conductor mask",
        "fierce precision",
        "blunt urgency",
        "score-centered discipline",
        "professional uncompromising standards",
        "Force the claim back to evidence",
        "exact receipt",
        "one operator-facing next action",
        "without a decision",
        "Conductor action MCQ",
    ]
    for phrase in required_phrases:
        assert phrase in section


def test_toscanini_musicology_is_score_as_evidence() -> None:
    section = _toscanini_section()

    for term in (
        "score",
        "source",
        "receipt",
        "seam",
        "marking",
        "tempo discipline",
        "fidelity",
        "exactness",
        "proof",
        "contradiction",
        "stale fact",
        "`last30days`",
    ):
        assert term in section

    assert "Toscanini = score as evidence, fidelity, tempo discipline, markings, exactness, no loose claims" in section
    assert 'Toscanini asks: "Where is it written, and does the execution obey it?"' in section
    assert "Toscanini makes the next action accountable" in section
    assert "Toscanini failure mode: heat without receipt" in section


def test_toscanini_is_distinct_from_other_prototypes() -> None:
    section = _toscanini_section()
    bernstein = _bernstein_section()
    karajan = _karajan_section()
    kleiber = _kleiber_section()

    assert "Bernstein = musical meaning, syntax, drama, transformation, felt stakes" in section
    assert "Karajan = total form, continuity, sonority, hierarchy, finish" in section
    assert "Kleiber = kinetic character, spring, danger, theatrical timing, local aliveness" in section
    assert "3-5 sentence orientation" in bernstein
    assert "2-4 sentence orientation" in karajan
    assert "1-3 sentence orientation" in kleiber
    assert "score as evidence" not in bernstein
    assert "score as evidence" not in karajan
    assert "score as evidence" not in kleiber


def test_toscanini_guardrails_reject_abusive_caricature() -> None:
    section = _toscanini_section()

    guardrails = [
        "Heat without abuse",
        "no insults, curses, humiliation, personal attacks",
        "fake Italianisms",
        "accent imitation",
        "ethnicity markers",
        "invented quotes",
        "Do not claim literal historical authenticity",
        "intensity must become specificity",
        "repo evidence or human authority",
    ]
    for phrase in guardrails:
        assert phrase in section


def test_toscanini_examples_pin_three_contexts_and_four_movement_options() -> None:
    section = _toscanini_section()

    assert "**Technical/code example**" in section
    assert "**Documentation/governance example**" in section
    assert "**Strategy/workflow example**" in section
    assert section.count("**Conductor action MCQ - Reply A-D for this `toscanini` pass**") == 3
    assert section.count("\nA. Allegro: ") == 3
    assert section.count("\nB. Andante: ") == 3
    assert section.count("\nC. Scherzo: ") == 3
    assert section.count("\nD. Finale: ") == 3


def test_all_five_voice_prototypes_are_present_and_rows_remain() -> None:
    text = _conductor_text()

    assert "## Toscanini conductor voice prototype" in text
    assert "## Furtwangler conductor voice prototype" in text
    assert "## Bernstein rehearsal voice prototype" in text
    assert "## Karajan conductor voice prototype" in text
    assert "## Kleiber conductor voice prototype" in text
    assert "| **furtwangler** | Hold the tension open, resist false closure" in text
    assert "| **toscanini** | Verify the seam, pin the receipt, and force the claim back to the evidence" in text
