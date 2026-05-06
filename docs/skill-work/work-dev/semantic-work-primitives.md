# Semantic work primitives

**Status:** WORK doctrine note. This is a repo-native synthesis for `work-dev`, not a rewrite of core governance doctrine and not a Grace-Mar Record claim.

## Definition

A **semantic work primitive** is a unit of work whose meaning is legible to an agent, not just whose surface is reachable.

For a unit of work to be semantically legible, the environment should make visible enough of the following:

- what object is being touched
- what action is being proposed
- what that action means in domain terms
- what permissions apply
- whether the action is reversible
- how correctness is checked
- what consequences follow if it succeeds or fails

A button click is not, by itself, a semantic work primitive.  
A refund, a reschedule, a staged merge, a compliance exception, or a meeting brief can be one if the system exposes enough meaning around it.

## Three layers: access, meaning, authority

This note uses a three-layer stack:

| Layer | Definition |
|------|------------|
| **Access** | The agent can touch the surface. |
| **Meaning** | The agent understands what kind of action this is in domain terms. |
| **Authority** | The system knows who may do it, under what review path, and with what consequences. |

Repo-native translation:

- **access** = browser reach, CLI reach, APIs, connectors, MCPs, filesystem or app surface access
- **meaning** = whether the unit of work is legible as a real object/action rather than only as a UI gesture
- **authority** = whether the boundary, approval path, and receipt/validation story are explicit

## Why this matters in strategy-codex

`strategy-codex` already has comparatively strong **authority** surfaces:

- runtime-vs-Record separation
- companion gate discipline
- staging before merge
- explicit approval boundaries
- observability and receipts on many operational paths

What this frame adds is a clearer name for the next design frontier:

- not merely giving agents more tools
- but making non-code work more semantically legible

In other words:

- this repo already resists confusing access with authority
- this note helps us also resist confusing access with meaning

## Why coding agents arrived first

Coding environments expose unusually rich semantic feedback:

- types
- tests
- linters
- modules
- package boundaries
- git history
- executable failure signals

That makes code more agent-legible than many other domains. The agent can inspect state, act on state, observe failure, and revise.

Many non-code workflows still hide meaning behind:

- forms
- dashboards
- calendars
- docs
- unwritten social context
- implicit approval norms

So the wedge is not "all work becomes coding."  
The wedge is that coding already exposes denser semantic structure than most other knowledge work.

## Browser/computer use stance

Browser and computer use are still important. They are often the only way to reach the messy middle of real work.

But they are best understood as:

- a **necessary bridge**
- a **shallow adapter**
- **not** a durable moat by themselves

This repo should continue to prefer the richest available interface:

1. typed / permissioned object
2. API / connector / MCP
3. browser / desktop fallback

That ordering is about semantic richness, not just convenience.

## Repo-native implication

The practical implication for `work-dev` is:

- Grace-Mar already has strong Record boundaries and authority surfaces
- the next frontier is making non-code work more semantically legible, not merely more tool-accessible

This affects how we evaluate new tools and workflows:

- Does the agent merely have access?
- Does the environment expose what the action means?
- Does the system make permissions, reversibility, validation, and review visible?

Those questions are often more important than "can the model click the button?"

## What this note does not do

This note does **not**:

- rename existing authority doctrine
- change the runtime-vs-Record contract
- claim the repo already exposes full semantic primitives for all domains
- require immediate schema or MCP changes

It is a language upgrade and an evaluation lens.

## Deferred implementation wedge

A later, separate pass may decide to enrich capability or workflow contracts with fields such as:

- unit of work
- semantic object
- reversibility
- approval requirement
- validation path
- blast radius

That is explicitly deferred. This pass is about architectural clarity, not schema churn.

## Cross-references

- [agentic-environment-principles.md](agentic-environment-principles.md) - environment quality, bounded execution, continuity, and policy before prompt cleverness
- [runtime-vs-record.md](../../runtime-vs-record.md) - why runtime utility does not become Record truth
- [authority-map.md](../../authority-map.md) - where authority lives and how the repo separates permission from execution
- [managed-agent-design.md](managed-agent-design.md) - persistent-agent and operator-runbook implications
- [../../../docs/mcp/README.md](../../../docs/mcp/README.md) - governed MCP surfaces as examples of structured access that still require clear authority handling
