from repo_io import ARTIFACTS_DIR
"""Shared helpers for repo-owned derived regeneration."""

from __future__ import annotations

import fnmatch
import json
import shlex
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RECEIPT_DIR = ARTIFACTS_DIR / "work-dev" / "rebuild-receipts"
RATIONALE_SCHEMA_ID = "schemas/registry/derived-artifact-rationale.v1.json"
RATIONALE_SCHEMA_VERSION = "1.0.0-derived-artifact-rationale"
RATIONALE_SIDECAR_SUFFIX = ".derived-rationale.json"

@dataclass(frozen=True)
class RebuildTarget:
    target_id: str
    description: str
    producer_script: str
    policy_mode: str
    rationale: str
    watch_patterns: tuple[str, ...]
    command_templates: tuple[tuple[str, ...], ...]
    outputs: tuple[str, ...]
    depends_on: tuple[str, ...] = ()
    human_review_required: bool = False
    owned_output_patterns: tuple[str, ...] = ()

    def commands_for_user(self, user: str) -> list[list[str]]:
        return [
            [part.format(user=user) for part in template]
            for template in self.command_templates
        ]

    def outputs_for_user(self, user: str) -> list[str]:
        return [part.format(user=user) for part in self.outputs]

    def owned_output_patterns_for_user(self, user: str) -> list[str]:
        patterns = self.owned_output_patterns or self.outputs
        return [part.format(user=user) for part in patterns]

