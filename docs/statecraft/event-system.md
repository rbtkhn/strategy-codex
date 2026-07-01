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
