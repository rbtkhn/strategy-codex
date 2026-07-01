# Statecraft Epistemic Audit System

This directory contains the canonical epistemic tracking system for geopolitical voice analysis.

**Path:** `statecraft/epistemic/` — shadow Python package nested under the operator `statecraft/` channel. **Epistemic Audit PR1** structure; **PR2** observation; **PR3** structuring; **PR4** analysis. Distinct from historical prediction PR1–PR8 in [`recursive-learning-journal.md`](../recursive-learning-journal.md).

## Core Principle

Statecraft epistemic audit does **not** perform forecasting.

It tracks, structures, and analyzes predictions made by external epistemic agents (voices).

## Pipeline Layers

| Layer | Status | Role |
| --- | --- | --- |
| `observation/` | **PR2 implemented** | Ingest raw voice captures → observation objects |
| `structuring/` | **PR3 implemented** | Event alignment + stance normalization |
| `analysis/` | **PR4 implemented** | Drift, divergence, regime-of-discourse |
| `plugins/` | future | Optional interpretive transformations |
| `pipeline/` | **PR4 partial** | Full chain: observation → structuring → analysis |
| `data/` | **PR2–PR4 output** | Generated epistemic-audit artifacts |

## Observation Layer (PR2)

**Input:** `observation/voice_captures/<voice>/*.md` — raw markdown captures (fixtures seeded; operator adds files manually).

**Output:** `data/observations.json` — generated envelope with deterministic observation objects.

**Run:**

```bash
python3 scripts/run_epistemic_observation.py
python3 scripts/run_epistemic_observation.py --dry-run
```

PR2 answers only: *what did each voice say?*

## Structuring Layer (PR3)

**Input:** `data/observations.json` + read-only [`statecraft/data/event-registry.json`](../data/event-registry.json).

**Output:** `data/structured_predictions.json` — normalized, event-aligned prediction records.

**Run:**

```bash
python3 scripts/run_epistemic_structuring.py
python3 scripts/run_epistemic_observation.py --layer structuring
```

PR3 introduces cross-voice comparability via shared event space and schema.

## Analysis Layer (PR4)

**Input:** `data/structured_predictions.json` (PR3 output).

**Output:** `data/analysis.json` — per-event analysis records + global summary.

**Run:**

```bash
python3 scripts/run_epistemic_analysis.py
python3 scripts/run_epistemic_observation.py --layer analysis
python3 scripts/run_epistemic_observation.py --layer all
```

**Per-event analysis record:**

```json
{
  "event_id": "china_tariff_capitulation_2025",
  "voice_drift": { "freeman": 0.0 },
  "cross_voice_divergence": 0.0,
  "regime_of_discourse": "stability",
  "trend": "stable discourse"
}
```

**Regime-of-discourse labels:** `fragmentation` | `stability` | `transition` | `convergence` — meta-pattern of disagreement structure, not geopolitical regime.

**Temporal note:** PR3 structured objects carry no timestamp. PR4 “drift” is confidence spread (`max - min`) per voice within scope until time-series enrichment lands in a future PR.

PR4 analyzes system-level behavior only — no truth assignment, event inference, or structured-data mutation.

## Data Split

| Surface | Path | Role |
| --- | --- | --- |
| Operator SSOT | [`statecraft/data/`](../data/) | Event registry, capture maps — operator-maintained (read-only input) |
| Generated artifacts (legacy) | [`runtime/artifacts/`](../../runtime/artifacts/) | `epistemic_state.json`, `signals.json`, `regimes.json` |
| Generated artifacts (shadow) | `statecraft/epistemic/data/` | `observations.json`, `structured_predictions.json`, `analysis.json` |

## Design Constraint

All **new** epistemic Python logic MUST reside within `statecraft/epistemic/`.

No external inference systems are considered authoritative without explicit migration.

## Legacy Pipeline (unchanged)

The live epistemic pipeline remains under `scripts/prediction/` (episystem canonical). PR4 does not replace or call it.

## Migration Map

| Shadow layer | Current canonical | Status |
| --- | --- | --- |
| `observation/` | Capture maps + source archive | Partial — `voice_captures/` only |
| `structuring/` | Registry compile / prediction notes | **PR3** |
| `analysis/` | `epistemic_core.py`, `soft_alignment.py` | **PR4** — shadow drift/divergence/regime |
| `plugins/` | `scripts/prediction/plugins/` | Not started |
| `pipeline/` | `scripts/run_prediction_pipeline.py` | Full PR2–PR4 chain |
| `data/` | `runtime/artifacts/epistemic_*.json` | All three shadow artifacts |

## Validation

```bash
python3 -m pytest tests/test_epistemic_observation.py tests/test_epistemic_structuring.py tests/test_epistemic_analysis.py -q
python3 scripts/run_epistemic_observation.py --layer all
```
