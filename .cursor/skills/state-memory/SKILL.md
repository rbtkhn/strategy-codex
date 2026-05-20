---
name: state-memory
description: "Build, mirror, or audit academy-statecraft state-memory architecture. Use when the operator says state-memory, asks to convert CIV-MEM into civilization/objects/state-memory.md, mirror the Russia/Iran structure into America or China, audit current state carriers, separate civilization memory from state carriers and object transmitters, or prevent biography drift in academy-statecraft lanes."
---

# State Memory

`state-memory` turns CIV-MEM and lane-local statecraft material into the academy-statecraft authority-memory layer. It keeps the lanes from sliding into biography by enforcing:

> Civilization stores state memory. Empire converts memory into reach. State carries present authority. Objects transmit signals. Transactions test whether authority can become settlement.

## Boundary

- WORK only; not Record.
- Do not edit PH-CIV corpus or CIV-MEM source files from this workflow.
- Do not create transaction files unless the operator separately asks.
- Use lane-local `updates/pending.md` for durable recursive candidates; live analysis proposes, human review decides.
- Preserve unrelated dirty files. State-memory edits should stay inside `codex/academy/statecraft/` unless the operator explicitly expands scope.

## Workflow

1. **Ground in repo truth.** Search the target lane and CIV-MEM inputs before drafting:

```powershell
rg -n "state-memory|heads-of-state|authority-structure|objects|CIV-MEM|CIV–CORE|CIV–STATE" codex/academy/statecraft research/repos/civilization_memory
```

2. **Identify CIV-MEM inputs.** Prefer the target civilization's `CIV–CORE–*.md`, `CIV–STATE–*.md`, doctrine / index files, and lane-local `civilization/seed-patterns.md`. Cite them in `## CIV-MEM Inputs`; do not rewrite them.
3. **Name the continuity pattern.** State what survives regime, dynasty, party, constitutional, or leadership changes.
4. **Separate authority forms from current carriers.** Historical authority forms belong in `civilization/objects/state-memory.md`; present carriers belong directly in `state/`.
5. **Classify people and offices.**
   - historical authority memory -> `civilization/objects/state-memory.md`
   - current state carrier -> `state/<carrier>.md`
   - diplomatic / ministerial / institutional signal transmitter -> `state/objects/<object>.md`
6. **Use the template.** Follow `codex/academy/statecraft/templates/state-memory.md`: `Continuity Pattern`, `Authority Forms`, `Current Carriers`, `Transaction Test`, `Failure Mode`, `CIV-MEM Inputs`.
7. **Wire the layer.** Link state-memory to current carriers, current carriers back to state-memory, and transmitter objects to both.
8. **Sweep stale links.** After moving files, search for old paths and biography drift:

```powershell
rg -n "heads-of-state|head-of-state.md|head-of-state pattern|biography" codex/academy/statecraft/<lane>
```

9. **Validate.** Run `python scripts/validate_skills.py`. If skill files were not touched, still use the stale-link search and a manual path check.

## Default Shapes

Use a flattened `state/` carrier layout for lanes where the operator has chosen the new structure:

```text
<lane>/civilization/objects/state-memory.md
<lane>/state/<current-carrier>.md
<lane>/state/objects/<transmitter>.md
```

Use the existing `state/heads-of-state/` layout for America and China until the operator explicitly asks to mirror the new structure there.

## Transaction Test

Every state-memory object should make transactions more usable. Include questions that test:

- whether the clause preserves the durable state interest;
- which current carrier must authorize, implement, sell, or restrain it;
- which historical wound, dignity claim, legitimacy grammar, or continuity burden the wording touches;
- what makes the settlement look like collapse, humiliation, overreach, or managed dependency;
- what observable mechanism proves implementation after the headline moment.

## Output

When answering without file edits, provide a compact architecture recommendation. When implementing, modify the lane files, run validation, and summarize:

- state-memory object added or refined;
- carrier files moved or linked;
- transmitter objects wired;
- stale links checked;
- validation result.
