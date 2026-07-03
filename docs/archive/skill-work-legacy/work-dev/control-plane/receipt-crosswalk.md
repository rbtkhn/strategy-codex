# Receipt Crosswalk

## Purpose

This crosswalk makes strategy-codex receipt surfaces legible as one control-plane map without pretending they are one universal log.

Use it when you need to answer:

- which receipt surface should this workflow use
- what does that surface actually prove
- what does it not prove
- where does review happen
- what is the rollback or supersession path
- does this surface affect governed state, or only runtime / inspection / coordination

For the larger design argument, see [frontier-agent-control-plane-direction.md](../frontier-agent-control-plane-direction.md) and [unified-execution-receipts.md](../unified-execution-receipts.md).

## Family map

| Family | What it is for | What it must not become |
|---|---|---|
| **Governance** | Durable state transition and gate/process audit | A substitute for companion approval |
| **Execution** | Tool, runtime, or delegated-work action trace | A claim that the action's content is true |
| **Inspection** | Artifact run / view / validation evidence under stated conditions | A merge or canonical truth path |
| **Coordination** | Operator workflow, continuity, and ritual state | A security-grade execution log |

## Shared control-plane fields

Every receipt surface should be readable against these shared questions, even when the underlying schema differs:

| Field | Question |
|---|---|
| `receipt_family` | Is this governance, execution, inspection, or coordination? |
| `receipt_kind` | Which specific receipt shape is this? |
| `actor` | Who or what performed the action? |
| `intent` | Why did it run? |
| `authority_class` | What permission or governance class applied? |
| `resources_read` | What did it consult? |
| `resources_written` | What did it change or produce? |
| `status` | Did it succeed, fail, block, or remain partial? |
| `review_surface` | Where does a human inspect or decide next? |
| `rollback_surface` | How does this get stopped, superseded, or repaired? |
| `record_authority` | Can this affect canonical Record truth? |
| `gate_effect` | Does it stage, propose, merge, or do nothing to the gate? |

This is a reading crosswalk, not a demand that all schemas use identical field names today.

## Live surfaces

| Surface | Family | What it proves | What it does not prove | Review surface | Rollback / supersession | Record authority / gate effect |
|---|---|---|---|---|---|---|
| `merge-receipts.jsonl` | Governance | Approved merge batch landed with receipt-level audit | That the merged content is wise or correct by itself | Gate review context, merge batch inspection | New approved merge or corrective follow-up | Record-adjacent; applied merge evidence |
| `pipeline-events.jsonl` | Governance | Staged/applied runtime event timeline | Full semantic correctness of candidate content | Event replay, gate inspection | Later event, rejection, repair, or merge | May stage/apply depending on event; not truth by itself |
| [action-receipts.md](../../../action-receipts.md) | Execution | Meaningful system action is inspectable after the fact | Record truth, merge approval, or a universal schema | Operator review of emitted receipt/log | Superseding receipt, later corrective action | Not Record; no merge path by default |
| Sandbox receipts | Execution | Delegated or persistent run request, authority class, command/task, and outcome | That the outcome should become governed state | Sandbox adapter outputs, operator review | Stop path, later run, or repair action | Runtime-only unless separately routed |
| [mcp-execution-receipts.md](../../../mcp/mcp-execution-receipts.md) | Execution | Tool-shaped action under a declared capability and authority binding | Canonical IX/Evidence fact or merge approval | Receipt JSON, audit report, human review if promoted | Later receipt, blocked action, or gated follow-up | WORK/runtime audit only; receipts alone never merge |
| Compute ledger | Execution | Cost, backend, task, and coarse outcome accountability | Review sufficiency or semantic correctness | Ledger inspection and related run receipts | New run or budget rule changes | Runtime/accounting only |
| Runtime observability | Execution | Worker/runtime counts, health, and produced artifact visibility | Approval, truth, or merge authority | Runtime dashboards and reports | New run, operator intervention, or repair | Runtime-only unless staged separately |
| Carry / strategy run receipts | Execution | Task-scoped run envelope and declared artifact expectations | That the packet content is strategically correct | Receipt JSON, review packet | Revised run or validator follow-up | non-authoritative |
| [workbench receipts](../workbench/README.md) | Inspection | Artifact behavior under stated run/inspection conditions | External facts, merge approval, or Record truth | Workbench receipt plus operator inspection | Revise artifact, re-run, or reject | `recordAuthority: none`, `gateEffect: none` |
| Verification runs | Inspection | Manual or scripted proof for a capability claim | Governed merge, identity update, or world truth beyond the tested scope | Verification receipt/readout | New verification pass | WORK-only proof support |
| Cadence events | Coordination | Operator picks, workflow rhythm, conductor/coffee state | Security log or execution proof | Cadence log and session continuity surfaces | New cadence event or explicit close | No Record authority; no merge path |
| Handoff / continuity receipts | Coordination | Re-entry and continuity anchor for the next operator pass | Canonical state mutation | Handoff file, continuity views | New handoff or fresh continuity run | WORK/runtime continuity only |
| Git history | Coordination plus governance support | Durable repo mutation audit once changes are committed | Uncommitted agent intent or gate meaning by itself | `git diff`, commit inspection | Revert, new commit, later merge | Repo mutation evidence; not Record authority alone |

## Selection rule

When adding or choosing a receipt surface:

1. Use **governance** surfaces for stage/apply/merge state.
2. Use **execution** surfaces for delegated runs, tool use, or runtime action.
3. Use **inspection** surfaces for artifact behavior and proof-of-run.
4. Use **coordination** surfaces for operator rhythm, continuity, and handoff.

Do not create a new family unless the existing four cannot honestly describe the action.

## Three failure modes to avoid

### 1. Fake unification

Do not flatten merge receipts, workbench receipts, MCP receipts, and cadence events into one pseudo-schema that hides why they differ.

### 2. Duplicate doctrine

Do not let this file re-argue all of [unified-execution-receipts.md](../unified-execution-receipts.md). That memo sets architecture policy; this file is the operator-facing map.

### 3. File dump without proof scope

A list of paths is not enough. Every surface needs a short statement of:

- what it proves
- what it does not prove
- where review happens

## When to add a new receipt surface

Add a new receipt surface only if all of the following are true:

- the action cannot be honestly represented by an existing family
- the operator needs to inspect it after the fact
- authority, review, and rollback would otherwise remain unclear
- extending an existing schema would be more misleading than helpful

If those conditions are not met, extend the current family or improve its crosswalk mapping instead.

## Recommended next move

After this crosswalk, the next highest-value implementation step is **field normalization at schema edges**, especially around:

- `receiptKind`
- `recordAuthority`
- `gateEffect`
- actor naming
- resources read/written
- status semantics

That is a schema-alignment wedge, not part of this document itself.
