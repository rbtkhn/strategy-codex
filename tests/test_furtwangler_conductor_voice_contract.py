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


def test_furtwangler_voice_is_scoped_to_furtwangler() -> None:
    section = _furtwangler_section()

    assert "This prototype applies only when resolved `conductor=furtwangler`" in section
    assert "It does not change `toscanini`, `karajan`, `kleiber`, or `bernstein` behavior" in section
    assert "not companion Voice" in section
    assert "not Record authority" in section


def test_furtwangler_contract_requires_tension_aware_orientation() -> None:
    section = _furtwangler_section()

    required_phrases = [
        "2-4 sentence orientation",
        "first-person conductor mask",
        "grave",
        "reflective",
        "tension-aware",
        "patient with unresolved structure",
        "Preserve the living tension",
        "If the work is not ready to resolve",
        "one operator-facing next action",
        "decline premature resolution",
        "Conductor action MCQ",
    ]
    for phrase in required_phrases:
        assert phrase in section


def test_furtwangler_musicology_is_living_tension() -> None:
    section = _furtwangler_section()

    for term in (
        "breath",
        "pressure",
        "suspension",
        "undertow",
        "long preparation",
        "inner necessity",
        "instability",
        "conflict",
        "delayed resolution",
        "living form",
    ):
        assert term in section

    assert "Furtwangler = living tension, organic time, contradiction, historical pressure, delayed resolution" in section
    assert 'Furtwangler asks: "What conflict must remain open before we decide?"' in section
    assert "Furtwangler makes the next action patient" in section
    assert "Furtwangler failure mode: mistaking vagueness for depth" in section


def test_furtwangler_is_distinct_from_other_prototypes() -> None:
    section = _furtwangler_section()
    toscanini = _toscanini_section()
    bernstein = _bernstein_section()
    karajan = _karajan_section()
    kleiber = _kleiber_section()

    assert "Toscanini = score as evidence, fidelity, tempo discipline, markings, exactness, no loose claims" in section
    assert "Bernstein = musical meaning, syntax, drama, transformation, felt stakes" in section
    assert "Karajan = total form, continuity, sonority, hierarchy, finish" in section
    assert "Kleiber = kinetic character, spring, danger, theatrical timing, local aliveness" in section
    assert "score as archive/placeholders/evidence" in toscanini
    assert "3-5 sentence orientation" in bernstein
    assert "2-4 sentence orientation" in karajan
    assert "1-3 sentence orientation" in kleiber
    assert "living tension" not in toscanini
    assert "living tension" not in bernstein
    assert "living tension" not in karajan
    assert "living tension" not in kleiber


def test_furtwangler_guardrails_reject_vague_depth_and_false_closure() -> None:
    section = _furtwangler_section()

    guardrails = [
        "Do not imitate accent, ethnicity, private biography, ideology, speech tics, invented quotes, or exact historical persona",
        "Do not use \"depth\" language to avoid action",
        "Do not romanticize ambiguity",
        "If evidence decides the issue, let Toscanini win",
        "the function is unresolved tension before synthesis",
        "The A-D movement menu must remain concrete",
    ]
    for phrase in guardrails:
        assert phrase in section


def test_furtwangler_examples_pin_three_contexts_and_four_movement_options() -> None:
    section = _furtwangler_section()

    assert "**Technical/code example**" in section
    assert "**Documentation/governance example**" in section
    assert "**Strategy/workflow example**" in section
    assert section.count("**Conductor action MCQ - Reply A-D for this `furtwangler` pass**") == 3
    assert section.count("\nA. Allegro: ") == 3
    assert section.count("\nB. Andante: ") == 3
    assert section.count("\nC. Scherzo: ") == 3
    assert section.count("\nD. Finale: ") == 3


def test_all_five_voice_prototypes_are_present_with_stable_rows() -> None:
    text = _conductor_text()

    for heading in (
        "## Toscanini conductor voice prototype",
        "## Furtwangler conductor voice prototype",
        "## Bernstein rehearsal voice prototype",
        "## Karajan conductor voice prototype",
        "## Kleiber conductor voice prototype",
    ):
        assert heading in text

    assert "| **toscanini** | Verify the seam, pin the receipt, and force the claim back to the archive/placeholders/evidence" in text
    assert "| **furtwangler** | Hold the tension open, resist false closure" in text
    assert "| **karajan** | Shape the long arc so the whole line lands cleanly" in text
    assert "| **kleiber** | Pick one hotspot, falsify it fast" in text
    assert "| **bernstein** | Make the stake legible in one line" in text
