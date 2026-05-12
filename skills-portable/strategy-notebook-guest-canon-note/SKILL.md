---
name: strategy-notebook-guest-canon-note
preferred_activation: speaker arc
description: "Create a host-stream guest speaker arc from repeated host x guest raw-inputs: rank the key episodes, explain the lane, place the note inside the host stream, and wire lattice or thread surfaces to cite it without inventing a new category."
portable: true
version: 0.1.0
tags:
  - operator
  - strategy-notebook
  - speaker-arc
  - guest-lane
---

# Strategy notebook guest speaker arc

**Preferred activation (operator):** say **`speaker arc`**.

**Compatibility note:** The portable skill slug remains `strategy-notebook-guest-canon-note` for manifest and sync stability. In live notebook language, use **speaker arc**.

Use this skill when a recurring guest run inside a host stream has become important enough to deserve a compact, reusable note that future routing can cite.

## When to run

- A host stream now has several raw-inputs with the same guest.
- The guest lane is clearly useful, but not a new lattice category by itself.
- The notebook needs a durable answer to:
  - why this guest run matters
  - which episodes anchor the arc
  - which file to open first
  - how the lane should be routed or paired
- A lattice row or thread handle should cite a compact note instead of re-explaining the lane each time.

## Workflow

1. **Confirm the ontology first**
   - Identify the **host stream** and the **guest run**.
   - Default to a **stream-local** note inside the host stream.
   - Do not invent a new top-level category just because the guest matters.
   - Do not place the note under shelves like `supporting-voices` unless the repo already uses that as a real taxonomy.

2. **Collect the ground set**
   - Find the canonical raw-input files for the host x guest run.
   - Make sure the run is real, not just a one-off appearance.
   - Prefer files already materialized in canonical raw-input over pointers or loose references.

3. **Rank by strategic value**
   - Rank the episodes by reusable notebook value, not by length or recency alone.
   - Favor:
     - the strongest single anchor
     - the best biographical or architectural file
     - the clearest application file
     - the best paired read
   - Say plainly why each ranked file matters.

4. **Write the speaker arc**
   - Keep it compact and reusable.
   - Use this shape:
     - title
     - `WORK only; not Record.`
     - purpose paragraph
     - `## Why this guest run matters`
     - `## Arc set`
     - `## Open first`
     - `## Routing use`
     - `## Boundaries`
   - In the arc table, include:
     - rank
     - date
     - title
     - why it matters most

5. **Preserve stream-local logic**
   - The note should read as **Host x Guest**, not as a standalone worldview bucket.
   - Keep the host stream explicit in the title and purpose.
   - If the guest also appears elsewhere, that does not change the default placement of this note.

6. **Wire the notebook surfaces**
   - Add a citation from the guest row in `COGNITION-LATTICE-SPEAKERS.md` when the guest belongs in the lattice.
   - Add or refine the `thread:<expert_id>` row in `strategy-commentator-threads.md`.
   - Point those surfaces at the speaker arc instead of duplicating the long explanation everywhere.

7. **Keep boundaries honest**
   - Say what the guest lane is good for.
   - Say what it is not the right tool for.
   - If the underlying files are auto-caption normalizations or otherwise imperfect, say so clearly.

## Placement rule

- Preferred home: `codex/<year>/<host-stream>/<host>-<guest>-speaker-arc.md`
- The note belongs to the **host stream**.
- The lattice and thread surfaces may cite the note.
- The note itself should not silently redefine the lattice.

## Guardrails

- Do not create a new ontology shelf just because a guest feels important.
- Do not confuse a guest speaker arc with a raw-input, profile, or corpus boundary.
- Do not rank by charisma, novelty, or word count alone.
- Do not overclaim certainty; if the lane is speculative or high-variance, say so.
- Do not flatten the guest into a generic ideology label when a more precise lane description is available.

## Success condition

The result is a compact host-stream speaker arc that future routing can cite directly, plus any needed lattice or thread pointers, without creating taxonomic drift.
