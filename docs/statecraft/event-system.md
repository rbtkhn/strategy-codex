# Event system — prediction questions


## Core doctrine

> A prediction note records a voice's stance.
> An event records the falsifiable question.
> Evaluation belongs to the event, not the isolated note.

## What is an event?

An **event** is a shared, falsifiable question registered in [`statecraft/data/event-registry.json`](../../statecraft/data/event-registry.json). Multiple prediction notes attach to the same `event_id`.

Events are **operator-maintained** (not generated). Review new events before adding them to the registry.

## What is a prediction note?

A **prediction note** lives under [`statecraft/notes/predictions/`](../../statecraft/notes/predictions/). Each note records one voice stance on one event at one point in time.

## Required event fields

| Field | Required | Notes |
| --- | --- | --- |
| `question` | yes | Falsifiable question text |
| `resolution_criteria` | yes | How resolution is judged |
| `status` | yes | `open`, `resolved`, `void`, or `deprecated` |

## Optional event fields

`category`, `start_date`, `close_date`, `outcome`, `resolved_date`, `resolution_source`, `horizon_type`, `horizon_cite`, `closure_trigger`, `falsifier`, `confirmation_criteria`, `not_falsifiable`, `resolution_scope`, `review_note`, `tags`

### Extended fields (rev. 3 → v4 Phase 3)

| Field | Role |
| --- | --- |
| `falsifier` | What observable outcome would prove the prediction wrong |
| `confirmation_criteria` | What would support the stated position (optional asymmetric pair with falsifier) |
| `not_falsifiable` | `true` when event is explicitly non-scorable (diagnostic / trajectory umbrella only with operator flag) |
| `resolution_scope` | Which subclaim a resolution applies to (e.g. ceasefire durability) |
| `review_note` | **Explanatory only — non-semantic.** Human context; checkers must not branch on this field |

### v4 schema (Phase 3 — trajectory decomposition)

| Field | Values | Notes |
| --- | --- | --- |
| `event_type` | `atomic` \| `trajectory` | Trajectory when `dimensions[]` non-empty |
| `prediction_type` | `falsifiable_claim` \| `probabilistic_claim` \| `trajectory` \| `not_falsifiable` | Maps from legacy `not_falsifiable` |
| `horizon` | `short` \| `medium` \| `long` | Derived from `horizon_type` / `start_date` when unset |
| `dimensions` | `[{id, label, falsifier?, confirmation_criteria?}]` | **Replaces child registry rows** for trajectories |
| `outcome_record` | `pending` \| `correct` \| `incorrect` \| `mixed` \| `not_scorable` | Shelf scoring lane |
| `first_seen` / `last_seen` | ISO dates | From timeline or registry dates |

**Retired (v4):** `parent_event_id`, `child_event_ids` — presence is **ERROR** in `check_event_registry.py` / `check_phase3.py`.

**Changelog:** append-only [`statecraft/data/event-registry-changelog.jsonl`](../../statecraft/data/event-registry-changelog.jsonl); compile via `python3 scripts/prediction/registry_writer.py compile`.

**Capture map:** trajectory parent rows use optional `dimension` (non-registry pointer), not `child_event_id`.

### v4.5 schema (Phase 3.5 — probabilistic falsifier)

| Field | Role |
| --- | --- |
| `falsifier_model` | Optional structured failure modes when string `falsifier` is absent or insufficient |
| `falsifier_model.failure_modes[]` | `{id, condition, probability}` — probabilities sum to 1.0 |
| `falsifier_model.inference_source` | `heuristic_v1` (stub infer) or `operator` (authored) |
| `falsifier_model.entropy` | Shannon entropy of mode weights — high → review queue |

**Compile acceptance (tiered):** event passes if **any** of: non-empty `falsifier`, valid `falsifier_model`, or `not_falsifiable`. Structural gates (orphans, fingerprint collision, trajectory v4) remain **ERROR**.

**Operator rule:** explicit string `falsifier` beats inferred model on wire-grade Freeman rows; do not replace resolved falsifiers with inference.

**Pipeline:** `probabilistic_falsifier_engine` runs before `registry_writer compile` (in-memory enrich). Advisory scores: `runtime/artifacts/prediction-semantic-scores.json`.

