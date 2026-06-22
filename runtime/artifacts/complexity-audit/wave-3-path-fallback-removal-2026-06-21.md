# Wave 3 Path Fallback Removal Receipt

**Date:** 2026-06-21

## What changed

Removed legacy fallback tuple tails for Wave 3 archive placeholder keys:

- `evidence`
- `reflection-proposals`
- `review-queue`

Runtime now resolves these keys to canonical paths only (`REPO_PATH_MIGRATIONS` single-tuple entries).

Updated [`path-fallback-retirement.yaml`](../../../path-fallback-retirement.yaml) (`legacy: []`, `keep_no_legacy`) and [`docs/path-fallback-retirement.md`](../../../docs/path-fallback-retirement.md) (Wave 3 retired section).

Added regression tests in [`tests/test_repo_path_strict.py`](../../../tests/test_repo_path_strict.py).

**Fallback tuple count:** 6 → **3** keys with `len(entry) > 1`.

## What did not change

- Wave 4 Grace-Mar compatibility fallbacks remain.
- Internal `grace_mar` package unchanged.
- Archive files not moved or deleted.

## Prerequisite

Readiness verified in [`wave-3-archive-placeholder-readiness-2026-06-21.md`](wave-3-archive-placeholder-readiness-2026-06-21.md).

## Checks run

| Check | Result |
|---|---|
| `python scripts/check_repo_path_strict.py` | **Pass** |
| `python scripts/check_repo_path_strict.py --strict` | **Pass** |
| `python scripts/check_repo_path_strict.py --wave 3` | **Pass** |
| `python -m pytest tests/test_repo_path_strict.py -q` | **Pass** |
| `python scripts/check_repo_health.py --quick` | **Pass** |

## Remaining work

- Wave 4 — Grace-Mar compatibility relocation to `platform/src/strategy_codex/compat/grace_mar_paths.py`.
- Promote strict-path scan to required CI after operator approval.
