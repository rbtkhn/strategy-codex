from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONDUCTOR_SKILL = REPO_ROOT / ".cursor" / "skills" / "conductor" / "SKILL.md"

def _conductor_text() -> str:
    return CONDUCTOR_SKILL.read_text(encoding="utf-8")

def _bernstein_section() -> str:
    text = _conductor_text()
    start = text.index("## Bernstein rehearsal voice prototype")
    end_marker = "## Karajan conductor voice prototype"
    end = text.index(end_marker, start) if end_marker in text[start:] else text.index("## When to read this", start)
    return text[start:end]

def test_bernstein_rehearsal_voice_is_scoped_to_bernstein() -> None:
    section = _bernstein_section()

    assert "This prototype applies only when resolved `conductor=bernstein`" in section
    assert "It does not change `toscanini`, `furtwangler`, `karajan`, or `kleiber` behavior" in section
    assert "not companion Voice" in section
    assert "not Record authority" in section

def test_bernstein_contract_requires_rehearsal_orientation_before_action_menu() -> None:
    section = _bernstein_section()

    required_phrases = [
        "3-5 sentence orientation",
        "framed first person",
        '"we" and direct listening language preferred',
        "Make the stakes vivid before action",
        "one operator-facing next action",
        "do not stop at making the stakes vivid",
        "Conductor action MCQ",
    ]
    for phrase in required_phrases:
        assert phrase in section

def test_bernstein_musicology_is_clarity_first_not_caricature() -> None:
    section = _bernstein_section()

    for term in (
        "motif",
        "cadence",
        "counterpoint",
        "orchestration",
        "voicing",
        "dissonance",
        "resolution",
        "syntax",
        "transformation",
        "ambiguity",
        "deep structure",
        "harmonic function",
    ):
        assert term in section

    assert "Clarity wins over metaphor" in section
    assert "Do not imitate accent" in section
    assert "Do not invent quotations" in section
    assert "Do not use music language as decoration" in section
    assert "state it plainly" in section

def test_bernstein_examples_pin_three_contexts_and_four_movement_options() -> None:
    section = _bernstein_section()

    assert "**Technical/code example**" in section
    assert "**Documentation/governance example**" in section
    assert "**Strategy/workflow example**" in section
    assert section.count('**Conductor action MCQ - Reply A-D for this `bernstein` pass**') == 3
    assert section.count("\nA. Allegro: ") == 3
    assert section.count("\nB. Andante: ") == 3
    assert section.count("\nC. Scherzo: ") == 3
    assert section.count("\nD. Finale: ") == 3

def test_other_conductor_shape_hints_remain_concise() -> None:
    text = _conductor_text()

    unchanged_rows = {
        "toscanini": "Verify the seam, pin the receipt, and force the claim back to the archive/placeholders/evidence",
        "furtwangler": "Hold the tension open, resist false closure",
        "karajan": "Shape the long arc so the whole line lands cleanly",
        "kleiber": "Pick one hotspot, falsify it fast",
    }
    for slug, phrase in unchanged_rows.items():
        assert f"| **{slug}** | {phrase}" in text

    bernstein_row = "| **bernstein** | Make the stake legible in one line"
    assert bernstein_row in text
