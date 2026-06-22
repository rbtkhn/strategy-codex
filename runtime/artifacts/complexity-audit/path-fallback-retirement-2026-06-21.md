# Path Fallback Retirement Receipt

**Date:** 2026-06-21

## What changed

- Added [`path-fallback-retirement.yaml`](../../../path-fallback-retirement.yaml) (29 keys, machine SSOT).
- Added [`docs/path-fallback-retirement.md`](../../../docs/path-fallback-retirement.md) (human mirror + wave order).
- Added `validate_repo_path_classification()` and `validate_path_fallback_retirement()` in [`scripts/repo_io.py`](../../../scripts/repo_io.py).
- Improved [`scripts/check_repo_path_strict.py`](../../../scripts/check_repo_path_strict.py) (summary, retirement candidates, `--json`).
- Expanded [`tests/test_repo_path_strict.py`](../../../tests/test_repo_path_strict.py) (10 tests).
- Updated [`docs/complexity-budget.md`](../../../docs/complexity-budget.md) path fallback retirement budget.
- Fixed missing `source_capture` in [`schemas/repo_map.schema.json`](../../../schemas/repo_map.schema.json) (repo-map route validation).
- **Runtime resolver behavior unchanged** — no fallback tuples removed.

## Classification summary

| Category | Keys |
|---|---:|
| `active_canonical` | 22 |
| `archive_placeholder` | 3 |
| `grace_mar_compat` | 4 |
| **Total** | **29** |

## Checks run

| Check | Result |
|---|---|
| `python scripts/check_repo_path_strict.py` | **Pass** (0 layout issues) |
| `python scripts/check_repo_path_strict.py --strict` | **Pass** |
| `python scripts/check_repo_path_strict.py --json` | **Pass** |
| `python -m pytest tests/test_repo_path_strict.py -q` | **10 passed** |
| `python scripts/check_repo_health.py --quick` | **Pass** |

## Remaining work

- **Wave 1** — remove active canonical fallbacks when dual layouts stay at zero.
- **Wave 2** — platform subpath fallbacks after apps verification.
- **Wave 3** — archive placeholders after queue audit.
- **Wave 4** — relocate Grace-Mar compat keys to `platform/src/strategy_codex/compat/grace_mar_paths.py`.
- Promote strict-path CI from advisory to required after operator approval.
