# Singularity Action Cards

WORK only; not Record.

This shelf contains dated action cards for declared Singularity loops.

Action cards convert loop attention into concrete, reviewable work.

```text
loop → action card → proof artifact → run receipt
```

## Standard

See [`docs/singularity/action-card-standard.md`](../../docs/singularity/action-card-standard.md).

## Template

Use [`TEMPLATE.md`](TEMPLATE.md).

## Layout

```text
singularity/action-cards/
  <loop-id>/
    YYYY-MM-DD.md
```

Domain shelves may hold richer artifacts. When that happens, action cards should link to the domain artifact rather than duplicate it.

## Examples

```text
singularity/action-cards/grace-gems-margin-policy-review/2026-07-01.md
singularity/action-cards/mountain-homestead-risk-register/2026-07-01.md
singularity/action-cards/predictive-history-education/2026-07-01.md
```

## Run receipts

Append-only history: [`runtime/operator-events/singularity-loop-runs.jsonl`](../../runtime/operator-events/singularity-loop-runs.jsonl)

Script: `python3 scripts/append_singularity_loop_run.py`
