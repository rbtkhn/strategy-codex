# Root File Budget CI Enforcement Receipt

**Date:** 2026-06-21

## What changed

- Promoted `python scripts/assert_root_file_budget.py --strict` to required CI.
- Removed advisory duplicate from repo-health advisory job.
- Aligned `check_repo_health.py --quick` to use `--strict` for root file budget.
- Updated regression test: strict mode passes at target count.
- Updated [`docs/complexity-budget.md`](../../../docs/complexity-budget.md) Phase 9 complete + CI rollout notes.

## Current invariant

```text
Root files (non-dot): 25 (max 25)
Over budget by: 0
```

## Checks run

| Check | Result |
|---|---|
| `python scripts/assert_root_file_budget.py --strict` | **Pass** |
| `python -m pytest tests/test_assert_root_file_budget.py -q` | **Pass** |
| `python scripts/check_repo_health.py --quick` | **Pass** (includes strict budget) |

## Preconditions (completed same program)

- Phase 1 compatibility relocations (template JSON, archive docs, workspace, DESIGN, instance-contract).
- Phase 2 operator ledger redirect + `ignore_local` for legacy root jsonl.

## Out of scope

- Primary routing doc count (still advisory via `audit_repo_complexity.py --check`).
- README/start-here trim.
- Skill-split doctrine relocation.
