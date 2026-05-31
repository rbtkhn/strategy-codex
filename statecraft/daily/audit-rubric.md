WORK only; not Record.

# Statecraft Daily Synthesis Audit Rubric

Purpose: make the `statecraft/daily` method auditable without reducing it to taste, vibes, or silent preference drift.

Use this rubric when checking a new or revised daily or monthly note against the active method in [METHOD.md](./METHOD.md).

## Audit Outcome Classes

- `Pass` - the note satisfies the contract and shows real synthesis
- `Pass With Watchpoints` - structurally sound, but one or two interpretive risks should be named
- `Fail` - the note misses a required contract element or shows one of the named regression modes

## Daily Note Audit

### 1. Structure

Check that the required sections exist and appear in order:

1. `Source Base`
2. `Executive Read`
3. `Dominant Themes`
4. `Lane Read`
5. `Five-Volume CIV-STATE Read`
6. `Speaker Value From This Batch`
7. `Tensions And Falsifiers`
8. `Best Next Moves`

Optional sections are allowed:

- `Companion Notes`
- `Archival Note`

Fail if a required section is missing, renamed beyond recognition, or substantially out of order.

### 2. Quote-Heavy Analytical Contract

Check that:

- `Dominant Themes` is analytical, not recap-only
- `Lane Read` contains real lane judgment rather than loose association
- `Speaker Value From This Batch` distinguishes speaker function rather than listing names
- `Tensions And Falsifiers` contains real falsifiers rather than generic caveats

For each analytical point in those sections, confirm:

- there is at least one verbatim inline quote anchor
- the quote anchor is at least `12` words long
- the quote proves the claim rather than merely gesturing at it

Fail if quotes are clipped into decorative tags or if an analytical section is mostly paraphrase with no visible source-bearing proof.

### 3. Five-Volume CIV-STATE Read

Check that the section exists after `Lane Read` and uses this exact order:

1. `China`
2. `Persia`
3. `Rome`
4. `Russia`
5. `America`

Check that each bullet:

- names what that civilization-state sees first in the object
- adds a distinct pressure, limit, or warning
- stays shorter and lighter than the quote-heavy core sections

Fail if:

- the order drifts
- one or more bullets are missing
- the bullets just restate the lane read in grander language
- `Rome` collapses into empty universality talk
- the section acts like a second lane router instead of a bounded deepener

### 4. Adaptive Reuse Test

Ask:

- what deeper truth did this note learn that a plain archive summary would likely miss?
- did the five-volume section sharpen, limit, or deepen the original read?
- do unlike speakers converge on a shared object, or did the note flatten disagreement into consensus theater?

Pass only if at least one real interpretive gain is visible.

Fail if the note looks complete but could have been produced by swapping names into a template.

## Monthly Note Audit

### 1. Structure

Check that the monthly note contains these sections in order:

1. `Source Base`
2. `Executive Read`
3. `Functional Convergence`
4. `Month Arcs`
5. `Lane Ownership Across The Month`
6. `Five-Volume CIV-STATE Read`
7. `Best Re-entry Days`
8. `What The Month Clarified`
9. `What The Month Still Did Not Settle`
10. `Best Next Companion Notes`

Fail if `Functional Convergence` is missing or if the note becomes a chronology replay.

### 2. Functional Convergence

Check that:

- the section names only active functions
- functions come from the fixed set:
  - `trap`
  - `threshold`
  - `architecture`
  - `implementation`
  - `battlefield`
  - `legitimacy`
  - `falsifier`
- unlike functions are shown converging on a shared object

Fail if the section turns into a speaker-credit table or names inactive functions just for completeness theater.

### 3. Month Compression

Check that:

- the month arcs identify a few governing objects, not a day-by-day replay
- lane ownership is hierarchical and clear
- best re-entry days point to the right parent notes
- unresolved tensions remain visible instead of being smoothed away

Fail if the month note mostly summarizes many days without compressing them into a smaller object set.

### 4. Five-Volume Deepening

Check the same five-bullet order used in daily notes:

1. `China`
2. `Persia`
3. `Rome`
4. `Russia`
5. `America`

Check that the section deepens the month object rather than simply rephrasing it.

Fail if the month-scale five-volume pass is decorative or if one speaker's worldview quietly dominates the whole monthly read.

## Named Failure Modes

These are automatic watchpoints and can independently justify failure:

- `quote ornament`
- `civ-state ornament`
- `synthetic averaging`
- `hidden speaker capture`
- `chronology drift`
- `stitched transcript collage`

## Proof Set

Use [benchmark-manifest.md](./benchmark-manifest.md) as the first falsification set.

Recommended default audit order:

1. [2026-05-29](./2026-05-29.md)
2. [2026-05-30](./2026-05-30.md)
3. [2026-05](./2026-05.md)

If a new method, prompt, skill, or automation hook weakens those proof cases, treat the change as suspect until the gain is clearly proven.
