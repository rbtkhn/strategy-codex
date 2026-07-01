# Statecraft Epistemic Audit System

This directory contains the canonical epistemic tracking system for geopolitical voice analysis.

**Path:** `statecraft/epistemic/` — shadow Python package nested under the operator `statecraft/` channel. **Epistemic Audit PR1–PR5** stack. Distinct from historical prediction PR1–PR8 in [`recursive-learning-journal.md`](../recursive-learning-journal.md).

## Core Principle

Statecraft epistemic audit does **not** perform forecasting.

It tracks, structures, and analyzes predictions made by external epistemic agents (voices).

## Pipeline Layers

| Layer | Status | Role |
| --- | --- | --- |
| `observation/` | **PR2** | Ingest raw voice captures → observation objects |
| `structuring/` | **PR3** | Event alignment + stance normalization |
| `analysis/` | **PR4** | Drift, divergence, regime-of-discourse |
| `temporal/` | **PR5** | Ordering, grouping, weak trend scaffolding |
| `plugins/` | future | Optional interpretive transformations |
| `pipeline/` | **PR5** | Full chain through temporal layer |
| `data/` | **PR2–PR5** | Generated epistemic-audit artifacts |

## Run (full chain)

```bash
python3 scripts/run_epistemic_observation.py --layer all
```

Individual layers:

```bash
python3 scripts/run_epistemic_observation.py          # observation
python3 scripts/run_epistemic_structuring.py          # structuring
python3 scripts/run_epistemic_analysis.py             # analysis
python3 scripts/run_epistemic_temporal.py             # temporal
```

## Temporal Scaffolding (PR5)

**Input:** `data/structured_predictions.json` + `data/observations.json` (timestamp join via `observation_id`).

**Output:** `data/temporal.json` — per-event timelines + weak trend labels.

**Per-event temporal record:**

```json
{
  "event_id": "china_tariff_capitulation_2025",
  "timeline": [
    {"voice": "freeman", "time_index": 0, "confidence": 0.85, "timestamp": "2026-..."}
  ],
  "trend": "stable",
  "ordering_confidence": 1.0
}
```

**Trend labels:** `slight_increase` | `slight_decrease` | `stable` (confidence delta ±0.1 on ordered series).

**Stability rules:**

- PR3/PR4 artifacts are **read-only** — temporal layer never mutates them
- Timestamps joined at runtime from PR2 observations; PR3 schema unchanged
- Not full time-series modeling — no derivatives, regime transitions, or forecasting

## Data Split

| Surface | Path | Role |
| --- | --- | --- |
| Operator SSOT | [`statecraft/data/`](../data/) | Event registry, capture maps — read-only input |
| Generated artifacts (legacy) | [`runtime/artifacts/`](../../runtime/artifacts/) | episystem outputs |
| Generated artifacts (shadow) | `statecraft/epistemic/data/` | observations, structured_predictions, analysis, temporal |

## Legacy Pipeline (unchanged)

The live epistemic pipeline remains under `scripts/prediction/` (episystem canonical).

## Validation

```bash
python3 -m pytest tests/test_epistemic_temporal.py tests/test_epistemic_analysis.py tests/test_epistemic_structuring.py tests/test_epistemic_observation.py -q
python3 scripts/run_epistemic_observation.py --layer all
```
