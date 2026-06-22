# Root File Budget Program — Phase 0–4 Complete (Proof Receipt)

**Date:** 2026-06-21  
**Status:** **Complete** — strict budget enforced in CI

## Summary

| Signal | Baseline | Final |
|---|---:|---:|
| Root files on disk (non-dot) | **34** | **25** |
| `max_root_files` | 20 → reconciled **25** | **25** |
| Over budget | **9+** | **0** |
| Strict CI gate | advisory | **required** |

Doctrine floor documented in [`docs/canonical-paths.md`](../../../docs/canonical-paths.md): skill splits (`skill-think.md`, `skill-write.md`, `skill-steward.md`) remain at repo root by policy.

## Phase ledger

| Phase | Scope | Outcome | Key commits |
|---|---|---|---|
| **0** | Manifest hygiene (`path-fallback-retirement.yaml`, slice plan, complexity-budget) | Unlisted routing file cleared | `659d19952`, `40bf8cf17` |
| **1** | Compatibility relocations (7 files off root) | 34 → 27 tracked root files | see wedge table below |
| **2** | Operator ledgers → `runtime/operator-events/` | 27 → **25** at target | `3465bb015` |
| **3** | Target reconciliation (`max_root_files` 25) | Doctrine floor aligned | `40bf8cf17` |
| **4** | CI promotion (`--strict` required) | Fail mode live | `d5f168c0a` |

### Phase 1 wedges (shipped)

| Root file | Canonical path | Commit |
|---|---|---|
| `template-manifest.json` | `platform/template/template-manifest.json` | `36365b279` |
| `template-source.json` | `platform/template/template-source.json` | `36365b279` |
| `how-instances-consume-upgrades.md` | `docs/archive/how-instances-consume-upgrades.md` | `4f0400444` |
| `license-record` | `docs/archive/license-record` | `4f0400444` |
| `grace-mar.code-workspace` | `.vscode/grace-mar.code-workspace` | `3cea92349` |
| `DESIGN.md` | `docs/skill-work/work-dev/DESIGN.md` | `6852630a3` |
| `instance-contract.json` | `platform/config/instance-contract.json` | `89afee571` |

## Invariants (post-program)

```text
Root files (non-dot): 25 / max 25
Legacy root jsonl: ignore_local (harness-events.jsonl, compute-ledger.jsonl)
Ledger writes: runtime/operator-events/ via operator_ledger_write_path
Template sync validator: platform/config/instance-contract.json (path-normalized)
```

## Acceptance (all met)

| # | Criterion | Evidence |
|---|---|---|
| 1 | `assert_root_file_budget.py --strict` passes locally | see checks below |
| 2 | Required CI job runs `--strict` | [`.github/workflows/repo-health.yml`](../../../.github/workflows/repo-health.yml) Required job |
| 3 | `check_repo_health.py --quick` mirrors strict budget | [`scripts/check_repo_health.py`](../../../scripts/check_repo_health.py) |
| 4 | Regression tests green | `tests/test_assert_root_file_budget.py` |
| 5 | Program receipts indexed | this file + linked receipts |

## Checks run (2026-06-21)

```bash
python scripts/assert_root_file_budget.py --strict
python -m pytest tests/test_assert_root_file_budget.py -q
```

| Check | Result |
|---|---|
| `assert_root_file_budget.py --strict` | **Pass** (25/25) |
| `test_assert_root_file_budget.py` | **Pass** |

## Related receipts

| Artifact | Path |
|---|---|
| Slice plan (living plan) | [root-file-budget-slice-plan-2026-06-21.md](root-file-budget-slice-plan-2026-06-21.md) |
| CI enforcement slice | [root-file-budget-ci-enforcement-2026-06-21.md](root-file-budget-ci-enforcement-2026-06-21.md) |
| Complexity policy | [docs/complexity-budget.md](../../../docs/complexity-budget.md) |
| Budget manifest | [root-file-budget.yaml](../../../root-file-budget.yaml) |

## Remaining complexity work (out of scope for this program)

- Primary routing doc count (`audit_repo_complexity.py --check` — still advisory).
- README / start-here trim (Phase 8 doc program).
- Optional skill-split relocation to `codex/` (doctrine change).
- Build manifest consolidation under `platform/deployment/`.

## Operator commands

```bash
python scripts/assert_root_file_budget.py          # warn mode
python scripts/assert_root_file_budget.py --strict # CI-equivalent
python scripts/check_repo_health.py --quick        # includes strict budget
```
