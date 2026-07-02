# Singularity loop system

## Principle

> Singularity is defined by the loops it runs, not the ideas it contains.

A **loop** is a recurring operational job with declared triggers, inputs, process steps, outputs, and state. Interpretive shelves (`notes/`, `essays/`, `synthesis/`, `workshop/`) are **outputs** of loops or documentation about them—not loops themselves.

## Layered model

| Layer | Location | Role |
| --- | --- | --- |
| Loop definitions | `singularity/loops/**/*.yaml` | SSOT for recurring jobs |
| Generated registry | `runtime/artifacts/loop-registry.json` | Build artifact for orchestration and CI |
| Orchestrator signals | `runtime/artifacts/singularity-signals.json` | Pending, blocked, and attention-required loop ids |
| Action cards | `singularity/action-cards/` | Dated work orders (WORK artifacts) |
| Run receipts | `runtime/operator-events/singularity-loop-runs.jsonl` | Append-only loop execution history |
| Output shelves | `singularity/notes/`, `essays/`, `synthesis/`, `workshop/` | Grandfathered interpretive holdings |
| Operating shelves | `singularity/education/`, `operations/` | Loop output cards and education/operations artifacts |
| Domain signals | `singularity/workshop/longitudinal/innermost-loop-signals.json` | Innermost Loop coverage data (not orchestrator state) |

New recurring work must declare a loop YAML. New interpretive artifacts should link to a producing loop when practical (via `output_shelves` on the loop or prose cross-links).

## Architectural role

```text
statecraft/   = perception system (signals, synthesis, judgment)
singularity/  = control system (loops, attention, action cards)
runtime/      = generated machine state
scripts/      = execution layer
```

Combined flow: **perception → decision → action → feedback**

Current phase: **declare → action card → proof → receipt → next-loop feed** — not yet execute/delegate/automate automatically.

Action card standard: [action-card-standard.md](action-card-standard.md) · shelf: [`singularity/action-cards/`](../../singularity/action-cards/README.md)

## Operating loop clusters

| Loop id | Category | Output shelf |
| --- | --- | --- |
| `innermost-loop-capture` | research | source-archive/singularity/innermost-loop/ |
| `moonshots-synthesis-watch` | research | singularity/workshop/sheets/ |
| `moonshots-intelligence-compile` | research | research/singularity-science/moonshots/ |
| `singularity-monthly-synthesis` | research | singularity/synthesis/ |
| `spine-health-check` | research | singularity/workshop/longitudinal/ |
| `work-cici-daily-ops` | projects | singularity/work-cici/ |
| `predictive-history-education` | projects | singularity/education/predictive-history/ (umbrella — source intake, routes to lesson pipeline) |
| `predictive-history-lesson-pipeline` | projects | singularity/education/predictive-history/lessons/, worksheets/, quizzes/, source-packets/ |
| `predictive-history-media-pack` | projects | singularity/education/predictive-history/media-packs/ |
| `predictive-history-media-quality-gate` | projects | singularity/education/predictive-history/media-review/ |
| `predictive-history-distribution-pack` | projects | singularity/education/predictive-history/distribution/ |
| `predictive-history-learner-feedback-review` | projects | singularity/education/predictive-history/feedback/ |
| `grace-gems-product-pipeline` | business | operations/grace-gems/products/, listings/drafts/, listings/photo-checklists/ |
| `grace-gems-margin-policy-review` | business | operations/grace-gems/listings/review/ |
| `grace-gems-marketplace-ops` | business | operations/grace-gems/ops/ |
| `grace-gems-search-conversion-review` | business | operations/grace-gems/listings/search-conversion/ |
| `grace-gems-customer-service` | business | operations/grace-gems/customer-service/ |
| `grace-gems-customer-promise-audit` | business | operations/grace-gems/customer-service/promise-audits/ |
| `mountain-homestead-ops` | business | operations/mountain-homestead/ops/, ops/weekly-cards/ |
| `mountain-homestead-risk-register` | business | operations/mountain-homestead/risk-register/ |
| `mountain-homestead-maintenance` | business | operations/mountain-homestead/maintenance/ |
| `mountain-homestead-wildfire-mitigation-review` | business | operations/mountain-homestead/wildfire-mitigation/ |
| `mountain-homestead-utilities-continuity` | business | operations/mountain-homestead/utilities-continuity/ |
| `mountain-homestead-water-systems-review` | business | operations/mountain-homestead/water-systems/ |
| `mountain-homestead-septic-review` | business | operations/mountain-homestead/septic/ |
| `mountain-homestead-seasonal-readiness` | business | operations/mountain-homestead/seasonal-readiness/ |

**Hard dependencies (Grace Gems):** `grace-gems-product-pipeline` → `grace-gems-margin-policy-review`; `grace-gems-marketplace-ops` → `grace-gems-search-conversion-review`; `grace-gems-customer-service` → `grace-gems-customer-promise-audit`.

**Hard dependencies (homestead):** `mountain-homestead-ops` → `mountain-homestead-maintenance` → `mountain-homestead-seasonal-readiness`; `mountain-homestead-ops` → `mountain-homestead-risk-register`; `mountain-homestead-ops` → `mountain-homestead-water-systems-review`; `mountain-homestead-maintenance` → wildfire-mitigation-review, utilities-continuity, septic-review.

