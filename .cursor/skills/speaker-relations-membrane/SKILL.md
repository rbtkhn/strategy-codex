---
name: speaker-relations-membrane
preferred_activation: speaker membrane
description: >-
  Audit or repair the membrane between speaker continuity folders and neutral
  cross-speaker relation notes in strategy-codex. Use when a note looks like
  `speaker A vs speaker B`, when comparison/tension material is living inside one
  speaker shelf, or when a move to `codex/speakers/relations/` should be paired
  with README, index, and orthogonality-review rewiring.
version: 0.1.0
tags:
  - operator
  - strategy-codex
  - speakers
  - membrane
  - relations
---

# speaker-relations-membrane

**Preferred activation (operator):** say **`speaker membrane`**.

Use this skill when the notebook needs to decide whether a speaker-facing object is:

- a **continuity surface** that belongs inside one speaker folder, or
- a **relation surface** that should live in [`codex/speakers/relations/`](../../codex/speakers/relations/).

## Core rule

If the object mainly answers **`speaker A versus speaker B`**, it should live in the neutral `relations/` namespace by default.

If it mainly answers **`who is speaker A in this notebook?`** or **`what continuity does speaker A own?`**, it belongs in the speaker's own shelf.

## Do not confuse these objects

- **speaker continuity**: profile, routing note, transcript, helix, cross-year note, host-local arc pointers
- **cross-speaker relation note**: tension note, bounded comparison audit, `where others stand relative to A vs B`
- **host-local arc**: `<host>-<speaker>-arc.md` or compatibility spelling in a host shelf; this stays host-local, not in `relations/`
- **speaker helix**: cross-host comparison inside one speaker's shelf; this stays speaker-local, not in `relations/`

## Ownership test

Run these questions before moving anything:

1. Does the note still make sense if read as **one speaker's continuity**?
2. Is the main retrieval question **`what does this speaker own?`** or **`how do these speakers differ?`**
3. Would keeping the note inside one shelf make the folder silently own another speaker's dispute?
4. Is the note being cited by more than one speaker shelf as a reusable comparison object?

If the answers point toward disagreement, contrast, or shared cross-shelf use, default to `relations/`.

## Workflow

1. **Classify the object**
   - continuity
   - relation
   - host-local arc
   - helix

2. **Find the current footprint**
   - search for the note path and title across [`codex/speakers/`](../../codex/speakers/)
   - identify every README, index, review note, or arc note that links to it

3. **Move or create the neutral note**
   - create the file under [`codex/speakers/relations/`](../../codex/speakers/relations/)
   - keep the original content unless the move itself requires wording updates
   - keep titles stable when possible so the relation remains rediscoverable

4. **Rewire the shelves**
   - update the source speaker README if it previously implied continuity ownership
   - update the other speaker README if it cites the note
   - update shelf review notes so they describe the object as neutral relation material, not continuity
   - update indexes only when they actually expose the moved object

5. **Teach the doctrine**
   - if the move reveals a recurring rule, add the smallest useful note to:
     - [`codex/speakers/README.md`](../../codex/speakers/README.md)
     - [`codex/speakers/map/open-first-routes.md`](../../codex/speakers/map/open-first-routes.md)
   - prefer one concise rule over a large taxonomy rewrite

6. **Verify**
   - confirm no stale links point at the old shelf-local path
   - confirm the relation note is now discoverable from both relevant speaker shelves
   - confirm the move did not imply that `relations/` owns continuity, arcs, or helixes

## Minimum repair set

When moving a relation note, update these together if they exist:

- source speaker `README.md`
- peer speaker `README.md`
- any local `*-surface-orthogonality-*.md` review that discusses the note
- the relation note's own internal links

Do not stop after moving the file. The membrane repair is incomplete if the shelf front doors still teach the old ownership.

## Guardrails

- Do not move host-local arcs into `relations/`.
- Do not move one speaker's bounded topical thread into `relations/` unless it has actually become a cross-speaker comparison object.
- Do not create `relations/` duplicates when one neutral note can be rewired cleanly.
- Do not leave compatibility stubs behind unless the repo genuinely needs them.
- Do not widen the move into a broad shelf rewrite unless the operator asks.

## Local references

- Shelf doctrine: [`codex/speakers/README.md`](../../codex/speakers/README.md)
- Open-first routing: [`codex/speakers/map/open-first-routes.md`](../../codex/speakers/map/open-first-routes.md)
- Neutral relation namespace: [`codex/speakers/relations/README.md`](../../codex/speakers/relations/README.md)
- Orthogonality template: [`codex/speakers/_templates/speaker-surface-orthogonality-review-template.md`](../../codex/speakers/_templates/speaker-surface-orthogonality-review-template.md)

## Success condition

After the pass, a future agent should be able to open either speaker shelf and learn:

- which notes belong to that speaker's continuity
- which notes are neutral cross-speaker relations
- where to open first for `speaker A` versus `speaker A vs speaker B`
