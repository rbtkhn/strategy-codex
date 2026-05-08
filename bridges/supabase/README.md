# Supabase structured memory bridge

This directory is a reference scaffold for the live OB1-compatible memory layer
described in `docs/integrations/ob1/structured-memory-mcp.md`.

The intent is:

- keep the live memory service native to Supabase + pgvector + Edge Functions
- preserve the existing `evidence -> prepared_context -> governed_state` bridge
  path through compatibility views
- keep the repo-local Grace-Mar session helpers as the source of truth for the
  local `start_session` / `wrap_up` wrappers

## Layout

| Path | Purpose |
|------|---------|
| `sql/agent_memory_v2_structured.sql` | Schema reference for the structured memory tables, compatibility views, and RLS scaffolding |
| `functions/structured-memory-mcp/index.ts` | Edge Function contract for the new MCP tools and capture routing |

## Contract

The bridge exposes structured memory surfaces for:

- `north_star`
- `active_projects`
- `decisions`
- `brags`
- `thinking`
- `session_events`

The MCP-facing tools are thin adapters:

- `start_session`
- `standup`
- `capture_decision`
- `capture_brag`
- `wrap_up`
- `get_briefing`
- generic capture routing with explicit hint or heuristic fallback

The live deployment should not replace the repo's current session lifecycle or
briefing helpers. It should reuse them conceptually and preserve backward
compatibility with older `evidence / prepared_context / governed_state` callers.

