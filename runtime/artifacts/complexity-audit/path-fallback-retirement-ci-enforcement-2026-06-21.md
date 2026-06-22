# Path Fallback Retirement CI Enforcement Receipt

**Date:** 2026-06-21

## What changed

- Promoted `python scripts/check_repo_path_strict.py --strict` to required CI.
- Moved path regression pytest (`test_repo_path_strict.py`, `test_grace_mar_paths.py`) to required job.
- Aligned `check_repo_health.py --quick` to use `--strict` for path scan.
- Enhanced regression test for zero legacy fallback tuples (key-level assert).
- Added retirement YAML test that no `legacy` entries remain.
- Updated [`docs/complexity-budget.md`](../../../docs/complexity-budget.md) to mark path fallback retirement complete.
- Updated [`docs/path-fallback-retirement.md`](../../../docs/path-fallback-retirement.md) with final status.

## Current invariant

```text
Fallback-bearing resolver keys: 0 (29 canonical-only migration keys)
```

## Checks run

| Check | Result |
|---|---|
| `python scripts/check_repo_path_strict.py --strict` | **Pass** |
| `python -m pytest tests/test_repo_path_strict.py tests/test_grace_mar_paths.py -q` | **Pass** |
| `python scripts/check_repo_health.py --quick` | **Pass** |

## Out of scope

- Root file budget.
- README/start-here trim.
- Internal `grace_mar` package rename.
- Archive movement or deletion.

## Remaining complexity work

- Root file budget enforcement.
- Generated manifest expansion.
- README/start-here final trim.