### v4.5 signal layer (Phase 4.5 — directional intelligence)

Read-only derived view — **does not** mutate registry, falsifier models, or ERROR-tier CI.

| Artifact | Role |
| --- | --- |
| `runtime/artifacts/prediction-signals.json` | Per-event directional signals from effective probability snapshots |
| `runtime/artifacts/prediction-regime-summary.json` | Aggregated system-level escalation / alignment / regime-shift summary |

**Effective distribution:** persisted `falsifier_model` when present; otherwise `inferred_view` via `probabilistic_falsifier_engine` at signal-build time only.

**Signal types:** `directional` · `convergence` · `divergence` · `regime_shift` · `saturation` — advisory; cross-voice alignment uses entropy-weighted cosine similarity (Macgregor high-entropy voices down-weighted).

**Pipeline:** after timeline, disagreement, and semantic scores; before voice shelf rebuild. Checker: `check_prediction_signals.py --advisory`.

### PR3 / signal task system (predictive tasks — heuristic v1)

Reframes Phase 4.5 signals as **supervised task features** — not descriptive analytics alone.

| Artifact | Role |
| --- | --- |
| `runtime/artifacts/signal-prediction-tasks.json` | Labeled examples + stub predictions for regime shift, escalation delta, voice convergence |

**Tasks:** `regime_shift` · `delta` (P_t → P_future) · `convergence` (freeman / mercouris / macgregor)

**Label structure:** `event_id`, `anchor_date`, `time_offset` (default 30d), `signal_vector` (5-dim), `future_outcome`, `predicted_outcome` — every example requires `interpretation: supervised_task_example`.

**Signal vector dims:** `confidence` · `cross_voice_alignment` · `drift_tail_mean` · `regime_shift_detected` · `entropy_score`

**Operator rule:** top-level `interpretation: supervised_task_space`; `task_source: heuristic_v1` — not ML training output, not Record truth. Labels from timeline anchors only.

**Pipeline:** after signal check; before ENGM. Checker: `check_signal_prediction_tasks.py --advisory`.

### ENGM / PR1 (epistemic narrative generative model — heuristic v1)

Read-only latent-variable view — **voices are stochastic sensors**, not truth generators. **Does not** mutate registry or replace signal layer.

| Artifact | Role |
| --- | --- |
| `runtime/artifacts/epistemic-generative-state.json` | Shared latent `Z_t` + per-event `event_probability` + per-voice softmax projections |

**Latent dims (n=4):** `geopolitical_tension` · `regime_stability` · `alliance_coherence` · `escalation_pressure` — heuristic mapping from regime summary + signals (`inference_source: heuristic_v1`).

**Observation model:** `P(observation_class | Z, v) = softmax(W_v · Z + bias_v)` for `affirm_escalation` / `affirm_deescalation` / `withhold`. Macgregor high-entropy sensor down-weight (reuse 4.5).

**Operator rule:** all event blocks require `interpretation: probabilistic_projection`; probabilities clamped `[0.02, 0.98]` — never mirror registry `outcome` as deterministic truth.

**Pipeline:** after signal extraction check; before voice shelves. Checker: `check_epistemic_generative_state.py --advisory`.

### PR2 / calibration loss (epistemic calibration — heuristic v1)

Read-only **evaluation metric** — scores system quality for future tuning; **does not** train weights, mutate registry, or claim Record truth.

| Artifact | Role |
| --- | --- |
| `runtime/artifacts/epistemic-calibration-loss.json` | Unified loss `L` + per-event components |

**Loss (heuristic v1):** `L = α·prediction_error + β·brier_score + γ·entropy_misalignment + δ·regime_shift_delay` (default weights 0.35 / 0.35 / 0.15 / 0.15).

**Ground truth:** Brier and prediction error on **resolved registry events only** (`outcome` yes/no → `y_true`; ENGM `event_probability` → `y_pred`). Low-N advisory when resolved count &lt; 5 — WARN only, not ERROR.

**Entropy misalignment:** `|H(predicted) − H(observed)|` from pooled ENGM observation probs vs timeline stance histogram; optional overconfidence nudge on resolved wrong-direction calls.

**Regime shift delay:** timeline `shifts` vs current signal/regime flags (stub — no historical signal snapshots).

