# Grace-Mar as a Governed Personal Agent Substrate

**Status:** WORK / architecture framing. This document adds no merge authority, no new runtime behavior, and no new gate schema.

Grace-Mar can be read as a governed personal substrate for agents: durable state lives in the git-backed Record, while runtime agents remain disposable helpers that read, draft, stage, and hand off. The core rule is unchanged: agents may operate around the Record, but canonical truth enters only through companion-approved promotion.

This matters now because frontier agents are becoming good enough to sustain long-running work, but not wise enough to own personal truth. Grace-Mar gives them a legible place to stand: read the durable surfaces, understand what is pending, preserve receipts, and return proposals to a human-gated path. The architectural bet is not more autonomy; it is better continuity without surrendering authorship.

## Substrate Shape

Grace-Mar already has the primitives agent systems need for long-running work:

- **Durable state:** `self.md`, `self-skills.md`, `self-library.md`, and `self-archive.md` define approved identity, capability, reference, and evidence surfaces.
- **Status machine:** `recursion-gate.md` separates proposed changes from approved Record truth.
- **Audit trail:** git history, merge receipts, pipeline events, runtime bundles, and cadence logs make changes replayable.
- **Work lanes:** `docs/skill-work/` gives agents bounded operating surfaces for strategy, development, Cici, politics, coffee, dream, and related WORK.
- **Runtime boundary:** `self-memory.md`, handoffs, prepared context, MCP receipts, and runtime complements improve continuity without becoming Record truth.

The substrate is useful because state is outside any one model context window. An agent can enter late, read the governed surfaces, and understand what is canonical, what is proposed, and what is only runtime continuity.

## Issue-Tracker Pattern

Enterprise issue trackers work as agent substrates because they provide ownership, status, permissions, comments, history, and handoffs. Grace-Mar maps those coordination primitives onto a personal cognitive fork:

- **Owner:** the companion holds authority over Record incorporation.
- **Status:** proposals move from staged candidate to approved merge only through the gate.
- **Permissions:** tools and agents may read or draft broadly on WORK surfaces, but protected Record writes stay governed.
- **Auditability:** commits, receipts, and event logs explain what changed and why.
- **Handoffs:** coffee, dream, bridge, runtime bundles, and lane notebooks preserve continuity across sessions and hosts.

The difference is the object of governance. Issue trackers govern tasks. Grace-Mar governs personal identity, evidence, skills, memory boundaries, and the Voice that speaks from them.

## External Agent Contract

External agents may:

- read approved Record, policy, runtime, and WORK surfaces according to local permissions;
- emit summaries, receipts, patch packets, evidence stubs, or candidate proposals;
- stage reviewable material through documented workflows when operator policy allows it;
- help route work through MCP, runtime complements, or lane-specific tools.

External agents may not:

- approve, reject, or merge `recursion-gate.md` candidates on their own;
- write directly to SELF, EVIDENCE, `bot/prompt.py`, or other protected Record surfaces;
- treat session memory, MCP output, web fetches, or successful tool calls as canonical truth;
- substitute autonomous sensemaking for companion review.

The safe pattern is: **read approved state -> create inspectable proposal -> preserve provenance -> companion review -> existing merge path**.

## Cognitive Linear Board

A possible future view is a **Cognitive Linear Board**: a read-only or stage-only projection over active work, skills, evidence, runtime state, and gate candidates. It would let external agents see:

- what is canonical;
- what is pending review;
- what work lanes are active;
- what receipts or handoffs explain recent state;
- where a proposal should be routed.

This is exploratory WORK framing, not a committed product interface or schema. Any implementation must preserve the same boundary: board views may organize and stage, but they do not approve or merge Record truth.

## Related

- [Architecture](architecture.md)
- [Agent 365 alignment](agent-365-alignment.md)
- [Apple Intelligence alignment](apple-intelligence-alignment.md)
- [Google Gemini / Vertex agent alignment](google-gemini-alignment.md)
- [AWS Bedrock AgentCore alignment](aws-agentcore-alignment.md)
- [Atlassian Rovo alignment](atlassian-rovo-alignment.md)
- [Runtime complements](runtime/runtime-complements.md)
- [MCP stack overview](mcp/mcp-stack-overview.md)
- [AGENTS.md](../AGENTS.md)
- [Recursion gate](../recursion-gate.md)

