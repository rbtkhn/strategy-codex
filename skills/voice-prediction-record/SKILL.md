---
name: voice-prediction-record
description: "Curate and rebuild a speaker prediction shelf from archive captures: public map, capture-map rows with verbatim excerpts, wire closure, and generated JSON/MD. Triggers: voice prediction record, prediction record, capture map recurate, rebuild predictions. Parameter: speaker slug (freeman, mercouris, …). Not synthesis or auto-file without curated rows."
preferred_activation: voice prediction record
activation: voice prediction record
portable: true
version: 0.1.0
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
- **Synthesizing quotes** — `public_excerpt` must be a **substring** of the archive capture body (ASR fidelity preserved).
- **Record merge** or wire-grade closure without operator decision on resolution stubs.

## Layer law

| Layer | Role |
|-------|------|
| **Source archive** | Verbatim capture SSOT — read body for excerpt alignment |
| **Public map** | Per-event operator framing: title, summary, scoring, **`prediction_object_terms`** |
| **Capture map** | Curated rows: `event_id`, `capture`, stance, speech_act, **`public_excerpt`** |
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

**Reference implementation:** Freeman — see host appendix for exact paths and script names until generic `--speaker` builders land.

## Read order (before editing)

1. **Public map** — confirm every pilot event has required fields and non-empty **`prediction_object_terms`**.
2. **Event registry** — `status`, `outcome`, horizons for closure-aware labels.
3. **Capture map** — row list; note `anchor_capture` overrides on public map when present.
4. **Archive bodies** — bounded `Read` on captures referenced by rows being edited (not repo-wide grep).
5. **Wire-events page** — closure stubs and related-event pairs for the speaker.

## Capture-map row schema

Required keys: **`event_id`**, **`capture`**, **`stance`**, **`speech_act`**, **`public_excerpt`**.

Optional keys:

| Field | Use |
|-------|-----|
| `appearance_date` | When episode date differs from capture folder date (dedupe in builder) |
| `context_note` | Operator framing when excerpt alone lacks object terms |
| `excerpt_exception` | Only **`short_decisive_sentence`** (requires `context_note`) |
| `prediction_object_terms` | Row-level override of public-map terms |
| `anchor_context_note` | Rendered at anchor + source-trail in MD |

**Speech acts:** `initial`, `restated`, `iterated`, `self_acknowledged_correct`, `self_acknowledged_incorrect`, `outcome_commentary`.

## Excerpt quality rules (non-negotiable)

These rules are enforced by `bootstrap_voice_capture_map.py --check`, builder, and checker via `voice_prediction_pilot.py`:

1. **Verbatim substring** — `public_excerpt` must appear in capture body after normalization (punctuation-insensitive). No partial-prefix fallback. Multi-segment excerpts use ` ||| ` between segments; each segment must match.
2. **Word floors** — anchor rows: **≥40 words**; appearance rows: **≥30 words**, unless `excerpt_exception: short_decisive_sentence`.
3. **Prediction object** — anchor excerpt must contain a **`prediction_object_terms`** hit (public map or row override). Appearances need object terms **or** a non-empty **`context_note`**.
4. **Complete sentence** — excerpt ends with `.!?` **or** is a verified verbatim fragment inside the capture (ASR tails allowed when substring-proven).
5. **Not title-like** — question titles, host lines, episode titles fail unless `short_decisive_sentence` + `context_note`.
6. **Ambiguous starts** — excerpts starting with `if this`, `they`, `he`, etc. fail when object terms are absent.
7. **Max length** — **80 words** unless operator explicitly splits across ` ||| ` segments within max per segment policy.
8. **No synthesis** — do not append invented closing sentences to “fix” ASR; extend only by selecting the **next verbatim span** from the same capture.

## Recuration procedure

When fixing anchors, deduping appearances, or onboarding a new voice:

1. **Define pilot events** in public map + event registry (pilot event order documented per voice).
2. **Identify captures** from voice index / prediction notes / registers — one row per meaningful stance touchpoint.
3. **Draft excerpt in editor** — copy verbatim from capture; run alignment mentally against object terms.
4. **Set anchor** — public map `anchor_capture` or first `initial` row; verify anchor passes stricter object-term rule.
5. **Dedupe** — same capture + event: prefer one row; use **`appearance_date`** when the public date differs from folder date.
6. **Validate map** — host bootstrap/check script with **`--check`** (curated map mode, not v1 rebuild).
7. **Rebuild shelf** — build script → `--check` → shape checker → pytest voice tests.
8. **Wire closure** (if event open/resolved) — grade hooks via [`news-verify`](../news-verify/SKILL.md); update registry + resolution stub; rebuild.

## Wire closure (operator)

1. Open speaker **wire-events** page → resolution stub for the event.
2. Grade closure hooks; paste verdict + cite into stub table.
3. Fill **Resolution decision (operator)**; set `resolution_source` for registry paste.
4. Update **event-registry.json** (`status`, `outcome`, `resolved_date`, `resolution_source`).
5. Rebuild generated surfaces so shelf + runtime prediction registry reflect closure.

## Agent behavior norms

- **Read captures before quoting** — never paraphrase into `public_excerpt`.
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
6. Spot-check: sampled anchor excerpts are capture-faithful; context notes render in MD anchor + source-trail cells.

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
