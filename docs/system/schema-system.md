# Schema system

**Purpose:** One registry, one validator, consistent enforcement for structured data in strategy-codex.

## Registry (SSOT)

[`schemas/registry.yaml`](../../schemas/registry.yaml) maps logical schema names to:

| Field | Meaning |
| --- | --- |
| `path` | JSON Schema file |
| `applies_to` | Glob relative to repo root |
| `format` | How to load instances (`json`, `json_object_map`, `markdown_frontmatter`, `jsonl`) |
| `scope` | Health grouping: `prediction`, `runtime`, `singularity`, or `all` |

Legacy gate/workflow schemas remain under [`schemas/registry/`](../registry/) until migrated into the manifest.

## Validation

```bash
python3 scripts/validate_all_schemas.py --scope prediction
python3 scripts/validate_all_schemas.py --scope singularity
python3 scripts/validate_all_schemas.py --scope all
```

[`scripts/validate_all_schemas.py`](../../scripts/validate_all_schemas.py) validates each matched file against its schema.

[`scripts/schema_invariants.py`](../../scripts/schema_invariants.py) enforces cross-object rules JSON Schema cannot express:

- resolved events require `outcome` in `{yes, no}`
- prediction `status: pending` when event is `open`
- prediction `status: resolved` when event is terminal (`resolved`, `void`, `deprecated`)

Specialized checkers (`check_event_integrity.py`, `check_prediction_registry.py`, `check_prediction_metrics.py`) delegate to the unified validator.

## Adding a schema

1. Add `schemas/<area>/<name>.schema.json`
2. Register it in `schemas/registry.yaml` with `applies_to`, `format`, and `scope`
3. Wire `--scope` in [`check_repo_health.py`](../../scripts/check_repo_health.py) when the check should be required
4. Add tests under `tests/test_validate_all_schemas.py`

## Prediction lifecycle

See [`docs/statecraft/prediction-system.md`](../statecraft/prediction-system.md).

## Principle

> Structure is defined once and enforced everywhere.
