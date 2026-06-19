# Repository artifacts (derived)

This tree holds **rebuildable, non-canonical** outputs from operator scripts. Nothing here is **Record truth**; recovery always points back to source files under ``, `docs/`, `skills/`, etc.

**Operator surface taxonomy:** Generated and operator-facing paths are classified in [docs/operator-surface-registry.md](../docs/operator-surface-registry.md). New dashboard-like artifacts should be registered there (and satisfy the **dashboard anti-sprawl policy** there) before being treated as part of the stable operator interface.

**Staleness:** Artifacts are often **generated snapshots**. If a file has **no** generation time or **unclear** source declaration, treat freshness as **unknown** or **possibly stale** and **verify** against the governing source files (e.g. ``, gate file) before relying on it for load-bearing operator decisions. Convention and levels: [docs/operator-surface-staleness.md](../docs/operator-surface-staleness.md).

**Structured-file validation:** Parses committed JSON under `runtime/artifacts/` (skipping very large blobs), `schemas/registry/`, and workflow examples; validates `pyproject.toml`, `.pre-commit-config.yaml` when PyYAML is available; checks critical relative links in operator/workflow READMEs. Does not change doctrine.

```bash
python scripts/validate_structured_files.py
```

Primary doctrine stays **derived / rebuildable / non-canonical**. If you use `shadow layer` as an informal metaphor for these outputs, treat it as a glossary aid only, not a replacement term. It is **not** the same thing as `shadow-merges`, `shadow autonomy`, or any implied “shadow Record”.

**Important distinction:** the portable-record schema [`schemas/registry/artifact-rationale.v1.json`](../schemas/registry/artifact-rationale.v1.json) is about **demonstrated capability rationale** alongside EVIDENCE. It is **not** the schema for everything under `/runtime/artifacts/`.

Repo-owned derived regeneration may also emit per-artifact rebuild sidecars such as
`runtime/artifacts/library-index.md.derived-rationale.json`. Those sidecars follow
[`schemas/registry/derived-artifact-rationale.v1.json`](../schemas/registry/derived-artifact-rationale.v1.json)
and describe **how to rebuild a derived file**, not why an EVIDENCE artifact was good.

**Repo root `runtime/prepared-context/`** (not under `runtime/artifacts/`) may hold operator drafts and `last-budget-builds.json`; see [runtime/prepared-context/README.md](../runtime/prepared-context/README.md) and [context-budgeting.md](../docs/runtime/context-budgeting.md). **Policy mode defaults** (not Record): [`platform/config/policy_modes/defaults.json`](../platform/config/policy_modes/defaults.json), [docs/policy-modes.md](../docs/policy-modes.md).

## Commit-worthiness rule

Derived artifacts are not all equal. Before committing a changed file under `runtime/artifacts/`, classify it:

| Class | Commit posture |
|-------|----------------|
| Stable operator surface | Commit when the surface is part of the normal workflow, registered or listed here, and useful for review diffs. |
| Historical receipt or report | Commit only when the run itself is evidence for a feature, audit, demo, or partner-facing claim. |
| Rebuildable local snapshot | Prefer regeneration on demand; do not commit just because a script ran. |
| Scratch / cache / temp output | Keep gitignored or local unless explicitly promoted into a report. |

When in doubt, commit the source doctrine, script, test, or receipt that proves the behavior before committing a refreshed dashboard. A generated Markdown file should say which operator decision it supports and which source it does not replace.

