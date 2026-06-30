# Frontier Agent Control Plane Direction


## Why this memo exists

As of May 2026, frontier AI development is converging on three pressures at once:

- agentic action across tools and long-horizon workflows
- compute and infrastructure as strategic substrate
- stronger institutional involvement in evaluation, safety, and deployment control

For strategy-codex, this means the project should not optimize to become "another smart assistant." The more durable direction is to become a **sovereign agent control plane**: a local-first operating layer for human-guided cognition and action, with explicit authority boundaries, inspectable receipts, reversible execution, and protected authorship.

## Product thesis

The project should evolve toward:

**A sovereign operating layer for human-guided cognition and action.**

That means:

- the system can coordinate work across chat, repo, browser, documents, and automations
- the human remains the authorizing center for durable identity and governed state
- memory, truth, and action are separated into distinct surfaces with different rules
- trust comes from inspectability and rollback, not from rhetorical confidence

## What the frontier implies

### 1. Compete on control plane, not raw model charisma

Frontier vendors are making models more agentic. That reduces the defensibility of "good conversation" as a moat. The more valuable layer is the one that answers:

- who can act
- what can be written
- what becomes canonical
- what requires approval
- what can be rolled back
- what counts as a receipt

This project already has the beginnings of that answer in the Record / Voice / WORK split, gated merge law, cadence surfaces, and stage-versus-merge distinction. Development should intensify those advantages.

### 2. Substrate sovereignty becomes more important, not less

As external vendors pull users toward hosted memory, hosted identity, and hosted agent loops, local-first governance becomes a stronger position.

The project should preserve:

- local canonical memory
- local governance and merge authority
- exportable identity artifacts
- portable, inspectable state rather than vendor-trapped synthesis

The goal is not isolation from frontier models. The goal is to use frontier models as helpers without letting them become the only place that meaning, continuity, or authorship lives.

### 3. Agent UX must foreground receipts, review, and reversibility

As systems become more proactive, "what happened?" becomes a central product question.

The project should treat the following as first-class user experience, not admin exhaust:

- execution receipts
- staged versus merged state
- visible approval boundaries
- clear rollback paths
- artifact provenance
- mode and authority changes

The right trust story is not "the agent is aligned." It is "the system shows its work, preserves boundaries, and can be corrected cleanly."

### 4. Supervised delegation beats autonomy theater

The frontier is normalizing agents that run in the background, call tools, and coordinate subagents. The project should support that pattern, but through bounded execution and explicit oversight rather than hidden autonomy.

Preferred posture:

- delegate work, not authorship
- automate staging, not governed merge
- use mode changes and escalation points intentionally
- require human sign-off where durable truth or identity is at stake

### 5. Identity surfaces and execution surfaces should diverge more cleanly

Many frontier products blur memory, action, and personality into a single conversational runtime. This project is stronger when it keeps them distinct:

- **Record** = authoritative, governed self-state
- **Voice** = queryable expression layer
- **WORK** = execution, drafting, strategy, tooling, and exploratory surfaces

That separation is not extra complexity. It is the main defense against silent authorship drift.

## Architecture consequences

### A. Treat strategy-codex as an agent control plane

The repo should increasingly act as a coordination substrate for multiple execution surfaces, not just as a prompt-and-doc store.

Target capabilities:

- route tasks across chat, local coding, browser, documents, and automations
- preserve shared authority vocabulary across those surfaces
- emit normalized receipts for actions and handoffs
- maintain stable surface contracts even as model providers change

### B. Prefer capability contracts over ad hoc integrations

Every major tool or agent surface should answer the same questions:

- what it can access
- what it can mutate
- what authority class it belongs to
- what receipt it emits
- what its rollback shape is
- what its failure mode is

This repo already has the beginnings of that discipline in `control-plane/` capability contracts. That pattern should expand, not remain optional niche documentation.

### C. Build continuity as explicit contract, not implied memory

Agent memory should remain inspectable and layered:

- canonical durable state
- session continuity
- derived observability
- temporary execution context

