# Unified Execution Receipts

WORK only; not Record.

## Purpose

This memo defines the next receipt-hardening wedge for strategy-codex:

**make cross-surface execution legible as one control-plane story without collapsing distinct authority surfaces into one universal log too early.**

The repo already has meaningful receipt surfaces:

- action receipts
- workbench receipts
- MCP execution receipts
- sandbox receipts
- merge receipts
- pipeline events
- cadence events
- carry/run receipts
- rebuild receipts

The problem is not absence. The problem is fragmentation. An operator can often inspect one surface in isolation, but the system does not yet present a stable, shared mental model for how those receipts line up across chat, coding, browser/tool use, strategy runs, automations, and governed merges.

## Decision

Do **not** build a premature universal Agent Action Log first.

Instead:

1. define a shared receipt vocabulary
2. normalize minimum control-plane fields across receipt families
3. preserve family-specific schemas where the subject actually differs
4. add crosswalk and aggregation later

This keeps the architecture honest:

- workbench receipts are not merge receipts
- merge receipts are not runtime execution receipts
- MCP governance receipts are not UI inspection receipts
- cadence events are not security/audit receipts

## Why this matters

As frontier systems become more agentic, user trust depends less on eloquence and more on:

- what acted
- with what authority
- against which substrate
- producing what artifact
- under whose review
- with what rollback path

If strategy-codex is becoming a sovereign agent control plane, receipt coherence is part of the product, not just internal hygiene.

## Relationship to the frontier direction memo

[frontier-agent-control-plane-direction.md](frontier-agent-control-plane-direction.md) sets the larger claim: strategy-codex should develop as a sovereign agent control plane. This memo is narrower. It only defines the receipt architecture wedge that supports that direction.

Use the distinction like this:

- read the frontier direction memo when deciding what the product is becoming
- read this memo when deciding how execution legibility should be structured

This memo should not re-argue the whole product thesis. It should stay focused on receipt families, shared vocabulary, review surfaces, rollback visibility, and phased normalization.

## Existing receipt families

### 1. Governance and merge receipts

These prove durable state transitions.

- `merge-receipts.jsonl`
- `pipeline-events.jsonl`
- gate-processing outputs from `process_approved_candidates.py`

What they answer:

- was something staged or applied
- what candidate or merge batch landed
- what approved it

### 2. Execution receipts

These prove an agent, tool, or runtime attempted and completed work.

- sandbox receipts
- MCP execution receipts
- compute-ledger-linked runtime receipts
- carry harness and strategy run receipts

What they answer:

- what ran
- with what authority class
- what it touched
- what happened

### 3. Inspection receipts

These prove an artifact was run, viewed, or checked under stated conditions.

- workbench receipts
- verification runs
- visual inspection outputs

What they answer:

- did the artifact behave as described in this environment
- what was observed
- what remains unresolved

### 4. Ritual and coordination receipts

These prove operator workflow state, not system authority.

- cadence events
- coffee picks
- conductor outcomes
- handoff receipts

What they answer:

- what branch of work was opened
- what the operator intended
- what continuity anchor exists

## Shared minimum vocabulary

Every receipt family should expose or be mappable to these fields, even if names differ internally:

| Shared concept | Meaning |
|---|---|
| `receipt_family` | Governance, execution, inspection, or coordination |
| `receipt_kind` | Specific schema kind, such as `workbench`, `mcp_execution`, `merge`, `carry_run` |
| `actor` | Human, assistant, script, worker, tool, or hybrid surface that initiated or performed the action |
| `intent` | Why this run or action happened |
| `authority_class` | What class of permission or governance rule applied |
| `resources_read` | Files, systems, or sources consulted |
| `resources_written` | Files or artifacts changed or produced |
| `status` | Success, blocked, failed, partial, or workflow-specific equivalent |
| `review_surface` | Where a human can inspect or decide on the outcome |
| `rollback_surface` | What can stop, undo, supersede, or revise this action |
| `record_authority` | Whether the receipt has any canonical authority over Record truth |
| `gate_effect` | Whether the receipt stages, proposes, merges, or has no gate effect |