| Path | Produced by | Policy |
|------|-------------|--------|
| `runtime/artifacts/civilizational-statecraft-public/` | *(retired)* | **Legacy** export residue only — SSOT staging is [`public/civ-state/`](../public/civ-state/). See [README-STAGING.md](civilizational-statecraft-public/README-STAGING.md). |
| `runtime/artifacts/work-notes/` | `scripts/new_work_note.py` | **Scratch** work notes from `docs/templates/work-note-template.md`. **Default:** `*.md` **gitignored**; `.gitkeep` preserves the directory. Not Record. |
| `runtime/artifacts/evidence-stubs/` | `scripts/new_evidence_stub.py`, **`scripts/research_to_evidence_stub.py`** | **Pre-canonical** evidence stubs ([README](evidence-stubs/README.md)); **`research_to_evidence_stub`** consumes [`schemas/research-evidence-input.v1.json`](../schemas/research-evidence-input.v1.json); **Default:** gitignored `*.md` like skill-cards. |
| `runtime/artifacts/patch-intake/` | **`scripts/coding_agent_patch_intake.py`** | **Candidate-proposal** patch-review packets ([README](patch-intake/README.md)); consumes [`schemas/coding-agent-patch-intake.v1.json`](../schemas/coding-agent-patch-intake.v1.json); **Default:** gitignored `*.md` except README. |
| `runtime/artifacts/statecraft-intake-queue/` | **`scripts/statecraft_intake_queue.py`** | **Derived** intake queue sidecars + optional digests ([README](statecraft-intake-queue/README.md)); schema [`statecraft-intake-sidecar.v1.json`](../schemas/registry/statecraft-intake-sidecar.v1.json); **Default:** gitignored `*.json`; optional committed `digest-*.md`. |
| `runtime/artifacts/mcp-admission/` | **`scripts/mcp_manifest_admission.py`** | **Planning-only** MCP manifest admission packets ([README](mcp-admission/README.md)); consumes [`schemas/mcp-server-manifest.v1.json`](../schemas/mcp-server-manifest.v1.json); **Default:** gitignored `*.md` except README + `.gitkeep`. |
| `runtime/artifacts/mcp-mock-runs/` | **`scripts/mcp_mock_harness.py`** | **Fixture** MCP-shaped mock-run packets ([README](mcp-mock-runs/README.md)); consumes [`schemas/mcp-mock-run.v1.json`](../schemas/mcp-mock-run.v1.json); **Default:** gitignored `*.md` except README + `.gitkeep`. |
| `runtime/artifacts/mcp-local-read/` | **`scripts/mcp_local_readonly.py`** | **Bounded** UTF-8 read packets ([README](mcp-local-read/README.md)); allowlist [`platform/config/mcp-local-read-allowlist.yaml`](../platform/config/mcp-local-read-allowlist.yaml); **Default:** gitignored `*.md` except README + `.gitkeep`. |
| `runtime/artifacts/mcp-local-index/` | **`scripts/mcp_local_index.py`** | **Metadata-only** directory index packets ([README](mcp-local-index/README.md)); same allowlist as local read; **Default:** gitignored `*.md` except README + `.gitkeep`. |
| `runtime/artifacts/mcp-governance-demo/` | **`scripts/run_mcp_governance_checks.py`** (manual steps in runbook) | **Derived** capability/authority/risk demo outputs under audit prefix ([README](mcp-governance-demo/README.md)); adapter demos use `governance-demo-*` files in standard MCP buckets. |
| `runtime/artifacts/mcp-governance-demo-report.md` | **`scripts/run_mcp_governance_checks.py`** | **Aggregated** pass/fail Markdown for the full governance sequence — WORK/runtime only; **Default:** gitignored; see [mcp-governance-runbook.md](../docs/mcp/mcp-governance-runbook.md). |
| `runtime/artifacts/mcp-risk-report.md`, `runtime/artifacts/mcp-risk-report.json` | **`scripts/mcp_risk_scan.py`** | **Derived** permission-risk scan over [`platform/config/mcp-capabilities.yaml`](../platform/config/mcp-capabilities.yaml) + [`platform/config/mcp-risk-policy.yaml`](../platform/config/mcp-risk-policy.yaml); planning-only; regenerate after registry/policy edits; [docs/mcp/mcp-risk-permission-scanner.md](../docs/mcp/mcp-risk-permission-scanner.md). |
| `runtime/artifacts/candidate-drafts/` | `scripts/new_candidate_draft.py` | **Pre-gate** human drafts; does not stage `recursion-gate.md`. **Default:** gitignored `*.md`. |
| `runtime/artifacts/skill-cards/` | `scripts/build_skill_cards.py` | **Rebuild** after portable skill edits. **Default:** contents are **gitignored** (see repo `.gitignore`); only `.gitkeep` preserves the directory. Optional CI snapshots if you want diff review. |
| `runtime/artifacts/context/` | `scripts/compress_active_lane.py` | **Ephemeral operator memos** with source paths. **Default:** gitignored except `.gitkeep`. Regenerate as needed; not a substitute for lane READMEs or `self-work.md`. |
| `runtime/artifacts/work-dev/interface-runtime/artifacts/` | operator or future tooling | **Derived** interface artifacts and metadata for cross-lane prototypes; WORK-only, non-canonical, delete/regenerate as needed. Prefer lane-specific buckets when a lane already has one. |
| `runtime/artifacts/work-dev/rebuild-receipts/` | `scripts/regenerate_all_derived.py` | **Derived** receipts for repo-owned regeneration runs. Tracks changed paths, selected targets, and run status; not Record, not gate authority. |
| `runtime/artifacts/work-dev/derived-regeneration-manifest.json` | `scripts/build_derived_regeneration_manifest.py` | **Derived** manifest for repo-owned rebuild targets, watch patterns, outputs, and dependencies. Not Record; supports incremental regeneration. |
| `runtime/artifacts/work-dev/rebuild-health/` | `scripts/report_rebuild_health.py` | **Derived** rebuild-health telemetry from rebuild receipts and the regeneration manifest. Operator observability only; not Record truth. |
| `runtime/artifacts/observability/work-coffee/conductor-eval/` | **`scripts/run_conductor_eval_harness.py`** | **Derived** Conductor MCQ metrics JSON ([schema](../schemas/registry/conductor-session-metrics.v1.json)); default `*.json` gitignored — [bucket README](observability/work-coffee/conductor-eval/README.md), [doc](../docs/skill-work/work-coffee/conductor-observability.md). |
| `runtime/artifacts/work-strategy/strategy-notebook/` | `scripts/strategy_page.py`, `scripts/compile_strategy_view.py`, `scripts/build_strategy_notebook_graph.py` | **Derived** JSONL receipts, `graph.json`, and `views/` for the strategy-notebook lane — not SSOT; see [work-strategy/strategy-notebook/README.md](work-strategy/strategy-notebook/README.md), [docs/runtime-vs-record.md](../docs/runtime-vs-record.md). |
| `runtime/artifacts/strategy-runs/`, `runtime/artifacts/run-receipts/` | `scripts/strategy_run.py` | **Derived** per-run `state.json` and event receipts — session envelope for work-strategy, not SSOT; see [STRATEGY-RUN-ARCHITECTURE.md](../docs/skill-work/work-strategy/STRATEGY-RUN-ARCHITECTURE.md), [docs/run-contract.md](../docs/run-contract.md). |
| `runtime/artifacts/strategy-run-report.md` | `scripts/build_strategy_run_report.py` | **Derived** markdown table of recent runs; delete and rebuild. |
| `runtime/artifacts/library-index.md` | `scripts/build_library_index.py` | **Derived** scan-first dashboard (at-a-glance, Start here, recent, compact by lane + appendix inventory) from `self-library.md` entries YAML — not SELF-LIBRARY truth; regenerate after library edits. See [docs/operator-dashboards.md](../docs/operator-dashboards.md). |
| `runtime/artifacts/lane-dashboards/README.md` | `scripts/build_lane_dashboards.py` | **Derived** lane/runtime snapshot (+ optional `work-lanes-dashboard.json`). Not canonical. |
| `runtime/artifacts/memory/memory-observability.md`, `runtime/artifacts/memory/memory-observability.json` | `scripts/build_memory_observability.py` | **Derived** continuity observability over cadence and handoff surfaces. Not Record and not MEMORY; coffee/dream may surface only a one-line non-blocking status from it. |
| `runtime/artifacts/review-dashboard.md` | `scripts/build_review_dashboard.py` | **Derived** view of `recursion-gate.md` — does not replace the gate file. |
| `runtime/artifacts/governance-posture.md` | `scripts/report_governance_posture.py` | **Derived** operator/partner one-pager (triad, gate, audit paths, verification commands) — not Record, not legal advice; [safety-story-ux.md](../docs/skill-work/work-dev/safety-story-ux.md). Regenerate after policy changes. |
| `runtime/artifacts/mcp-capability-report.md` | `scripts/mcp_capability_audit.py` | **Derived** audit table + danger-flag heuristics over [`platform/config/mcp-capabilities.yaml`](../platform/config/mcp-capabilities.yaml); planning-only; [docs/mcp/governed-mcp-layer.md](../docs/mcp/governed-mcp-layer.md). Regenerate after registry edits. |
| `runtime/artifacts/mcp-authority-report.md` | `scripts/mcp_authority_check.py` | **Derived** lane ↔ authority-map cross-check over [`platform/config/mcp-authority-bindings.yaml`](../platform/config/mcp-authority-bindings.yaml) + registry + [`platform/config/authority-map.json`](../platform/config/authority-map.json); planning-only; [docs/mcp/mcp-authority-bindings.md](../docs/mcp/mcp-authority-bindings.md). Regenerate after bindings or map edits. |
| `runtime/artifacts/mcp-receipts/` | `scripts/mcp_receipt.py` | **Derived** MCP governance receipt JSON (audit metadata); WORK/runtime only; not Record — see [mcp-receipts/README.md](mcp-receipts/README.md), [docs/mcp/mcp-execution-receipts.md](../docs/mcp/mcp-execution-receipts.md). Optional committed examples under version control. |
| `runtime/artifacts/mcp-receipt-report.md` | `scripts/mcp_receipt_audit.py` | **Derived** validation summary over `runtime/artifacts/mcp-receipts/*.json`; regenerate after receipt edits. |
| `runtime/artifacts/gate-board.md` | `scripts/build_gate_board.py` | **Kanban-style** candidate/review snapshot — not authoritative; [docs/gate-board.md](../docs/gate-board.md). |
| `runtime/artifacts/work-lanes-dashboard.json` | `scripts/build_work_lanes_dashboard.py` | **WORK** telemetry aggregate; input to lane dashboard script. |
| `runtime/artifacts/forecast/` | `scripts/run_forecast_baselines.py` | **Forecast artifact JSON** + optional `.summary.md` — WORK-layer; [policy](forecast/README.md), [lane](../docs/skill-work/work-forecast/README.md). |
| `runtime/artifacts/simulations/` | `python -m integrations.scenario_lab.run_gated_simulation`, `python -m integrations.scenario_lab.visualize_simulation` | **Derived** Scenario Lab pilot packets, run reports, manifests, and visualization-ready outputs; simulation-only, advisory, and not governed truth; see [bucket README](simulations/README.md). |
| `runtime/artifacts/receipts/forecast/` | `scripts/run_forecast_baselines.py` | **Forecast run receipts** — legibility only; [policy](receipts/forecast/README.md). |
| `runtime/artifacts/uncertainty-reports/` | _(optional)_ operator / CI | **Optional** sidecars for uncertainty envelope JSON — not Record; [folder README](uncertainty-reports/README.md). |
| `runtime/artifacts/review-packets/` | `scripts/runtime/review_orchestrator.py` | **Optional** Markdown review packets (`--output`; **`--task-anchor` required**) — not Record; [folder README](review-packets/README.md). |
| `runtime/artifacts/shadow-merges/` | `scripts/runtime/shadow_merge_simulator.py` | **Optional** Markdown shadow-merge preview reports (`--output`) — not Record; [folder README](shadow-merges/README.md), [doc](../docs/orchestration/shadow-merge-simulator.md). |
| `runtime/artifacts/classification-reports/` | `scripts/runtime/surface_misclassification_detector.py` | **Optional** Markdown surface-classification risk reports (`--output`) — advisory, not Record; [folder README](classification-reports/README.md), [doc](../docs/orchestration/surface-misclassification-detector.md). |
| `runtime/artifacts/route-recommendations/` | `scripts/recommend_route.py` | **Advisory** task-to-lane heuristic receipts (markdown); derived, gitignored defaults; see [bucket README](route-recommendations/README.md), [doc](../docs/route-recommendation.md). |
| `runtime/artifacts/skill-evals/` | `scripts/runtime/skill_eval_clinic.py` | **Optional** JSON/Markdown skill evaluation clinic reports — derived, not canonical skills; [skill-evaluation-clinic.md](../docs/skill-work/work-dev/skill-evaluation-clinic.md). |
| `runtime/artifacts/benchmarks/composition/` | Kleiber composition benchmark protocol | **Work-layer** Strategy-codex composition benchmark outputs and scoring notes; run only from Kleiber Conductor Action Menu option D / Finale; [bucket README](benchmarks/composition/README.md), [protocol](../docs/skill-work/work-dev/kleiber-composition-benchmark.md). |
| `runtime/artifacts/context-failure-reports/` | `scripts/runtime/context_failure_clinic.py` | **Optional** JSON/Markdown context-failure diagnostic reports — derived; [context-failure-diagnostics-clinic.md](../docs/runtime/context-failure-diagnostics-clinic.md). |
| `runtime/artifacts/example-context-output.md` | _(fixture)_ | Non-canonical sample Markdown for clinic docs and manual CLI runs (not Record). |
| `runtime/artifacts/codegraph/` | `python -m integrations.codegraph.export_code_context`, `python -m integrations.codegraph.generate_architecture_bundle` | **Derived** bounded CodeGraph pilot exports, Markdown reports, and presentation-prep bridge inputs; WORK-only, rebuildable, and not governed state; see [bucket README](codegraph/README.md). |
| `runtime/artifacts/external-codex/` | **`scripts/build_external_codex_neighborhood.py`**, **`scripts/build_external_codex_family_report.py`** | **Derived** structural neighborhood **JSON** / optional **`.neighborhood.md`** (single subject); **family** JSON / optional **`.family.md`** (cluster by selector); schemas [`external-codex-neighborhood-report.v1.json`](../schemas/registry/external-codex-neighborhood-report.v1.json), [`external-codex-family-report.v1.json`](../schemas/registry/external-codex-family-report.v1.json); [bucket README](external-codex/README.md), [doc](../docs/skill-work/work-dev/external-codex-explorer.md); **Default outputs** gitignored — committed **`examples/`** only. |
| `runtime/artifacts/handoffs/` | `checkpoint_session.py`, `build_handoff_packet.py` | **Runtime** session checkpoints and handoff packets — not Record; [folder README](handoffs/README.md), [long-horizon doctrine](../docs/runtime/long-horizon-work.md). |
| `runtime/artifacts/repo-surgeon/` | **`scripts/repo_surgeon.py`** (Phase 1) | **Derived** structural health report — orchestrates existing checks + scoped link/portability scan; **Default:** gitignored `latest.*` and dated snapshots; committed README only; [bucket README](repo-surgeon/README.md), [phase0 alignment](../docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md). |
| `runtime/artifacts/statecraft-war-room/` | **`scripts/statecraft_war_room.py`** (Phase 2) | **Derived** statecraft object rollup from intake + daily + transactions; **Default:** gitignored `latest.*`; committed README only; [bucket README](statecraft-war-room/README.md), [phase0 alignment](../docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md). |
| `runtime/artifacts/operator-command-deck/` | **`scripts/operator_command_deck.py`** (Phase 3) | **Derived** repo-wide operator cockpit aggregating Surgeon + War Room; **Default:** gitignored `latest.*`; committed README only; [bucket README](operator-command-deck/README.md), [phase0 alignment](../docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md). |
| `runtime/artifacts/operator-dashboard/` | **`scripts/operator_dashboard.py`** (Phase 4) | **Derived** umbrella index stitching the three aggregators; **Default:** gitignored `latest.*`; committed README only; [bucket README](operator-dashboard/README.md), [phase0 alignment](../docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md). |
| `runtime/prepared-context/last-budget-builds.json` | `build_budgeted_context.py` | **Optional** per-lane receipt for last budgeted build (repo root); see [context-budgeting.md](../docs/runtime/context-budgeting.md). |

