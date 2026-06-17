---
name: statecraft-helix-synthesis
description: Build helix-first repo-root statecraft synthesis and retrieval surfaces above already-mature lane objects. Use when the operator asks for canonical-family synthesis, problem-shape routing, meta-synthesis, settlement-room or escalation-governance comparison, or corpus-level orientation surfaces in statecraft/states. Do not use for first-wave lane construction, governing-pair diagnosis, or CIV-STATE front-door/volume hardening.
portable: true
version: 0.1.0
tags:
- operator
- work-strategy
- statecraft
- synthesis
portable_source: skills-portable/statecraft-helix-synthesis/SKILL.md
synced_by: sync_portable_skills.py
---
# Statecraft Helix Synthesis

Use this skill to build the helix-first synthesis and retrieval layer above mature repo-root statecraft lanes.

This skill starts **after** lane-level first-wave work is already materially real. Its job is not to create base lane objects from scratch. Its job is to turn an already-usable lane set into a corpus with:

- canonical-family synthesis notes
- orientation / retrieval surfaces
- meta-surfaces above the family layer
- a cleaner path from lane evidence to cross-lane judgment

## Boundary

- WORK only; not Record.
- Do not edit PH-CIV corpus or CIV-MEM source files from this workflow.
- Do not silently widen beyond the intended layer. Stay inside the synthesis / retrieval wedge unless the operator explicitly expands scope.
- Preserve unrelated dirty files.
- Do not claim a synthesis layer exists until the control plane, generated metrics, and retrieval docs all agree.

## Preconditions

Use this skill only when most or all of the following are already true:

- the relevant lanes already have helix-primary routing
- the five first-wave strand surfaces are materially real
- lane-level or lane-set verification has already happened
- the next problem is no longer lane construction, but cross-lane interpretation

If those conditions are false, use a lower-layer skill first.

## Output ladder

Build upward in this order unless the operator explicitly chooses a different wedge:

1. **Canonical-family synthesis**
   Compare several lanes through one named family.
2. **Orientation / retrieval**
   Help readers choose between lane, family, and strand entry.
3. **Problem-shape routing**
   Group family notes by entry problem instead of title alone.
4. **Meta-synthesis**
   Join adjacent family notes into a larger architecture object.
5. **Operator-task routing**
   Group the corpus by what the operator is trying to do: diagnose, draft a clause, design settlement, review escalation, compare lanes.

Do not jump upward until the lower layer is real enough to support the next one.

## Workflow

1. **Ground in current layer truth.**
   Read the existing lane helixes, the relevant strand objects, and the active migration control-plane notes before drafting. Prefer the smallest set of files that proves the pattern.

2. **Name the exact synthesis target.**
   Decide whether the work is:
   - a family note
   - an orientation / retrieval note
   - a problem-shape router
   - a meta-surface
   - an operator-task router

3. **Find the governing hinge.**
   State the one deeper rule that the note is trying to expose. If the hinge cannot be stated in one or two sentences, the target is probably still too blurry.

4. **Keep layers distinct.**
   - lane helix: primary lane interpretation
   - strand: evidence-bearing lane surfaces
   - family note: one cross-lane question
   - orientation note: entry routing
   - meta-surface: synthesis of adjacent family notes

   Do not let a family note bloat into a router, or a router bloat into another family note.

5. **Use the common synthesis shape.**
   A strong family or meta note usually includes:
   - `Scope`
   - `Claim` or `Meta Claim`
   - `Cross-Lane Matrix`
   - `Shared Structural Rule`
   - `Failure Modes` or `Falsifiers`
   - `Drafting Implications`
   - `Return Path`

6. **Preserve lane specificity inside synthesis.**
   Do not flatten the lanes into generic IR language. Each lane should still sound like itself while contributing to a shared rule.

7. **Wire the retrieval layer immediately.**
   After adding a new synthesis or orientation note:
   - update the migration front door
   - update the active orientation surface or problem-shape router
   - make the next move more explicit than before

8. **Regenerate and verify the control plane.**
   Rebuild the inventory / budget artifacts and confirm:
   - markdown and JSON counts agree
   - surface counts moved as expected
   - the prose front doors still tell the truth about the current layer

9. **Prefer the next leverage point.**
   After verification, identify the next highest-value layer move:
   - missing family note
   - missing router
   - missing meta-surface
   - operator-task surface
   - lane-comparison surface

## Drafting tests

Before finalizing a note, check:

1. Could this have been written without opening the current lane helixes and strand objects?
   If yes, it is probably too generic.

2. Is the note doing one layer's job clearly?
   If not, split it.

3. Does the note leave a cleaner next step than before?
   If not, it is probably ornamental.

4. Do the control-plane counts and front-door prose agree with the new artifact?
   If not, the layer is not actually landed.

## Default operator-facing summary

When you finish a pass, summarize:

- what new synthesis or retrieval artifact was added
- what layer it belongs to
- what rule it exposed
- what control-plane counts changed
- what the next highest-leverage move is

Keep the close-out compact. The point of this layer is to improve navigation and judgment, not to bury the operator in inventory.


## Cursor / grace-mar instance

## strategy-codex instance

- Root working area for this skill: [codex/academy/statecraft](/C:/dev/strategy-codex/codex/academy/statecraft) with the main control plane under [civ-state/migration](/C:/dev/strategy-codex/codex/academy/statecraft/states/migration).
- Preferred source stack for synthesis work:
  - lane helixes such as [America helix](/C:/dev/strategy-codex/codex/academy/statecraft/america/helix.md)
  - first-wave strand objects under each lane's `civilization/` and `empire/`
  - migration control-plane notes in [civ-state/migration](/C:/dev/strategy-codex/codex/academy/statecraft/states/migration)
- Preferred generator command after edits:

```powershell
python scripts/build_civ_emp_migration_inventory.py
```

- Preferred validation commands after listed-skill edits:

```powershell
python scripts/sync_portable_skills.py --skill statecraft-helix-synthesis
python scripts/sync_portable_skills.py --verify --skill statecraft-helix-synthesis
python scripts/validate_skills.py
```

- Keep this skill scoped to the statecraft synthesis layer. Do not let it drift into PH-CIV authoring, raw CIV-MEM backfill, or Record-bearing surfaces unless the operator explicitly asks.
