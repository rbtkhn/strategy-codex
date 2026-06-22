# Wave 4 Grace-Mar Compatibility Fallback Readiness Receipt

**Date:** 2026-06-21

## What changed

- Audited Wave 4 Grace-Mar compatibility fallback readiness.
- Fixed and hardened [`platform/src/strategy_codex/compat/grace_mar_paths.py`](../../../platform/src/strategy_codex/compat/grace_mar_paths.py) — was broken (`ImportError` importing `REPO_ROOT` from `grace_mar.repo_io`).
- Repo root now derived from `__file__` (canonical-only helpers; no legacy fallback in compat module).
- Added `bootstrap_dir()` helper alongside `bot_dir()`, `recursion_gate_staging_dir()`, `grace_mar_instance_dir()`.
- Verified canonical archive paths exist; checked active root-level legacy references (0 active refs).
- Added `readiness: ready` to Wave 4 entries in [`path-fallback-retirement.yaml`](../../../path-fallback-retirement.yaml).
- Added [`tests/test_grace_mar_paths.py`](../../../tests/test_grace_mar_paths.py) and Wave 4 readiness/guard tests in [`tests/test_repo_path_strict.py`](../../../tests/test_repo_path_strict.py).

**Runtime resolver behavior unchanged** — Wave 4 fallback tuples remain in `REPO_PATH_MIGRATIONS`.

## Wave 4 keys

- `bot`
- `recursion-gate-staging`
- `bootstrap`

## Results

| Key | Readiness |
|---|---|
| `bot` | ready |
| `recursion-gate-staging` | ready |
| `bootstrap` | ready |

## Compat module fix

| Before | After |
|---|---|
| Imported `REPO_ROOT` / `resolve_repo_path` from `grace_mar.repo_io` (wrong root: `platform/`) | `_REPO_ROOT = Path(__file__).resolve().parents[4]` |
| Missing `bootstrap_dir()` | All three archive subpaths + instance root exposed |

## What did not change

- Wave 4 fallback tuple tails in `scripts/repo_io.py` (audit slice only).
- `BOT_DIR = resolve_repo_path("bot")` in `repo_io.py` — follow-up migration target.
- Archive files not moved or deleted.
- Internal `grace_mar` package unchanged.

## Checks run

| Check | Result |
|---|---|
| `python scripts/check_repo_path_strict.py` | **Pass** |
| `python scripts/check_repo_path_strict.py --strict` | **Pass** |
| `python scripts/check_repo_path_strict.py --wave 4` | **Pass** (3/3 ready) |
| `python scripts/check_repo_path_strict.py --wave 4 --json` | **Pass** |
| `python scripts/check_repo_path_strict.py --wave 4 --strict-readiness` | **Pass** |
| `python -m pytest tests/test_repo_path_strict.py tests/test_grace_mar_paths.py -q` | **Pass** |
| `python scripts/check_repo_health.py --quick` | **Pass** |

## Remaining work

- Migrate Grace-Mar-only callers to `strategy_codex.compat.grace_mar_paths`.
- Remove Wave 4 fallback tuple tails in a separate PR (`legacy: []` / `keep_no_legacy` in YAML).
- **Fallback count: 3 → 0** — completes path-fallback retirement program.