**Companion-specific large blobs** (e.g. under `runtime/artifacts/`) follow separate rules in `.gitignore` and instance docs — not this folder.

## Regeneration contract

For the current repo-owned target set, use:

```bash
python3 scripts/regenerate_all_derived.py --changed --dry-run
python3 scripts/regenerate_all_derived.py --all
```

That flow writes three distinct non-canonical metadata families:

- **Rebuild receipts** under `runtime/artifacts/work-dev/rebuild-receipts/` — one receipt per regeneration run
- **Target manifest** at `runtime/artifacts/work-dev/derived-regeneration-manifest.json` — the declared target registry
- **Derived-artifact rationale sidecars** next to covered outputs — one sidecar per rebuilt artifact path

## Derived-artifact rationale sidecars

Sidecar naming is intentionally literal:

- `runtime/artifacts/library-index.md`
- `runtime/artifacts/library-index.md.derived-rationale.json`

The sidecar records rebuild provenance only:

- `producer_script`
- `policy_mode`
- `generated_at`
- `artifact_path`
- `canonical_surfaces_touched` (always `false`)
- `rebuild_command`
- `inputs`
- `rationale`
- `human_review_required`

Schema: [`schemas/registry/derived-artifact-rationale.v1.json`](../schemas/registry/derived-artifact-rationale.v1.json)

## Cleanup rule

Derived regeneration is **target-owned**, not whole-tree destructive:

- single-file outputs are overwritten by their producer scripts
- directory cleanup is allowed only for files explicitly owned by the selected rebuild target
- `.gitkeep` and unrelated artifact families must be preserved

This is why repo-owned regeneration stays narrower than “delete all of `/runtime/artifacts/` and hope.”

See also: [docs/skills/skill-card-spec.md](../docs/skills/skill-card-spec.md), [docs/skill-work/active-lane-compression.md](../docs/skill-work/active-lane-compression.md), [docs/operator-dashboards.md](../docs/operator-dashboards.md) (Library / lane / review Markdown dashboards).