**Soft feeds (homestead):** risk-register → ops (top 5 actions); utilities-continuity → ops; wildfire/water/septic → maintenance; risk/wildfire/continuity → seasonal-readiness. Full graph: [`operations/mountain-homestead/README.md`](../../operations/mountain-homestead/README.md).

**Soft feeds (Grace Gems):** margin-policy-review → marketplace-ops (approved listings); search-conversion-review → product-pipeline (experiments); customer-promise-audit → margin-policy-review (corrections); customer-service → marketplace-ops (unresolved issues). Full graph: [`operations/grace-gems/README.md`](../../operations/grace-gems/README.md).

**Hard dependencies (Predictive History education):** `predictive-history-education` → `predictive-history-lesson-pipeline` → `predictive-history-media-pack` → `predictive-history-media-quality-gate` → `predictive-history-distribution-pack` → `predictive-history-learner-feedback-review`.

**Soft feeds (PH education):** learner-feedback-review → lesson-pipeline and media-quality-gate (revision queue); media-quality-gate → distribution-pack (approved assets only). Full graph: [`singularity/education/predictive-history/README.md`](../../singularity/education/predictive-history/README.md).

## Loop schema

Each file under `singularity/loops/` is a YAML document with a top-level `loop:` key:

```yaml
loop:
  id: example-loop
  category: research          # projects | business | research | personal
  trigger:
    type: manual              # event | time | manual
    schedule: weekly          # optional stub for future scheduling
    description: When the operator requests a pass
  inputs:
    - description: What must be available before the loop runs
  process:
    steps:
      - description: First operational step
  outputs:
    - description: What the loop produces or updates
  state:
    status: active            # active | paused | completed
  dependencies:
    - loop_id: other-loop-id
  last_run: null
  output_shelves:
    - singularity/synthesis/
```

JSON Schema: [`schemas/singularity/loop.schema.json`](../../schemas/singularity/loop.schema.json)

Cross-object invariants (unique ids, valid dependencies, no cycles) are enforced by `scripts/singularity_loop_invariants.py`.

## Creating a loop

1. Pick a category folder under `singularity/loops/` (`research/`, `projects/`, `business/`, `personal/`).
2. Add `<loop-id>.yaml` using kebab-case id matching the filename stem.
3. Run `python3 scripts/build_loop_registry.py` to refresh the registry artifact.
4. Run `python3 scripts/validate_all_schemas.py --scope singularity` to validate YAML and artifacts.

## How loops interact

- **Dependencies** declare ordering or prerequisite loops (`dependencies[].loop_id`).
- **Output shelves** document where loop outputs land without moving existing files.
- **Orchestrator** reads the generated registry, not raw YAML (`scripts/run_singularity_loops.py`).

```text
singularity/loops/*.yaml  →  build_loop_registry.py  →  loop-registry.json
                                                      →  run_singularity_loops.py (stub)
                                                      →  singularity-signals.json (--status)
singularity/action-cards/<loop-id>/<date>.md  →  proof artifact
                                              →  append_singularity_loop_run.py
                                              →  singularity-loop-runs.jsonl
```

## Orchestrator (v1 stub)

`scripts/run_singularity_loops.py` lists loops from the registry. Default behavior is dry-run (no execution, no `last_run` updates).

```bash
python3 scripts/run_singularity_loops.py --active-only
python3 scripts/run_singularity_loops.py --status   # refresh orchestrator signals stub
```

`runtime/artifacts/singularity-signals.json` tracks orchestrator-facing state only:

- `pending_loops` — paused loops awaiting operator decision
- `blocked_loops` — loops blocked on external dependency
- `attention_required` — active loops with no recorded `last_run`

Domain signal detail (Innermost Loop front timelines, coverage gaps) stays in `singularity/workshop/longitudinal/innermost-loop-signals.json`.

**Session hooks (v1):** `operator_coffee.py` and `operator_daily_warmup.py` refresh orchestrator signals on coffee session start; `auto_dream.py` refreshes on successful end-of-day pass. When non-empty, a one-line brief may appear in warmup or dream output.

## Naming disambiguation

[`scripts/repo_convergence_registry.py`](../../scripts/repo_convergence_registry.py) defines `LoopSpec` for **repo CI/build convergence** (validators, builders, hybrid gates). That is a separate abstraction from singularity operational loops.

## Validation

```bash
python3 scripts/build_loop_registry.py
python3 scripts/build_loop_registry.py --check
python3 scripts/check_loop_registry.py
python3 scripts/run_singularity_loops.py --active-only
python3 scripts/check_singularity_loop_runs.py
python3 scripts/validate_all_schemas.py --scope singularity
python3 scripts/check_repo_health.py --quick
```

## Non-goals (current phase)

- No automated scheduling or AI delegation
- No automatic `last_run` updates from run receipts
- No merge of innermost-loop domain signals into orchestrator signals
- No deletion or mass relocation of grandfathered output shelves
