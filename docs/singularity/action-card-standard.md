# Singularity Action Card Standard

## Purpose

A Singularity action card is a dated, reviewable work order for a declared loop.

It turns loop attention into concrete action:

```text
loop signal → action card → proof artifact → run receipt → next loop feed
```

Action cards are not automation. They are the bridge between declared loops and operated loops.

## Location

Action cards live under:

```text
singularity/action-cards/<loop-id>/<YYYY-MM-DD>.md
```

Use quoted dates in YAML frontmatter (`date: "2026-07-01"`) so validators receive strings, not parsed date objects.

Domain-specific action cards may also be mirrored or linked from loop output shelves, for example:

```text
operations/grace-gems/listings/review/
operations/mountain-homestead/risk-register/
```

The action-card index should point to canonical domain artifacts instead of duplicating large content.

## Required Sections

Each action card must include:

1. Loop
2. Situation
3. Decision
4. Execution
5. Review Gate
6. Outcome

Use [`singularity/action-cards/TEMPLATE.md`](../../singularity/action-cards/TEMPLATE.md) as the starting point.

## Status Values

Use only:

```text
planned
done
blocked
skipped
revised
rejected
```

## Proof Rule

A completed action card should link to at least one proof artifact when practical.

Examples:

- listing review file
- risk register
- mitigation proof note
- customer response draft
- search/conversion review
- water-system checklist
- weekly ops card

## Run Receipts

After acting on a card, append a run receipt:

```bash
python3 scripts/append_singularity_loop_run.py \
  --loop-id <loop-id> \
  --status done \
  --action-card singularity/action-cards/<loop-id>/<YYYY-MM-DD>.md \
  --proof-artifact <path-to-proof> \
  --next-loop-id <downstream-loop-id>
```

Receipts append to [`runtime/operator-events/singularity-loop-runs.jsonl`](../../runtime/operator-events/singularity-loop-runs.jsonl).

## Next-Loop Feeds

If an action card produces work for another loop, list it under `next_loop_ids`.

Examples:

```text
grace-gems-margin-policy-review → grace-gems-marketplace-ops
mountain-homestead-risk-register → mountain-homestead-ops
mountain-homestead-wildfire-mitigation-review → mountain-homestead-seasonal-readiness
```

## Boundary

Action cards do not silently change loop definitions, governed state, external accounts, customer messages, or business policy.

They stage work for human review and receipt logging.

## Related

- [Loop system](loop-system.md)
- [Action cards shelf](../../singularity/action-cards/README.md)
