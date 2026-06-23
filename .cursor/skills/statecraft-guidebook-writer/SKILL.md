---
name: statecraft-guidebook-writer
description: "Write or refine Part 3 statecraft synthesis essays in statecraft/states, especially `statecraft-<civ>.md` chapters. Use when the operator wants a present-tense guidebook for modern statesmen: operational synthesis that turns Civilization and Empire into a live diplomatic read through order, legitimacy, equilibrium, and judgment under pressure without collapsing into recap or policy memo."
preferred_activation: statecraft-guidebook-writer
activation: statecraft-guidebook-writer
category: product-narrative
status: active
scope_class: repo-governed
---
# Statecraft Guidebook Writer

Use this skill to write the Part 3 `statecraft-<civ>.md` layer as a real statesman's guidebook chapter.

This is a **writing-and-synthesis** skill for the canonical Part 3 essay. Its job is to convert the volume's deeper inheritance and outward instrument into a live read of room, leverage, pressure, timing, and settlement possibility.

It is not a chapter-architecture skill and it is not a full transaction-drafting skill.

## Use this skill when

- the operator wants to create or revise a `statecraft-<civ>.md` chapter
- Part 3 needs to feel like a present-tense diplomatic operating chapter rather than a recap shell
- the writer needs to synthesize `civilization-<civ>`, `empire-<civ>`, `geo-strategy-<civ>`, `secret-history-<civ>`, and `game-theory-<civ>`
- the operator wants urgent-clinical prose oriented toward modern statesmanly judgment
- the issue is how to read a civilization-state under live pressure, not just how to describe it historically

## Do not use this skill when

- the task is defining the volume architecture itself
- the operator wants Part 1 or Part 2 written as distinct chapter families
- the task is already a live clause, sanctions package, or transaction design
- the work is speaker-side commentary or PH-CIV public exposition

## Core law

- Part 3 is **operational synthesis**
- Part 3 turns `Civilization` and `Empire` into a **live read**
- Part 3 is an **umbrella with real synthesis**, not a table of contents
- Part 3 is centered on **crisis interpretation**
- Part 3 should move **near the edge of drafting, but stop short**
- Part 3 closes on the **live pressure pattern**
- Part 3 should feel implicitly shaped by a statesman's concern for:
  - order
  - legitimacy
  - equilibrium
  - judgment under pressure

## Voice law

The prose should feel:

- urgent-clinical
- serious and stripped down
- judgment-heavy rather than information-heavy
- very present-tense
- diplomatic rather than academic

Do not imitate any named author overtly. Let the frame be felt through chapter logic, not through citation theater.

## Required structure

Default section law for `statecraft-<civ>.md`:

- `## Where This Sits`
- `## Reading Posture`
- `## Statecraft Pressure Points`
- `## Limits of the Frame`
- `## Return Path`
- `## Core Thesis`
- `## Statecraft Logic`
- `## Geo-Strategy Pressure`
- `## Secret-History Activation`
- `## Game-Theory Pressure`
- `## Present Statecraft Carrier`
- `## Boundary Rules`
- `## Live Pressure Pattern`
- `## Drafting Consequence`
- `## Key CIV-MEM Anchors`

Do not improvise a new shape unless the operator explicitly wants one.

## Workflow

1. **Read the supporting parts first.**
   Open:
   - `civilization-<civ>.md`
   - `empire-<civ>.md`
   - `geo-strategy-<civ>.md`
   - `secret-history-<civ>.md`
   - `game-theory-<civ>.md`

2. **Name the live governing problem.**
   State in one sentence what present-tense problem a statesman is trying to read:
   recognition, burden, overreach, dignity, fragmentation, room, equilibrium, or settlement.

3. **Find the pressure geometry.**
   Identify:
   - what order is trying to hold
   - what legitimacy still carries
   - what equilibrium is still possible
   - what current pressure is narrowing room

4. **Write synthesis, not recap.**
   Each middle section must generate a new read:
   - geo-strategy -> room, chokepoints, exposure, carrying conditions
   - secret-history -> activation, humiliation, sacred residue, narrative trigger
   - game-theory -> escalation geometry, incentive structure, bargaining logic

5. **Force the present carrier into view.**
   The chapter must explicitly name the current carrier and explain what it inherits now.

6. **End on live pressure.**
   The `Live Pressure Pattern` section should state the present geometry a statesman must actually see, not merely summarize earlier sections.

7. **Stay one step short of transaction drafting.**
   `Drafting Consequence` may imply how to approach the problem, but should stop before becoming a clause pack, sanctions memo, or negotiation script.

## Guidebook questions

Let these questions silently govern the chapter:

- what order is trying to hold?
- what legitimacy still carries?
- what equilibrium is still possible?
- what ideological or moral reading is outrunning experience?
- what room remains for settlement?
- what current carrier is under pressure to choose between restoration, escalation, and compromise?

## Failure modes

Avoid these specifically:

- recap shell
- abstract doctrine index
- general grand-strategy essay detached from the current carrier
- overt homage or named-author imitation
- policy memo specificity
- moral theater replacing judgment
- historical survey replacing present-tense diagnosis

## Default output shape

When asked for a compact planning answer before writing, use:

```markdown
**Statecraft guidebook pass**
- Live governing problem:
- Order at stake:
- Legitimacy carrier:
- Equilibrium question:
- Present carrier:
- Likely live pressure pattern:
```

## Success condition

This skill succeeds when Part 3 reads like a serious guidebook for a modern statesman: the civilization-state becomes legible as a live diplomatic problem, the subordinate lenses are synthesized rather than listed, and the chapter closes on a present-tense pressure geometry rather than a summary.

## strategy-codex instance notes

- Canonical volume shelf: [statecraft/states/volumes/README.md](../../../statecraft/states/volumes/README.md)
- Current Part 3 chapter family lives under:
  - [China statecraft](../../../statecraft/states/volumes/civ-state-china/statecraft-china.md)
  - [Persia statecraft](../../../statecraft/states/volumes/civ-state-persia/statecraft-persia.md)
  - [Rome statecraft](../../../statecraft/states/volumes/civ-state-rome/statecraft-rome.md)
  - [Russia statecraft](../../../statecraft/states/volumes/civ-state-russia/statecraft-russia.md)
  - [America statecraft](../../../statecraft/states/volumes/civ-state-america/statecraft-america.md)
- Companion architecture skill:
  - [civ-state-volume-architect](../civ-state-volume-architect/SKILL.md)

## Preferred validation commands after skill edits

```powershell
python scripts/validate_skills.py
```
