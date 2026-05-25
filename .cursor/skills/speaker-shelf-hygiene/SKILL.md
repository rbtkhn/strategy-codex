---
name: speaker-shelf-hygiene
preferred_activation: speaker shelf
description: >-
  Audit or repair a strategy-codex speaker shelf when the work is about person
  arcs, routing stacks, month support, raw-input benches, compatibility residue,
  or citation hygiene. Use for requests like "audit the ritter-arc", "compare
  freeman/parsi/ritter", "align these arcs", "what are the thinnest months", or
  "make sure nothing is wrongly excluded from the arc".
version: 0.1.0
tags:
  - operator
  - strategy-codex
  - speakers
  - shelf
  - arcs
  - routing
---

# Speaker shelf hygiene

**Preferred activation (operator):** say **`speaker shelf`**.

Use this skill when the question is about whether a speaker shelf is **shaped correctly**, **complete enough**, and **citation-safe enough** to serve as a durable notebook object.

This skill is for:

- person-arc audits
- month-by-month shelf breakdowns
- comparing one speaker shelf to another
- aligning multiple shelves to the same retrieval contract
- deciding whether a month deserves bounded support
- checking whether raw-input items were wrongly excluded
- fixing placeholder leakage and compatibility overreach

This skill is **not** for:

- daily YouTube discovery or missing-episode recovery
- transcript cleanup as such
- cross-speaker `A vs B` ownership disputes that belong under `relations/`
- generic statecraft synthesis

For those cases, prefer:

- [`check-streams`](../check-streams/SKILL.md) for live source discovery and raw-input recovery
- [`transcript-cleanup`](../transcript-cleanup/SKILL.md) for transcript text cleanup
- [`speaker-relations-membrane`](../speaker-relations-membrane/SKILL.md) for neutral relation-note placement
- [`skill-strategy`](../skill-strategy/SKILL.md) for notebook synthesis and strategy-page work

## Shared shelf contract

Unless a local shelf explicitly says otherwise, treat the canonical speaker stack as:

1. `person arc`
2. `routing`
3. `raw-input index` or equivalent appearance bench
4. `helix / crossing surface`
5. one `support spine` appropriate to the speaker
6. bounded `month / strand support` for mature retrieval months
7. `compatibility residue`, clearly demoted

Short rule:

`front door -> support spine -> provenance bench -> compatibility last`

The shelf should make these distinctions legible without forcing every speaker into the exact same shape.

Wrapper note:

- `index.md` and `README.md` may sit above the canonical stack as wrapper front doors
- wrappers do not replace the `person arc`, `routing`, `raw-input`, or `helix` jobs
- a wrapper passes only if it routes cleanly into those owned surfaces without making a legacy file feel primary

## Audit workflow

### 1. Map the live route stack

Open the speaker folder and identify:

- any wrapper front doors such as `index.md` or `README.md`
- the person arc
- the routing note or equivalent front-door guidance
- the raw-input bench
- the helix or cross-host comparison surface
- the recurring support spine
- any month-level support surfaces
- any bare `*-thread.md` or `*-transcript.md` compatibility residue

Use these references:

- [`codex/speakers/README.md`](../../../codex/speakers/README.md)
- [`codex/speakers/map/open-first-routes.md`](../../../codex/speakers/map/open-first-routes.md)
- [`codex/speakers/_templates/speaker-surface-orthogonality-review-template.md`](../../../codex/speakers/_templates/speaker-surface-orthogonality-review-template.md)

### 2. Classify surfaces by job

For each surface, ask:

- is this a first-open route?
- is this a support spine?
- is this a provenance bench?
- is this a comparison surface?
- is this compatibility residue only?

Do not let a compatibility file silently function as a primary surface.

### 3. Audit month support

When the user asks for a month-by-month breakdown:

- compare actual raw-input / appearance density against the shelf's visible month support
- identify which months are mature retrieval months
- identify which months are only continuity carryover
- note whether a mature month still lives only inside compatibility residue

Use the same decision rule across shelves:

- mature retrieval month -> dedicated bounded support surface
- continuity carryover month -> leave in compatibility residue

Exception:

- if a month is mature but its useful first-open jobs are already cleanly owned by host-local arcs, the shelf may use a `speaker-owned support spine` that explains why chronology stays host-led instead of creating a native speaker month page
- in that case, the audit should say explicitly that the month is mature, but `host-led mature` rather than `speaker-month-led`

### 4. Arc-preserving repair priority

Do not rank thin raw-inputs by incompleteness alone. Rank them by how much shelf truth they damage if they remain thin.

Use a two-step workflow:

1. classify the month
2. rank the thin captures inside that month

Month-status labels:

- `continuity carryover` = useful continuity, but not yet a bounded support month
- `mature bridge month` = a real retrieval month where the crisis logic or recurring strands are clearly forming, but not yet fully stabilized
- `mature dense-core month` = a mature month where repeated structures are stable enough to justify strong bounded support and first-open month retrieval

Short rule:

`month status first -> repair priority second`

#### Completion benchmark

For high-value or main speakers, the long-run shelf-completion target is not merely broad capture coverage. The real benchmark is:

- `mature every segment`

In practice this means:

- each important month becomes a real bounded retrieval segment
- each month carries the correct maturity judgment
- no structurally important month remains only raw-input spillover when it materially shapes the arc
- neighboring months form a legible progression rather than a pile of repaired fragments
- major arc-threads can be followed month over month without forcing reconstruction from thin gaps

