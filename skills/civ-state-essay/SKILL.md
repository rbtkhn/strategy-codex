---
name: civ-state-essay
preferred_activation: civ-state essay
description: "Write, revise, or QA reader-facing CIV-STATE essays in the public book tree — civic-chain, hex-frame, sub-lenses, constitutional parts, cross-volume shelf. Use when the operator says civ-state essay, essay prose pass, civic-chain pass, humanizing pass, or light prose pass. Do not use for upstream retrieve/frame (civ-state), volume architecture (civ-state-volume-architect), or archive intake."
portable: true
version: 0.2.1
tags:
  - operator
  - work-strategy
  - civ-state
  - prose
scope_class: repo-governed
---

# CIV-STATE Essay

**WORK only; not Record.**

**Activation:** `civ-state essay` · `civ-state-essay` · `essay prose pass` · `civic-chain pass` · **`humanizing pass`** · **`light prose pass`** · **`essay humanize`** (when class is clear)

Procedure skill for **reader-facing essay prose** under the staged public CIV-STATE book tree. Classify the essay **and pass type** before editing. Doctrine lives in the generic essay template and reader guide — this skill owns **workflow, boundaries, and QA gates**, not a second copy of prose law.

**Default calibration:** Rome pilot (literary-academic, geo-strategic, source-bearing weave, civic-chain word + quote bands). Other volumes follow volume `essays/README.md` when rules differ.

## Use this skill when

- creating or revising a reader-facing essay under `<public-civ-state>/volumes/{vol}/essays/`
- running a prose, geo-strategic, citation, or **source-weave** pass on civic-chain nodes
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

| Class | File pattern (typical) | Primary scaffold | Prose / QA in v0.2 |
|-------|----------------------|------------------|-------------------|
| **Civic-chain** | `essay-{vol}-{slug}.md` | Generic essay template + `{vol}` meta sidecar + registry | ~2,400–2,600 body words; ~450–550 quoted primary/pre-modern in `"…"` (Rome genesis–augustus) |
| **Hex-frame** | `hexagonal-*-{vol}.md` | Hexagonal template + connectivity / essay-types | Six-lens table + membrane laws; **not** civic-chain word/quote band |
| **Sub-lens** | `{lens}-{vol}.md` | Volume essays README + existing essay shape | Prose voice + citation; geo-strategic when lens is place-based; no forced civic-chain length |
| **Constitutional** | `civilization-{vol}.md` · `empire-{vol}.md` | Part scale | New work → part-writer skills; bounded prose QA only here |
| **Cross-volume** | `<public-civ-state>/essays/*.md` | Cross-volume essays README | Template prose rules; length per file |

If class is unsettled, open volume connectivity / essays README (host appendix paths) or **`civ-state` B. Retrieve** — do not guess.

## Civic-chain pass router (Rome pilot — classify after essay class)

For **`essay-{vol}-{slug}.md`** civic-chain nodes, pick **one pass** before editing. Later passes assume structure and quote weave from earlier passes are **frozen** unless operator says otherwise.

| Pass | Operator phrases | Scope | QA `--class` |
|------|------------------|-------|----------------|
| **Source-bearing** | `civic-chain pass`, source-bearing expansion, v0.1.48-style | Expand body + woven `"…"` quotes; geo-strategic + standalone | `civic-chain-rome-v2` |
| **Humanizing** | `humanizing pass`, `essay humanize`, v0.1.49-style | In-place rhythm, verbs, lived institutions, causality, active quote intro/interpret; **no new H2s** | `civic-chain-rome-humanize` |
| **Light human-prose** | `light prose pass`, light human-prose, v0.1.50-style | Surgical: motif variation, dedupe formula transitions, micro-asides, sharper closings; **no structural rewrite** | `civic-chain-rome-humanize` |

**Quoted band (all civic-chain passes):** **450–550** words in `"…"` — humanize band does **not** waive quote limits.

**Default body band by essay state:** Republic, Caesar, Augustus (post v0.1.48, not yet humanized) → **v2** (2,400–2,600). Genesis (post v0.1.49+) and any essay after an explicit humanizing pass → **humanize** (2,400–2,800) until operator folds bands.

