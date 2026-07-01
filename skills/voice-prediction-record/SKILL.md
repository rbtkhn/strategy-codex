---
name: voice-prediction-record
description: "Curate and rebuild a speaker prediction shelf from archive captures: public map, capture-map rows with verbatim excerpts, wire closure, and generated JSON/MD. Triggers: voice prediction record, prediction record, capture map recurate, rebuild predictions. Parameter: speaker slug (freeman, mercouris, …). Not synthesis or auto-file without curated rows."
preferred_activation: voice prediction record
activation: voice prediction record
portable: true
version: 0.3.0
category: truth-pipeline
status: active
scope_class: repo-governed
tags:
  - statecraft
  - voices
  - predictions
  - source-archive
requires:
  - news-verify
outputs:
  - "<speaker>-predictions.md"
  - "<speaker>-predictions.json"
  - "<speaker>-prediction-capture-map.json"
---
# Voice prediction record

**Preferred activation:** **`voice prediction record <speaker>`** — e.g. **`voice prediction record freeman`**. Aliases: **`prediction record`**, **`capture map recurate`**, **`rebuild predictions`**.

**Parameter:** **`<speaker>`** — voice slug matching `statecraft/voices/<speaker>/` (e.g. `freeman`, `mercouris`, `mearsheimer`). If omitted, ask which voice before editing maps or running builders.

**Scope:** WORK-only **prediction shelf** — curated **capture-map rows** joined to shared **event registry** events, with **verbatim public excerpts** from archive captures. Default **Ship** when operator names recuration or rebuild; **Think** when comparing event design only.

**Not in scope:**

- **Source intake** — land captures first ([`statecraft-source-intake`](../statecraft-source-intake/SKILL.md)).
- **Helix / daily synthesis** — route to [`state-synthesis`](../state-synthesis/SKILL.md) after the shelf exists.
- **Synthesizing quotes** — `public_excerpt_raw` must be a **capture substring**; **`public_excerpt`** may be display-repaired only when **`asr_repair`** documents the change (see below).
- **Record merge** or wire-grade closure without operator decision on resolution stubs.

## Layer law

| Layer | Role |
|-------|------|
| **Source archive** | Verbatim capture SSOT — read body for excerpt alignment |
| **Public map** | Per-event operator framing: title, summary, scoring, **`prediction_object_terms`** |
| **Capture map** | Curated rows: stance, speech_act, speaker attribution, **raw + display excerpts**, ASR repair metadata |
| **Event registry** | Shared falsifiable events (`status`, `outcome`, closure dates) |
| **Generated shelf** | `<speaker>-predictions.json` / `.md` — **do not hand-edit** |

Notebook / chat synthesis **links** to the shelf; it does not replace capture-map curation.

## Artifact families (per speaker)

Replace `<speaker>` with the voice slug:

| Artifact | Purpose |
|----------|---------|
| `<speaker>-prediction-public-map.json` | Event metadata + **`prediction_object_terms`** (required per event) |
| `<speaker>-prediction-capture-map.json` | Curated appearance rows + excerpts |
| `<speaker>-prediction-thesis-map.json` | Optional related-event / title-conflict patterns |
| `<speaker>-prediction-auto-file.json` | Optional auto-materialize hooks (calibration lane) |
| `<speaker>-predictions.md` / `.json` | Generated public record |
| `<speaker>-prediction-wire-events.md` | Operator index: wire stubs, rebuild chain, checklist |

**Reference implementation:** Freeman (`freeman-predictions-v3` capture-map contract) — see host appendix for paths and rebuild chain.

## Read order (before editing)

1. **Public map** — confirm every pilot event has required fields and non-empty **`prediction_object_terms`**.
2. **Event registry** — `status`, `outcome`, horizons for closure-aware labels.
3. **Capture map** — row list; note `anchor_capture` overrides on public map when present.
4. **Archive bodies** — bounded `Read` on captures referenced by rows being edited (not repo-wide grep).
5. **Wire-events page** — closure stubs and related-event pairs for the speaker.

## Capture-map row schema

Required keys: **`event_id`**, **`capture`**, **`stance`**, **`speech_act`**, **`public_excerpt`**.

**Normalized on load** (defaults keep Mercouris stub rows green):

