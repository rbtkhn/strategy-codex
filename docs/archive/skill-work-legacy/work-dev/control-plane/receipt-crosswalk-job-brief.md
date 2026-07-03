# Job brief - Receipt Crosswalk

**Status:** WORK artifact. Not Record truth, not MEMORY, not gate approval.

## Objective

Create the first repo-native `receipt crosswalk` surface that makes strategy-codex receipt families legible as one control-plane map without pretending they are one universal log.

## Audience

Primary audience is the operator or coding agent working inside `work-dev` who needs to answer:

- what receipt surfaces exist
- what each one proves
- what each one does not prove
- where to look for review and rollback
- which surfaces affect governed state versus runtime/inspection/coordination only

Secondary audience is future integration/spec work that needs a stable reference before adding new receipt emitters or normalizing fields.

## Success criteria

- Would ship / would send test: another agent can use the crosswalk to choose the right receipt family for a new tool or workflow without inventing a new log by default.
- Functional bar: the output clearly indexes active receipt families, maps them to shared control-plane vocabulary, and links to their current docs or schemas.
- Quality bar: the crosswalk stays honest about authority differences and does not flatten merge, execution, inspection, and coordination into fake sameness.
- Proof or acceptance check: links resolve locally, the family map matches current doctrine in `unified-execution-receipts.md`, and the output is useful enough to reference from `work-dev/README.md`.

## Tone and voice

- Primary tone: terse, architectural, operator-facing
- Reference examples: `diagnostics-control-plane.md`, `agentic-receipt-map.md`, `safety-story-ux.md`
- Words, styles, or patterns to avoid: inflated manifesto language, fake universality, vague “trust the agent” phrasing

## Must include

- the active receipt families: governance, execution, inspection, coordination
- current concrete surfaces under each family
- what each surface proves
- what each surface does not prove
- review surface and rollback surface where meaningful
- explicit authority notes: `recordAuthority`, `gateEffect`, or family-equivalent language
- a short “when to add a new receipt family vs when to extend an existing one” rule

## Must avoid

- creating a new authority surface
- implying receipts prove truth rather than process
- proposing immediate migration of all existing schemas
- collapsing cadence or ritual logs into security-grade execution receipts
- quietly changing governed merge behavior

## Constraints

- Length / format: one compact markdown doc, table-heavy where useful
- Brand, legal, or governance limits: non-authoritative; no Record implications
- Technical limits: no schema rewrite required in this wedge
- Context budget: should be readable in one pass by an operator during implementation planning

## Positive examples

- [unified-execution-receipts.md](../unified-execution-receipts.md)
- [agentic-receipt-map.md](../agentic-receipt-map.md)
- [diagnostics-control-plane.md](../diagnostics-control-plane.md)

## Negative examples

- A pseudo-universal log spec that erases the difference between merge receipts, workbench receipts, MCP receipts, and cadence events
- A purely philosophical memo with no concrete index of live surfaces
- A surface that lists files but does not explain proof scope or authority boundaries

## Context and references

- Source files:
  - [unified-execution-receipts.md](../unified-execution-receipts.md)
  - [agentic-receipt-map.md](../agentic-receipt-map.md)
  - [../../../../../docs/action-receipts.md](../../../action-receipts.md)
  - [../workbench/README.md](../workbench/README.md)
  - [../../../../../docs/mcp/mcp-execution-receipts.md](../../../mcp/mcp-execution-receipts.md)
  - [safety-story-ux.md](../safety-story-ux.md)
- Prior briefs or outputs:
  - [frontier-agent-control-plane-direction.md](../frontier-agent-control-plane-direction.md)
- Data / links:
  - live receipt paths under `runtime/artifacts/`, `pipeline-events.jsonl`, `merge-receipts.jsonl`, and related runtime folders

## Routing

- Lane: `work-dev`
- Default tool or specialist: coding agent working in control-plane / architecture mode
- Human checkpoint: operator reviews the crosswalk before any schema-alignment or aggregation implementation starts

## Acceptance

- [ ] Objective is specific enough that another agent would know what to optimize.
- [ ] Audience and success criteria are explicit.
- [ ] Examples or constraints replace vague adjectives where possible.
- [ ] Any Record, MEMORY, or gate implications are named as separate approval paths.
