# Agentic Receipt Map (work-dev)

**Status:** WORK-layer audit map. This is not Record authority, not a new governance surface, and not a universal Agent Action Log.

## Core Rule

The model is not enough. For agentic workflows, safety is shown by permissions, context boundaries, receipts, revocation, and pressure defaults.

Use this map before adding a new action log. First ask which existing surface already proves intent, authority, action, cost, result, and review.

## Existing Receipt Surfaces

| Surface | What it proves | Typical producer | Notes |
|---------|----------------|------------------|-------|
| Git history | Durable repo mutation audit: commit, author, timestamp, diff, branch | Git / operator workflow | Best receipt for committed file changes; does not explain uncommitted agent intent by itself. |
| `pipeline-events.jsonl` | Pipeline or runtime event stream with timestamped actions | Bot/runtime scripts and integration flows | Useful for staging and runtime provenance; not universal across all tools. |
| `merge-receipts.jsonl` | Approved candidate merge receipts and applied gate outcomes | `process_approved_candidates.py` | Record-adjacent receipt for gate-approved merges only; agents still cannot bypass the gate. |
| Cadence events | Operator cadence, coffee/conductor selections, and workflow ritual events | Work-cadence tooling | Useful for session rhythm and operator intent; not a security log. |
| Compute ledger | Per-invocation cost, backend, task, and outcome tracking | Sandbox/integration ledger helpers | Useful for budget and run accountability. |
| Sandbox receipts | Tool/run request, authority class, command/task, outcome, and errors | Sandbox adapter implementations | Preferred receipt for delegated or persistent execution. |
| Runtime observability | JSONL observations, counts, health, and produced artifacts | Runtime workers and dashboards | Operational visibility; must remain runtime-only unless staged through the gate. |

## Minimum Receipt Expectation

For any persistent, delegated, or write-capable agent workflow, the operator should be able to recover:

- Intent: why the agent ran.
- Context: what the human could see, what the agent could see, and what was withheld.
- Authority: permission scope, denied actions, and blast radius.
- Action: tool, command, task, or integration surface used.
- Outcome: success, failure, files touched, artifacts produced, or no-op.
- Review: cadence and human reviewer.
- Revocation: stop path, owner, stop receipt, and final state.

## Future Gap

A universal Agent Action Log may be useful later, but it is a future gap, not v1. Before creating one, define event types, retention, tamper-evidence, secret handling, query needs, and how it relates to existing git, pipeline, merge, cadence, compute, sandbox, and runtime-observability receipts.

Until then, prefer explicit receipt mapping in the Plan Mission `Agentic Risk & Safety Review` and the `agent-surface-template.yaml` `audit.receipt_surfaces` field.