**Operator rule:** top-level `interpretation: calibration_metric`; `calibration_source: heuristic_v1` — not optimization output, not deterministic truth.

**Pipeline:** after ENGM check; before voice shelves. Checker: `check_epistemic_calibration_loss.py --advisory`.

### PR4 / epistemic dataset (ML-ready generator — heuristic v1)

Reproducible **train/test dataset** from the full epistemic stack — **does not** train models or mutate registry.

| Artifact | Role |
| --- | --- |
| `runtime/artifacts/epistemic-dataset.json` | Temporally split rows (`train` / `test`) with voice observations, latent features, task labels |

**Row grain:** one row per `event_id × anchor_date` — PR3 task labels consolidated in `task_labels`.

**Temporal split:** `train` when `anchor_date < T`; `test` when `anchor_date ≥ T` (default `T = 2026-01-01`). Prevents hindsight leakage via `outcome_censored`: registry `outcome` only when `resolved_date ≤ anchor_date`.

**Guarantees:** registry falsifier gate (dedup policy); compression checked in pipeline; `falsifier_model_snapshot` in-row only when missing — never registry write.

**Operator rule:** `interpretation: ml_ready_dataset`; `dataset_source: heuristic_v1` — generator only, not trained model output.

**Pipeline:** after calibration loss check; before voice shelves. Checker: `check_epistemic_dataset.py --advisory`.

### PR5 / baseline forecasts (evaluation — heuristic v1)

Statistical **baseline comparison** against ENGM — answers whether the epistemic stack beats naive probabilistic models.

| Artifact | Role |
| --- | --- |
| `runtime/artifacts/baseline-forecast-metrics.json` | Brier, accuracy, ECE, regime F1 per baseline on test split |

**Baselines (v1):** persistence (`P_{t+1}=P_t`); Beta–Bernoulli Bayesian update from voice stances; logistic trend on anchor time; transformer **deferred PR5b**.

**System reference:** ENGM `event_probability` — not a baseline; scored in `comparison.system_minus_persistence`.

**Evaluation lanes:** probability metrics on uncensored `outcome` rows only; regime F1 on all test rows vs `task_labels.regime_shift`.

**Low-N advisory:** WARN when `test_probability_n < 5` or `test_shift_support < 1` — current corpus is structurally valid but not yet discriminative.

**Operator rule:** `interpretation: baseline_evaluation`; `baseline_source: heuristic_v1` — evaluation only, not trained model output.

**Pipeline:** after epistemic dataset check; before voice shelves. Checker: `check_baseline_forecasts.py --advisory`.

### PR6 / ablation study (subsystem contribution — heuristic v1)

In-process **ablation evaluation** — measures Brier `performance_drop` when each subsystem is disabled vs full stack.

| Artifact | Role |
| --- | --- |
| `runtime/artifacts/ablation-study.json` | Per-variant core + structural metrics; `drops[]` with Brier delta |

**Variants (v1):** full; no_compression; no_falsifier_model; no_signal_extraction; no_disagreement_graph.

**Drop metric:** `performance_drop = variant.brier - full.brier` (positive = subsystem contributes; variant worse when disabled).

**Structural diagnostics:** entropy stability, graph coherence, cross-voice alignment mean — not used for drop scalar in v1.

**Low-N advisory:** WARN when `test_probability_n < 5` — drops may be `null` with `"note": "low_n"`.

**Operator rule:** `interpretation: ablation_evaluation`; `ablation_source: heuristic_v1` — no registry mutation, no subprocess pipeline reruns.

**Pipeline:** after baseline forecasts check; before voice shelves. Checker: `check_ablation_study.py --advisory`.

### PR7 / MVEL — multi-voice extraction layer (heuristic v1)

Capture-map–grounded **multi-voice trajectory extraction** — aligned probabilistic claim paths over shared events.

| Artifact | Role |
| --- | --- |
| `runtime/artifacts/multivoice-extracted-dataset.json` | Combined cross-voice trajectories |
| `runtime/artifacts/event-alignment-map.json` | Matched + unmatched (review queue) audit |
| `runtime/artifacts/voice-trajectories-{speaker}.json` | Per-voice trajectory slices |

**Claim SSOT:** curated capture-map `public_excerpt` rows — not archive NLP sentence scan.