TARGETS: tuple[RebuildTarget, ...] = (
    RebuildTarget(
        target_id="derived-regeneration-manifest",
        description="Machine-readable manifest of repo-owned derived rebuild targets",
        producer_script="scripts/build_derived_regeneration_manifest.py",
        policy_mode="Rebuild",
        rationale="Capture the current rebuild target registry in one inspectable manifest so incremental regeneration stays explicit and bounded.",
        watch_patterns=(
            "scripts/derived_regeneration.py",
            "scripts/build_derived_regeneration_manifest.py",
            "docs/skill-work/work-dev/derived-regeneration.md",
        ),
        command_templates=(("python3", "scripts/build_derived_regeneration_manifest.py"),),
        outputs=("runtime/artifacts/work-dev/derived-regeneration-manifest.json",),
    ),
    RebuildTarget(
        target_id="rebuild-health-summary",
        description="Derived health summary of repo-owned rebuild receipts",
        producer_script="scripts/report_rebuild_health.py",
        policy_mode="Surface",
        rationale="Summarize receipt-backed derived rebuild activity so the health summary stays inspectable without touching canonical sources.",
        watch_patterns=(
            "runtime/artifacts/work-dev/rebuild-receipts/**",
            "runtime/artifacts/work-dev/derived-regeneration-manifest.json",
            "scripts/report_rebuild_health.py",
        ),
        command_templates=(("python3", "scripts/report_rebuild_health.py"),),
        outputs=("runtime/artifacts/work-dev/rebuild-health/summary.json",),
        depends_on=("derived-regeneration-manifest",),
    ),
    RebuildTarget(
        target_id="repo-surgeon",
        description="Structural health report for operator maintenance triage",
        producer_script="scripts/repo_surgeon.py",
        policy_mode="Rebuild",
        rationale="Aggregate layout, path adoption, skill, link, and portability checks into an advisory runtime report without replacing individual validators.",
        watch_patterns=(
            "docs/**",
            "skills/**",
            "statecraft/**",
            "scripts/assert_root_folder_layout.py",
            "scripts/check_repo_path_adoption.py",
            "scripts/validate_skills.py",
            "scripts/repo_surgeon.py",
            "scripts/operator_report_utils.py",
            "runtime/artifacts/repo-surgeon/README.md",
        ),
        command_templates=(
            (
                "python3",
                "scripts/repo_surgeon.py",
                "--out",
                "runtime/artifacts/repo-surgeon/latest.md",
                "--json-out",
                "runtime/artifacts/repo-surgeon/latest.json",
                "--run-existing-checks",
            ),
        ),
        outputs=(
            "runtime/artifacts/repo-surgeon/latest.md",
            "runtime/artifacts/repo-surgeon/latest.json",
        ),
    ),
    RebuildTarget(
        target_id="statecraft-war-room",
        description="Advisory rollup of live statecraft objects from intake, daily synthesis, and transaction router",
        producer_script="scripts/statecraft_war_room.py",
        policy_mode="Rebuild",
        rationale="Aggregate intake queue, daily synthesis, sidecars, and transaction-router fit into a read-only operator dashboard without replacing SSOT surfaces.",
        watch_patterns=(
            "statecraft/synthesis/**",
            "statecraft/notes/wire/**",
            "source-archive/statecraft/**",
            "runtime/artifacts/statecraft-intake-queue/**",
            "statecraft/sheets/transaction-router.md",
            "scripts/statecraft_war_room.py",
            "runtime/artifacts/statecraft-war-room/README.md",
        ),
        command_templates=(
            (
                "python3",
                "scripts/statecraft_war_room.py",
                "--out",
                "runtime/artifacts/statecraft-war-room/latest.md",
                "--json-out",
                "runtime/artifacts/statecraft-war-room/latest.json",
                "--latest-days",
                "7",
                "--max-objects",
                "12",
            ),
        ),
        outputs=(
            "runtime/artifacts/statecraft-war-room/latest.md",
            "runtime/artifacts/statecraft-war-room/latest.json",
        ),
    ),
    RebuildTarget(
        target_id="operator-command-deck",
        description="Repo-wide what-next cockpit aggregating Surgeon, War Room, git, and backlog signals",
        producer_script="scripts/operator_command_deck.py",
        policy_mode="Rebuild",
        rationale="Rank advisory next actions from upstream dashboard producers and lightweight operator receipts without replacing harness warmup or handoff paste paths.",
        watch_patterns=(
            "runtime/artifacts/repo-surgeon/latest.json",
            "runtime/artifacts/statecraft-war-room/latest.json",
            "skills/skill-candidates.md",
            "runtime/prepared-context/last-budget-builds.json",
            "runtime/artifacts/review-packets/**",
            "recursion-gate.md",
            "archive/grace-mar-instance/recursion-gate.md",
            "scripts/operator_command_deck.py",
            "scripts/repo_surgeon.py",
            "scripts/statecraft_war_room.py",
            "runtime/artifacts/operator-command-deck/README.md",
        ),
        command_templates=(
            (
                "python3",
                "scripts/operator_command_deck.py",
                "--out",
                "runtime/artifacts/operator-command-deck/latest.md",
                "--json-out",
                "runtime/artifacts/operator-command-deck/latest.json",
                "--max-next-actions",
                "5",
            ),
        ),
        outputs=(
            "runtime/artifacts/operator-command-deck/latest.md",
            "runtime/artifacts/operator-command-deck/latest.json",
        ),
    ),
    RebuildTarget(
        target_id="operator-dashboard",
        description="Umbrella index stitching Repo Surgeon, War Room, and Command Deck outputs",
        producer_script="scripts/operator_dashboard.py",
        policy_mode="Rebuild",
        rationale="One-shot full regen of the three aggregators plus a stitched operator cockpit index without replacing individual bucket producers.",
        watch_patterns=(
            "runtime/artifacts/repo-surgeon/latest.json",
            "runtime/artifacts/statecraft-war-room/latest.json",
            "runtime/artifacts/operator-command-deck/latest.json",
            "scripts/operator_dashboard.py",
            "runtime/artifacts/operator-dashboard/README.md",
        ),
        command_templates=(
            ("python3", "scripts/operator_dashboard.py"),
        ),
        outputs=(
            "runtime/artifacts/operator-dashboard/latest.md",
            "runtime/artifacts/operator-dashboard/latest.json",
        ),
        depends_on=("repo-surgeon", "statecraft-war-room", "operator-command-deck"),
    ),
    # library-index target retired — see continuity/README.md § Operator books
    RebuildTarget(
        target_id="work-lanes-dashboard-json",
        description="work-lane JSON aggregate for lane dashboards",
        producer_script="scripts/build_work_lanes_dashboard.py",
        policy_mode="Rebuild",
        rationale="Aggregate lane telemetry into a machine-readable feed that downstream operator dashboards can rebuild from without touching Record files.",
        watch_patterns=(
            "runtime/artifacts/work-dev/work-dev-status-summary.json",
            "runtime/artifacts/work-strategy/strategy-observability.json",
            "runtime/artifacts/work-cadence/cadence-pressure-report.json",
            "scripts/build_work_lanes_dashboard.py",
        ),
        command_templates=(("python3", "scripts/build_work_lanes_dashboard.py"),),
        outputs=("runtime/artifacts/work-lanes-dashboard.json",),
    ),
    RebuildTarget(
        target_id="lane-dashboards",
        description="Markdown lane dashboard derived from runtime observations and JSON feeds",
        producer_script="scripts/build_lane_dashboards.py",
        policy_mode="Surface",
        rationale="Compose runtime observations and work-lane telemetry into a derived operator dashboard for navigation across active lanes.",
        watch_patterns=(
            "runtime/observations/**",
            "runtime/artifacts/work-lanes-dashboard.json",
            "runtime/artifacts/handoffs/**",
            "runtime/prepared-context/last-budget-builds.json",
            "scripts/build_lane_dashboards.py",
            "scripts/build_work_lanes_dashboard.py",
        ),
        command_templates=(
            ("python3", "scripts/build_work_lanes_dashboard.py"),
            ("python3", "scripts/build_lane_dashboards.py"),
        ),
        outputs=("runtime/artifacts/lane-dashboards/README.md",),
        depends_on=("work-lanes-dashboard-json",),
    ),
    RebuildTarget(
        target_id="review-dashboard",
        description="Review dashboard derived from recursion-gate",
        producer_script="scripts/build_review_dashboard.py",
        policy_mode="Surface",
        rationale="Provide a compact operator view of pending and recently processed gate candidates while keeping recursion-gate.md authoritative.",
        watch_patterns=(
            "recursion-gate.md",
            "scripts/build_review_dashboard.py",
        ),
        command_templates=(("python3", "scripts/build_review_dashboard.py"),),
        outputs=("runtime/artifacts/review-dashboard.md",),
    ),
    RebuildTarget(
        target_id="gate-board",
        description="Kanban-style gate board derived from recursion-gate",
        producer_script="scripts/build_gate_board.py",
        policy_mode="Surface",
        rationale="Translate gate candidate state into a dashboard board for operator triage without changing candidate status or merge authority.",
        watch_patterns=(
            "recursion-gate.md",
            "scripts/build_gate_board.py",
        ),
        command_templates=(("python3", "scripts/build_gate_board.py"),),
        outputs=("runtime/artifacts/gate-board.md",),
    ),
    RebuildTarget(
        target_id="governance-posture",
        description="Governance posture one-pager derived from audit-facing user files",
        producer_script="scripts/report_governance_posture.py",
        policy_mode="Surface",
        rationale="Summarize governance posture and audit paths in a derived one-pager for operator or partner review.",
        watch_patterns=(
            "self.md",
            "self-archive.md",
            "self-evidence.md",
            "recursion-gate.md",
            "merge-receipts.jsonl",
            "pipeline-events.jsonl",
            "harness-events.jsonl",
            "session-log.md",
            "scripts/report_governance_posture.py",
            "docs/skill-work/work-dev/safety-story-ux.md",
            "docs/runtime-vs-record.md",
        ),
        command_templates=(
            ("python3", "scripts/report_governance_posture.py", "-u", "{user}"),
        ),
        outputs=("runtime/artifacts/governance-posture.md",),
        human_review_required=True,
    ),
    RebuildTarget(
        target_id="strategy-notebook-graph",
        description="Strategy-notebook graph and derived views",
        producer_script="scripts/build_strategy_notebook_graph.py",
        policy_mode="Strategy",
        rationale="Project markdown-canonical strategy notebook structure into derived graph views for orientation, clustering, and navigation.",
        watch_patterns=(
            "docs/skill-work/work-strategy/strategy-notebook/**",
            "scripts/build_strategy_notebook_graph.py",
        ),
        command_templates=(("python3", "scripts/build_strategy_notebook_graph.py"),),
        outputs=(
            "runtime/artifacts/work-strategy/strategy-notebook/graph.json",
            "runtime/artifacts/work-strategy/strategy-notebook/views/watch-clusters.json",
            "runtime/artifacts/work-strategy/strategy-notebook/views/expert-convergence.json",
        ),
    ),
    RebuildTarget(
        target_id="work-dev-compound-autoresearch",
        description="Work-dev compound and Autoresearch operator summaries",
        producer_script="scripts/build_work_dev_compound_dashboard.py",
        policy_mode="Surface",
        rationale="Rebuild work-dev compound dashboards and exports when compound notes or Autoresearch run notes change, keeping research scaffolding inspectable without Record authority.",
        watch_patterns=(
            "docs/skill-work/work-dev/compound-notes/**",
            "docs/skill-work/work-dev/autoresearch-runs/**",
            "scripts/work_dev_compound_refresh.py",
            "scripts/export_work_dev_compound_gate_candidates.py",
            "scripts/build_work_dev_compound_dashboard.py",
            "scripts/work_dev/compound_notes.py",
        ),
        command_templates=(
            ("python3", "scripts/work_dev_compound_refresh.py"),
            ("python3", "scripts/export_work_dev_compound_gate_candidates.py"),
            ("python3", "scripts/build_work_dev_compound_dashboard.py"),
        ),
        outputs=(
            "runtime/artifacts/work-dev-compound-refresh.md",
            "runtime/artifacts/work-dev-compound-gate-candidates.md",
            "runtime/artifacts/work-dev-compound-dashboard.md",
        ),
    ),
    RebuildTarget(
        target_id="decision-ledger-summary",
        description="Derived summary of WORK-only operator decisions",
        producer_script="scripts/build_decision_ledger_summary.py",
        policy_mode="Surface",
        rationale="Summarize durable work-dev operator decisions for quick recovery while keeping the decision ledger itself as the non-canonical source.",
        watch_patterns=(
            "docs/skill-work/work-dev/decision-ledger.md",
            "scripts/build_decision_ledger_summary.py",
        ),
        command_templates=(("python3", "scripts/build_decision_ledger_summary.py"),),
        outputs=("runtime/artifacts/work-dev/decision-ledger-summary.md",),
    ),
)

