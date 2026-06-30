---
audience: operator
authority: doctrine
record_status: none
---

# Agent Handoff Queue

**Status:** Phase 1 — local, file-based, validator-backed handoff surface.

**Queue root:** [`runtime/operator-queue/`](../runtime/operator-queue/README.md)

**Validator:** `python3 scripts/check_agent_handoff_queue.py`

## Purpose

The Agent Handoff Queue is a visible handoff surface for agent and human work.

It exists so private chat output can become reviewable work without making the operator the copy/paste path between sessions, agents, and repo tools.

## Core rule

- No agent handoff without a visible queue item.
- No completed queue item without a receipt (when `status: agent_done`).
- No receipt promotes authority automatically.

The validator catches obvious authority-boundary violations; real authority remains governed by existing gates, review, and membrane validators. The queue **coordinates** work — it is **not** the enforcement layer.

## When to use this queue

Use Agent Handoff Queue when work needs to move between a human and an agent, between agents, or across sessions with visible ownership, context, stop conditions, and receipt requirements.

Do not use Agent Handoff Queue for passive session continuity, proposal intake, or generated repo-state reports.

**Threshold:** Create a queue item when work **crosses a boundary** (sessions, agents, humans, repo surfaces, authority gates). Do **not** require queue items for tiny single-session edits completed immediately with a visible result in chat or commit.

## Adjacent surface boundaries

| Surface | Use for | Not for |
|---------|---------|---------|
| [`runtime/artifacts/handoffs/`](../runtime/artifacts/handoffs/README.md) | Session continuity, re-entry packets | Active work assignment |
| [`runtime/artifacts/patch-intake/`](../runtime/artifacts/patch-intake/README.md) | Candidate proposals / patch intake | Task status tracking |
| [`run_repo_convergence.py`](../scripts/run_repo_convergence.py) | Derived artifact rebuilds + validators | Human/agent work ownership |
| [`runtime/operator-events/`](../runtime/operator-events/README.md) | Append-only audit JSONL | Work queue items |
| **`runtime/operator-queue/`** | Active handoff work with owner/status/receipt | Passive memory or generated reports |

## Operator workflow

The queue slots in at **handoff points**, not every coffee turn or EXECUTE slice.

**Rule of thumb:** boundary crossed → queue item; same session, same agent, done now → skip.

### Typical session arc

```text
coffee / reentry → pick lane → ingest / strategy / EXECUTE slice → validators → ship receipt
```

The queue complements chat, menus, harness warmup, and `operator_handoff_check.py`.

### When to create a queue item

| Trigger | Status | Example |
|---------|--------|---------|
| Continue work in a later session | `agent_todo` | Multi-session refactor across pytest + docs |
| Agent must not guess | `needs_input` | Validator integration timing ambiguous |
| Work hits authority boundary | `gate_required` | Doctrine edit needs operator decision |
| Intentional ship arc across dirty WIP | `agent_todo` → `agent_done` | One item per arc with context and DoD |
| Slice complete, audit trail wanted | `agent_done` + receipt | Commands run, changed files, convergence evidence |

### When to skip the queue

- Single-session fix shipped in the same thread
- Passive re-entry only → handoffs
- Candidate patch/proposal → patch-intake
- Strategy source intake — archive land + synthesis sufficient
- Repo state check only → `run_repo_convergence.py --check`

### Typical day

| Beat | Queue role |
|------|------------|
| Morning `coffee` | Glance `agent-todo/` and `needs-input/` — `operator_coffee.py` or `check_agent_handoff_queue.py --glance` |
| Strategy ingest | Usually none |
| EXECUTE one-shot slice | Usually none if same session to ship |
| Multi-session work | Create `agent_todo` with context + definition_of_done |
| Agent blocked | Move to `needs-input/` with exact `blocking_question` |
| Doctrine / Record touch | `gate_required` if agent stops at boundary |
| EOD / `dream` | Review `agent_done` receipts; void stale experiments |

### Work loop with repo convergence

```text
queue item → agent claim (agent-working/) → edits → run_repo_convergence --check → receipt → operator review
```

Convergence validates **repo state**; the queue tracks **work state**.

### Minimal adoption path (Phase 1)

