---
name: statecraft-bridge
preferred_activation: statecraft-bridge
description: "Bridge a live speaker claim into the correct Persia/Iran CIV-EMP retrieval profile. Use when the operator says statecraft-bridge, bridge a speaker claim, recognition-first vs settlement-first, or needs a Marandi-vs-Parsi retrieval choice before Persia/Iran statecraft drafting."
---

# Statecraft Bridge

`statecraft-bridge` is the post-lane retrieval bridge for Persia/Iran statecraft. It is not a fifth lane, not a coffee menu option, and not a substitute for `state-deploy` or `state-persia`.

Use it when the object is already speaker-heavy and Persia/Iran-owned, but still needs the right `civ-emp` retrieval profile before lane-local drafting begins.

Short doctrine:

- `state-deploy` decides the lane
- `statecraft-bridge` decides the retrieval profile
- `state-persia` decides what Persia/Iran can draft, carry, accept, reject, and institutionalize

## Boundary

- WORK only; not Record.
- V1 is a general bridge skill with a Persia/Iran pilot inside.
- V1 only supports:
  - Marandi adapter
  - Parsi adapter
  - Persia/Iran lane outputs
- Do not restate full lane doctrine.
- Do not become generic speaker commentary.
- If the object is already fully transactional, hand off instead of re-bridging.

## Source Order

Open sources in this order unless the request is already narrower:

1. `codex/academy/statecraft/bridges/README.md`
2. the relevant adapter:
   - `codex/academy/statecraft/bridges/marandi-civ-emp-retrieval-adapter.md`
   - `codex/academy/statecraft/bridges/parsi-civ-emp-retrieval-adapter.md`
3. `codex/academy/statecraft/bridges/worked-examples.md` when the object is mixed, unfamiliar, or disputed
4. the narrowest relevant `civ-emp` object
5. the named Iran-lane follow-on surfaces

## Workflow

1. **Classify the live claim**
   - `recognition/legitimacy`
   - `implementation/architecture`
2. **Choose the adapter**
   - Marandi for recognition-first, legitimacy-first, sovereignty-pressure reads
   - Parsi for settlement-first, guarantee-first, architecture reads
3. **Open the narrowest relevant `civ-emp` object first**
4. **Translate into the Iran lane**
   - open only the surfaces named by the adapter
5. **Force one counterweight check**
   - degradation, overreach, humiliating verification, weak carriers, self-isolation, or architecture collapse
6. **Produce a bridge brief**
   - positional diagnosis, settlement brief, or explicit handoff

## Decision Rules

- If the claim is clearly Marandi-type, route directly to the Marandi adapter and say why.
- If the claim is clearly Parsi-type, route directly to the Parsi adapter and say why.
- If the claim is mixed, name the ambiguity explicitly and let the menu resolve emphasis.
- If the object is already fully in transaction form, hand off to:
  - `state-persia`
  - `codex/academy/statecraft/sheets/transaction-router.md`
  - a named Iran transaction
- If the object is not honestly Persia/Iran-owned, say so and hand back toward `state-deploy`.

## Default Output

When invoked without a settled output shape, use exactly this format:

```markdown
**Statecraft Bridge**
- Live claim:
- Bridge classification:
- Chosen adapter:
- Shared source object:
- Why this route:
- Main counterweight:

**Bridge Result**
- Recognition or settlement read:
- Best next lane surface:
- Likely output shape:

**Bridge Menu - reply A-D**
A. [recognition-threshold / dignity read]
B. [guarantee / sequencing / settlement read]
C. [lane handoff or transaction-aware route]
D. [falsifier / counterweight / objection test]
```

Make the A-D options topic-specific when a named object is present.

## Handoff Rule

When the operator replies with a letter after a bridge brief, execute that path rather than reprinting the menu.

- `A` = recognition-threshold / dignity route
- `B` = settlement / guarantee / sequencing route
- `C` = lane handoff or transaction-aware route
- `D` = falsifier / counterweight / objection route

## Recursive-Update Membrane

If repeated bridge usage exposes a durable retrieval pattern, confusion class, or handoff failure, record it in:

- `docs/skill-work/work-coffee/statecraft-bridge-observation-loop.md`

Do not directly rewrite:

- `codex/academy/statecraft/bridges/`
- `codex/academy/statecraft/iran/helix.md`
- `codex/academy/statecraft/iran/civilization/`
- `codex/academy/statecraft/iran/transactions/`
