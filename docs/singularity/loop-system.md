# Singularity loop system

WORK only; not Record.

## Principle

> Singularity is defined by the loops it runs, not the ideas it contains.

A **loop** is a recurring operational job with declared triggers, inputs, process steps, outputs, and state. Interpretive shelves (`notes/`, `essays/`, `synthesis/`, `workshop/`) are **outputs** of loops or documentation about them—not loops themselves.

## Layered model

| Layer | Location | Role |
| --- | --- | --- |
| Loop definitions | `singularity/loops/**/*.yaml` | SSOT for recurring jobs |
| Generated registry | `runtime/artifacts/loop-registry.json` | Build artifact for orchestration and CI |
| Orchestrator signals | `runtime/artifacts/singularity-signals.json` | Pending, blocked, and attention-required loop ids |
| Output shelves | `singularity/notes/`, `essays/`, `synthesis/`, `workshop/` | Grandfathered interpretive holdings |
| Domain signals | `singularity/workshop/longitudinal/innermost-loop-signals.json` | Innermost Loop coverage data (not orchestrator state) |

New recurring work must declare a loop YAML. New interpretive artifacts should link to a producing loop when practical (via `output_shelves` on the loop or prose cross-links).

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
python3 scripts/validate_all_schemas.py --scope singularity
python3 scripts/check_repo_health.py --quick
```

## Non-goals (current phase)

- No automated scheduling or AI delegation
- No merge of innermost-loop domain signals into orchestrator signals
- No deletion or mass relocation of grandfathered output shelves
