> **ARCHIVED (Grace-Mar corpus).** Fork growth is **not** default strategy-codex routing. **`fork revive` only** — see [grace-mar-instance-boundary.md](../../docs/grace-mar-instance-boundary.md).

# Atlassian Rovo Alignment

**Status:** WORK / architecture positioning; issue-tracker substrate comparison; not Record truth, not a roadmap commitment.

**Last updated:** 2026-05-03

Atlassian Rovo is the closest external reference for the issue-tracker-as-agent-substrate pattern. Unlike hyperscaler agent control planes, Rovo starts from the work substrate itself: Jira work items, Confluence pages, comments, status, ownership, permissions, automation, and audit history. That is why it maps so directly to Grace-Mar's `recursion-gate.md`, WORK lanes, receipts, cadence logs, bridge/dream handoffs, and architecture docs.

The important lesson is not that Grace-Mar should become Jira. It is that durable coordination objects become agent-operable state when they have clear ownership, lifecycle, permissions, comments, and replayable history. Grace-Mar applies that pattern to cognitive-fork governance with a stronger boundary: agents may route and stage, but only companion-approved promotion can create Record truth.

## Atlassian Reference Point

Atlassian describes Rovo agents as configurable AI teammates available in Rovo Chat, automation rules, Confluence pages, Jira issues, and Studio. Rovo agents can take actions such as organizing, creating, and editing Jira work items or Confluence pages when the user has permission ([Atlassian Support: Rovo agents](https://support.atlassian.com/rovo/docs/agents/)).

Atlassian supports out-of-the-box third-party MCP agents in Confluence and Jira. Rovo acts as the LLM layer, while third-party MCP servers provide tool invocation; site admins must enable each MCP server before users can access it ([Atlassian Support: out-of-the-box third-party MCP agents](https://support.atlassian.com/rovo/docs/out-of-the-box-third-party-mcp-agents/)).

Atlassian also provides a Rovo MCP Server as a cloud bridge between Atlassian Cloud and external AI tools. It can give tools real-time access to Jira, Confluence, and Compass data through OAuth 2.1, with access governed by the user's existing Atlassian permissions ([Atlassian Support: Rovo MCP Server getting started](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/)).

Atlassian's MCP guidance recommends least privilege, review of high-impact changes, and audit-log monitoring; its third-party MCP usage guidelines also warn that data sent to third-party MCP providers is outside Atlassian's commitments while processed or stored there ([Atlassian Support: use Rovo MCP Server](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/use-atlassian-rovo-mcp-server/); [Atlassian Support: third-party MCP usage guidelines](https://support.atlassian.com/security-and-access-policies/docs/rovo-out-of-the-box-third-party-mcp-agents-usage-guidelines/)).

## Grace-Mar Analogue

Grace-Mar maps the issue-tracker substrate pattern onto cognitive-fork governance:

| Atlassian / Rovo pattern | Grace-Mar local governance analogue |
|---|---|
| Jira work items | `recursion-gate.md` candidates, WORK tasks, lane notebooks, and candidate lifecycle. |
| Confluence pages | Architecture docs, strategy notebook, evidence/work docs, and substrate framing. |
| Status / ownership | Candidate states, authority map, companion approval, and operator lane responsibility. |
| Comments / history | Merge receipts, cadence logs, bridge/dream handoffs, runtime receipts, and git history. |
| Rovo agents | Skill-work agents, operator assistants, conductor/coffee/dream workflows. |
| MCP servers | Grace-Mar MCP adapters, runtime complements, and external harness membranes. |
| Admin tool controls | Protected surfaces, stage-only workflows, validation exits, and no merge authority. |

The substrate matters because agents need more than context. They need state with lifecycle, permissions, provenance, and a place to put proposed changes without confusing proposals for truth.

## Boundary Lesson

The strongest Grace-Mar lesson from Rovo is:

**Existing filesystem or tool access must not imply Record authority.**

Atlassian permissioning lets an MCP client act with the user's access. Grace-Mar must preserve a stricter membrane: a tool may have filesystem access, MCP access, or runtime credentials and still have no right to approve candidates, edit protected Record surfaces, or treat successful tool output as canonical truth.

## Possible Future Adapters

These are exploration paths, not committed roadmap items:

- **Issue-tracker projection:** document a read-only or stage-only view over gate candidates, active work lanes, receipts, and handoffs. This belongs to Cognitive Linear Board framing, not a second source of truth.
- **MCP intake hardening:** compare Atlassian's admin-enabled MCP server model with Grace-Mar MCP admission docs and protected-surface rules.
- **Candidate lifecycle comparison:** map Jira-style statuses to Grace-Mar proposal states for operator UX only, without changing the gate schema.
- **Egress review checklist:** adapt Atlassian's third-party MCP warning into a Grace-Mar checklist for external runtime complements and connector use.

## Boundary Rules

- Do not describe Grace-Mar as Jira, Confluence, Rovo, or an Atlassian replacement.
- Do not treat issue status, comments, workflow automation, MCP output, or filesystem permissions as Record truth.
- Do not create an Atlassian integration, Jira schema, Rovo agent, MCP bridge, or candidate-status migration without a separate implementation plan.
- Do not imply that tool access, OAuth permission, admin enablement, or successful automation grants merge authority over the Record.
- Do not duplicate Grace-Mar's existing gate, authority map, runtime-complements, or MCP admission stack.

## Positioning

Atlassian validates the work-substrate side of the agentic turn: durable coordination objects with permissions, lifecycle, comments, automation, and audit history become powerful agent-operable state. Grace-Mar applies that pattern to personal cognitive governance: agents can route, draft, and stage around the Record, but only the companion can promote truth into it.

## Related

- [Agent substrate](agent-substrate.md)
- [Agent 365 alignment](agent-365-alignment.md)
- [AWS Bedrock AgentCore alignment](aws-agentcore-alignment.md)
- [Runtime vs durable Record](runtime-vs-record.md)
- [Runtime complements](runtime/runtime-complements.md)
- [MCP stack overview](mcp/mcp-stack-overview.md)
