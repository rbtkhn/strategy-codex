---
name: empire-part-writer
preferred_activation: empire-part-writer
description: >-
  Write or refine Part 2 empire essays in statecraft/civ-state, especially
  `empire-<civ>.md` chapters. Use when the operator wants the outward-instrument
  chapter of a CIV-STATE volume: machinery-first, severe-strategic, centered on
  projection stack, coercion within broader carriage, tragic necessity, and a
  present-tense imperial instrument rather than a conquest chronicle.
---

# Empire Part Writer

Use this skill to write the Part 2 `empire-<civ>.md` layer as the outward-instrument chapter of a CIV-STATE volume.

This is a **writing-and-instrument** skill for the canonical Part 2 essay. Its job is to show how a civilization scales outward, what machinery carries that scale, where burden accumulates, and how overreach begins to outrun the civilization beneath it.

It is not a volume-architecture skill, not a Part 1 civilization-writing skill, and not a live transaction-drafting skill.

## Use this skill when

- the operator wants to create or revise an `empire-<civ>.md` chapter
- Part 2 needs to expose projection machinery rather than sound like a conquest narrative
- the prose should emphasize coercion, logistics, finance, law, alliances, route control, and infrastructural carriage
- the chapter needs a tragic-necessity frame rather than either celebration or denunciation
- the operator wants the essay to close on a present-tense imperial instrument and its order claim

## Do not use this skill when

- the task is defining the volume architecture itself
- the operator wants Part 1 or Part 3 written as distinct chapter families
- the task is a live lane diagnosis, statecraft synthesis, or transaction design
- the work is public PH-CIV exposition rather than CIV-STATE doctrine

## Core law

- Part 2 explains outward instrument
- Part 2 exposes the machinery
- empire is recognized through projection machinery
- coercion is central, but not alone
- procedural and infrastructural carriers matter strongly
- empire amplifies civilization and risks outrunning it
- the tone is severe-strategic
- the essay closes on the present instrument
- the chapter must never collapse into a conquest chronicle

## Voice law

The prose should feel:

- severe-strategic
- machinery-first
- unsentimental
- infrastructurally serious
- pressure-aware
- present-tense at the close

Do not let the essay become imperial pageantry, flat denunciation, or abstract systems jargon detached from concrete carriers.

## Required structure

Default section law for `empire-<civ>.md`:

- `## Where This Sits`
- `## Reading Posture`
- `## Imperial Pressure Points`
- `## Limits of the Frame`
- `## Return Path`
- `## Core Thesis`
- `## Empire Logic`
- `## Projection Stack`
- `## Coercion and Carriage`
- `## Overreach and Maintenance`
- `## Present Imperial Instrument`
- `## Boundary Rules`
- `## Present Instrument Claim`
- `## Drafting Consequence`
- `## Key CIV-MEM Anchors`

Do not improvise a new shape unless the operator explicitly asks for one.

## Workflow

1. **Read the front door and adjacent surfaces first.**
   Open:
   - the volume `README.md`
   - the matching `civilization-<civ>.md`
   - relevant lane-local empire-instrument or support surfaces if they exist

2. **Name the imperial function clearly.**
   State how this civilization scales outward:
   - incorporation
   - corridor control
   - maritime command
   - depth seeking
   - alliance lattice
   - tributary ordering
   - other bounded pattern if truly necessary

3. **Build the projection stack before polishing prose.**
   Identify the real machinery:
   - force
   - finance
   - law
   - logistics
   - sanctions
   - routes and chokepoints
   - alliances
   - bureaucracy / administration

4. **Keep coercion central but embedded.**
   Force matters, but it must be shown inside the larger carriage system rather than as the whole explanation.

5. **Make maintenance and overreach visible.**
   The chapter should always show how empire burdens itself, what it must preserve, and where its machinery starts to outrun the civilization it claims to defend.

6. **Preserve the civilization / empire tension.**
   Keep asking whether the outward instrument is still answerable to the civilizational core or has become self-justifying machinery.

7. **End with the present instrument.**
   `Present Imperial Instrument` and `Present Instrument Claim` should state what stack exists now and what order it says it is sustaining.

## Empire questions

Let these questions silently govern the chapter:

- how does this civilization project outward?
- what machinery actually carries that projection?
- what role does coercion play inside the larger stack?
- what must be maintained for the instrument to keep working?
- where does empire begin to outrun civilization?
- what present carrier now bears the outward instrument?
- what order does that instrument claim to sustain?

## Failure modes

Avoid:

- conquest chronicle
- heroic empire prose
- denunciation without anatomy
- treating force as the only mechanism
- ignoring logistics, finance, law, or infrastructure
- forgetting maintenance burden
- failing to name the present instrument clearly

## Default output shape

When asked for a compact planning answer before writing, use:

```markdown
**Empire part pass**
- Projection pattern:
- Main machinery:
- Coercion inside carriage:
- Maintenance burden:
- Present imperial instrument:
- Present instrument claim:
```

## Success condition

This skill succeeds when Part 2 reads like the necessary hard middle of a CIV-STATE volume: the operator understands how the civilization projects, what machinery carries it, where overreach begins, and what live instrument still claims to hold order now.

## strategy-codex instance notes

- Canonical volume shelf: [statecraft/civ-state/volumes/README.md](../../../statecraft/civ-state/volumes/README.md)
- Current Part 2 chapter family lives under:
  - [China empire](../../../statecraft/civ-state/volumes/civ-state-china/empire-china.md)
  - [Persia empire](../../../statecraft/civ-state/volumes/civ-state-persia/empire-persia.md)
  - [Rome empire](../../../statecraft/civ-state/volumes/civ-state-rome/empire-rome.md)
  - [Russia empire](../../../statecraft/civ-state/volumes/civ-state-russia/empire-russia.md)
  - [America empire](../../../statecraft/civ-state/volumes/civ-state-america/empire-america.md)
- Companion skills:
  - [civ-state-volume-architect](../civ-state-volume-architect/SKILL.md)
  - [civilization-part-writer](../civilization-part-writer/SKILL.md)
  - [statecraft-guidebook-writer](../statecraft-guidebook-writer/SKILL.md)

## Preferred validation commands after skill edits

```powershell
python scripts/validate_skills.py
```
