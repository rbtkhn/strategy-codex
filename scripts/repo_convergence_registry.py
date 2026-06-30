"""Declarative loop registry for repo-wide convergence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from check_transaction_term_usage import TIER1_DOCS, TIER2_SKILLS

LoopKind = Literal["validator", "builder", "hybrid", "gate_reporter"]


@dataclass(frozen=True)
class LoopSpec:
    kind: LoopKind
    inputs: tuple[str, ...]
    commands: tuple[tuple[str, ...], ...]
    writes: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    description: str = ""


def _membrane_inputs() -> tuple[str, ...]:
    """Scheduling triggers mapped to membrane validator watch lists."""
    # trigger: check_membrane_policy_light.GOVERNED_SCAN_*
    governed = (
        "docs/work-membrane-v2.md",
        "docs/harness-architecture-map.md",
        "docs/runtime-vs-record.md",
        "docs/intelligence-harness.md",
        "statecraft/work-membrane.md",
        "singularity/work-membrane.md",
        "statecraft/synthesis/day",
        "statecraft/research/bridges",
        "runtime/runtime-complements",
    )
    # trigger: check_transaction_term_usage.TIER1_DOCS + TIER2_SKILLS
    transaction = tuple(TIER1_DOCS) + tuple(TIER2_SKILLS)
    # trigger: check_work_record_doctrine.iter_scan_roots
    work_record = (
        "statecraft",
        "docs",
        "continuity",
        "scripts",
        "skills",
        ".cursor",
        "README.md",
        "AGENTS.md",
        "contributing.md",
    )
    # trigger: check_record_surface_retirement.SCAN_ROOTS + ROOT_FILES
    record_retirement = (
        "docs",
        ".cursor",
        "statecraft",
        "singularity",
        "continuity",
        "continuity/README.md",
        "research",
        "skills",
        "library",
        "README.md",
        "AGENTS.md",
        "LLM-ROUTING.md",
        "memory.md",
        "repo-map.yaml",
    )
    seen: set[str] = set()
    ordered: list[str] = []
    for group in (governed, transaction, work_record, record_retirement):
        for path in group:
            if path not in seen:
                seen.add(path)
                ordered.append(path)
    return tuple(ordered)


LOOPS: dict[str, LoopSpec] = {
    "routing": LoopSpec(
        kind="validator",
        description="Repo routing pins, front doors, and path strictness",
        inputs=(
            "README.md",
            "LLM-ROUTING.md",
            "repo-map.yaml",
            "docs/start-here.md",
            "docs/canonical-paths.md",
            "docs/root-directory-map.md",
        ),
        commands=(
            ("scripts/validate_repo_routing.py",),
            ("scripts/check_routing_front_doors.py",),
            ("scripts/check_repo_path_strict.py", "--strict"),
        ),
    ),
    "membrane": LoopSpec(
        kind="validator",
        description="Work/Record membrane, transaction term law, Record surface retirement",
        inputs=_membrane_inputs(),
        commands=(
            ("scripts/check_membrane_policy_light.py",),
            ("scripts/check_work_record_doctrine.py",),
            ("scripts/check_transaction_term_usage.py", "--strict", "--skills-strict"),
            ("scripts/check_record_surface_retirement.py",),
        ),
    ),
    "statecraft_predictions": LoopSpec(
        kind="builder",
        description="Prediction registry, metrics, disagreement, and timeline artifacts",
        inputs=(
            "statecraft/notes/predictions",
            "statecraft/data/event-registry.json",
            "schemas/registry",
        ),
        commands=(
            ("scripts/validate_all_schemas.py", "--scope", "prediction"),
            ("scripts/check_event_integrity.py",),
            ("scripts/build_prediction_registry.py",),
            ("scripts/check_prediction_registry.py",),
            ("scripts/build_prediction_metrics.py",),
            ("scripts/check_prediction_metrics.py",),
            ("scripts/build_prediction_disagreement.py",),
            ("scripts/check_prediction_disagreement.py",),
            ("scripts/build_prediction_timeline.py",),
            ("scripts/check_prediction_timeline.py",),
        ),
        writes=(
            "runtime/artifacts/prediction-registry.json",
            "runtime/artifacts/prediction-metrics.json",
            "runtime/artifacts/prediction-disagreement.json",
            "runtime/artifacts/prediction-timeline.json",
        ),
    ),
    "statecraft_notes": LoopSpec(
        kind="validator",
        description="Statecraft notes gate (warn + changed Tier A strict)",
        inputs=(
            "statecraft/notes",
            "statecraft/synthesis",
            "statecraft/data/event-registry.json",
        ),
        depends_on=("statecraft_predictions",),
        commands=(
            ("scripts/check_statecraft_notes.py", "--warn"),
            (
                "scripts/check_statecraft_notes.py",
                "--strict",
                "--changed-only",
                "--tier-a-only",
            ),
        ),
    ),
    "generated_surfaces": LoopSpec(
        kind="validator",
        description="Generated manifest drift and prediction artifact freshness",
        inputs=(
            "generated-manifest.yaml",
            "runtime/artifacts",
        ),
        depends_on=("statecraft_predictions",),
        commands=(
            ("scripts/check_generated_surfaces.py", "--check", "--strict"),
            ("scripts/check_generated_prediction_artifacts.py",),
        ),
    ),
    "essay_surfaces": LoopSpec(
        kind="validator",
        description="Essay and prose duplication boundaries",
        inputs=(
            "essays",
            "statecraft/notes",
            "singularity/notes",
            "docs/prose-index.md",
        ),
        commands=(("scripts/check_doc_duplication.py",),),
    ),
    "schema": LoopSpec(
        kind="validator",
        description="Structured schema validation across registry surfaces",
        inputs=(
            "schemas",
            "generated-manifest.yaml",
            "pyproject.toml",
            ".pre-commit-config.yaml",
        ),
        commands=(("scripts/validate_all_schemas.py",),),
    ),
    "continuity_layer": LoopSpec(
        kind="validator",
        description=(
            "Continuity layer status, word counts, contract ownership, "
            "encoding hygiene, and derived report"
        ),
        inputs=(
            "continuity",
            "codex/README.md",
            "scripts/audit_continuity_rename.py",
            "scripts/check_text_encoding_hygiene.py",
            "scripts/check_continuity_status.py",
            "scripts/check_continuity_contract_index.py",
            "scripts/build_continuity_report.py",
            "scripts/strategy/update_strategy_notebook_word_counts.py",
        ),
        commands=(
            ("scripts/audit_continuity_rename.py", "--strict"),
            ("scripts/check_text_encoding_hygiene.py", "--scope", "continuity", "--warn"),
            ("scripts/check_continuity_status.py",),
            ("scripts/check_continuity_contract_index.py",),
        ),
    ),
}
