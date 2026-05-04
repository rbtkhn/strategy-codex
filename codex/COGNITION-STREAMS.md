# Polyphonic Cognition Streams

WORK only; not Record.

## Purpose

Strategy-codex is scaffolded around **polyphonic cognition streams**: durable interpretive voices that can receive daily inputs, preserve source provenance, and be compared contrapuntally without forcing synthesis.

The current lattice has eight streams: `Alkorshid`, `Diesen`, `Davis`, `Mercouris`, `Crooke`, `Parsi`, `Pape`, and `Ritter`. The count is not permanent; filenames, schemas, and public doctrine should stay count-neutral.

## Stream Model

A cognition stream is the top-level analytical unit. It carries:

- **Interpretive voice:** the stream's characteristic way of seeing strategy.
- **Axis:** a compact orientation label such as `Synthesis`, `Order`, or `Escalation`.
- **Source habits:** where the stream is usually fed from, including host channels, essays, interviews, transcripts, or operator-supplied captures.
- **Contrapuntal relations:** harmony, tension, bridges, absences, and falsifiers against other streams.
- **Automation readiness:** enough routing structure that future daily stream input can become reliable when tooling improves.

Do not treat streams as a hierarchy. A host/channel stream and an expert-lens stream can be equally central even when their source surfaces differ.

## Stream Profile Calibration

Use `skill-elicitation` as an optional checkpoint when a stream profile needs operator judgment that cannot be inferred safely from sources alone. High-value prompts include:

- What makes this stream's interpretive voice distinct?
- Where does this stream converge with or diverge from the others?
- Which recurring mechanism, failure mode, or active weave cue belongs in the profile?
- Which civ-mem lens is live here, and what would falsify the analogy?

This checkpoint is review-first WORK. It may refine stream profiles, routing notes, or EOD page choices after confirmation, but it does not auto-ingest sources, compose pages, or create Record claims.

## Legacy Thread Handles

`thread:<expert_id>` remains a low-level routing and provenance handle. It is not the public scaffold.

Use `thread:<expert_id>` when a raw input, inbox line, transcript entry, or strategy-page block needs a stable join key for:

- speaker attribution
- rolling transcript triage
- historical drift checks
- predictive accuracy checks
- legacy script compatibility

New prose should prefer **cognition stream** when naming the analytical lane, and mention `thread:<expert_id>` only when discussing routing, file paths, or machine joins.

## Current Stream Map

| Stream | Stable handle | Axis | Source/provenance note |
|--------|---------------|------|------------------------|
| Alkorshid | `thread:alkorshid` | Synthesis | Dialogue Works / host-framing captures |
| Diesen | `thread:diesen` | Order | Glenn Diesen channel and multipolar-order inputs |
| Davis | `thread:davis` | Conflict | Daniel Davis / military feasibility inputs |
| Mercouris | `thread:mercouris` | Statecraft | Alexander Mercouris and The Duran captures |
| Crooke | `thread:crooke` | Process | Alastair Crooke essays and interviews |
| Parsi | `thread:parsi` | Scope | Trita Parsi / negotiation-scope inputs |
| Pape | `thread:pape` | Escalation | Robert Pape / escalation-clock inputs |
| Ritter | `thread:ritter` | Mechanics | Scott Ritter / military-technical inputs |

The stable handle column is intentionally a compatibility layer. The stream name is the public analytical label.

## Daily Input Direction

The long-term goal is daily stream input automation. This pass does not implement that automation.

Minimum future requirements:

- reliable source discovery
- timestamped provenance capture
- dedupe across channels, reposts, and transcript mirrors
- raw-input normalization
- `cognition_stream` / `thread:` routing
- human review before notebook mutation

Until those are feasible, daily capture remains operator-guided: inbox first, raw-input when warranted, then end-of-day composition.

## Derived Graph

The derived graph lives under `artifacts/skill-work/work-strategy/interview-graph/` and emits count-neutral `cognition-streams-graph.*` artifacts.

The graph is an orientation surface, not notebook truth. Canonical strategy judgment remains in raw-input, `strategy-page` blocks, and `chapters/YYYY-MM/days.md`.
