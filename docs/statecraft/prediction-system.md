# Prediction system — lifecycle

Structured prediction work uses **lifecycle fields** and **schema validation**, not global WORK/Record banners.

## Lifecycle model

```text
prediction:
  pending → resolved

event:
  open → resolved
```

Outcome is recorded on the **event** only after resolution (`outcome: yes | no`).

Terminal event statuses (`void`, `deprecated`) map prediction notes to `status: resolved`.

## Surfaces

| Surface | Path |
| --- | --- |
| Event registry | [`statecraft/data/event-registry.json`](../../statecraft/data/event-registry.json) |
| Prediction notes | [`statecraft/notes/predictions/`](../../statecraft/notes/predictions/) |
| Generated registry | [`runtime/artifacts/prediction-registry.json`](../../runtime/artifacts/prediction-registry.json) |
| Metrics | [`runtime/artifacts/prediction-metrics.json`](../../runtime/artifacts/prediction-metrics.json) |

## Required prediction frontmatter

```yaml
---
note_type: prediction
event_id: example_event
speaker: freeman
date_made: 2025-01-14
stance: yes
source: source-archive/statecraft/2025-01-14/example.md
status: pending
---
```

## Validation

```bash
python3 scripts/validate_all_schemas.py --scope prediction
python3 scripts/check_event_integrity.py
```

Schema registry: [`docs/system/schema-system.md`](../system/schema-system.md).

Event doctrine: [`event-system.md`](event-system.md).

## Principle

> Truth is defined by state and validation—not by labeling.