This is a **crosswalk vocabulary**, not an instruction to rewrite every schema immediately.

## Invariants

### Invariant 1: receipts prove process, not truth

No receipt family should imply that a claim about the world or the self is true merely because it was logged.

### Invariant 2: receipt clarity beats false unification

If two receipt families describe genuinely different subjects, keep separate schemas and harmonize by mapping, not flattening.

### Invariant 3: Record authority remains explicit

Receipts must say whether they can affect canonical state:

- `recordAuthority: none`
- `gateEffect: none`

should remain normal defaults outside governed merge paths.

### Invariant 4: review path must be visible

A receipt that cannot tell the operator where to inspect or decide next is incomplete as a control-plane artifact.

### Invariant 5: rollback path must be legible

For any persistent, delegated, or write-capable workflow, the operator should know how to stop, supersede, or repair it.

## Recommended normalized fields by family

### Governance and merge receipts

Must clearly expose:

- candidate or batch identity
- approval source
- applied status
- affected canonical surfaces
- checksum or integrity fields where relevant
- parent event linkage where available

### Execution receipts

Must clearly expose:

- actor kind and actor name
- authority class
- declared intent
- resources read and written
- result status
- errors or denials
- artifact outputs

### Inspection receipts

Must clearly expose:

- artifact under inspection
- run conditions
- what was observed
- operator judgment or status
- revision summary
- explicit `recordAuthority: none`

### Coordination receipts

Must clearly expose:

- operator choice or workflow state
- continuity implication
- linked artifact or next action when relevant

They should not masquerade as security-grade execution logs.

## What should change first

### Phase 1: publish the receipt crosswalk

Create a stable operator/developer reference for:

- receipt families
- what each proves
- what each does not prove
- where it lives
- how it maps to shared control-plane fields

This memo is the design seed for that phase.

### Phase 2: standardize names at schema edges

Without breaking existing tools, move schemas and generators toward clearer overlap in:

- `receiptKind`
- `recordAuthority`
- `gateEffect`
- actor naming
- resources read/written
- status semantics

This should happen opportunistically when touching each family, not as a giant all-at-once refactor.

### Phase 3: add a receipt aggregation view

Build a derived report or dashboard that lets an operator ask:

- what happened recently
- what changed durable state
- what only staged proposals
- what artifacts were inspected
- what runs failed or were blocked

This should be a **derived view**, not a new authority surface.

### Phase 4: enforce minimum receipt discipline on new agent surfaces

Any new persistent or write-capable surface should declare:

- which receipt family it emits
- what authority class it runs under
- where its review surface is
- how rollback works

This belongs in capability contracts and surface templates.

## Non-goals

Do not do these in the first wedge:

- invent a universal log schema that pretends all actions are the same
- migrate every historical receipt family at once
- merge cadence/ritual events into governance logs
- let receipt unification become a stealth merge-authority change
- replace existing family-specific docs that are already good

## Implementation candidates

Good near-term follow-ons from this memo:

1. a `receipt-crosswalk.md` operator table that indexes all active receipt surfaces
2. a small schema-alignment pass on one family, such as sandbox or carry receipts
3. a derived `receipt-summary` report under `artifacts/`
4. capability-contract additions that require `review_surface` and `rollback_surface`

## Recommended next move

The best next implementation wedge is:

**build the receipt crosswalk first.**

Why:

- it improves legibility immediately
- it does not force premature schema churn
- it exposes the highest-value field mismatches before code changes
- it creates a stable control-plane reference for future integrations

## Bottom line

Strategy-codex should not try to win by pretending every action is one homogeneous event stream. It should win by making **different kinds of action legible in a shared governance language**.

That means:

- distinct receipt families
- shared control-plane vocabulary
- explicit authority and rollback
- derived aggregation instead of hidden unification

This is the right receipt architecture for a sovereign, human-gated agent control plane.
