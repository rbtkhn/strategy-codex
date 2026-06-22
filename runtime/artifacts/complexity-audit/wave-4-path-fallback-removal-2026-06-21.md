# Wave 4 Path Fallback Removal Receipt

**Date:** 2026-06-21

## What changed

Removed legacy fallback tuple tails for Wave 4 Grace-Mar compatibility keys:

- `bot`
- `recursion-gate-staging`
- `bootstrap`

Runtime now resolves these keys to canonical paths only (`REPO_PATH_MIGRATIONS` single-tuple entries).

`BOT_DIR` in [`scripts/repo_io.py`](../../../scripts/repo_io.py) now uses `GRACE_MAR_INSTANCE_DIR / "bot"` instead of `resolve_repo_path("bot")`.

Updated [`path-fallback-retirement.yaml`](../../../path-fallback-retirement.yaml) (`legacy: []`, `keep_no_legacy`) and [`docs/path-fallback-retirement.md`](../../../docs/path-fallback-retirement.md) (Wave 4 retired section).

Added regression tests in [`tests/test_repo_path_strict.py`](../../../tests/test_repo_path_strict.py) including `test_no_legacy_fallback_tuples_remain`.

**Fallback tuple count:** 3 → **0** keys with `len(entry) > 1`. Path-fallback retirement program complete.

## What did not change

- [`platform/src/strategy_codex/compat/grace_mar_paths.py`](../../../platform/src/strategy_codex/compat/grace_mar_paths.py) — canonical archaeology helpers unchanged.
- Internal `grace_mar` package unchanged.
- Archive files not moved or deleted.

## Prerequisite

Readiness verified in [`wave-4-grace-mar-compat-readiness-2026-06-21.md`](wave-4-grace-mar-compat-readiness-2026-06-21.md).

## Checks run

| Check | Result |
|---|---|
| `python scripts/check_repo_path_strict.py` | **Pass** |
| `python scripts/check_repo_path_strict.py --strict` | **Pass** |
| `python scripts/check_repo_path_strict.py --wave 4 --strict-readiness` | **Pass** |
| `python scripts/audit_repo_complexity.py --check` | **Pass** (`legacy_fallback_entries`; other thresholds may still warn) |
| `python -m pytest tests/test_repo_path_strict.py tests/test_grace_mar_paths.py -q` | **Pass** |
| `python scripts/check_repo_health.py --quick` | **Pass** |

## Remaining work

- Optional: migrate fork-revive scripts from `repo_io.BOT_DIR` to `strategy_codex.compat.grace_mar_paths`.
- Promote strict-path scan to required CI after operator approval.
- Root file budget (`root_files`) — separate complexity slice.
