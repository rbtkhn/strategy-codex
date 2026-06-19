> **ARCHIVED (Grace-Mar corpus).** Fork growth is **not** default strategy-codex routing. **`fork revive` only** — see [grace-mar-instance-boundary.md](../../docs/grace-mar-instance-boundary.md).

# Agent 365 Alignment

**Status:** WORK / architecture positioning; not Record truth, not a roadmap commitment.

**Last updated:** 2026-05-03

Microsoft Agent 365 validates a broad architectural shift: as agents become ordinary work infrastructure, value moves from raw model access toward observability, governance, identity, security, and auditability. Grace-Mar is not an enterprise control plane and should not be positioned as one. Its local analogue is narrower and more sovereign: a human-gated substrate for cognitive forks where agents may read approved surfaces, preserve receipts, and prepare reviewable proposals without owning canonical truth.

## Microsoft Reference Point

Microsoft describes Agent 365 as a control plane that lets organizations observe, govern, and secure agents across the organization, with general availability on May 1, 2026 ([Microsoft Agent 365](https://www.microsoft.com/en-us/microsoft-agent-365)). Microsoft announced Agent 365 GA for $15 per user and Microsoft 365 E7 for $99 per user in its March 9, 2026 Frontier Suite announcement ([Microsoft Official Blog](https://blogs.microsoft.com/blog/2026/03/09/introducing-the-first-frontier-suite-built-on-intelligence-trust/)); the May 1, 2026 security blog also describes Agent 365 as available standalone at USD15 per user per month or in Microsoft 365 E7 ([Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/05/01/microsoft-agent-365-now-generally-available-expands-capabilities-and-platform/integrations/)).

Microsoft's technical observability layer builds on OpenTelemetry and is designed to capture agent invocation traces, sessions, tool calls, and exceptions so Microsoft admin center, Defender, and Purview can support monitoring, compliance, and threat detection ([Microsoft Learn: Agent observability](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/reference/observability-schema/)).

## Grace-Mar Analogue

Grace-Mar maps the same control-plane concerns onto a personal and small-org cognitive-fork setting:

| Agent 365 concern | Grace-Mar local governance analogue |
|---|---|
| Observability | Inspection reports, gate-board views, merge receipts, cadence logs, runtime bundles, and workflow observability. |
| Governance | `recursion-gate.md`, authority map, runtime-vs-Record boundaries, and companion-approved promotion. |
| Identity / lifecycle | Portable working identity, runtime bundles, inter-fork package boundaries, and recipient-gated sharing. |
| Security / compliance | Source-of-truth ordering, evidence-linked proposals, validation exits, protected Record surfaces, and audit-friendly git history. |
| Risk management | Pre-merge oversight and review-before-canonicalization, rather than post-hoc cleanup after autonomous mutation. |

The analogy is useful, but limited. Agent 365 governs enterprise agent fleets. Grace-Mar governs the relationship between external agents, WORK surfaces, runtime continuity, and a companion-owned Record. The strongest complementarity is not scale; it is authorship.

## Possible Future Adapters

These are exploration paths, not committed roadmap items:

- **Redacted OTel-compatible export:** map selected runtime or workflow observability fields into an OpenTelemetry-shaped sample under explicit operator command. This requires privacy review, redaction rules, and clear proof that exported traces are not Record truth.
- **Agent 365 compatibility profile:** document how an external enterprise agent ID could reference an existing Grace-Mar runtime bundle or portable-working-identity export. This must remain a thin compatibility layer over current exports, not a second identity stack.
- **Admin-center style projection:** a read-only or stage-only board over active work, pending candidates, receipts, and skill surfaces. This belongs to the broader Cognitive Linear Board framing and must not approve or merge.

## Boundary Rules

- Do not add Agent 365 compatibility as a default runtime behavior.
- Do not create a telemetry schema or exporter without a separate privacy and redaction plan.
- Do not commit enriched traces by default; use explicit, redacted samples only when the operator asks.
- Do not treat Microsoft admin-center compatibility as merge authority, Record authority, or proof of truth.
- Do not move hosted-tier pricing or market packaging into architecture docs unless the operator explicitly opens a strategy note.

## Positioning

Grace-Mar can be described as a lightweight, local-first governance scaffold for cognitive forks. Agent 365 is the enterprise control-plane reference point; Grace-Mar is the human-gated personal substrate that keeps identity, evidence, skills, and runtime continuity legible without surrendering authorship.

## Related

- [Agent substrate](agent-substrate.md)
- [Observability](observability.md)
- [Runtime vs durable Record](runtime-vs-record.md)
- [Portable working identity](portable-working-identity.md)
- [MCP stack overview](mcp/mcp-stack-overview.md)