TARGETS_BY_ID = {target.target_id: target for target in TARGETS}

def normalize_rel_path(path: str) -> str:
    return Path(path).as_posix().lstrip("./")

def detect_git_changed_paths(repo_root: Path = REPO_ROOT) -> list[str]:
    """Return repo-relative changed paths from the current worktree."""
    proc = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []

    changed: set[str] = set()
    for raw_line in proc.stdout.splitlines():
        if not raw_line:
            continue
        path_part = raw_line[3:]
        if " -> " in path_part:
            path_part = path_part.split(" -> ", 1)[1]
        changed.add(normalize_rel_path(path_part))
    return sorted(changed)

def path_matches_target(path: str, target: RebuildTarget) -> bool:
    rel = normalize_rel_path(path)
    return any(fnmatch.fnmatch(rel, pattern) for pattern in target.watch_patterns)

def select_targets_for_paths(paths: list[str]) -> list[RebuildTarget]:
    rel_paths = [normalize_rel_path(path) for path in paths]
    selected: list[RebuildTarget] = []
    for target in TARGETS:
        if any(path_matches_target(path, target) for path in rel_paths):
            selected.append(target)
    return selected

def expand_with_downstream(selected_targets: list[RebuildTarget]) -> list[RebuildTarget]:
    """Include downstream targets that depend on any selected target."""
    selected_ids = {target.target_id for target in selected_targets}
    changed = True
    while changed:
        changed = False
        for target in TARGETS:
            if target.target_id in selected_ids:
                continue
            if any(dep in selected_ids for dep in target.depends_on):
                selected_ids.add(target.target_id)
                changed = True
    return [TARGETS_BY_ID[target_id] for target_id in selected_ids]

