> **ARCHIVED (Grace-Mar corpus).** Fork growth is **not** default strategy-codex routing. **`fork revive` only** — see [grace-mar-instance-boundary.md](../../docs/grace-mar-instance-boundary.md).

# AWS Bedrock AgentCore Alignment

**Status:** WORK / architecture positioning; not Record truth, not a roadmap commitment.

**Last updated:** 2026-05-03

AWS Bedrock AgentCore is the cleanest hyperscaler analogue for Grace-Mar's runtime-complements and observability layer. It is not a cognitive-fork system and should not be treated as one. Its relevance is infrastructural: secure agent runtime, memory, identity, gateways, tools, policy, observability, and production operation.

Grace-Mar should not be positioned as an AWS managed runtime or cloud agent platform. Its local analogue is narrower: a human-gated cognitive-fork substrate where runtime helpers may act around the Record, but durable identity, evidence, skills, and memory claims require companion-approved promotion.

## AWS Reference Point

AWS describes Amazon Bedrock AgentCore as an agentic platform for building, deploying, and operating agents securely at scale using any framework and foundation model. The overview emphasizes permissions and governance, secure scale, production monitoring, and modular services that can work together or independently with open-source frameworks and different foundation models ([AWS docs: AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)).

AWS AgentCore observability automatically generates session metrics for agents running in AgentCore runtime and can also monitor memory, gateway, built-in tools, identity, and policy resources through CloudWatch generative AI observability, logs, metrics, spans, and traces ([AWS docs: AgentCore generated observability data](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-service-provided.html)).

AWS also documents explicit observability configuration for AgentCore resources, including CloudWatch Transaction Search, runtime, memory, gateway, built-in tools, identity resources, and support for AWS Distro for OpenTelemetry instrumentation for custom metrics and agents hosted outside AgentCore ([AWS docs: Add observability to AgentCore resources](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html)).

## Grace-Mar Analogue

Grace-Mar maps AgentCore's production-runtime concerns onto a local cognitive-fork governance setting:

| AgentCore concern | Grace-Mar local governance analogue |
|---|---|
| Runtime | Runtime complements, worker traces, prepared context, and bounded external harnesses. |
| Memory | `self-memory.md` and runtime memory as continuity only, not Record truth. |
| Gateway / tools | MCP adapters, tool admission docs, and lane-specific action boundaries. |
| Identity | Authority map, protected Record surfaces, and explicit operator/companion authority. |
| Policy | Runtime-vs-Record doctrine, recursion gate, and review-before-canonicalization. |
| Observability | Receipts, validation exits, cadence logs, runtime bundles, and report artifacts. |
| CloudWatch / OTel | Possible redacted export shapes, but only under explicit operator command and privacy review. |

The analogy is useful, but bounded. AWS optimizes secure production operation for agents across cloud resources. Grace-Mar optimizes local authorship: what can be read, what may be drafted, what remains runtime-only, and what may become durable Record truth.

## Possible Future Adapters

These are exploration paths, not committed roadmap items:

- **AgentCore-shaped runtime receipt sample:** map selected Grace-Mar runtime-complement receipts into a CloudWatch / AgentCore-style sample, redacted and generated only by explicit operator command.
- **Policy resource comparison:** compare AgentCore policy observability with Grace-Mar authority-map and runtime-vs-Record boundaries, without creating a second policy engine.
- **Gateway / MCP compatibility note:** document how Grace-Mar MCP adapters differ from cloud gateways and how stage-only tool use remains protected.
- **Memory boundary comparison:** contrast AgentCore memory metrics with Grace-Mar `self-memory.md` and runtime memory so session continuity does not become canonical truth.

## Boundary Rules

- Do not describe Grace-Mar as a replacement for Amazon Bedrock AgentCore, CloudWatch, IAM, or Bedrock governance.
- Do not treat cloud runtime success, metrics, spans, traces, memory, gateway logs, or policy events as Record truth.
- Do not create an AgentCore adapter, CloudWatch exporter, OTel pipeline, gateway bridge, or policy integration without a separate implementation plan.
- Do not imply that cloud identity, runtime deployment, gateway approval, or policy telemetry grants merge authority over the Record.
- Do not duplicate Grace-Mar's existing runtime-complements, MCP, or portability stack; any compatibility layer must be thin and explicitly stage-only.

## Positioning

AWS validates the production-runtime side of the agentic turn: secure deployment, memory, gateways, identity, policy, and observability for agents operating at scale. Grace-Mar adds a local cognitive-fork governance layer: human-gated meaning, evidence promotion, portable Record surfaces, and durable separation between runtime help and canonical truth.

## Related

- [Agent substrate](agent-substrate.md)
- [Agent 365 alignment](agent-365-alignment.md)
- [Apple Intelligence alignment](apple-intelligence-alignment.md)
- [Google Gemini / Vertex agent alignment](google-gemini-alignment.md)
- [Runtime vs durable Record](runtime-vs-record.md)
- [Runtime complements](runtime/runtime-complements.md)
- [MCP stack overview](mcp/mcp-stack-overview.md)
