"""Regression checks for conductor documentation links."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

CONDUCTOR_DOCS = (
    "AGENTS.md",
    ".cursor/skills/coffee/SKILL.md",
    ".cursor/skills/conductor/SKILL.md",
    ".cursor/skills/dream/SKILL.md",
    ".cursor/skills/skill-strategy/SKILL.md",
    "docs/operator-skills.md",
    "docs/skill-work/work-cadence/work-cadence-events.md",
    "docs/skill-work/work-coffee/CONDUCTOR-PASS.md",
    "docs/skill-work/work-dev/dev-notebook/README.md",
    "docs/skill-work/work-dev/dev-notebook/work-dev/journal/README.md",
)

REMOVED_STRATEGY_NOTEBOOK_TARGETS = (
    "docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md",
    "docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md",
    "work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md",
    "work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md",
)

LIVE_CONDUCTOR_TARGETS = (
    "codex/CONDUCTOR-IMPROVEMENT-LOOP.md",
    "codex/CONDUCTOR-CLOSE-TEMPLATE.md",
)


def test_conductor_docs_do_not_reference_removed_strategy_notebook_targets() -> None:
    offenders: list[str] = []
    for doc in CONDUCTOR_DOCS:
        text = (REPO_ROOT / doc).read_text(encoding="utf-8")
        for target in REMOVED_STRATEGY_NOTEBOOK_TARGETS:
            if target in text:
                offenders.append(f"{doc}: {target}")

    assert not offenders, "removed conductor strategy-notebook links found:\n" + "\n".join(
        offenders
    )


def test_live_conductor_targets_exist() -> None:
    missing = [target for target in LIVE_CONDUCTOR_TARGETS if not (REPO_ROOT / target).is_file()]

    assert not missing, "missing live conductor target(s): " + ", ".join(missing)


def test_conductor_loop_wires_coffee_pick_to_dream_rollup_contract() -> None:
    loop = (REPO_ROOT / "codex/CONDUCTOR-IMPROVEMENT-LOOP.md").read_text(encoding="utf-8")
    coffee = (REPO_ROOT / ".cursor/skills/coffee/SKILL.md").read_text(encoding="utf-8")
    dream = (REPO_ROOT / ".cursor/skills/dream/SKILL.md").read_text(encoding="utf-8")

    assert "Coffee / dream contract" in loop
    assert "picked=conductor conductor=<slug>" in loop
    assert "conductor_rollup_24h" in loop
    assert "Coffee -> dream conductor handoff" in coffee
    assert "orientation-only" in coffee
    assert "completed_passes" in dream
    assert "orientation_only" in dream


def test_conductor_loop_ssot_prefers_new_name_only_cadence_shape() -> None:
    loop = (REPO_ROOT / "codex/CONDUCTOR-IMPROVEMENT-LOOP.md").read_text(encoding="utf-8")

    assert "picked=conductor" in loop
    assert "picked=E conductor=slug" not in loop
    assert "coffee` hub **E**" not in loop


def test_conductor_action_menu_requires_partial_arc_state() -> None:
    skill = (REPO_ROOT / ".cursor/skills/conductor/SKILL.md").read_text(encoding="utf-8")
    protocol = (REPO_ROOT / "docs/skill-work/work-coffee/CONDUCTOR-PASS.md").read_text(
        encoding="utf-8"
    )

    for text in (skill, protocol):
        assert "Complete -" in text
        assert "Open -" in text
        assert "Parked -" in text
        assert "D / Finale is not required for every useful arc" in text or (
            "Finale is a lifecycle close" in text
        )


def test_conductor_action_menu_requires_option_quality_gate() -> None:
    skill = (REPO_ROOT / ".cursor/skills/conductor/SKILL.md").read_text(encoding="utf-8")
    protocol = (REPO_ROOT / "docs/skill-work/work-coffee/CONDUCTOR-PASS.md").read_text(
        encoding="utf-8"
    )

    for text in (skill, protocol):
        assert "Option quality" in text
        assert "distinct" in text
        assert "lifecycle" in text
        assert "interchangeable" in text
