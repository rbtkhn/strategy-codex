# Google Gemini / Vertex Agent Alignment

**Status:** WORK / architecture positioning; not Record truth, not a roadmap commitment.

**Last updated:** 2026-05-03

Google's closest analogue to Agent 365 is also a stack rather than a single product: Vertex AI Agent Builder for building, scaling, and governing enterprise agents; Agentspace / Gemini Enterprise-style workplace access for enterprise search, assistants, and custom agents; Google Cloud IAM and security controls for permissions; and Android / Gemini surfaces for personal assistant behavior. The alignment with Grace-Mar is strongest around open agent infrastructure, source-grounded enterprise data access, tool governance, interoperability, and observability.

Grace-Mar should not be positioned as a Google Cloud agent platform or managed runtime. Its local analogue is narrower: a human-gated cognitive-fork substrate where agents may use governed context, produce receipts, and propose changes without becoming the authority over identity, evidence, skills, or memory.

## Google Reference Point

Google describes Vertex AI Agent Builder as a platform to build, scale, and govern enterprise-grade agents grounded in enterprise data. Its product page emphasizes agent development with ADK and open frameworks, managed runtime, session and memory support, evaluation, observability, registry, agent identity through IAM, Model Armor, Security Command Center, MCP, and Agent2Agent interoperability ([Google Cloud: Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder)).

Google's documentation describes Vertex AI Agent Builder as a suite for building, scaling, and governing AI agents in production across the full agent lifecycle ([Google Cloud docs: Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)).

Google Agentspace is described as an intranet search, AI assistant, and agentic platform that connects organizational data sources with permissions-aware access and can host custom AI agents ([Google Cloud: What is Google Agentspace?](https://cloud.google.com/agentspace/docs/overview)). Its security documentation highlights IAM, Workforce Identity Federation, Google Identity, Workload Identity Federation, VPC Service Controls, encryption with CMEK, audit logging, and compliance controls ([Google Cloud: Agentspace security overview](https://cloud.google.com/agentspace/agentspace-enterprise/docs/security-overview)).

## Grace-Mar Analogue

Grace-Mar maps Google's agent-platform concerns onto a local cognitive-fork governance setting:

| Google concern | Grace-Mar local governance analogue |
|---|---|
| Build / scale / govern agents | Portable skills, WORK lanes, runtime complements, and explicit stage-only execution surfaces. |
| Enterprise data grounding | SELF-LIBRARY, EVIDENCE, source-of-truth ordering, and retrieval boundaries. |
| Agent identity / IAM | Authority map, protected surfaces, operator permissions, and companion-approved promotion. |
| Observability / tracing | Receipts, cadence logs, validation exits, runtime bundles, and observability reports. |
| Registry / approved agents and tools | Portable skills manifest, MCP admission docs, and skill-work lane boundaries. |
| A2A / MCP interoperability | MCP adapters, runtime complements, and portable export/import contracts. |
| Memory / sessions | Runtime memory and self-memory as non-Record continuity, never canonical truth. |

The analogy is useful, but bounded. Google optimizes cloud-managed agent development, enterprise data access, and production orchestration. Grace-Mar optimizes local authorship: what agents are allowed to read, what they may draft, and what can become durable Record truth only after human review.

## Possible Future Adapters

These are exploration paths, not committed roadmap items:

- **Vertex-shaped observability sample:** map selected Grace-Mar runtime receipts into a Google-style tracing or observability sample under explicit operator command, with privacy and redaction review first.
- **Agentspace-style read surface:** explore a read-only projection over active work, skills, evidence pointers, and pending gate candidates. This should remain a Cognitive Linear Board variant, not a managed-agent registry.
- **A2A / MCP compatibility note:** document how Grace-Mar runtime complements could interoperate with agent-to-agent or MCP-style systems while preserving stage-only writes.
- **Grounding contract comparison:** compare Google enterprise-data grounding with Grace-Mar SELF-LIBRARY / EVIDENCE boundaries so retrieval does not become Record promotion.

## Boundary Rules

- Do not describe Grace-Mar as a replacement for Vertex AI Agent Builder, Agentspace, Gemini Enterprise, or Google Cloud IAM.
- Do not treat Google-style memory, session state, traces, or enterprise search results as canonical truth.
- Do not create a Google adapter, managed runtime, registry, A2A bridge, or observability exporter without a separate implementation plan.
- Do not imply that cloud identity, IAM, registry approval, or tool governance grants merge authority over the Record.
- Do not duplicate Grace-Mar's existing portability stack; any compatibility profile must be thin over runtime bundles, MCP docs, and portable-working-identity exports.

## Positioning

Google validates the infrastructure side of the agentic turn: open frameworks, managed runtimes, enterprise data grounding, tool governance, observability, and inter-agent protocols. Grace-Mar adds a local cognitive-fork governance layer: human-gated meaning, evidence promotion, portable Record surfaces, and durable separation between runtime help and canonical truth.

## Related

- [Agent substrate](agent-substrate.md)
- [Agent 365 alignment](agent-365-alignment.md)
- [Apple Intelligence alignment](apple-intelligence-alignment.md)
- [Runtime vs durable Record](runtime-vs-record.md)
- [Runtime complements](runtime/runtime-complements.md)
- [MCP stack overview](mcp/mcp-stack-overview.md)