**Human-prose anti-patterns (checklist — detail in template/reader-guide):** repeated motif phrases (`public, bounded, returnable`); formula transitions (`The point is not…`, `What matters here…`); neat thesis-summary paragraph closings; abstract noun clusters without verbs. Cap formula stock phrases at **≤2** per essay on light passes.

## Prose doctrine (pointer — read SSOT)

Before editing civic-chain or long prose essays, read the host appendix paths for:

- **Generic essay template** — standalone rule, citation + quotation weave, literary-academic voice, geo-strategic checklist, schematic ban, EXECUTE checklist
- **Reader guide** — literary-academic + geo-strategic + source-bearing expectation

**Core habits (summary only):**

1. **Narrate first, interpret second** — institution → place → pressure → conclusion
2. **Geo-strategic** — every place name carries constraint or incentive; not map trivia
3. **Source weave** — ~20% body = verbatim primary/pre-modern in `"…"` at turning points; modern scholarship (except Gibbon/Mommsen as quoted reception) in `## Notes` only
4. **Standalone** — no peer-essay links, chain/defer voice, or codex routing in body
5. **Swap, don't pad** — at fixed word band, replace schematic/abstract lines when adding quotes or geo depth
6. **Later passes, surgical only** — humanizing and light human-prose passes edit **inside** existing H2s; do not re-expand word count on v2 band essays without operator approval

**Schematic ban (body):** grammar, hinge, apparatus, sequence, strain, logic, stacks, substrate, nullification, category work, city-form, machinery, shell, smaller world (and similar planning shorthand unless earned in context). *Proof* allowed when earned in narrative context.

## Execution order (Windows-safe)

1. **Classify** essay class (router table) **and civic-chain pass type** when applicable.
2. **Read SSOT** — template comment block and/or class template (bounded read; host appendix).
3. **One essay file per turn** — no parallel StrReplace/Write on multiple essay paths.
4. **Write before broad Read** when plan SSOT is locked.
5. **Git** — explicit paths only; no repo-wide status/diff unless operator asks.
6. **One hang** → narrow to single Write or operator terminal handoff (cross-link RLJ parallel-ban — host appendix).

For **validator-first** menu picks (word count, validate public tree), run in the same turn after the pick.

## QA gates

### All prose classes

- All body `[^n]` resolve in `## Notes`
- **Modern-surname rule:** fail Syme, Goldsworthy, Everitt, Durant in body; **allow Gibbon/Mommsen only inside `"…"`** as quoted reception
- Schematic grep clean (ban list above)
- Standalone — no internal essay links or defer voice
- Optional before mirror: read-aloud one section per essay

### Civic-chain only

Run `check_civ_state_essay_prose.py` with the **`--class`** matching the pass (host appendix).

| QA class | Body words | Quoted words | When |
|----------|------------|--------------|------|
| **`civic-chain-rome-v2`** | 2,400–2,600 | 450–550 | Source-bearing pass; republic/caesar/augustus default |
| **`civic-chain-rome-humanize`** | 2,400–2,800 | 450–550 | Humanizing or light human-prose pass; genesis post v0.1.49+ |

- Authorial prose (body minus quoted) **~1,950–2,050** on v2 band at ~20% quote ratio
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
- Do **not** apply civic-chain word/quote band unless operator explicitly sets one

## Ship

1. Commit essay + docs under `<public-civ-state>/` with explicit paths.
2. Run `validate_civilizational_statecraft_public.py` on public tree when structural/registry touched.
3. **Mirror publish** only when operator says **ship**, **publish**, or **VERSION** — host publish script (appendix).
4. After substantive ship, offer **`recursive learn`** for machine-law journal (do not auto-append).

## Default output (after classify)

```markdown
**CIV-STATE Essay**
- Essay class:
- Civic-chain pass (if any):
- Target file(s):
- Scaffold SSOT:
- QA `--class`:
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
3. No schematic or modern-surname body violations on touched essays (Gibbon/Mommsen exception: inside `"…"` only).
4. Civic-chain edits stay in word + quoted bands for the **pass-appropriate `--class`**, or operator explicitly waived.
5. `validate_skills.py` clean after skill file changes; public validator run when registry/structure changed.

**Fail when:** civic-chain word/quote band applied to hex-frame; doctrine pasted into skill instead of template; parallel multi-file essay edits on Windows EXECUTE; mirror publish without operator ship verb.
