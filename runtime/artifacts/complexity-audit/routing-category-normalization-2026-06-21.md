# Routing Category Normalization Receipt

**Date:** 2026-06-21

## What changed

- Added `category` to all **48** repo-map routes (path-first four-way model).
- Added **`statecraft-source-capture`** path_pattern route (`kind: source_capture`, `category: source`).
- Added `source_capture` to repo-map schema `kind` enum; `category` now required on every route.
- Replaced kind-only inference with `expected_route_category()` in `validate_repo_routing.py`.
- Generator hard-fails on missing category; regenerated `LLM-ROUTING.md`.
- Expanded routing tests (category coverage, four-quadrant check, blank-cell guard).
- Updated `docs/routing-reference.md` for required categories.
- Added manifest TODO comments for uncovered generated families.

## Categories

- `source` — 1 route
- `work` — 41 routes
- `generated` — 5 routes
- `archive` — 1 route

**4/4 quadrants represented.**

## Checks run

| Check | Result |
|---|---|
| `python scripts/validate_repo_routing.py --strict` | **Pass** |
| `python scripts/generate_llm_routing.py --check` | **Pass** |
| `python scripts/check_generated_surfaces.py --manifest-only` | **Pass** (6 entries) |
| `python scripts/check_generated_surfaces.py --headers-only --strict` | **Pass** |
| `python scripts/check_repo_path_strict.py` | **Pass** |
| `python scripts/check_repo_health.py --quick` | **Pass** |
| `pytest tests/test_routing_generated.py tests/test_check_generated_surfaces.py tests/test_strategy_codex_cli.py -q` | **15 passed** |

## Remaining work

- Retire legacy path fallbacks (`REPO_PATH_MIGRATIONS`).
- Enforce root file budget (fail mode).
- Complete generated manifest coverage (per-day day-index, month inventories).
- Trim README/start-here if still over budget.
- Optional: add `docs/archive/grace-mar.md` archive route for discoverability.
