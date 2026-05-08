# Runtime Memory for Strategy Codex

**Status:** Runtime-only. Non-canonical. Rebuildable.

This document defines the small operational memory layer used by typical
Strategy Codex workflows. It is meant to reduce friction during active work,
not to create another Record.

## Top 5 use cases

1. Session start briefing
2. Post-tool context capture
3. Decision capture
4. Retrieval miss logging
5. Wrap-up / handoff

## Contract

- Git remains canonical for durable Record changes.
- Runtime memory stores observations, continuity, and retrieval feedback.
- Retrieval misses are operational feedback, not identity claims.
- Sync receipts are audit trails for Git-to-runtime propagation, not approval.
- This runtime layer is adjunct to the OB1 structured-memory bridge; it does
  not define a second bridge contract or a second Record.

## Repo-local implementation

The runtime helpers live in `src/grace_mar/runtime/runtime_memory.py`.

They build payloads for:

- `runtime_observations`
- `sessions`
- `retrieval_misses`
- `sync_receipts`

The MCP-facing alias `capture_observation` maps onto the runtime observation
builder so generic runtime captures can stay explicit without changing the OB1
bridge contract.

The runtime helper also renders `get_briefing(...)` and `standup(...)` briefs
from structured memory surfaces, mirroring the bridge-facing briefing shape
without becoming the bridge contract itself.

The session closeout path is exposed as `wrap_up(...)`, which returns the same
runtime-only payload as `build_wrap_up_session(...)` but reads like the rest of
the runtime API.

They also produce a compact session-start brief from:

- `session-log.md`
- `recursion-gate.md`
- `self-evidence.md`
- `docs/skill-work/work-dev/workspace.md`
- `docs/skill-work/work-dev/session-continuity-contract.md`

## Typical workflow

- Start from the briefing.
- Capture what the tool or search revealed.
- Record decisions explicitly.
- Log retrieval misses when the search path fails.
- Wrap up with open loops and the next entry point.

## Relationship to the OB1 bridge

The OB1 structured-memory bridge remains a separate integration contract.
This runtime layer is smaller and more local: it supports Strategy Codex's own
session continuity and retrieval workflow without becoming canonical storage or
duplicating the bridge contract.
