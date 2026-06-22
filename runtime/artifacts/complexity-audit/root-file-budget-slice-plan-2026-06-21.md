# Root File Budget — Phased Slice Plan

**Date:** 2026-06-21

## Current state

| Signal | Value |
|---|---|
| Root files on disk (non-dot) | **25** (at target) |
| Over budget by | **0** |

Preflight: `python scripts/assert_root_file_budget.py` · `--strict` fails.

## Doctrine floor (why 20 is tight)

[`docs/canonical-paths.md`](../../../docs/canonical-paths.md) requires active split skill files at repo root: `skill-think.md`, `skill-write.md`, `skill-steward.md`.

**Hard-to-move categories (25 files minimum):**

| Category | Count | Examples |
|---|---:|---|
| required_public | 3 | README, LICENSE, contributing |
| agent | 2 | AGENTS, instance-doctrine |
| build | 11 | pyproject, Docker, compose, mkdocs, render, … |
| routing | 5 | repo-map, lanes, manifests, path-fallback-retirement |
| generated | 1 | LLM-ROUTING.md |
| skill splits (doctrine) | 3 | skill-think/write/steward |

**Compatibility / operator candidates (8 files):** DESIGN.md, how-instances-consume-upgrades.md, grace-mar.code-workspace, license-record, template-manifest.json, template-source.json, instance-contract.json, docker-compose.transcripts.yml

Relocating all compatibility files saves **~8** tracked root files → **~25 remain** — still **5 over** max 20 without doctrine or build consolidation.

## Recommended phases

### Phase 0 — Manifest hygiene (this slice starter)

- Add `path-fallback-retirement.yaml` to [`root-file-budget.yaml`](../../../root-file-budget.yaml) (routing).
- Index this plan in complexity-audit README.
- Update [`docs/complexity-budget.md`](../../../docs/complexity-budget.md) with phased table and doctrine floor note.

**Outcome:** unlisted warning cleared; count unchanged.

### Phase 1 — Compatibility relocations (low risk)

Move to documented archive/template paths; update links:

| File | Target |
|---|---|
| `how-instances-consume-upgrades.md` | `docs/archive/how-instances-consume-upgrades.md` | **Done** |
| `license-record` | `docs/archive/license-record` | **Done** |
| `template-manifest.json` | `platform/template/template-manifest.json` | **Done** |
| `template-source.json` | `platform/template/template-source.json` | **Done** |
| `DESIGN.md` | `docs/skill-work/work-dev/DESIGN.md` (update creative-pipeline links) | **Done** |
| `grace-mar.code-workspace` | `.vscode/grace-mar.code-workspace` | **Done** |
| `instance-contract.json` | `platform/config/instance-contract.json` | **Done** |

**Est. reduction:** 7–8 tracked root files → **~25–26** on disk.

### Phase 2 — Operator ledgers (local hygiene) — **Done** 2026-06-21

- Ledgers write via `operator_ledger_write_path` → `runtime/operator-events/`.
- Root `harness-events.jsonl` / `compute-ledger.jsonl` moved to `ignore_local` (legacy root copies ignored by budget).
- Removed operator ledger entries from `root-file-budget.yaml` allowlist.

**Outcome:** root count **25** (at `max_root_files` target).

### Phase 3 — Target reconciliation

**Done (2026-06-21):** Option **A** — raised `max_root_files` to **25** with documented doctrine floor in [`root-file-budget.yaml`](../../../root-file-budget.yaml) and [`docs/complexity-budget.md`](../../../docs/complexity-budget.md). [`scripts/audit_repo_complexity.py`](../../../scripts/audit_repo_complexity.py) threshold aligned.

Remaining options if count must fall further:

- **B)** Relocate skill splits to `codex/` + update [`docs/canonical-paths.md`](../../../docs/canonical-paths.md) (doctrine change).
- **C)** Consolidate build manifests under `platform/deployment/` (higher risk for CI/Docker).

### Phase 4 — CI promotion

Promote `assert_root_file_budget.py --strict` to required job (mirror path-fallback enforcement) **only after** Phase 1–3 bring count ≤ target.

## Out of scope

- README / start-here trim (Phase 8 doc program).
- Internal `grace_mar` rename.
- Archive bundle moves.

## Acceptance (full program)

1. `assert_root_file_budget.py --strict` passes locally and in CI.
2. Required CI job includes `--strict` root file budget step.
3. Receipt: `root-file-budget-ci-enforcement-YYYY-MM-DD.md`.

## Commands

```bash
python scripts/assert_root_file_budget.py
python scripts/assert_root_file_budget.py --strict
python scripts/audit_repo_complexity.py --check
```
