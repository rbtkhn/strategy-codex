---
name: civ-state-essay
preferred_activation: civ-state essay
description: "Write, revise, or QA reader-facing CIV-STATE essays in the public book tree — civic-chain, hex-frame, sub-lenses, constitutional parts, cross-volume shelf. Use when the operator says civ-state essay, civ-state-essay, essay prose pass, or civic-chain pass. Do not use for upstream retrieve/frame (civ-state), volume architecture (civ-state-volume-architect), or archive intake."
portable: true
version: 0.1.0
tags:
  - operator
  - work-strategy
  - civ-state
  - prose
scope_class: repo-governed
---

# CIV-STATE Essay

**WORK only; not Record.**

**Activation:** `civ-state essay` · `civ-state-essay` · `essay prose pass` · `civic-chain pass` (when class is clear)

Procedure skill for **reader-facing essay prose** under the staged public CIV-STATE book tree. Classify the essay **before** editing. Doctrine lives in the generic essay template and reader guide — this skill owns **workflow, boundaries, and QA gates**, not a second copy of prose law.

**Default calibration:** Rome pilot (literary-academic, geo-strategic, Notes-only, civic-chain word band). Other volumes follow volume `essays/README.md` when rules differ.

## Use this skill when

- creating or revising a reader-facing essay under `<public-civ-state>/volumes/{vol}/essays/`
- running a prose, geo-strategic, or citation pass on civic-chain nodes
- encoding or polishing a hex-frame demonstrator
- bounded prose QA on a sub-lens or cross-volume essay
- shipping essay edits to the public tree (commit; mirror only when operator says ship/publish/VERSION)

## Do not use this skill when

- the task is upstream **Frame / Retrieve / Promote / Review** — use **`civ-state`**
- the task is volume README law, chapter-family design, or sovereignty-chain scaffold — use **`civ-state-volume-architect`**
- the task is hardening an already-defined volume front door — use **`civ-state-volume-harden`**
- the task is **new** civilization or empire **part** authoring at scale — hand off to **civilization-part-writer** / **empire-part-writer** (this skill may still do bounded prose QA on existing parts)
- the task is archive intake, lane-local synthesis, or PH-CIV manuscript work outside `<public-civ-state>/`

## Essay-class router (classify first)

| Class | File pattern (typical) | Primary scaffold | Prose / QA in v1 |
|-------|----------------------|------------------|------------------|
| **Civic-chain** | `essay-{vol}-{slug}.md` | Generic essay template + `{vol}` meta sidecar + registry | Full prose doctrine; ~1,850–2,150 body words before `## Notes` (Rome genesis–augustus) |
| **Hex-frame** | `hexagonal-*-{vol}.md` | Hexagonal template + connectivity / essay-types | Six-lens table + membrane laws; **not** civic-chain word band |
| **Sub-lens** | `{lens}-{vol}.md` | Volume essays README + existing essay shape | Prose voice + citation; geo-strategic when lens is place-based; no forced civic-chain length |
| **Constitutional** | `civilization-{vol}.md` · `empire-{vol}.md` | Part scale | New work → part-writer skills; bounded prose QA only here |
| **Cross-volume** | `<public-civ-state>/essays/*.md` | Cross-volume essays README | Template prose rules; length per file |

If class is unsettled, open volume connectivity / essays README (host appendix paths) or **`civ-state` B. Retrieve** — do not guess.

## Prose doctrine (pointer — read SSOT)

Before editing civic-chain or long prose essays, read the host appendix paths for:

- **Generic essay template** — standalone rule, citation doctrine, literary-academic voice, geo-strategic checklist, schematic ban, EXECUTE checklist
- **Reader guide** — literary-academic + geo-strategic expectation

**Core habits (summary only):**

1. **Narrate first, interpret second** — institution → place → pressure → conclusion
2. **Geo-strategic** — every place name carries constraint or incentive; not map trivia
3. **Citation** — modern secondary names in `## Notes` only; body = authorial synthesis + ancient/official voices
4. **Standalone** — no peer-essay links, chain/defer voice, or codex routing in body
5. **Swap, don't pad** — at fixed word band, replace schematic/abstract lines when adding geo or institutional depth

**Schematic ban (body):** grammar, hinge, apparatus, sequence, strain, proof, logic, stacks, substrate, nullification, category work, city-form, machinery, shell, smaller world (and similar planning shorthand unless earned in context).

## Execution order (Windows-safe)

1. **Classify** essay class (router table).
2. **Read SSOT** — template comment block and/or class template (bounded read; host appendix).
3. **One essay file per turn** — no parallel StrReplace/Write on multiple essay paths.
4. **Write before broad Read** when plan SSOT is locked.
5. **Git** — explicit paths only; no repo-wide status/diff unless operator asks.
6. **One hang** → narrow to single Write or operator terminal handoff (cross-link RLJ parallel-ban — host appendix).

For **validator-first** menu picks (word count, validate public tree), run in the same turn after the pick.

## QA gates

### All prose classes

- All body `[^n]` resolve in `## Notes`
- Modern-surname body grep clean (Gibbon, Mommsen, Syme, Goldsworthy, Everitt, Durant, etc.)
- Schematic grep clean (ban list above)
- Standalone — no internal essay links or defer voice
- Optional before mirror: read-aloud one section per essay

### Civic-chain only

- Body word count **1,850–2,150** (split on `## Notes`)
- Geo-strategic swap-don't-pad at band
- Re-count after surgical trim (de-dup may drop below floor)
- Meta sidecar unchanged unless operator scoped routing edits
- Registry anchor matches file slug

### Hex-frame only

- Six-lens table complete; membrane laws honored
- Registered in volume essays README; links to connectivity / term anchors
- No duplication of term-file rosters — link segments only

### Sub-lens / cross-volume

- Prose voice + citation doctrine; geo-strategic when place is load-bearing
- Do **not** apply civic-chain word band unless operator explicitly sets one

## Ship

1. Commit essay + docs under `<public-civ-state>/` with explicit paths.
2. Run `validate_civilizational_statecraft_public.py` on public tree when structural/registry touched.
3. **Mirror publish** only when operator says **ship**, **publish**, or **VERSION** — host publish script (appendix).
4. After substantive ship, offer **`recursive learn`** for machine-law journal (do not auto-append).

## Default output (after classify)

```markdown
**CIV-STATE Essay**
- Essay class:
- Target file(s):
- Scaffold SSOT:
- Prose pass (if any):
- QA gates to run:

**Next:** [edit | QA only | ship | classify unclear → civ-state Retrieve]
```

## Related operations

| Operation | When |
|-----------|------|
| **civ-state** | Essay class unsettled; need shelf / primary / theory retrieve |
| **civ-state-volume-architect** | Volume part law or chapter-family change |
| **civilization-part-writer** / **empire-part-writer** | New constitutional part authoring |
| **recursive-learn** | Post-ship machine law; geo-strategic revision law cross-link |
| **validator-first** | Menu pick = run validate/word-count same turn |

Host-specific paths, QA recipes, and publish commands: **CURSOR_APPENDIX** (generated sync target).

## Verification / Proof Standard

**Pass when:**

1. Essay class stated and matching scaffold opened (or handoff named).
2. Class-appropriate QA gates run; failures reported with file + gate name.
3. No schematic or modern-surname body violations on touched essays.
4. Civic-chain edits stay in word band or operator explicitly waived band.
5. `validate_skills.py` clean after skill file changes; public validator run when registry/structure changed.

**Fail when:** civic-chain word band applied to hex-frame; doctrine pasted into skill instead of template; parallel multi-file essay edits on Windows EXECUTE; mirror publish without operator ship verb.
