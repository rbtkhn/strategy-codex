---
name: civ-state-essay
preferred_activation: civ-state essay
description: "Write, revise, or QA reader-facing CIV-STATE essays in the public book tree — civic-chain, hex-frame, sub-lenses, constitutional parts, cross-volume shelf. Use when the operator says civ-state essay, essay prose pass, civic-chain pass, humanizing pass, or light prose pass. Do not use for upstream retrieve/frame (civ-state), volume architecture (civ-state-volume-architect), or archive intake."
portable: true
version: 0.2.5
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

**Recommended sequence:** source-bearing (v2) → **humanizing** (humanize) → optional **light human-prose** (humanize). Light pass may run on v2 only when deduping before humanizing; post-humanizing light pass targets formula tails and reception stacks.

| Pass | Operator phrases | Scope | QA `--class` |
|------|------------------|-------|----------------|
| **Source-bearing** | `civic-chain pass`, source-bearing expansion, v0.1.48-style | Expand body + woven `"…"` quotes; geo-strategic + standalone | `civic-chain-rome-v2` |
| **Humanizing** | `humanizing pass`, `essay humanize`, v0.1.49-style | In-place rhythm, verbs, lived institutions, causality, active quote intro/interpret; **no new H2s** | `civic-chain-rome-humanize` |
| **Light human-prose** | `light prose pass`, light human-prose, v0.1.50-style | Surgical: motif variation, dedupe formula transitions, micro-asides, sharper closings; **no structural rewrite** | `civic-chain-rome-humanize` |

**Quoted band (all civic-chain passes):** **450–550** words in `"…"` — humanize band does **not** waive quote limits.

### Rome civic-chain essay state (QA class — check before edit)

Pin from target file + [`release-history.md`](../../public/civ-state/docs/release-history.md) when unsure.

| Essay | File | QA `--class` (current) | Pass notes |
|-------|------|------------------------|------------|
| Genesis | `essay-rome-genesis.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · Gibbon Notes-only |
| Republic | `essay-rome-republic.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · L55 institutions |
| Caesar | `essay-rome-caesar.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · reception → Notes |
| Augustus | `essay-rome-augustus.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · reception → Notes |

After any **humanizing** pass on a node, default QA class for later edits on that file → **humanize** until operator folds bands.

**Human-prose anti-patterns (checklist — detail in template/reader-guide):** repeated motif phrases (`public, bounded, returnable`; prize catalogues; liberty/elections thesis loops); formula transitions (`The point is not…`, `What matters here…`, `Memory that…`); neat thesis-summary paragraph closings; **meta quote wrappers** (`moralized… compressed rhetoric`, `One modern analyst would later write`); abstract noun clusters without verbs; **calendar metonym for assassination** (bare `the Ides` / `After the Ides` — name the event or use full **Ides of March** only when the date is load-bearing). Cap formula stock phrases at **≤2** per essay on light passes.

### Source discipline (body vs Notes — Rome civic-chain)

**Body `"…"` quotes:** primary ancient sources (historians, poets, speeches, laws, inscriptions, official documents, Roman legal language) **plus medieval secondary** when load-bearing (e.g. early chroniclers used as witness text).

**Notes only (never body):** Gibbon, Mommsen, Syme, Goldsworthy, Everitt, Durant, Gruen, and all modern paraphrase composites. Preserve substance as **authorial synthesis** in body; keep full attribution and composite text in `## Notes` with `*(Modern / reception framing — not body SSOT)*` or equivalent label.

- **Deprecated in body:** `Later reception would add` · `Later reception would also add` · `Later reception fixed the verdict` — migrate modern reception to Notes; replace with authorial prose + ancient quote weave.
- **Ban:** `One modern analyst` · `Later constitutional history would add` · `Later analysis compressed` as authorial frames; modern surnames outside `"…"` in authorial prose.
- **Florus / epitome witnesses:** embed ancient `"…"` in body; do not describe compression in meta voice only.
- **Band floor after reception removal:** expand **ancient** quotes and embodied beats in the same turn — do not backfill quoted band with modern reception.

### Essay citation inventory (Rome — downstream of active essays)

**SSOT:** `public/civ-state/volumes/rome/rome-bibliography.md` — flat chronological list of sources **used across active `essay-rome-*` nodes**, with public-domain URL sub-lines (English default; Latin/Greek second line when essays quote heavily in original). **Derived from essays** (body authorial references + `## Notes`) — not imported from the retrieve shelf. **Not** the upstream retrieve shelf — that remains [`sources/rome/bibliography.md`](../../public/civ-state/sources/rome/bibliography.md) (`civ-state` Frame/Retrieve); volume door [`source-shelf.md`](../../public/civ-state/volumes/rome/source-shelf.md).

**Current coverage (v0.2):** civic-chain four — genesis · republic · caesar · augustus.

- **Before source-bearing or new ancient quotes:** check the inventory for an existing PD edition; reuse its URL sub-line.
- **After a pass adds a new cited work in `## Notes` or body:** append the work to `rome-bibliography.md` in the same turn if not already listed (plain title bullet + indented URL sub-lines; copyrighted modern secondary = plain text, no link).
- **When the next `essay-rome-*` node goes active** (registry / essays README status → active): scan that essay's body + `## Notes` for sources; **append only new works** to `rome-bibliography.md` — dedupe by author + title; do **not** bulk-import from `sources/rome/`.
- **Essay body:** remains standalone — no links to the inventory in body prose; routing pointers live in volume/essays README and meta sidecar only.

### Cross-chain voice (Rome civic-chain four)

