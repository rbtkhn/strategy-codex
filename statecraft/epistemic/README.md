# Statecraft Epistemic Audit System

This directory contains the canonical epistemic tracking system for geopolitical voice analysis.

**Path:** `statecraft/epistemic/` — shadow Python package nested under the operator `statecraft/` channel. **Epistemic Audit PR1–PR5** stack. Distinct from historical prediction PR1–PR8 in [`recursive-learning-journal.md`](../recursive-learning-journal.md).

## Core Principle

Statecraft epistemic audit does **not** perform forecasting.

It tracks, structures, and analyzes predictions made by external epistemic agents (voices).

## Pipeline Layers (orthogonal responsibilities)

| Layer | Status | Role |

| --- | --- | --- |

| `observation/` | **PR2** | Pure ingestion — raw voice captures → observation objects |

| `structuring/` | **PR3** | Meaning mapping — event alignment, stance, confidence |

| `analysis/` | **PR4** | Cross-sectional comparison — divergence and voice spread only |

| `temporal/` | **PR5** | Pure ordering — timestamp sort and event grouping only |

| `plugins/` | future | Optional interpretive transformations |

| `pipeline/` | **PR5** | Full chain through temporal layer |

| `data/` | **PR2–PR5** | Generated epistemic-audit artifacts |

**Global rule:** No overlapping semantics across layers — no trend, regime-of-discourse, drift labels, or stability/fragmentation language in PR2–PR5.

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

## Layer outputs

**Observation (PR2):**

```json

{

  "observation_id": "...",

  "voice": "freeman",

  "raw_text": "...",

  "timestamp": "2026-...",

  "sentences": ["..."]

}

```

**Structuring (PR3):**

```json

{

  "observation_id": "...",

  "voice": "freeman",

  "event_id": "china_tariff_capitulation_2025",

  "prediction": "...",

  "stance": "high_confidence",

  "confidence": 0.85,

  "sentences": ["..."]

}

```

**Analysis (PR4):**

```json

{

  "event_id": "china_tariff_capitulation_2025",

  "cross_voice_divergence": 0.012,

  "voice_spread": {"freeman": 0.0, "macgregor": 0.0}

}

```

**Temporal (PR5):**

```json

{

  "event_id": "china_tariff_capitulation_2025",

  "timeline": [

    {"voice": "freeman", "time_index": 0, "confidence": 0.85, "timestamp": "2026-..."}

  ]

}

```

**Stability rules:**

- PR3/PR4 artifacts are **read-only** — temporal layer never mutates them

- Timestamps joined at runtime from PR2 observations; PR3 schema unchanged

- Not full time-series modeling — no derivatives, regime transitions, trend inference, or forecasting

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

python3 -m pytest tests/test_epistemic_temporal.py tests/test_epistemic_analysis.py tests/test_epistemic_structuring.py tests/test_epistemic_observation.py tests/test_statecraft_epistemic_namespace.py -q

python3 scripts/run_epistemic_observation.py --layer all

```

