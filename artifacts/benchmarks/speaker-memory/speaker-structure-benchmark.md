# Speaker Structure Benchmark

**Status:** work-layer benchmark doctrine. Not Record. Not EVIDENCE.

Purpose: define a reusable metric language for comparing speaker shelves without reducing everything to subjective vibe or raw file count.

This benchmark is for questions like:

- Is `freeman` denser than `baud`?
- Is `crooke` more mature than `armstrong`?
- Is a shelf high-volume but structurally incomplete?
- Has a speaker object become helix-first, or is it still cross-host reinforced?

## Design Principle

Use a **score vector first** and a **composite second**.

The vector is:

- `density`
- `completeness`
- `coherence`
- `maturity`

Do not let `maturity` substitute for the underlying dimensions.

## Dimension Definitions

### 1. Density

Density asks: how much structured recurrence and interpretive material exists here?

Count signals such as:

- materialized transcript-bearing appearances
- distinct host lanes
- host-local arcs
- helix or cross-host comparative surfaces
- arc-thread atlas presence
- recurrence across months, not just one burst

Density is **not** raw file accumulation alone. Repetitive low-yield files should not outrank a smaller but more recursively useful shelf.

Suggested score anchors:

- `1`: sparse, mostly one-offs
- `3`: real recurrence with at least one strong branch
- `5`: multi-host recurrence with dense comparative and thread-bearing structure

### 2. Completeness

Completeness asks: does the shelf have the surfaces it claims to have, and are the known appearances actually materialized?

Check:

- speaker object present
- routing note present
- raw-input index present when needed
- helix / cross-host note present when claimed
- host-local arcs present when referenced
- externally evidenced appearances materialized locally
- direct watch URLs pinned where recoverable
- broken or placeholder links minimized

Suggested score anchors:

- `1`: many missing required surfaces; major evidence gaps
- `3`: core surfaces exist; some capture or URL gaps remain
- `5`: shelf structure and known evidence are substantially closed

### 3. Coherence

Coherence asks: do the surfaces agree on what the object is and how it should be routed?

Look for:

- consistent classification language
- no contradiction between README, object note, helix note, and routing note
- non-core appearances kept in the raw-input bench instead of being forced into fake arcs
- host-local arcs doing interpretation; lattice staying secondary
- legacy compatibility files kept subordinate to canonical structures

Suggested score anchors:

- `1`: contradictory or confused surface claims
- `3`: mostly coherent with some drift or legacy leakage
- `5`: strong agreement across object, routing, helix, and README surfaces

### 4. Maturity

Maturity asks: how fully formed is the speaker object as a reusable notebook instrument?

Maturity should be derived from the first three dimensions plus continuity.

Continuity signals include:

- cross-year note or clear historical carry
- stable host transformations
- thread atlas or durable theses, not only episodic commentary
- open-first routes that remain valid after new ingest

Suggested score anchors:

- `1`: embryonic or provisional object
- `3`: clearly useful but still branch-thin
- `5`: durable object whose structure survives comparison, extension, and routing pressure

## Composite Guidance

If a composite is needed, use this default weighting:

- `density`: `0.20`
- `completeness`: `0.30`
- `coherence`: `0.30`
- `maturity`: `0.20`

Why this weighting:

- `completeness` and `coherence` should carry more weight than file mass
- `density` matters, but should not dominate
- `maturity` is partly derivative and should not double-count the whole system

## Output Shape

Preferred benchmark output:

```json
{
  "speaker": "freeman",
  "scores": {
    "density": 4.6,
    "completeness": 4.2,
    "coherence": 4.8,
    "maturity": 4.5
  },
  "composite": 4.52,
  "evidence": {
    "host_lanes": 4,
    "materialized_transcripts": 23,
    "host_local_arcs": 4,
    "helix_present": true,
    "cross_year_note_present": true,
    "watch_url_coverage": "partial"
  },
  "notes": [
    "Strongest cross-host helix on disk",
    "Density is structured, not merely volumetric",
    "Dialogue Works URL coverage still incomplete"
  ]
}
```

Markdown table form is also acceptable, but the vector must remain visible.

## Anti-Gaming Rules

- Do not reward raw transcript pileup without routeable structure.
- Do not reward doctrinal inflation such as calling every reinforced object a mature helix.
- Do not equate one hot crisis month with cross-year maturity.
- Do not hide missing URLs or materialization gaps behind a high prose-quality score.

## First Calibration Set

Suggested initial comparison pack:

- `freeman`
- `crooke`
- `baud`
- `armstrong`
- `blumenthal`

This gives:

- one likely helix-first leader
- one mature comparative object
- one dense but possibly differently shaped object
- one single-branch-mature object
- one real but thinner cross-host reinforced object

## Relationship to Existing Speaker-Memory Benchmarks

- `SM-1` repairs a speaker object.
- `SM-2` ranks a host-local arc and chooses open-first routes.
- `SM-3` scores the shelf structure itself.
- `SM-4` compares several speaker objects using the shared metric language.

Use the benchmarks together, not as rivals.