Essays remain **standalone** — no peer-essay links, `essay-rome-*` body links, or defer voice (`as the previous essay showed`). **Voice continuity** is allowed: later nodes may assume institutional strain the reader already met (federation → provincial command → legions vs Senate) without re-proving the full arc. Dedupe re-argument in lede/closing when an earlier node already load-bears the same thesis.

**Pass focus hints (not prose templates):** early nodes — institutions, Polybius as later writer; middle — provincial *imperium*, prize pressure; Caesar — *dignitas*, reception dedupe, forms without control; Augustus — settlement/restoration (TBD).

## Prose doctrine (pointer — read SSOT)

Before editing civic-chain or long prose essays, read the host appendix paths for:

- **Generic essay template** — standalone rule, citation + quotation weave, literary-academic voice, geo-strategic checklist, schematic ban, EXECUTE checklist
- **Reader guide** — literary-academic + geo-strategic + source-bearing expectation

**Core habits (summary only):**

1. **Narrate first, interpret second** — institution → place → pressure → conclusion
2. **Geo-strategic** — every place name carries constraint or incentive; not map trivia
3. **Source weave** — ~20% body = verbatim primary/pre-modern in `"…"` at turning points; **modern scholarship (incl. Gibbon, Mommsen, Syme, Goldsworthy, Everitt, Durant) in `## Notes` only** — authorial synthesis carries modern insight in body
4. **Standalone + chain voice** — no internal essay links or defer voice; assume prior-node strain when later civic-chain node
5. **Swap, don't pad** — at fixed word band, replace schematic/abstract lines when adding quotes or geo depth
6. **Later passes, surgical only** — humanizing and light human-prose passes edit **inside** existing H2s; do not re-expand word count on v2 band essays without operator approval

**Schematic ban (body):** grammar, hinge, apparatus, sequence, strain, logic, stacks, substrate, nullification, category work, city-form, machinery, shell, smaller world (and similar planning shorthand unless earned in context). *Proof* allowed when earned in narrative context.

## Execution order (Windows-safe)

1. **Classify** essay class (router table) **and civic-chain pass type** when applicable; read **essay state** table for QA `--class`.
2. **Light pass optional pre-flight:** read-only anti-pattern inventory (formula motifs, reception stack count, catalogue repeats) before edit when operator requests grep/inventory or pass is light human-prose.
3. **Read SSOT** — template comment block and/or class template (bounded read; host appendix).
4. **One essay file per turn** — no parallel StrReplace/Write on multiple essay paths.
5. **Write before broad Read** when plan SSOT is locked.
6. **Git** — explicit paths only; no repo-wide status/diff unless operator asks.
7. **One hang** → narrow to single Write or operator terminal handoff (cross-link RLJ parallel-ban — host appendix).
8. **Band floor after dedupe:** if light pass drops body or quoted words below band floor, restore with **embodied beats or quote weave** — not catalogue/prize lists.

For **validator-first** menu picks (word count, validate public tree), run in the same turn after the pick.

## QA gates

### All prose classes

- All body `[^n]` resolve in `## Notes`
- **Modern-surname rule:** fail Syme, Goldsworthy, Everitt, Durant, Gibbon, Mommsen in authorial prose outside `"…"`; modern reception and paraphrase composites in `## Notes` only with label
- Schematic grep clean (ban list above)
- Standalone — no internal essay links or defer voice
- Optional before mirror: read-aloud one section per essay

### Civic-chain only

Run `check_civ_state_essay_prose.py` with the **`--class`** from essay state table (host appendix).

| QA class | Body words | Quoted words | When |
|----------|------------|--------------|------|
| **`civic-chain-rome-v2`** | 2,400–2,600 | 450–550 | Source-bearing pass; augustus default until humanized |
| **`civic-chain-rome-humanize`** | 2,400–2,800 | 450–550 | Humanizing or light human-prose; genesis / republic / caesar post-humanize |

- Authorial prose (body minus quoted) **~1,950–2,050** on v2 band at ~20% quote ratio
- Geo-strategic swap-don't-pad at band
- Re-count after surgical trim (de-dup may drop below floor — see band-floor restore)
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
- Essay state / QA `--class`:
- Target file(s):
- Scaffold SSOT:
- QA gates to run:

**Next:** [edit | QA only | pre-flight grep | ship | classify unclear → civ-state Retrieve]
```

## Related operations

| Operation | When |
|-----------|------|
| **civ-state** | Essay class unsettled; need shelf / primary / theory retrieve |
| **civ-state-note** | Bounded WORK note on `statecraft/notes/` with CIV-STATE retrieve pre-pass — not public essay |
| **civ-state-volume-architect** | Volume part law or chapter-family change |
| **civilization-part-writer** / **empire-part-writer** | New constitutional part authoring |
| **recursive-learn** | Post-ship machine law; geo-strategic revision law cross-link |
| **validator-first** | Menu pick = run validate/word-count same turn |

Host-specific paths, QA recipes, and publish commands: **CURSOR_APPENDIX** (generated sync target).

## Verification / Proof Standard

**Pass when:**

1. Essay class stated and matching scaffold opened (or handoff named).
2. Class-appropriate QA gates run; failures reported with file + gate name.
3. No schematic or modern-surname body violations on touched essays (Gibbon/Mommsen / reception composites exception: inside `"…"` only).
4. Civic-chain edits stay in word + quoted bands for the **pass-appropriate `--class`**, or operator explicitly waived.
5. `validate_skills.py` clean after skill file changes; public validator run when registry/structure changed.

**Fail when:** civic-chain word/quote band applied to hex-frame; doctrine pasted into skill instead of template; parallel multi-file essay edits on Windows EXECUTE; mirror publish without operator ship verb.
