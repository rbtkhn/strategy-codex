# Statecraft Epistemic Audit System

This directory contains the canonical epistemic tracking system for geopolitical voice analysis.

**Path:** `statecraft/epistemic/` — shadow Python package nested under the operator `statecraft/` channel. This is **Epistemic Audit PR1** (structural foundation only); it is distinct from historical prediction PR1–PR8 documented in [`recursive-learning-journal.md`](../recursive-learning-journal.md).

## Core Principle

Statecraft epistemic audit does **not** perform forecasting.

It tracks, structures, and analyzes predictions made by external epistemic agents (voices).

## Pipeline Layers

1. `observation/` → raw voice captures
2. `structuring/` → normalized prediction objects
3. `analysis/` → temporal and regime-level behavior tracking
4. `plugins/` → optional interpretive transformations
5. `pipeline/` → orchestration layer
6. `data/` → generated epistemic-audit artifacts (future)

## Data Split

| Surface | Path | Role |
| --- | --- | --- |
| Operator SSOT | [`statecraft/data/`](../data/) | Event registry, capture maps — operator-maintained |
| Generated artifacts (today) | [`runtime/artifacts/`](../../runtime/artifacts/) | `epistemic_state.json`, `signals.json`, `regimes.json` |
| Generated artifacts (future) | `statecraft/epistemic/data/` | Shadow migration target for epistemic-audit outputs |

Do not conflate operator-maintained JSON under `statecraft/data/` with generated outputs under `statecraft/epistemic/data/`.

## Design Constraint

All **new** epistemic Python logic MUST reside within `statecraft/epistemic/`.

No external inference systems are considered authoritative without explicit migration.

## Current Canonical Pipeline (unchanged in PR1)

The live epistemic pipeline remains under `scripts/prediction/` (episystem canonical). See [event-system.md — Episystem canonical](../../docs/statecraft/event-system.md#episystem-canonical-single-epistemic-pipeline--heuristic-v1) and [prediction-system.md](../../docs/statecraft/prediction-system.md).

PR1 introduces the shadow namespace only — no runtime behavior changes, no import rewiring, no pipeline replacement.

## Migration Map (PR2+)

Documentation-only forward map; no code moves in PR1.

| Future layer | Current canonical (unchanged) |
| --- | --- |
| `observation/` | Capture maps in `statecraft/data/*-prediction-capture-map.json`; source archive |
| `structuring/` | Registry compile / `statecraft/notes/predictions/` |
| `analysis/` | `scripts/prediction/epistemic_core.py`, `soft_alignment.py` |
| `plugins/` | `scripts/prediction/plugins/` |
| `pipeline/` | `scripts/run_prediction_pipeline.py`, `scripts/prediction/run_pipeline.py` |
| `data/` | `runtime/artifacts/epistemic_*.json` (generated) |

## Non-goals (PR1)

This PR does **not**:

- implement observation parsing
- implement structuring logic
- implement analysis engines
- modify existing prediction systems
- introduce SAL / MVEL / EIC logic
- replace `statecraft/predictions/`, `statecraft/data/`, or `scripts/prediction/`

## Validation

Expected behavior:

- repo builds successfully
- no import changes required
- existing pipelines unaffected
- `statecraft/epistemic/` exists but unused

Optional CI: `tests/test_statecraft_epistemic_namespace.py`