1. **Continue this tomorrow** → `agent-todo/`
2. **Agent blocked, don't guess** → `needs-input/`
3. **Slice shipped, need audit trail** → `agent-done/` + receipt

Run `python3 scripts/check_agent_handoff_queue.py` when queue items change.

## Lifecycle

```text
request → queue item → claim → work → receipt → review / done
```

## Status grammar

| Status | Directory | Meaning |
|--------|-----------|---------|
| `agent_todo` | `agent-todo/` | Ready to claim |
| `agent_working` | `agent-working/` | Claimed and active |
| `needs_input` | `needs-input/` | Stopped; human answer required |
| `gate_required` | `gate-required/` | Authority boundary reached |
| `agent_done` | `agent-done/` | Completed with receipt |
| `void` | `void/` | Intentionally retired |

Directory name and frontmatter `status` must agree.

## Queue item schema

### Core required (every item)

```yaml
id:
title:
status:
owner:
requester:
created_at:
membrane_class:
context:              # non-empty list of repo-relative paths
definition_of_done:   # non-empty list
receipt_required:     # boolean
```

Filename: `ahq-YYYYMMDD-NNN-short-slug.md` — frontmatter `id` must match the prefix.

### Recommended (warn default; fail with `--strict`)

```yaml
allowed_actions:
forbidden_actions:
stop_conditions:
priority:
labels:
```

For `agent_working`, also recommend `claimed_at` and `claimed_by`.

### Status-required fields

| Status | Required |
|--------|----------|
| `agent_done` | `receipt` object (always; `receipt_required: false` is invalid for done) |
| `needs_input` | `blocking_question` object |
| `gate_required` | `gate` object |
| `void` | non-empty `void_reason` |

## Receipt grammar

```yaml
receipt:
  completed_at:
  actor:
  stopped_because:
  changed_files: []      # or evidence explaining no file changes
  commands_run: []
  evidence: []
  remaining_questions: []
```

`receipt_required: true` means completion must produce a receipt when transitioning to done.

## Needs-input grammar

```yaml
blocking_question:
  asked_at:
  question:
  needed_from:
```

Must state exactly what blocked work — not vague "need clarification."

## Gate-required grammar

```yaml
gate:
  type:
  reason:
  required_decision:
  candidate_files: []   # optional
```

The queue may stage a gate; it must not cross it automatically.

## Void grammar

```yaml
void_reason: "Short reason the item was retired"
```

## Membrane class mapping

Frontmatter uses machine values; doctrine uses display labels from [`work-membrane-v2.md`](work-membrane-v2.md).

| Frontmatter value | Doctrine label |
|-------------------|----------------|
| `record` | Record |
| `governed_adjacent` | governed adjacent |
| `instrumental_work` | instrumental work |
| `runtime_derived` | runtime / derived |
| `external_complement` | external complements |

Queue items are typically `instrumental_work`.

## Commit / retire hygiene

- Commit durable examples and completed/voided items useful as receipts or references.
- Do **not** commit ordinary active `agent-working/` items unless intentional cross-machine or cross-operator handoff.
- Void stale experiments rather than leaving ambiguous `agent-working/` items indefinitely.

## Relationship to repo convergence

| Tool | Role |
|------|------|
| Agent Handoff Queue | Work movement — owner, status, context, receipt |
| Repo convergence | Repo state coherence — derived artifacts and validators |

Typical loop:

```text
queue item → agent work → repo convergence --check → receipt → human review
```

Repo convergence does not create queue items in Phase 1.

## Non-goals (Phase 1)

- No background daemon or polling loop
- No Slack, Linear, or GitHub Issues integration
- No automatic Record / doctrine / source-archive mutation
- No enrollment in `check_repo_health.py --quick` until grammar stabilizes

## Roadmap

### Phase 2

- `scripts/claim_agent_handoff_item.py`
- `scripts/complete_agent_handoff_item.py`
- `scripts/move_agent_handoff_item.py`
- `scripts/build_agent_handoff_report.py`
- Receipt mirror to `runtime/operator-events/agent-handoffs.jsonl`
- Stale warnings (defaults: `agent_working` > 48h, `needs_input` > 7d, `gate_required` > 14d)

### Phase 3+

- Optional `repo_convergence:` block on receipts
- External complement bridges (import/export only; no authority transfer)
