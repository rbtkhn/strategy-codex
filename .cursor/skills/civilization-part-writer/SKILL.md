---
name: civilization-part-writer
preferred_activation: civilization-part-writer
description: >-
  Write or refine Part 1 civilization essays in statecraft/civ-state,
  especially `civilization-<civ>.md` chapters. Use when the operator wants the
  legitimacy-bearing opening of a CIV-STATE volume: operator-orienting,
  continuity-backed, high-metaphysical but governed, beauty-and-form aware, and
  closed by a present-tense continuity claim rather than a generic history
  survey.
---

# Civilization Part Writer

Use this skill to write the Part 1 `civilization-<civ>.md` layer as the legitimacy-bearing opening of a CIV-STATE volume.

This is a **writing-and-legitimation** skill for the canonical Part 1 essay. Its job is to orient the operator to what kind of civilization-state this is, why it belongs in the set, what order it carries through time, and what continuity claim is still alive now.

It is not a volume-architecture skill, not a Part 2 empire-writing skill, and not a live transaction-drafting skill.

## Use this skill when

- the operator wants to create or revise a `civilization-<civ>.md` chapter
- Part 1 needs to legitimate the core rather than sound like a neutral overview
- sovereign continuity needs to be absorbed into the civilization essay rather than treated as a separate canonical opening
- the prose should speak about sacred order, beauty, form, style, and deep grammar without drifting into vagueness
- the operator wants a civilization essay that closes on a live continuity claim rather than on a chronology

## Do not use this skill when

- the task is defining the volume architecture itself
- the operator wants Part 2 or Part 3 written as distinct chapter families
- the task is a live lane diagnosis, statecraft synthesis, or transaction design
- the work is public PH-CIV exposition rather than CIV-STATE doctrine

## Core law

- Part 1 orients the operator
- Part 1 legitimates the core
- Part 1 is high-metaphysical but governed
- sovereign continuity is the backbone
- civilization is recognized through continuity of order
- beauty, form, and style are admissible truth-bearing elements
- contested cases should remain visibly contested where needed
- the essay closes on a present-tense continuity claim
- the chapter must never collapse into a generic history survey

## Voice law

The prose should feel:

- elevated-strategic
- legitimacy-first
- continuity-backed
- metaphysical, but tethered
- serious about beauty, form, canon, and style
- present-tense at the close

Do not let the essay become blood-and-soil myth, museum prose, or decorative civilizational fog.

## Required structure

Default section law for `civilization-<civ>.md`:

- `## Where This Sits`
- `## Reading Posture`
- `## Civilizational Pressure Points`
- `## Limits of the Frame`
- `## Return Path`
- `## Core Thesis`
- `## Civilizational Logic`
- `## Sovereign Continuity`
- `## Deep Grammar and Form`
- `## Rupture, Restoration, and Style`
- `## Present Civilizational Carrier`
- `## Boundary Rules`
- `## Continuity Claim`
- `## Drafting Consequence`
- `## Key CIV-MEM Anchors`

Do not improvise a new shape unless the operator explicitly asks for one.

## Workflow

1. **Read the front door and continuity support first.**
   Open:
   - the volume `README.md`
   - any existing `sovereign-continuity.md`
   - the closest sacred-grammar and state-memory surfaces if needed

2. **Name the civilization-state claim clearly.**
   State what kind of civilization-state this is:
   - strong core case
   - transformed continuity case
   - contested edge case
   - other bounded type if truly necessary

3. **Make sovereign continuity the backbone.**
   The continuity chain must be structurally central, not ornamental.
   Show:
   - opening
   - rupture
   - restoration
   - present carrier

4. **Treat civilization as order, not just culture.**
   The chapter should answer how a durable form of order survives through time, not merely what artifacts or customs exist.

5. **Use beauty and form as disciplined evidence.**
   Form, canon, sacred order, architecture, literature, ritual, and style may deepen the chapter, but they must point back to legitimacy, continuity, and present use.

6. **Preserve asymmetry and contestation.**
   If the case is unstable, transformed, or contested, say so rather than forcing symmetry with stronger cases.

7. **End with the continuity claim.**
   `Continuity Claim` should name what is still alive now and what the present carrier says it bears.

## Civilization questions

Let these questions silently govern the chapter:

- what kind of civilization-state is this?
- what order is actually being carried?
- where does sovereign continuity begin?
- what deeper grammar legitimates the chain?
- what ruptures test but do not erase it?
- what beauty, form, or civilizational style reveal the deeper order?
- what present carrier now claims to bear that inheritance?

## Failure modes

Avoid:

- generic chronology
- decorative founder language
- museum-survey prose
- metaphysics detached from legitimacy
- pure culturalism with no order-bearing argument
- flattening contested cases into fake certainty
- treating sovereign continuity as a side note

## Default output shape

When asked for a compact planning answer before writing, use:

```markdown
**Civilization part pass**
- Civilization-state type:
- Order-bearing continuity:
- Sovereign opening:
- Deep grammar:
- Present carrier:
- Continuity claim:
```

## Success condition

This skill succeeds when Part 1 reads like the rightful opening of a CIV-STATE volume: the operator understands what order this civilization carries, why it belongs in the set, how continuity survives rupture, and what live continuity claim still stands now.

## strategy-codex instance notes

- Canonical volume shelf: [statecraft/civ-state/volumes/README.md](../../../statecraft/civ-state/volumes/README.md)
- Current Part 1 chapter family lives under:
  - [China civilization](../../../statecraft/civ-state/volumes/civ-state-china/civilization-china.md)
  - [Persia civilization](../../../statecraft/civ-state/volumes/civ-state-persia/civilization-persia.md)
  - [Rome civilization](../../../statecraft/civ-state/volumes/civ-state-rome/civilization-rome.md)
  - [Russia civilization](../../../statecraft/civ-state/volumes/civ-state-russia/civilization-russia.md)
  - [America civilization](../../../statecraft/civ-state/volumes/civ-state-america/civilization-america.md)
- Companion skills:
  - [civ-state-volume-architect](../civ-state-volume-architect/SKILL.md)
  - [statecraft-guidebook-writer](../statecraft-guidebook-writer/SKILL.md)

## Preferred validation commands after skill edits

```powershell
python scripts/validate_skills.py
```