**Alignment:** validate `event_id` against registry; optional `prediction_object_terms` fallback; **unmatched → review queue only** — no registry mutation.

**Probabilities:** heuristic v1 stance map (`yes→0.75`, `no→0.25`, …) + speech_act confidence; clamped `[0.02, 0.98]`.

**Cross-voice:** `alignment_score` via entropy-weighted cosine on latest per-voice probabilities; Macgregor down-weight at high entropy.

**Operator rule:** `interpretation: multivoice_extraction`; `extraction_source: heuristic_v1`; `registry_mutation: false` — advisory only, not Record truth.

**Pipeline:** after semantic scores; before signal extraction. Checker: `check_multivoice_extraction.py --advisory`.

### Status vs record (shelf lane)

| Layer | SSOT | Values |
| --- | --- | --- |
| **Registry** | `event-registry.json` | `status`: open · resolved · void · deprecated; `outcome`: yes · no · null |
| **Shelf record label** | generated from registry + timeline | Correct · Open — consistent · Open — shifted · Open — trajectory · … |

Generated Markdown must **not** invent ambiguity. Nuance lives in registry fields (`resolution_scope`, `review_note`), not in hand-edited shelf prose.

### Wire resolution stubs

Registry closure for wire-grade events uses canonical stubs:

```text
statecraft/notes/wire/prediction-resolution-<event-id>.md
```

Example: `prediction-resolution-gaza-ceasefire-holds-2025.md` for `gaza_ceasefire_holds_2025`.

Set `resolution_source` to stub path + anchor (e.g. `#resolution-decision`). Do not create ad hoc closure filenames outside this pattern.

## Event horizons (voice-sourced only)

Do **not** embed operator calendar windows in `question` text (year-end pilots, H1 slices, news-cycle deadlines) unless the **voice explicitly stated that date** in the source capture.

| Field | When to use |
| --- | --- |
| `close_date` | Only when the voice **named a calendar date** in speech for the falsifier. Otherwise `null`. |
| `closure_trigger` | When the voice gave an **event-closure condition** (e.g. resume fighting, deal reached) without a calendar end. |
| `horizon_type` | `none` · `freeman_date` · `freeman_event_closure` — audit label for Freeman pilot rows. |
| `horizon_cite` | Archive path + short quote stub documenting the horizon source. |
| `resolved_date` | When the operator or wire **judged** the outcome, or when an **observable event** occurred — not a stand-in for a voice deadline that was never spoken. |

Pilot convenience windows are **forbidden** in registry questions.

## Allowed statuses

```text
open
resolved
void
deprecated
```

## Allowed outcomes

```text
yes
no
null
```

Rules:

- `outcome` must be `null` unless `status == "resolved"`.
- When `status == "resolved"`, `outcome` must be `yes` or `no`.

## Event ID naming

- Lowercase **snake_case** only
- Unique across the registry
- Preferred pattern: `<actor>_<object>_<outcome>`

Examples:

```text
russia_odessa_control
us_bitcoin_reserve_passage
china_taiwan_blockade
fed_rate_cut_2026_h1
```

## Prediction note frontmatter

```yaml
---
note_type: prediction
event_id: russia_odessa_control
speaker: mercouris
date_made: 2025-03-10
stance: no
confidence: medium
source: source-archive/statecraft/2025-03-10/example.md
status: pending
---
```

Required: `event_id`, `speaker`, `date_made`, `stance`, `source`, `status` (`pending` | `resolved`).

Allowed stances: `yes`, `no`, `conditional`, `uncertain`.

Optional confidence: `low`, `medium`, `high`.

Prediction notes must **not** be promoted to shelf-native doctrinal notes without explicit review.

## Validation

```bash
python3 scripts/check_event_registry.py
python3 scripts/check_event_registry.py --strict-enrolled
python3 scripts/validate_all_schemas.py --scope prediction
python3 scripts/check_event_integrity.py
python3 scripts/check_statecraft_notes.py --warn
```

## Related

- [prediction-system.md](prediction-system.md) — lifecycle model
- [prediction-metrics.md](prediction-metrics.md) — registry and accuracy
- [prediction-analysis.md](prediction-analysis.md) — disagreement and timeline
- [schema-system.md](../system/schema-system.md) — registry and validator