| Field | Default | Role |
|-------|---------|------|
| `quote_speaker` | guest slug (`freeman`, `mercouris`, …) | Who speaks in the display quote |
| `public_excerpt_raw` | copy of `public_excerpt` | Verbatim capture substring — **audit SSOT** |
| `public_excerpt` | copy of raw or repaired display | Rendered in JSON/MD |
| `asr_repair` | `none` | Repair tier (see ASR table) |
| `asr_repair_notes` | `[]` | Required when `asr_repair` is `punctuation_capitalization_obvious_asr` |
| `public_display` | `true` | `false` → JSON audit only; omitted from public MD source trail |

**`quote_speaker` values**

| Value | Public MD | Rules |
|-------|-----------|-------|
| guest slug (`freeman`, …) | blockquote | Normal excerpt quality gates |
| `mixed` | **Host setup:** + blockquote + **Context:** | Requires `host_setup` + `context_note` |
| `host` | never (when `public_display: false`) | Host question / framing only |
| `operator_summary` | never | Summary-grade row; `asr_repair: not_public_verbatim` typical |

Optional keys (unchanged + extensions):

| Field | Use |
|-------|-----|
| `appearance_date` | When episode date differs from capture folder date (dedupe in builder) |
| `host_setup` | Host question or framing for **`mixed`** rows |
| `context_note` | Operator framing when excerpt alone lacks object terms; required for **`mixed`** |
| `excerpt_exception` | Only **`short_decisive_sentence`** (requires `context_note`) |
| `prediction_object_terms` | Row-level override of public-map terms |
| `dimension` | Trajectory parent only — non-registry dimension id (replaces deprecated `child_event_id`) |
| `anchor_context_note` | Legacy alias — prefer `context_note` on anchor row |

**Speech acts:** `initial`, `restated`, `iterated`, `self_acknowledged_correct`, `self_acknowledged_incorrect`, `outcome_commentary`.

## ASR repair tiers (`asr_repair`)

| Value | `public_excerpt` vs capture |
|-------|----------------------------|
| `none` | Display must be capture substring (same as raw policy) |
| `punctuation_capitalization` | Display may fix caps/punctuation only |
| `punctuation_capitalization_filler_boundary` | Above + remove filler at phrase boundaries (`um`, `uh`) |
| `punctuation_capitalization_obvious_asr` | Above + conservative obvious ASR (`Israel is is`, `Husalah`→Hezbollah); **requires `asr_repair_notes`** |
| `not_public_verbatim` | Operator summary / non-quote row (`operator_summary`) |

**Invariant:** `public_excerpt_raw` is always validated as a capture substring. Display divergence is allowed only when `asr_repair != none`.

## Excerpt quality rules (non-negotiable)

Enforced by `bootstrap_voice_capture_map.py --check`, builder, and checker via `voice_prediction_pilot.py`:

### Substring proof

1. **`public_excerpt_raw`** — must appear in capture body after normalization. Multi-segment raw uses ` ||| `; each segment must match.
2. **`public_excerpt`** — when `asr_repair == none`, must also be a capture substring. When `asr_repair != none`, skip display substring check; enforce repair tier + notes instead.

### Speaker gates

3. **`host`** + `public_display: true` → fail. Same for **`operator_summary`**.
4. **`mixed`** — non-empty **`host_setup`**, **`public_excerpt`**, and **`context_note`** required.
5. **Guest / mixed** with `public_display: true` — excerpt quality rules below apply to **`public_excerpt`** (display text).

### Display quality

6. **Word floors** — anchor rows: **≥40 words**; appearance rows: **≥30 words**, unless `excerpt_exception: short_decisive_sentence` + `context_note`.
7. **Prediction object** — anchor excerpt must hit **`prediction_object_terms`** (public map or row override). Appearances need object terms **or** non-empty **`context_note`**.
8. **Complete sentence** — display ends with `.!?` **or** is a verified verbatim fragment when `asr_repair == none`.
9. **Not title-like** — question titles, host lines, episode titles fail unless `short_decisive_sentence` + `context_note`.
10. **Ambiguous starts** — `if this`, `they`, `he`, etc. fail when object terms are absent.
11. **Host leakage** — guest excerpts must not contain host-address tokens (`Ambassador`, `as we speak`, `Chris cut number`, …) unless `quote_speaker: mixed`.
12. **Obvious ASR fragments** — display must not contain patterns like `Israel is is`, `Husalah`, mid-word clips (`do`, `yes`, leading `um`/`uh`).
13. **Dangling ends** — display must not end on `rather`, `and`, `the`, `but`, `even`, etc.
14. **Max length** — **80 words** per display excerpt unless operator splits with ` ||| ` (each segment ≤80).