def topologically_sort_targets(selected_targets: list[RebuildTarget]) -> list[RebuildTarget]:
    """Sort selected targets so upstream dependencies run first."""
    selected_ids = {target.target_id for target in selected_targets}
    remaining = {target.target_id: set(target.depends_on) & selected_ids for target in selected_targets}
    ordered: list[RebuildTarget] = []

    while remaining:
        ready = sorted(target_id for target_id, deps in remaining.items() if not deps)
        if not ready:
            unresolved = ", ".join(sorted(remaining.keys()))
            raise ValueError(f"cyclic derived regeneration dependencies: {unresolved}")
        for target_id in ready:
            ordered.append(TARGETS_BY_ID[target_id])
            remaining.pop(target_id)
            for deps in remaining.values():
                deps.discard(target_id)

    return ordered

def matched_paths_for_target(paths: list[str], target: RebuildTarget) -> list[str]:
    return [
        normalize_rel_path(path)
        for path in paths
        if path_matches_target(path, target)
    ]

def sidecar_path_for_artifact(artifact_path: str) -> str:
    return f"{normalize_rel_path(artifact_path)}{RATIONALE_SIDECAR_SUFFIX}"

def build_rebuild_command(target: RebuildTarget, user: str) -> str:
    commands = target.commands_for_user(user)
    return " && ".join(" ".join(shlex.quote(part) for part in command) for command in commands)

