# Predictive History CIV-MEM Context Implementation Handoff

> In cross-repo handoffs, specify the intended experience transformation first,
> then define the structural contracts that preserve it. This handoff therefore
> begins not from implementation alone, but from the change it is meant to
> create in first contact with the target object: what the reader or operator
> notices, how the object is framed, and how it can be re-entered later with
> greater coherence. The structures that follow are not ends in themselves, but
> the smallest durable contracts needed to preserve that better encounter across
> surfaces, tools, and later revisions.

WORK only; not Record. This file is the **consolidated direct-transfer spec**
for later implementation in the canonical external
`rbtkhn/predictive-history` repo.

## Summary

Implement CIV-MEM in Predictive History as a **top-of-unit contextualization
system** that changes how each lecture/chapter is first encountered. The goal
is to ensure the reader enters each unit through a larger
historical-civilizational horizon, not as isolated transcript, topic, or
commentary.

That transformation should improve:

- **attention**: what the reader notices first
- **framing**: how the unit is understood at entry
- **re-entry**: how the unit can be returned to later with coherence

## Authority surfaces

Before implementing, identify in the actual Predictive History repo:

- the existing authoring surface that already functions as the canonical
  **evidence/media pack**
- the canonical **lecture/chapter entry** surface
- the lightest suitable authority surface for the active voice profile

Rules:

- extend the existing source-of-truth surfaces
- do not invent a parallel pack or second competing contextual layer unless the
  current structure is unusable
- if multiple plausible surfaces exist, choose the one already acting as source
  of truth and name that choice in the implementation summary

## Three-layer contract

Implement and preserve three layers:

### 1. Payload

Canonical, structured, pack-owned, and reusable across surfaces.

Required fields:

- `Primary object`
- `Historical arc`
- `Dominant slots`
- `Reader orientation`
- `Fit strength`
- optional `Mismatch / limit note`

### 2. Rendering

Visible `## CIV-MEM Context` block, lecture/chapter-facing, derived from the
payload.

Rendering may be rephrased for readability, but it may **not** become an
independent second CIV-MEM interpretation.

### 3. Voice

Rendering-only, with one active profile:

- `house-default`

Future voice tuning must not require payload-schema redesign.

Anti-failure rule:

- do not store only freeform CIV-MEM prose in the pack and manually duplicate
  it on lecture/chapter pages
- preserve a stable payload structured enough to survive reuse, voice changes,
  and future surfaces

## Pack contract

Extend the canonical evidence/media pack with a stable CIV-MEM orientation
section.

Required behavior:

- one authoritative payload per unit
- payload remains valid even if rendered prose later changes
- optional rendered draft may exist, but payload remains the authority

Suggested pack section shape:

```markdown
## CIV-MEM orientation

- **Primary object:** ...
- **Historical arc:** ...
- **Dominant slots:** ...
- **Reader orientation:** ...
- **Fit strength:** strong | medium | light
- **Mismatch / limit note:** ...   # optional
```

## Visible reader-facing block

Add a reader-facing `## CIV-MEM Context` block near the top of each
lecture/chapter.

Required behavior:

- after title/basic metadata
- before transcript density or deep exposition
- clearly different from `At a glance`
- compact enough to scan
- substantial enough to orient reading

Default rendering shape:

- 1 compact framing paragraph
- 2-4 short labeled lines
- roughly 90-180 words in normal cases
- shorter in low-fit cases

Functional distinction:

- `At a glance` = immediate topic and argument
- `CIV-MEM Context` = larger historical-civilizational horizon and reading
  posture

## Voice authority

Declare one active voice profile only:

- `house-default`

Its role must be explicit in one real PH authority surface chosen during
discovery. That surface may be a template constant, config value, generator
setting, or doctrine file, but it must be named in the implementation summary.

`house-default` rules:

- historical cartographer as base
- civilizational guide as secondary tone
- prophetic-historical lift only rarely
- open with placement, not drama
- prefer "where this sits" over "what this proves"
- do not let rhetoric outrun fit or evidence

## Low-fit handling

CIV-MEM must remain present even when fit is weak.

Low-fit behavior:

- shorter and narrower
- less rhetorical weight
- explicit about limits when needed
- optional `Mismatch / limit note` should surface when useful

Rule:

- always present
- not always equally weighty

## Rollout order

1. Discover and bind the real PH authority surfaces.
2. Add the structured payload to the canonical pack.
3. Declare `house-default` in one authority surface.
4. Add the derived `## CIV-MEM Context` block to lecture/chapter entry.
5. Build a golden calibration set.
6. Only after calibration succeeds, widen to more units.

Required golden set:

- one strongly civilizational lecture
- one mediated/interview-style unit
- one lower-fit formative or literary unit
- optionally one cooler rerender of an existing payload to prove modulation

Defer until after calibration:

- mass rewrite of the corpus
- additional voice profiles
- any second CIV-MEM authoring surface
- broad rollout before cross-fit examples read correctly

## Acceptance checks

- a future editor can identify exactly which PH surface owns payload, which
  surface renders the visible block, and which surface declares active voice
- each calibrated unit has a structured CIV-MEM payload with all required
  fields
- the visible `## CIV-MEM Context` block is clearly derived from the payload
  and does not introduce a separate CIV-MEM interpretation
- opening a calibrated lecture/chapter cold gives the reader a larger
  historical-civilizational frame before transcript or exposition density
  begins
- `CIV-MEM Context` and `At a glance` do distinct jobs
- weaker-fit units remain meaningful without inflated rhetoric
- one payload can be rerendered in a cooler voice without schema changes

## Defaults

- the canonical writable PH repo is external and must be modified there, not in
  `strategy-codex`
- this transfer package is the design source, not the implementation target
- prefer small durable structural hooks over broad corpus rewriting
- the golden set must span different fit and genre conditions, not merely three
  convenient examples from one series
