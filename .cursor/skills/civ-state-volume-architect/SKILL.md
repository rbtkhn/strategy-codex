---
name: civ-state-volume-architect
preferred_activation: civ-state-volume-architect
description: >-
  Create, refound, or normalize CIV-STATE volume architecture in
  statecraft/states. Use when the operator wants to define or enforce the
  canonical volume-part law, rename or add chapter families, rewire volume
  READMEs, or keep Civilization, Empire, and Statecraft distinct while placing
  geo-strategy, secret-history, and game-theory beneath Part 3.
---

# CIV-STATE Volume Architect

Use this skill to shape the architecture of `statecraft/states/volumes/` as a stable book-form, not a pile of files.

This skill is for **volume law and chapter-family design**. It decides what parts a volume has, what each part is for, how the front door routes into them, and how subordinate essays sit beneath them.

It is **not** the same as `civ-state-volume-harden`. That skill strengthens an already-defined front door or volume case. This skill changes or enforces the deeper architecture itself.

## Use this skill when

- the operator wants to define or revise the canonical parts of a CIV-STATE volume
- chapter families are being added, renamed, retired, or demoted
- a volume README opener block needs to be rebuilt around a new part order
- `geo-strategy`, `secret-history`, and `game-theory` need to be treated as subordinate lenses rather than peer top-level parts
- bridge doctrine or promotion doctrine must be updated because a new CIV-STATE destination family now exists
- multiple volume folders need to be kept structurally parallel during a shelf-wide change

## Do not use this skill when

- the task is just polishing one already-correct essay
- the operator wants a live object diagnosed through the governing pair framework
- the work is PH-CIV public authoring or transcript maintenance
- the task belongs to lane-local transaction drafting rather than CIV-STATE architecture

## Core law

- A CIV-STATE volume is a guided book-form, not a flat bundle.
- `README.md` is the front door, not a chapter.
- The current canonical top-level volume order is:
  1. `civilization-<civ>.md`
  2. `empire-<civ>.md`
  3. `statecraft-<civ>.md`
- Part 3 `statecraft-<civ>.md` is a real synthesis chapter, not a thin index.
- `geo-strategy-<civ>.md`, `secret-history-<civ>.md`, and `game-theory-<civ>.md` are subordinate Statecraft sub-essays.
- Legacy support files may remain on disk, but they must stop pretending to be canonical if doctrine has moved past them.

## Required checks

For any CIV-STATE architecture pass, resolve these explicitly:

1. What are the canonical top-level parts now?
2. What files are subordinate rather than coequal?
3. What exact order should the volume opener block show?
4. What shelf doctrine must change in `statecraft/states/volumes/README.md`?
5. What bridge or promotion notes must be updated so the membrane matches the new destination set?

If any of those five are still fuzzy, the architecture pass is not finished.

## Workflow

1. **Name the active volume law first.**
   State the current canonical part order in one line before editing files.

2. **Separate top-level parts from subordinate lenses.**
   Decide what the volume opens through and what it descends into.
   Never let subordinate essays silently masquerade as coequal parts.

3. **Lock each part's job.**
   Distinguish clearly:
   - `Civilization` legitimates the core
   - `Empire` exposes outward instrument
   - `Statecraft` converts the first two into live statesmanlike judgment

4. **Set file naming before prose expansion.**
   Resolve whether the family is generic or named-per-civilization first.
   Avoid writing full chapter bodies before the filename law is stable.

5. **Rewire the opener block and the volume shelf together.**
   Do not change one without the other.
   The per-volume `README.md` files and [statecraft/states/volumes/README.md](../../../statecraft/states/volumes/README.md) should tell the same story.

6. **Update membrane surfaces when destination classes change.**
   If a new family becomes canonical, update:
   - [PH-CIV to CIV-STATE bridge](../../../statecraft/states/ph-civ-to-civ-state-bridge.md)
   - [PH-CIV promotion ledger](../../../statecraft/states/ph-civ-promotion-ledger.md)

7. **Mark residue honestly.**
   If an older file remains on disk for continuity, label it as support, legacy, or drill-down rather than letting it compete with the new architecture.

8. **Validate parallelism across all five volumes.**
   Check that each volume folder contains the same top-level families and that opener-block ordering matches the shelf law.

## Three-part doctrine

Use this as the default constitutional shape unless the operator explicitly supersedes it:

- `civilization-<civ>.md`
  - operator-opening essay
  - legitimacy-bearing core
  - continuity-bearing civilization argument

- `empire-<civ>.md`
  - outward-instrument essay
  - projection stack
  - coercion, finance, logistics, alliance, maintenance, overreach

- `statecraft-<civ>.md`
  - present-tense guidebook essay
  - operational synthesis
  - live diplomatic judgment under pressure

Statecraft sub-essays:

- `geo-strategy-<civ>.md`
- `secret-history-<civ>.md`
- `game-theory-<civ>.md`

These deepen the Part 3 read. They do not replace it.

## Architectural guardrails

- Do not let README count as a chapter.
- Do not let Part 3 collapse into a recap shell.
- Do not let `Empire` absorb `Civilization`.
- Do not let subordinate lenses silently retake top-level status.
- Do not leave bridge doctrine behind after a chapter-family change.
- Do not delete legacy files casually when a support-note role would preserve continuity more safely.
- Do not widen into lane-local rewriting unless the operator explicitly expands scope.

## Default output shape

When answering with an architectural recommendation, prefer:

```markdown
**CIV-STATE volume law**
- Canonical top-level parts:
- Subordinate Statecraft lenses:
- Opener block order:
- Shelf doctrine changes:
- Membrane changes:
- Legacy residue treatment:
```

## Success condition

This skill succeeds when a CIV-STATE volume reads like a stable constitutional book-form: the top-level parts are clear, subordinate lenses are properly nested, the shelf and volume fronts agree, and future chapter writing can proceed without reopening structural confusion.

## strategy-codex instance notes

- Canonical shelf front door: [statecraft/states/README.md](../../../statecraft/states/README.md)
- Canonical volume map: [statecraft/states/volumes/README.md](../../../statecraft/states/volumes/README.md)
- Primary membrane notes:
  - [ph-civ-to-civ-state-bridge.md](../../../statecraft/states/ph-civ-to-civ-state-bridge.md)
  - [ph-civ-promotion-ledger.md](../../../statecraft/states/ph-civ-promotion-ledger.md)
- Companion architecture-adjacent skills:
  - [civ-state-volume-harden](../civ-state-volume-harden/SKILL.md)
  - [statecraft-framework](../statecraft-framework/SKILL.md)

## Preferred validation commands after skill edits

```powershell
python scripts/validate_skills.py
```