def build_rationale_payload(
    *,
    target: RebuildTarget,
    user: str,
    artifact_path: str,
    generated_at: str,
    matched_paths: list[str],
) -> dict:
    inputs = matched_paths or [normalize_rel_path(path) for path in target.watch_patterns]
    payload: dict[str, object] = {
        "$schema": RATIONALE_SCHEMA_ID,
        "schemaVersion": RATIONALE_SCHEMA_VERSION,
        "producer_script": target.producer_script,
        "policy_mode": target.policy_mode,
        "generated_at": generated_at,
        "artifact_path": normalize_rel_path(artifact_path),
        "canonical_surfaces_touched": False,
        "rebuild_command": build_rebuild_command(target, user),
        "inputs": inputs,
        "rationale": target.rationale,
        "human_review_required": target.human_review_required,
    }
    return payload

def cleanup_owned_outputs(repo_root: Path, *, target: RebuildTarget, user: str) -> list[str]:
    cleaned: list[str] = []
    for pattern in target.owned_output_patterns_for_user(user):
        rel_pattern = normalize_rel_path(pattern)
        if not any(char in rel_pattern for char in "*?[]"):
            continue
        for path in sorted(repo_root.glob(rel_pattern)):
            if path.name == ".gitkeep" or not path.is_file():
                continue
            path.unlink()
            cleaned.append(normalize_rel_path(path.relative_to(repo_root).as_posix()))
            sidecar_path = repo_root / sidecar_path_for_artifact(path.relative_to(repo_root).as_posix())
            if sidecar_path.is_file():
                sidecar_path.unlink()
                cleaned.append(normalize_rel_path(sidecar_path.relative_to(repo_root).as_posix()))
    return cleaned

def build_manifest_payload() -> dict:
    """Machine-readable manifest for current derived regeneration targets."""
    return {
        "schemaVersion": "1.0.0-derived-regeneration-manifest",
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "recordAuthority": "none",
        "gateEffect": "none",
        "targets": [
            {
                "targetId": target.target_id,
                "description": target.description,
                "producerScript": target.producer_script,
                "policyMode": target.policy_mode,
                "humanReviewRequired": target.human_review_required,
                "watchPatterns": list(target.watch_patterns),
                "commands": [" ".join(cmd) for cmd in target.command_templates],
                "outputs": list(target.outputs),
                "rationaleSidecars": [sidecar_path_for_artifact(output) for output in target.outputs],
                "dependsOn": list(target.depends_on),
                "ownedOutputPatterns": list(target.owned_output_patterns or target.outputs),
            }
            for target in TARGETS
        ],
    }

def default_receipt_path(
    *,
    receipt_prefix: str = "derived-rebuild",
    receipt_dir: Path = DEFAULT_RECEIPT_DIR,
    now: datetime | None = None,
) -> Path:
    ts = now or datetime.now(timezone.utc)
    stamp = ts.strftime("%Y%m%d-%H%M%S")
    return receipt_dir / f"{receipt_prefix}-{stamp}.json"

def write_receipt(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