The project should resist the frontier tendency to let "the model remembers" replace clear continuity rules. Explicit file- and receipt-based continuity is slower to market but stronger as infrastructure.

### D. Keep human judgment load-bearing at the merge boundary

The hardest design temptation will be to smooth away approval friction. Some friction should be removed, but the authority boundary itself should remain visible and meaningful.

The right direction is:

- lighter approvals
- better review packets
- cleaner diffs
- stronger summaries

Not:

- silent governed merges
- identity updates through implication
- hosted memory replacing local approval

## Structural fit with receipt hardening

This memo and [unified-execution-receipts.md](unified-execution-receipts.md) do different jobs and should stay distinct.

- **This memo** sets the product thesis, architecture direction, and prioritization logic.
- **Unified execution receipts** defines the first concrete control-plane hardening wedge under that thesis.

The overlap is intentional but bounded:

- both care about inspectability, rollback, and cross-surface coherence
- only this memo should make broad product-direction claims
- only the receipt memo should define receipt-family normalization strategy

If these docs start repeating each other, keep this one at the level of thesis and sequence, and keep the other one at the level of control-plane execution detail.

## Next five implementation priorities

### 1. Unify receipts across execution surfaces

Create a more uniform receipt story for coding runs, browser actions, automations, review packets, and stage-only handbacks.

Why:

- trust scales with inspectability
- cross-surface work becomes legible
- rollback and audit improve immediately

### 2. Harden the local-first memory and continuity stack

Improve the distinction and observability across:

- Record truth
- memory / continuity
- WORK notebooks and lane artifacts
- execution-local temporary state

Why:

- frontier products are collapsing these layers
- your differentiation depends on not collapsing them

### 3. Standardize supervised delegation flows

Make delegation patterns more explicit for:

- task scoping
- plan approval
- background execution
- escalation
- human interrupt / redirect
- closure and durable outcome logging

Why:

- agentic behavior is becoming table stakes
- bounded delegation is one of the repo's strongest design instincts

### 4. Improve approval ergonomics without weakening sovereignty

Reduce operator burden through better summaries, grouped approvals, and smaller review surfaces.

Why:

- approval fatigue is real
- the answer is better review UX, not weaker governance

### 5. Build a first-class control-plane interface layer

Strengthen operator-facing surfaces that explain:

- what the system knows
- what it is doing
- what is pending
- what changed
- what needs a decision

Why:

- the frontier is moving from raw model interaction to orchestrated work environments
- your product should feel like an operating layer, not a scattered bundle of scripts

## Suggested implementation order

To keep the long arc coherent, use this order:

1. **Receipt crosswalk** - create the stable operator/developer map of receipt families, what they prove, and how they relate.
2. **Receipt field normalization** - align the highest-value shared fields across receipt families without forcing one schema.
3. **Derived receipt summary** - build the first operator-facing aggregation layer over governance, execution, inspection, and coordination surfaces.
4. **Delegation-flow hardening** - standardize supervised delegation paths once the receipt and review story is stronger.
5. **Approval-ergonomics improvements** - tighten grouped review, summaries, and decision surfaces without weakening the merge boundary.
6. **Control-plane interface layer** - present the resulting state as a first-class operating surface rather than a collection of lane-specific tools.

This order matters because it builds trust infrastructure before heavier orchestration.

## Anti-goals

Do not optimize the project toward:

- generic chatbot parity
- hidden autonomy as a prestige feature
- vendor-dependent memory as the main continuity layer
- prompt cleverness as substitute for control-plane design
- collapsing Record and WORK because it feels more seamless

## Decision rule

When choosing between two plausible features, prefer the one that increases:

- human authority
- inspectability
- portability
- rollback quality
- cross-surface coherence
- authorship preservation

Prefer against the one that mainly increases:

- vibe of autonomy
- vendor lock-in
- invisible statefulness
- seductive but unauditable convenience

## Bottom line

The frontier direction validates the deepest instinct already present in strategy-codex: the winning layer is not just better text generation. It is **governed orchestration with preserved authorship**.

The project should become better at coordinating powerful models and tools while staying visibly, structurally answerable to the human whose work and judgment it is meant to serve.