### Recuration discipline

15. **Extend raw first** — when ASR tails truncate, extend **`public_excerpt_raw`** to the next contiguous verbatim span in the same capture before applying display repair.
16. **No silent synthesis** — do not invent closing sentences; documented repair only via **`asr_repair`** + **`asr_repair_notes`**.

## Markdown rendering (generated shelf)

### Event anchor block

- **Guest quote:** `> "…"` (optional `context_note` above quote when not `mixed`).
- **Mixed:** `**Host setup:** …` + blockquote + `**Context:** …` (same shape as source-trail excerpt cell).
- **`public_display: false`** — row stays in JSON; excluded from source-trail table.

### Source trail table (public-facing)

Each event section includes one collapsible **Source trail** with this header (**required** — checker fails on legacy headers):

```md
| Date | Channel | Episode | Stance | Excerpt |
| --- | --- | --- | --- | --- |
```

**Deprecated (must not appear):** `Date | Appearance | Stance | Exact words` · `Date | Appearance | Stance | Verbatim excerpt`

| Column | Source | Notes |
|--------|--------|-------|
| **Date** | `appearance.date` | Use `appearance_date` on capture row when deduping same capture |
| **Channel** | `citation.channel` | e.g. Judging Freedom, Dialogue Works |
| **Episode** | `citation.title` | `[title](youtube_url)` when URL present; plain title otherwise |
| **Stance** | `stance` | `yes` / `no` / `uncertain` |
| **Excerpt** | `public_excerpt` (+ speaker metadata) | Guest: `"…"` or `context — "…"`; mixed: host setup + blockquote + context |

Builder SSOT: `SOURCE_TRAIL_HEADER`, `format_episode_cell()`, `format_source_trail_row()` in [`scripts/build_voice_predictions.py`](../../scripts/build_voice_predictions.py).

Checker enforces: new header once per event; ban old headers; public rows require `citation.channel` + `citation.title` (YouTube URL optional).

Example mixed row:

```md
| 2025-01-14 | Judging Freedom | [AMB. Chas Freeman : Netanyahu Instigating War with Iran.](https://www.youtube.com/watch?v=uu2-wa9ue5w) | yes | **Host setup:** Chris cut — … > "If this happens, …" **Context:** Freeman was answering … |
```

### Method footnote

Generated MD notes that displayed excerpts may include documented ASR repair; raw strings live in JSON (`public_excerpt_raw`).

## Recuration procedure

When fixing anchors, deduping appearances, or onboarding a new voice:

1. **Define pilot events** in public map + event registry (pilot event order documented per voice).
2. **Identify captures** from voice index / prediction notes / registers — one row per meaningful stance touchpoint.
3. **Draft raw excerpt** — copy verbatim into **`public_excerpt_raw`**; set **`public_excerpt`** (same or repaired) and **`asr_repair`** tier when display differs.
4. **Set speaker** — default guest slug; use **`mixed`** / **`host`** / **`operator_summary`** when host framing or summary rows apply; set **`public_display: false`** for non-quote audit rows.
5. **Set anchor** — public map `anchor_capture` or first public `initial` row; anchor must be guest or **`mixed`** with guest portion in display excerpt.
6. **Dedupe** — same capture + event: prefer one row; use **`appearance_date`** when the public date differs from folder date.
7. **Validate map** — host bootstrap/check script with **`--check`** (curated map mode, not v1 rebuild).
8. **Rebuild shelf** — build script → `--check` → shape checker → pytest voice tests.
9. **Wire closure** (if event open/resolved) — grade hooks via [`news-verify`](../news-verify/SKILL.md); update registry + resolution stub; rebuild.

## Wire closure (operator)

**Stub naming (canonical):** `statecraft/notes/wire/prediction-resolution-<event-id>.md` — `<event-id>` must match registry key exactly.