Use this as the density standard for mature speaker shelves:

- not file count
- not transcript count
- but month-by-month retrieval maturity across the speaker's canonical run

For audit language, distinguish:

- `segment completeness` = the important months exist as canonical support surfaces
- `segment maturity` = each month is thick enough and correctly classified for bounded reading
- `arc continuity` = the month ladder reads as a real progression
- `thread continuity` = major strands remain traceable across adjacent months

If a month is already mature but several key captures remain header-only, stub-level, or otherwise too thin to carry real retrieval weight, say so explicitly:

- `mature but structurally under-repaired`

Treat those thin captures as structural shelf inputs, not only provenance defects.

#### Repair rubric for thin captures

Score each thin or stub candidate on these six axes, `0-3` each:

- `Body deficit`
  - `0` = substantial body already present
  - `1` = usable but thin or provenance-light
  - `2` = partial / weak body
  - `3` = header-only stub, placeholder, or effectively empty
- `Month dependence`
  - `0` = little effect on month support
  - `1` = helpful but non-essential
  - `2` = materially strengthens the month's support logic
  - `3` = one of the captures the month's retrieval identity clearly depends on
- `Sequence damage`
  - `0` = absence barely affects sequence legibility
  - `1` = weakens a local run
  - `2` = breaks a visible crisis or argument sequence
  - `3` = leaves a major jump in a high-value escalation run
- `Motif load`
  - `0` = mostly one-off
  - `1` = touches one recurring thread
  - `2` = materially reinforces one major motif
  - `3` = reinforces multiple core motifs at once
- `Tone-preservation`
  - `0` = little tonal value
  - `1` = modest tonal support
  - `2` = preserves a visible rhetorical or emotional inflection
  - `3` = preserves a major temperature jump or hardening turn needed for later support surfaces
- `Shelf leverage`
  - `0` = low downstream shelf value
  - `1` = useful to one surface
  - `2` = improves more than one of raw-input bench, month support, helix, routing, or support spine
  - `3` = high leverage across several shelf surfaces

Score bands:

- `0-6` = low
- `7-10` = medium
- `11-14` = high
- `15-18` = critical

Tie-break order:

1. higher `Month dependence`
2. higher `Sequence damage`
3. higher `Tone-preservation`
4. earlier item inside the crisis run or month sequence

Operator-facing output may use compact lines like:

- `2026-02-14 | critical | breaks February escalation run; reinforces Ukraine/Iran/Europe coupling; needed for mature month support`

This doctrine is for:

- deciding which thin captures most weaken the shelf if left thin
- deciding whether a month deserves bounded support
- explaining why a month may be mature but still structurally under-repaired

This doctrine is not for:

- replacing [`check-streams`](../check-streams/SKILL.md) live discovery or raw-input materialization
- replacing transcript cleanup or transcript-quality repair workflows

### 5. Audit source boundaries

Keep this distinction explicit:

- `raw-input` = provenance and appearance material
- `page / refined page / appearance map` = citation-bearing support surfaces
- `thread / transcript` = compatibility or carryover unless clearly promoted

Helper captures, generic transcript stubs, X bundles, and date-named placeholders may remain visible in exhaustive benches, but they should not masquerade as top-tier speaker evidence.

### 6. Audit placeholder leakage

Primary speaker surfaces should not carry unresolved fake-canonical placeholders such as `TBD` watch URLs.

Priority order for fixes:

1. page / manifest surfaces claiming fake canon
2. front-door route surfaces
3. support spines and month surfaces
4. compatibility residue, demoted with explicit warnings if true resolution is not yet possible

If a canonical URL is genuinely unresolved:

- keep the appearance structurally visible
- say it is unresolved locally
- route to the best raw-input or page surface instead

### 7. Repair in the right order

Default repair order:

1. page / manifest / raw-input truth
2. route-layer wording
3. month-support gaps
4. compatibility demotion fences
5. optional shelf polish

Do not start by rewriting the biggest legacy file if a smaller page, manifest, or month surface can make the shelf honest first.

### 8. Verify

After edits, test these questions:

- "Who is this speaker?" -> person arc
- "Where do I open first?" -> routing
- "What was actually captured?" -> raw-input bench
- "How does the speaker change across hosts?" -> helix or cross-host surface
- "What is the strongest month cluster?" -> bounded month support

Also verify:

- no unresolved `TBD` markers in primary surfaces
- compatibility files are visibly non-canonical
- raw-input benches remain broader than canonical support surfaces where appropriate

## Comparison mode

When comparing shelves such as Freeman, Parsi, and Ritter:

- compare **retrieval jobs**, not cosmetics
- note where one shelf is stronger in architecture, month support, or source discipline
- avoid forcing one speaker to inherit another speaker's doctrine if the source shape does not justify it

Useful comparison axes:

- front-door clarity
- support-spine maturity
- month support quality
- source-boundary strictness
- compatibility containment
- citation hygiene

## Success condition

After the pass, a future agent should be able to tell:

- what the speaker shelf owns
- where to open first
- which months are mature
- which surfaces are support vs provenance
- which legacy files are compatibility only

If the shelf still requires rereading a legacy `thread.md` to answer all of those questions, the hygiene pass is not finished.
