# Wave 2 Platform Path Fallback Readiness Receipt

**Date:** 2026-06-21

## What changed

- Audited Wave 2 platform subpath fallback readiness.
- Verified canonical paths for Wave 2 keys.
- Checked for active root-level legacy references in `scripts/`, `tests/`, and `platform/`.
- Added `readiness: ready` to Wave 2 entries in [`path-fallback-retirement.yaml`](../../../path-fallback-retirement.yaml).
- Added `collect_wave_readiness_report()` and `keys_for_wave()` in [`scripts/repo_io.py`](../../../scripts/repo_io.py).
- Extended [`scripts/check_repo_path_strict.py`](../../../scripts/check_repo_path_strict.py) with `--wave N` and `--strict-readiness`.
- Added regression tests in [`tests/test_repo_path_strict.py`](../../../tests/test_repo_path_strict.py) documenting that Wave 2 is still fallback-bearing but ready for removal.

**Runtime resolver behavior unchanged** — no Wave 2 fallback tuples removed.

## Wave 2 keys

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

## Results

| Key | Readiness |
|---|---|
| `app` | ready |
| `bin` | ready |
| `config` | ready |
| `deployment` | ready |
| `extension` | ready |
| `integrations` | ready |
| `miniapp` | ready |
| `profile` | ready |
| `template` | ready |
| `users` | ready |

## Checks run

| Check | Result |
|---|---|
| `python scripts/check_repo_path_strict.py` | **Pass** |
| `python scripts/check_repo_path_strict.py --strict` | **Pass** |
| `python scripts/check_repo_path_strict.py --wave 2` | **Pass** (10/10 ready) |
| `python scripts/check_repo_path_strict.py --wave 2 --json` | **Pass** |
| `python -m pytest tests/test_repo_path_strict.py -q` | **17 passed** |
| `python scripts/check_repo_health.py --quick` | **Pass** |

## Remaining work

- Remove Wave 2 fallback tuple tails in a separate PR (expected fallback count: 16 → 6).
- Keep Wave 3 and Wave 4 untouched.