1. Open speaker **wire-events** page → resolution stub for the event.
2. Grade closure hooks; paste verdict + cite into stub table.
3. Fill **Resolution decision (operator)** on stub; set `resolution_source` to stub path + anchor (e.g. `#resolution-decision`).
4. Update **event-registry.json** (`status`, `outcome`, `resolved_date`, `resolution_source`, optional `resolution_scope`). Use **`review_note`** for human context only — checkers must not branch on it.
5. Rebuild generated surfaces so shelf + runtime prediction registry reflect closure.

**Review queue:** [`statecraft/predictions/review-queue.md`](../../statecraft/predictions/review-queue.md) · `python3 scripts/check_event_registry.py --emit-review-queue` · `python3 scripts/check_phase3.py --emit-review-queue`

## Phase 3 pipeline (registry-first)

Full orchestrator:

```bash
python3 scripts/run_prediction_pipeline.py
```

Order: semantic extractor (stub) → compression report → **probabilistic falsifier inference** → falsifier validator → registry compile → prediction registry → timeline → disagreement → **semantic scores** → **PR7 MVEL** → **signal extraction** → **PR3 signal prediction tasks** → **ENGM** → **PR2 calibration loss** → **PR4 epistemic dataset** → **PR5 baseline forecasts** → **PR6 ablation study** → voice shelves → event pages → `check_phase3` → semantic scores check (advisory).

**PR7 / MVEL — multi-voice extraction (advisory):**

- **Read-only:** `multivoice-extracted-dataset.json`, `event-alignment-map.json`, `voice-trajectories-{speaker}.json` — capture-map trajectories with probabilistic projections.
- **Not registry write:** unmatched claims → `event-alignment-map.json` review queue only; `registry_mutation: false`.
- **Claim SSOT:** capture-map `public_excerpt` rows — not archive NLP in v1.
- **Pipeline placement:** after semantic scores, before signal extraction.
- **Checker:** `python3 scripts/check_multivoice_extraction.py --advisory`

**PR6 / ablation study (advisory):**

- **Read-only:** `ablation-study.json` — five in-process variants; Brier `performance_drop` vs full system.
- **Not causal proof at low-N:** `interpretation: ablation_evaluation`; drops may be `null` when `test_probability_n < 5`.
- **Pipeline placement:** after baseline forecasts check, before voice shelf rebuild.
- **Checker:** `python3 scripts/check_ablation_study.py --advisory`

**PR5 / baseline forecasts (advisory):**

- **Read-only:** `baseline-forecast-metrics.json` — persistence, Bayesian, logistic-trend baselines vs ENGM on PR4 test split.
- **Not training:** `interpretation: baseline_evaluation`; `baseline_source: heuristic_v1` — evaluation only; transformer deferred PR5b.
- **Low-N:** WARN when test probability N &lt; 5 or no shift support — advisory, not ERROR.
- **Pipeline placement:** after epistemic dataset check, before voice shelf rebuild.
- **Checker:** `python3 scripts/check_baseline_forecasts.py --advisory`

**PR4 / epistemic dataset (advisory):**

- **Read-only:** `epistemic-dataset.json` — temporal train/test split with voice observations, latent features, censored outcomes.
- **Not training:** `interpretation: ml_ready_dataset`; `dataset_source: heuristic_v1` — ML-ready generator, not fitted model.
- **Pipeline placement:** after calibration loss check, before voice shelf rebuild.
- **Checker:** `python3 scripts/check_epistemic_dataset.py --advisory`

**PR3 / signal task system (advisory):**

- **Read-only:** `signal-prediction-tasks.json` — supervised examples for regime shift, escalation delta, voice convergence.
- **Not training:** `interpretation: supervised_task_space`; `task_source: heuristic_v1` — task target space for future tuning, not descriptive analytics alone.
- **Pipeline placement:** after signal check, before ENGM.
- **Checker:** `python3 scripts/check_signal_prediction_tasks.py --advisory`

**PR2 / calibration loss (advisory):**

- **Read-only:** `epistemic-calibration-loss.json` — unified `L` from prediction error, Brier, entropy misalignment, regime-shift delay.
- **Resolved-only Brier:** `y_true` from registry `outcome`; `y_pred` from ENGM `event_probability`; low-N WARN when resolved count &lt; 5.
- **Not training:** `interpretation: calibration_metric`; `calibration_source: heuristic_v1` — metric for future tuning, not Record truth.
- **Pipeline placement:** after ENGM check, before voice shelf rebuild.
- **Checker:** `python3 scripts/check_epistemic_calibration_loss.py --advisory`

