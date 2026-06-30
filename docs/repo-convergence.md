# Repo convergence

**Status:** Phase 1 — local/manual convergence runner for derived artifacts and validators.

The repo convergence orchestrator brings **declared loops** back into agreement with their **input watch paths** after edits. It is **not** a daemon, scheduler, or authority engine.

```bash
python3 scripts/run_repo_convergence.py --check
python3 scripts/run_repo_convergence.py --write
python3 scripts/run_repo_convergence.py --explain
```

## Purpose

`strategy-codex` already has many specialized validators and builders. The orchestrator makes **dependency logic explicit**:

- What changed?
- Which loops are affected?
- Which derived artifacts need rebuilding?
- Which validators must run?
- Is the repo converged?

It does **not** answer doctrine promotion, Record mutation, event resolution, or essay publication — those remain human-governed.

## Non-goals

- No background daemon or file watcher
- No hidden auto-commits
- No automatic Record / source-archive / doctrine promotion
- Does **not** replace [`scripts/check_repo_health.py`](../scripts/check_repo_health.py) in Phase 1

## Modes

| Mode | Behavior |
|------|----------|
| `--check` (default) | Non-mutating. Skips unchanged builders (`needs_write` if inputs changed). Runs validators only when loop inputs are dirty or `--all`. |
| `--write` | Runs dirty builders (declared writes only), then validators when dirty. Updates committed state on success. |
| `--explain` | Prints loop graph (inputs, writes, depends_on, commands). |

Other flags: `--loop NAME`, `--all`, `--json`, `--quiet`, `--strict`.

## Recommended workflow

After editing prediction notes, routing pins, or generated surfaces:

```bash
python3 scripts/run_repo_convergence.py --write
python3 scripts/check_repo_health.py --quick
```

Pre-ship **full validator sweep** (when narrowed inputs may have skipped loops):

```bash
python3 scripts/run_repo_convergence.py --all --check
# or
python3 scripts/check_repo_health.py --quick
```

## Loop registry

Declared in [`scripts/repo_convergence_registry.py`](../scripts/repo_convergence_registry.py):

| Loop | Kind | Depends on | Writes |
|------|------|------------|--------|
| `routing` | validator | — | — |
| `membrane` | validator | — | — |
| `statecraft_predictions` | builder | — | `runtime/artifacts/prediction-*.json` |
| `statecraft_notes` | validator | `statecraft_predictions` | — |
| `generated_surfaces` | validator | `statecraft_predictions` | — |
| `essay_surfaces` | validator | — | — |
| `schema` | validator | — | — |

Phase 1 **intentionally omits** (still in health only): Freeman predictions, voice guest indexes, root file budget, archive boundary, retired-path sentinels.

## Input narrowing policy

Loop `inputs` are **scheduling triggers**, not the full validator scan scope. Paths are derived from underlying script watch lists (`TIER1_DOCS`, `GOVERNED_SCAN_*`, `SCAN_ROOTS`, etc.).

When a validator still scans broadly at runtime but inputs are narrow, use `--all` or `check_repo_health --quick` as backstops.

**Maintenance:** When validator scan constants change, update the matching loop `inputs` in the same PR.

## Safety boundaries

**Allowed automatic writes:** `runtime/artifacts/*`, convergence report/state, operator-event JSONL.

**Forbidden automatic writes:** Record surfaces, source archive, event resolution, doctrine promotion, identity-bearing truth.

## Outputs

| Path | Role |
|------|------|
| `runtime/artifacts/repo-convergence-report.json` | Last run status per loop |
| `runtime/artifacts/repo-convergence-state.json` | Committed input-hash baseline (shared dirty detection) |
| `runtime/operator-events/repo-convergence.jsonl` | Append-only loop outcome ledger |

## Related tools

| Tool | Role |
|------|------|
| [`check_repo_health.py`](../scripts/check_repo_health.py) | CI-shaped preflight fan-out (unconditional quick checks) |
| [`validate.py`](../scripts/validate.py) | CI validation inventory + `validation-run.v1` JSON |
| [`regenerate_all_derived.py`](../scripts/regenerate_all_derived.py) | Work-dev derived regeneration + receipts |
| [`derived-regeneration.md`](skill-work/work-dev/derived-regeneration.md) | Rebuild target contract |

## Naming note

**Not** gate `convergence_check()` in [`scripts/stage_gate_candidate.py`](../scripts/stage_gate_candidate.py) — that function means gate candidate sighting, not repo health convergence.

## Roadmap (deferred)

- `--since REF` git-diff prioritization
- Multi-pass fixed-point convergence
- Git diff write-boundary enforcement
- `gate_reporter` loops
- Freeman / codex-continuity loops
- `check_repo_health --quick` calling `run_repo_convergence --check` (after stabilization)
