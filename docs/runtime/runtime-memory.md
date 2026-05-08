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

## Repo-local implementation

The runtime helpers live in `src/grace_mar/runtime/runtime_memory.py`.

They build payloads for:

- `runtime_observations`
- `sessions`
- `retrieval_misses`
- `sync_receipts`

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
session continuity and retrieval workflow without becoming canonical storage.