**ENGM / PR1 — epistemic generative model (advisory):**

- **Read-only:** `epistemic-generative-state.json` — latent `Z_t` + voice-as-sensor softmax projections + `event_probability`.
- **Not truth:** every event block labeled `interpretation: probabilistic_projection`; `inference_source: heuristic_v1`.
- **Pipeline placement:** after signals, before voice shelf rebuild.
- **Checker:** `python3 scripts/check_epistemic_generative_state.py --advisory`

**Phase 4.5 — signal extraction (advisory):**

- **Read-only:** derives `prediction-signals.json` + `prediction-regime-summary.json`; never writes registry.
- **Effective model:** persisted `falsifier_model` or `inferred_view` at build time; explicit string `falsifier` on wire rows unchanged.
- **Macgregor-safe:** high-entropy voices down-weighted in cross-voice alignment.
- **Checker:** `python3 scripts/check_prediction_signals.py --advisory`

**Phase 3.5 — falsifier doctrine:**

- **Explicit falsifier beats infer:** hand-authored string `falsifier` on wire-grade rows is never replaced by heuristic inference.
- **Missing falsifier:** compile path may infer additive `falsifier_model` (`inference_source: heuristic_v1`) — labeled uncertainty, not ground truth.
- **Tiered CI:** orphans, fingerprint collision, trajectory v4 invalid, invalid `falsifier_model` shape → **ERROR**; high-entropy inferred models → **WARN** + review queue.
- **Operator review:** `python3 scripts/check_phase3.py --emit-review-queue` · `runtime/artifacts/falsifier-inference-report.json`

**Compression rules (Macgregor seeds):**

- **Rule A — anti-splitting:** same predictive fingerprint → merge references, no new `event_id`
- **Rule B — predictive difference:** new event only when falsifier, horizon, or `mechanism_tag` differs
- **Rule C — trajectory:** never emit child `event_id`; use parent `dimensions[]` only

**Notes-lane enrollment:** a voice shelf may ship capture-map-first; full enrollment requires timeline entries per shared `event_id` (see skill appendix).

## Agent behavior norms

- **Read captures before quoting** — never paraphrase into **`public_excerpt_raw`**; display repair must be documented in **`asr_repair`**.
- **One voice per invocation** — do not mix Freeman rows into Mercouris maps.
- **Windows discipline** — one shell chain for validate + build + test; no parallel archive reads after a hang.
- **Hand-edit maps only** — generated JSON/MD are rebuild targets.

## Verification / Proof Standard

Done when **all** pass for the named `<speaker>`:

1. Capture-map bootstrap/check: **0 issues**.
2. Builder: **`--check`** on JSON and MD (drift-free).
3. Shape checker: **0 violations** (capture map + shelf JSON).
4. Voice pytest module: green (or generic prediction tests when added).
5. **`generated-manifest.yaml`** includes capture-map check entry when the voice is enrolled.
6. Spot-check: sampled **`public_excerpt_raw`** strings are capture-faithful; source-trail tables use **Date | Channel | Episode | Stance | Excerpt** (one table per event).

Report exit codes and issue counts; do not claim ship on chat summary alone.

## Onboarding a new voice

1. Register `VoiceConfig` in `scripts/voice_prediction_pilot.py` (`VOICE_REGISTRY`).
2. Author `<speaker>-prediction-public-map.json` with **`prediction_object_terms`** per event.
3. Hand-build or bootstrap **capture map**; run **`bootstrap_voice_capture_map.py --speaker <slug> --check`** until clean.
4. Add **wire-events** operator page + resolution stubs for pilot events.
5. Enroll **generated-manifest** capture-map gate + shelf drift group.
6. Add pytest coverage mirroring Freeman shape tests.

## Related skills

| Skill | When |
|-------|------|
| [`statecraft-source-intake`](../statecraft-source-intake/SKILL.md) | Missing archive capture for a row |
| [`news-verify`](../news-verify/SKILL.md) / [`wire-verify`](../wire-verify/SKILL.md) | Closure hook grading |
| [`speaker-shelf-maintenance`](../runbooks/speaker-shelf-maintenance.runbook.md) | Index hygiene before crawl |
