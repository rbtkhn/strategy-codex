# Wave 2 Path Fallback Removal Receipt

**Date:** 2026-06-21

## What changed

Removed legacy fallback tuple tails for Wave 2 platform subpath keys:

- `app`
- `bin`
- `deployment`
- `config`
- `extension`
- `integrations`
- `miniapp`
- `users`
- `template`
- `profile`

Runtime now resolves these keys to canonical paths only (`REPO_PATH_MIGRATIONS` single-tuple entries).

Updated [`path-fallback-retirement.yaml`](../../../path-fallback-retirement.yaml) (`legacy: []`, `keep_no_legacy`) and [`docs/path-fallback-retirement.md`](../../../docs/path-fallback-retirement.md) (Wave 2 retired section).

Added regression tests in [`tests/test_repo_path_strict.py`](../../../tests/test_repo_path_strict.py).

**Fallback tuple count:** 16 → **6** keys with `len(entry) > 1`.

## What did not change

- Wave 3 archive placeholder fallbacks remain.
- Wave 4 Grace-Mar compatibility fallbacks remain.
- Internal `grace_mar` package unchanged.
- Archive files not moved or deleted.

## Prerequisite

Readiness verified in [`wave-2-platform-readiness-2026-06-21.md`](wave-2-platform-readiness-2026-06-21.md) (commit `65807a14a`).

## Checks run

| Check | Result |
|---|---|
| `python scripts/check_repo_path_strict.py` | **Pass** |
| `python scripts/check_repo_path_strict.py --strict` | **Pass** |
| `python scripts/check_repo_path_strict.py --wave 2` | **Pass** |
| `python -m pytest tests/test_repo_path_strict.py -q` | **Pass** |
| `python scripts/check_repo_health.py --quick` | **Pass** |

## Remaining work

- Wave 3 — archive placeholder audit and removal when clean.
- Wave 4 — Grace-Mar compatibility relocation to `platform/src/strategy_codex/compat/grace_mar_paths.py`.
- Promote strict-path scan to required CI after operator approval.
