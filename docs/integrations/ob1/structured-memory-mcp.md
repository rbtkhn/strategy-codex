# Structured Memory MCP

**Status:** Bridge contract and local scaffold.

This document defines the structured-memory extension to the OB1 bridge:
session lifecycle hooks, first-class structured memory surfaces, compatibility
views for the legacy evidence / prepared_context / governed_state path, and the
tool names used by the live Supabase Edge Function.

The repo-local implementation keeps two boundaries clear:

1. **Grace-Mar session lifecycle stays authoritative locally.** The thin
   `start_session` / `wrap_up` wrappers in
   `src/grace_mar/structured_memory.py` delegate to the existing
   `grace_mar.fork_lifecycle` helpers.
2. **OB1 remains a mixed-trust runtime.** The live Supabase bridge may store
   structured memory, but it does not replace the Record or the repo gate.

The runtime-only helper in `src/grace_mar/runtime/runtime_memory.py` is
adjacent to this bridge contract. It shapes session briefs, runtime
observations, and retrieval feedback for Strategy Codex workflows, but it does
not define a separate OB1 integration path or a second memory ontology.

---

## Structured surfaces

The bridge stores five purpose-driven surfaces plus session events:

- `north_star`
- `active_projects`
- `decisions`
- `brags`
- `thinking`
- `session_events`

The surfaces are intentionally narrower than a flat "thoughts" bucket. They let
the bridge preserve workflow intent without collapsing everything into one
undifferentiated memory type.

### Compatibility mapping

The new surfaces remain backward compatible with the older three-layer naming
used by earlier bridge callers.

| Structured surface | Legacy compatibility surface |
|-------------------|------------------------------|
| `north_star` | `governed_state` |
| `active_projects` | `governed_state` |
| `decisions` | `governed_state` |
| `brags` | `prepared_context` |
| `thinking` | `prepared_context` |
| `session_events` | `evidence` |

This is a compatibility label, not a semantic claim that the older layers are
identical to the new ones.

---

## Tool contract

The live MCP Edge Function exposes the following tools:

- `start_session`
- `standup`
- `capture`
- `capture_observation`
- `capture_decision`
- `capture_brag`
- `wrap_up`
- `get_briefing`
- session event aliases:
  - `session_start`
  - `prompt_submit`
  - `post_tool_use`
  - `session_end`

### Tool behavior

- `start_session` creates the session boundary and logs the start event.
- `prompt_submit` and `post_tool_use` log lifecycle events inside the session.
- `wrap_up` closes the session and records the wrap-up event.
- `standup` and `get_briefing` render the live structured surfaces into a
  compact or full markdown brief.
- `capture_observation` is the explicit runtime-observation alias for generic
  capture payloads.
- `capture_decision` writes to `decisions`.
- `capture_brag` writes to `brags`.
- `capture` routes content using explicit surface hints first, then heuristic
  fallback.

### Routing rule

The capture router follows a hybrid rule:

1. Explicit `surface_hint` wins.
2. Otherwise, the content is scored by keyword families.
3. If nothing matches, the entry falls back to `thinking`.

This keeps old untyped callers working without inventing a second ontology.

---

## Live bridge shape

The live bridge scaffold lives under `bridges/supabase/`:

- `sql/agent_memory_v2_structured.sql`
- `functions/structured-memory-mcp/index.ts`

That scaffold is intentionally separate from the repo's Record-gated surfaces.
It is a deployment contract and a reference implementation, not the canonical
identity store.

---

## Operational guidance

- Use `start_session` and `wrap_up` as thin adapters.
- Keep the repo-local briefing helpers as the source of truth for session
  lifecycle behavior.
- Preserve the legacy `evidence / prepared_context / governed_state` path with
  compatibility views or wrappers.
- Do not add autonomous sync between OB1 and the Record. The bridge is still
  operator-initiated and observable.
