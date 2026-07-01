# Statecraft Epistemic Audit System

This directory contains the canonical epistemic tracking system for geopolitical voice analysis.

**Path:** `statecraft/epistemic/` — shadow Python package nested under the operator `statecraft/` channel. **Epistemic Audit PR1** established structure; **PR2** implements the observation layer. Distinct from historical prediction PR1–PR8 in [`recursive-learning-journal.md`](../recursive-learning-journal.md).

## Core Principle

Statecraft epistemic audit does **not** perform forecasting.

It tracks, structures, and analyzes predictions made by external epistemic agents (voices).

## Pipeline Layers

| Layer | Status | Role |
| --- | --- | --- |
| `observation/` | **PR2 implemented** | Ingest raw voice captures → observation objects |
| `structuring/` | PR3+ | Normalized prediction objects |
| `analysis/` | PR4+ | Temporal and regime-level behavior tracking |
| `plugins/` | future | Optional interpretive transformations |
| `pipeline/` | **PR2 partial** | Orchestration (`run_observation_layer`) |
| `data/` | **PR2 output** | Generated epistemic-audit artifacts |

## Observation Layer (PR2)

**Input:** `observation/voice_captures/<voice>/*.md` — raw markdown captures (fixtures seeded; operator adds files manually).

**Output:** `data/observations.json` — generated envelope with deterministic observation objects.

**Run:**

```bash
python3 scripts/run_epistemic_observation.py
python3 scripts/run_epistemic_observation.py --dry-run
```

**Schema (observation object):**

```json
{
  "observation_id": "<uuid5>",
  "voice": "macgregor",
  "source_file": "statecraft/epistemic/observation/voice_captures/macgregor/sample.md",
  "raw_text": "...",
  "timestamp": "2026-01-23T12:00:00+00:00",
  "extracted_sentences": ["..."]
}
```

PR2 answers only: *what did each voice say?* No event alignment, probabilities, signals, or regimes.

## Data Split

| Surface | Path | Role |
| --- | --- | --- |
| Operator SSOT | [`statecraft/data/`](../data/) | Event registry, capture maps — operator-maintained |
| Generated artifacts (legacy) | [`runtime/artifacts/`](../../runtime/artifacts/) | `epistemic_state.json`, `signals.json`, `regimes.json` |
| Generated artifacts (shadow) | `statecraft/epistemic/data/` | `observations.json` and future layer outputs |

Do not conflate operator-maintained JSON under `statecraft/data/` with generated outputs under `statecraft/epistemic/data/`.

## Design Constraint

All **new** epistemic Python logic MUST reside within `statecraft/epistemic/`.

No external inference systems are considered authoritative without explicit migration.

## Legacy Pipeline (unchanged)

The live epistemic pipeline remains under `scripts/prediction/` (episystem canonical). PR2 does not replace or call it. See [event-system.md — Episystem canonical](../../docs/statecraft/event-system.md#episystem-canonical-single-epistemic-pipeline--heuristic-v1).

## Migration Map

| Shadow layer | Current canonical | PR2 status |
| --- | --- | --- |
| `observation/` | Capture maps + source archive | Partial — `voice_captures/` only; capture-map bridge deferred |
| `structuring/` | Registry compile / `statecraft/notes/predictions/` | Not started |
| `analysis/` | `scripts/prediction/epistemic_core.py`, `soft_alignment.py` | Not started |
| `plugins/` | `scripts/prediction/plugins/` | Not started |
| `pipeline/` | `scripts/run_prediction_pipeline.py` | Observation hook only |
| `data/` | `runtime/artifacts/epistemic_*.json` | `observations.json` only |

## Validation

```bash
python3 -m pytest tests/test_epistemic_observation.py -q
python3 scripts/run_epistemic_observation.py
python3 scripts/check_repo_health.py --quick
```
