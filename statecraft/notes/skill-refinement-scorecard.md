---
note_id: skill-refinement-scorecard
note_type: synthesis
authority_level: review-needed
source_basis: mixed
essay_candidate: false
created_at: 2026-06-18
updated_at: 2026-06-28
---
# Skill Refinement Scorecard


## Purpose

This note gives `statecraft/` a reusable way to judge whether skill refinements are producing real operational gains rather than cleaner wording alone.

The point is not to reward doctrinal elegance. The point is to measure whether the skill layer causes less misrouting, less taxonomy drift, less public-language opacity, and less operator correction load over time.

## Core Claim

The expected long-term benefit of skill refinement is:

`truer routing -> lower recovery cost -> more consistent output -> faster operator iteration`

Skills are not just prompt wrappers. They are active carriers of repo law. If they teach old topology, they quietly reintroduce obsolete structure into live work. If they teach current topology, they reduce the amount of energy the system spends recovering from its own instructions.

## What These Refinements Were Trying To Fix

The current pass targeted five recurring failure surfaces:

- CIV-STATE retrieval skipping the `shelf-reader -> primary-sources -> secondary-sources -> return` switchboard
- `archive/` and `source-archive/` blur in source intake
- lane routing forgetting that `/codex` is continuity beneath `statecraft/`, not a replacement for transcript-family intake
- public-facing prose inheriting internal doctrine language without translation
- note promotion and essay promotion drifting back into mirror logic or weak prose-class distinction

## Scorecard

### 1. First-pass placement accuracy

Definition:

- percent of new artifacts that land in the correct top-level surface without later manual re-homing

Examples:

- `source-archive/`
- `/codex`
- `statecraft/`
- `singularity/`
- `notes/`
- `essays/`

Targets:

- acceptable operating baseline: `>= 85%`
- strong long-term target: `>= 95%`

### 2. Skill-induced correction rate

Definition:

- percent of skill-run outputs that require manual correction because the skill routed to the wrong layer or wrong artifact class

Targets:

- near-term: `< 15%`
- long-term: `< 5%`

### 3. Prose classification accuracy

Definition:

- percent of promoted prose objects that remain correctly classified as `note` or `essay` after later review

Targets:

- near-term: `>= 80%`
- long-term: `>= 90%`

### 4. Duplicate-authority ambiguity rate

Definition:

- number of cases where a promoted object creates uncertainty about canonical location or governing copy

Targets:

- near-term: reduce by `50%`
- long-term: `< 1` ambiguous case per `20` promotions

### 5. Public-vocabulary translation success

Definition:

- number of unexplained opaque internal terms left in outward-facing prose

Watch terms:

- `carriage`
- `switchboard`
- `settlement-bearing`
- `legitimacy grammar`
- `outward instrument`

Targets:

- near-term: `< 3` opaque internal terms per long essay
- long-term: `0` unexplained opaque internal terms in public prose

### 6. CIV-STATE retrieval discipline

Definition:

- percent of CIV-STATE retrieval runs that correctly distinguish:
  - `shelf-reader` for traversal guidance
  - `primary-sources` when wording is decisive
  - `secondary-sources` only when interpretive difficulty appears

Targets:

- near-term: `>= 75%`
- long-term: `>= 90%`

### 7. Source-truth contamination rate

Definition:

- number of times summaries, synthesis, or control notes leak into `source-archive/`

Targets:

- near-term: `< 1` per month
- long-term: `0`

### 8. Operator clarification load

Definition:

- how often the operator must restate “put that in X, not Y” after invoking a relevant skill

Targets:

- near-term: reduce by `30-50%`
- long-term: reduce by `70%+`

### 9. Time-to-usable-output

Definition:

- median turns from skill invocation to a correctly shaped usable artifact

Targets:

- near-term improvement: `20-30%` faster
- long-term improvement: `40%` faster on repeated workflows

### 10. Skill integrity

Definition:

- validation pass rate
- portable/local sync mismatch count

Targets:

- validation: `100%`
- sync mismatches after edits: `0`

## Best Lead Indicator

The best compact benchmark is:

`manual re-routing events per 20 skill-driven tasks`

Targets:

- acceptable current threshold: `<= 4`
- strong long-term threshold: `<= 1`

This is the best single indicator because it captures whether the skill layer is actually reducing recovery work rather than just sounding more correct.

## Monthly Use

A lightweight monthly check can be done with four questions:

1. How many recent skill-driven tasks landed in the wrong top-level surface?
2. How many note/essay promotions had to be reclassified later?
3. How often did public prose leak opaque internal jargon?
4. How often did the operator have to manually redirect the skill’s placement logic?

If those numbers are falling, the refinements are doing real work.

## Boundary

This scorecard is for operational judgment, not false precision theater.

It does not require exhaustive logging of every run. Approximate operator review over a bounded sample is usually enough to show whether the skill layer is becoming more truthful or merely more elaborate.
