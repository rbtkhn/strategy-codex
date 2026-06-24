---
name: arc-to-chapter-seeds
description: Extract additive chapter-seed ideas from an upstream arc without letting the arc govern the destination work. Use when the operator wants chapter ideas harvested from a speaker arc, lane arc, cross-host arc, or historical arc, especially for statecraft volume buildout inside strategy-codex.
portable: true
version: 0.1.0
category: product-narrative
status: active
scope_class: repo-governed
tags:
- operator
- work-strategy
- statecraft
- chapter-seeds
- extraction
portable_source: skills/arc-to-chapter-seeds/SKILL.md
synced_by: sync_portable_skills.py
---
# Arc To Chapter Seeds

Use this skill to harvest chapter-generating ideas from an arc and preserve them in an additive upstream seed list.

This skill is for the stage before full chapter writing. Its job is to turn a live arc into:

- concrete chapter ideas
- clean attribution
- visible quote anchors
- likely lane or strand partner surfaces
- a seed list that can keep growing without hardening into architecture too early

## Boundary

- WORK only; not Record.
- Do not let the source arc silently become the governing architecture of the destination corpus.
- Do not confuse chapter seeds with finished chapter plans.
- Do not move source-workshop language into destination-corpus surfaces unless the operator explicitly asks.
- Preserve attribution discipline: host, guest, relay, and originator are not interchangeable.

## Use This Skill When

Most or all of the following are true:

- there is already a material arc on disk
- the operator wants chapter ideas, not just a summary of the arc
- the destination work is still upstream or planning-side
- the challenge is to extract reusable seeds without over-crediting the source arc

If the operator wants a finished chapter, use a later writing workflow instead.

## Output Shape

Produce one of these:

1. **Detailed bridge note**
   Use when one arc deserves its own seed surface.

2. **Additive seed-list section**
   Use when the destination lane already has a cumulative seed file and this arc should be appended.

3. **Correction pass**
   Use when existing seeds drifted into bad attribution or over-claimed the arc's role.

## Workflow

1. **Locate the real arc surface.**
   Open the canonical arc or stream note first, not just a derivative mention.

2. **Read one layer deeper.**
   Open the strongest raw-input or theme surfaces that actually carry the examples.
   Do not rely only on a routing summary when the task needs quote-grade attribution.

3. **Separate contribution types.**
   Distinguish:
   - what the host contributes
   - what the guest contributes
   - what the raw example itself contributes
   - what later notebook interpretation added

4. **Reject ornamental examples.**
   Keep only examples that do real chapter-generating work:
   - expose a pattern
   - sharpen a mechanism
   - pressure a false analogy
   - open a lane-specific chapter question

5. **Name the chapter pressure clearly.**
   Good seeds usually sound like:
   - a chapter title candidate
   - a chapter problem
   - a chapter contrast
   - a chapter falsifier

6. **Show the quotes.**
   Every seed must show the specific quote or compact quote cluster from which it was derived.
   Do not merely cite the source file; surface the actual lines or phrases doing the generative work.

7. **Map to likely lane partners.**
   For each strong seed, name the most relevant lane surfaces:
   - helix
   - state-memory
   - geo
   - war
   - peace
   - empire instrument
   - or another lane-local surface

8. **Keep the seed additive.**
   Write the result so future arcs can extend it without collapsing the seed file into final architecture.

9. **Preserve the rule.**
   State explicitly when needed:
   the source arc is a chapter-generator, not a chapter-governor.

## Drafting Tests

Before finalizing, check:

1. Could this seed have been written without opening the actual arc and raw-input?
   If yes, it is probably too generic.

2. Is the seed tied to a real example or phrasing move?
   If not, it is probably just your own synthesis disguised as extraction.

3. Can the operator see the exact quote that generated the seed?
   If not, the extraction surface is too opaque.

4. Have host and guest contributions been separated?
   If not, attribution drift is likely.

5. Does the seed help write a chapter later?
   If not, it may be a nice observation but not a true chapter seed.

6. Is the destination still upstream?
   If the note reads like destination-corpus doctrine, it has probably gone too far.

## Preferred Seed Pattern

For each strong seed, prefer a compact structure:

- `Seed title`
- `Use when`
- `Why it matters`
- `Quote anchor`
- `Arc contribution`
- `Likely lane partners`

Use a fuller bridge note only when several seeds from one arc need their own shared rule or caution.

## Common Failure Modes

- treating a host's framing vocabulary as if the guest originated it
- treating a guest's concept as if the host now owns it
- confusing speaker summary with chapter generation
- letting one powerful arc over-govern the lane
- filling the seed list with observations that will never become chapters

## Default Close-Out

When finishing a pass, summarize:

- which arc was harvested
- which seeds were added or corrected
- what attribution issue mattered most
- which seed now looks strongest for later chapter materialization


## Cursor / strategy-codex instance

## strategy-codex instance

- Root working areas for this skill:
  - [codex/speakers](/C:/dev/strategy-codex/codex/speakers)
  - [codex/academy/statecraft](/C:/dev/strategy-codex/codex/academy/statecraft)
- Preferred source stack for China- or statecraft-facing seed extraction:
  - canonical speaker or host arc notes under [codex/speakers](/C:/dev/strategy-codex/codex/speakers)
  - strongest supporting **source archive** captures under [source-archive/statecraft/](/C:/dev/strategy-codex/source-archive/statecraft/) (legacy pre-migration files may still appear under [codex/years/2026/raw-input](/C:/dev/strategy-codex/codex/years/2026/raw-input) — archaeology only)
  - lane destination or upstream seed files such as [China volume seeds](/C:/dev/strategy-codex/codex/academy/statecraft/china/china-volume-seeds.md)
- Preferred validation commands after listed-skill edits:

```powershell
python scripts/sync_portable_skills.py --skill arc-to-chapter-seeds
python scripts/sync_portable_skills.py --verify --skill arc-to-chapter-seeds
python scripts/validate_skills.py
```

- Keep this skill upstream. Do not let it write destination-corpus doctrine or imply that a seed list has already become a chapter architecture.
