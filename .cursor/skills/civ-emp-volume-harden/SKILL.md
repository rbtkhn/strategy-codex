---
name: "civ-emp-volume-harden"
description: "Harden or create CIV-EMP front-door and volume architecture surfaces. Use when the operator wants civilization-state diagnostics, sovereignty-chain scaffolds, opener doctrine normalization, or retrieval-oriented volume doctrine in statecraft/civ-emp."
portable: true
version: "0.1.0"
tags:
  - "operator"
  - "work-strategy"
  - "statecraft"
  - "civ-emp"
  - "doctrine"
portable_source: "skills-portable/civ-emp-volume-harden/SKILL.md"
synced_by: "sync_portable_skills.py"
---
# CIV-EMP Volume Harden

Use this skill to harden the CIV-EMP front door and the volume README layer.

This is an **operator-doctrine** skill. Its job is to make CIV-EMP volumes clearer, truer, and more retrievable. It should standardize civilization-state framing, sovereignty-chain logic, opener doctrine, and retrieval consequences without flattening real historical asymmetry.

## Use this skill when

- the operator wants to create or tighten a CIV-EMP volume README
- the CIV-EMP front door needs clearer civilization-state doctrine
- a volume needs a stronger sovereignty-chain scaffold
- founder language feels decorative, over-symmetrical, or weakly grounded
- a case needs opener-doctrine normalization
- the operator wants a bounded civilization-state audit of one volume case

## Do not use this skill when

- the task is archive intake into `source-archive/statecraft`
- the task is lane-local helix drafting or transaction design
- the task is raw `civilization_memory` backfill
- the task belongs in PH-CIV/public manuscript authoring rather than repo-root statecraft doctrine

## Core law

- `civilization_memory` is evidence, not the operator-facing conceptual frame
- `civ-emp` is the operator-facing source base
- volume README surfaces sit above raw source-memory and below lane-local drafting
- final reasoning should sound like CIV-EMP doctrine, not imported civ-mem notes

## Required checks

For any CIV-EMP volume pass, resolve these four checks explicitly:

1. **Civilization-state claim**
2. **Sovereignty chain**
3. **Deep grammar / sovereign opening / current carrier**
4. **Retrieval consequence** of each layer

If one of those four is still blurry, the volume is not hardened yet.

## Opener doctrine

Every volume should identify:

- **Deep grammar** - sacred, mythic, literary, or civilizational substrate
- **Sovereign opening** - the first figure or formation that opens the political continuity chain
- **Current carrier** - the present institution, regime, church, or state form that bears the chain now

Use opener types precisely:

- **Foundational sovereign**
- **Traditional foundational sovereign**
- **Foundational continuity sovereign**

Do not force false symmetry. Some founders are documentary. Some are traditional. Some open longer chains whose present state appears later.

## Workflow

1. **Identify the target layer.**
   Decide whether the work is:
   - front-door CIV-EMP doctrine
   - a volume README hardening pass
   - opener-doctrine normalization
   - a civilization-state audit of one case

2. **Resolve the sovereignty chain before polishing prose.**
   Name what survives rupture, what mutates, and what current carrier still bears continuity.

3. **Separate the five beginning-types clearly.**
   Distinguish:
   - mythic prehistory
   - sacred grammar
   - sovereign opening
   - birth of the present state
   - current carrier

4. **Force asymmetry where truth requires it.**
   If one case has weaker documentary footing, say so. If one case needs a bridge state or transformed carrier, say so. If one case is an edge case whose present state begins much later than its continuity opener, say so.

5. **Write the opener block and the thesis together.**
   The opener block should not be decorative. The opening thesis and civilization-state diagnostic should reflect the same logic.

6. **Bind the doctrine to retrieval.**
   Make the next move clearer:
   - deep grammar -> Sacred Grammar / literature / legitimacy
   - sovereign opening -> state-memory / founding / origin objects
   - current carrier -> helix / state / transaction

   When legitimacy is clearly governing, route to the Sacred Grammar shelf first rather than directly to lane-local summaries.

7. **Close in CIV-EMP language.**
   The final prose should read like operator doctrine: compact, comparative, and retrieval-aware.

## Case patterns

- **Clean sovereign opener + deeper sacred grammar**
  Example shape: sacred grammar precedes a historically legible sovereign founder.

- **Traditional founder with weaker documentary footing**
  Use when the opener is conventionally authoritative but not equally documentary.

- **Transformed continuity with indispensable bridge state**
  Use when the chain survives through major institutional mutation and requires a bridge carrier to stay legible.

- **Continuity opener distinct from present-state birth**
  Use when the longer continuity chain begins earlier than the present state proper.

## Guardrails

- Do not use `civilization_memory` as the operator-facing conceptual frame.
- Do not make all five cases falsely symmetrical.
- Do not confuse present regime carrier with sovereign opening.
- Do not write decorative founder language without retrieval consequences.
- Do not overstate documentary firmness.
- Do not flatten contested inheritance into fake certainty.
- Do not widen into lane or transaction rewriting unless the operator explicitly expands scope.

## Success condition

The CIV-EMP front door or volume surface reads as a stronger civilization-state instrument: opener doctrine is explicit, sovereignty-chain logic is clearer, asymmetry is preserved honestly, and the operator can tell where to retrieve next.


## Cursor / grace-mar instance

**strategy-codex instance notes**

- Canonical front-door doctrine surface: [statecraft/civ-emp/README.md](/C:/dev/strategy-codex/statecraft/civ-emp/README.md)
- Canonical volume map: [statecraft/civ-emp/volumes/README.md](/C:/dev/strategy-codex/statecraft/civ-emp/volumes/README.md)
- Volume surfaces to harden:
  - [Vol I - China](/C:/dev/strategy-codex/statecraft/civ-emp/volumes/vol-i-china/README.md)
  - [Vol II - Persia](/C:/dev/strategy-codex/statecraft/civ-emp/volumes/vol-ii-persia/README.md)
  - [Vol III - Rome](/C:/dev/strategy-codex/statecraft/civ-emp/volumes/vol-iii-rome/README.md)
  - [Vol IV - Russia](/C:/dev/strategy-codex/statecraft/civ-emp/volumes/vol-iv-russia/README.md)
  - [Vol V - America](/C:/dev/strategy-codex/statecraft/civ-emp/volumes/vol-v-america/README.md)
- Use `civilization_memory` only as evidence for this skill; CIV-EMP surfaces remain the operator-facing layer.
- Keep volume passes bounded to CIV-EMP architecture surfaces unless the operator explicitly widens scope into lane, transaction, or source-memory files.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill civ-emp-volume-harden
python scripts/sync_portable_skills.py --verify --skill civ-emp-volume-harden
python scripts/validate_skills.py
```
