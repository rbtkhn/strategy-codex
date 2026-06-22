---
name: civ-state-essay
preferred_activation: civ-state essay
description: Write, revise, or QA reader-facing CIV-STATE essays in the public book tree — civic-chain, hex-frame, sub-lenses, constitutional parts, cross-volume shelf. Use when the operator says civ-state essay, essay prose pass, civic-chain pass, humanizing pass, or light prose pass. Do not use for upstream retrieve/frame (civ-state), volume architecture (civ-state-volume-architect), or archive intake.
portable: true
version: 0.2.6
tags:
- operator
- work-strategy
- civ-state
- prose
scope_class: repo-governed
portable_source: skills/civ-state-essay/SKILL.md
synced_by: sync_portable_skills.py
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
| **Geo-branch (Rome)** | `essay-{vol}-{slug}.md` · tier geo-branch | Same template + meta + registry | **Same word + quote bands** as civic-chain when operator sets Rome pilot QA; standalone rival/place arc — not genesis→augustus chain order |
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

### Rome essay-rome state (QA class — check before edit)

Pin from target file + [`release-history.md`](../../public/civ-state/docs/release-history.md) when unsure.

**Civic-chain four:**

| Essay | File | QA `--class` (current) | Pass notes |
|-------|------|------------------------|------------|
| Genesis | `essay-rome-genesis.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · Gibbon Notes-only · *Aeneid* I.1–2 |
| Republic | `essay-rome-republic.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · L55 institutions · Punic compress (no Virgil body) |
| Caesar | `essay-rome-caesar.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · reception → Notes |
| Augustus | `essay-rome-augustus.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · reception → Notes · *Aeneid* VI · *Georgics* I |

**Geo-branch (Rome pilot — civic-chain bands, no chain read order):**

| Essay | File | QA `--class` (current) | Pass notes |
|-------|------|------------------------|------------|
| Carthage | `essay-rome-carthage.md` | **`civic-chain-rome-humanize`** | rival-system · historiography + epic memory · *Aeneid* I + IV · anti-dup vs republic Livy XXII.54 |

After any **humanizing** pass on a node, default QA class for later edits on that file → **humanize** until operator folds bands.

**Human-prose anti-patterns (checklist — detail in template/reader-guide):** repeated motif phrases (`public, bounded, returnable`; prize catalogues; liberty/elections thesis loops); formula transitions (`The point is not…`, `What matters here…`, `Memory that…`); neat thesis-summary paragraph closings; **meta quote wrappers** (`moralized… compressed rhetoric`, `One modern analyst would later write`); abstract noun clusters without verbs; **calendar metonym for assassination** (bare `the Ides` / `After the Ides` — name the event or use full **Ides of March** only when the date is load-bearing). Cap formula stock phrases at **≤2** per essay on light passes.

### Source discipline (body vs Notes — Rome civic-chain)

**Body `"…"` quotes:** primary ancient sources (historians, poets, speeches, laws, inscriptions, official documents, Roman legal language) **plus medieval secondary** when load-bearing (e.g. early chroniclers used as witness text).

**Notes only (never body):** Gibbon, Mommsen, Syme, Goldsworthy, Everitt, Durant, Gruen, and all modern paraphrase composites. Preserve substance as **authorial synthesis** in body; keep full attribution and composite text in `## Notes` with `*(Modern / reception framing — not body SSOT)*` or equivalent label.

- **Deprecated in body:** `Later reception would add` · `Later reception would also add` · `Later reception fixed the verdict` — migrate modern reception to Notes; replace with authorial prose + ancient quote weave.
- **Ban:** `One modern analyst` · `Later constitutional history would add` · `Later analysis compressed` as authorial frames; modern surnames outside `"…"` in authorial prose.
- **Florus / epitome witnesses:** embed ancient `"…"` in body; do not describe compression in meta voice only.
- **Band floor after reception removal:** expand **ancient** quotes and embodied beats in the same turn — do not backfill quoted band with modern reception.

### Literary / epic witnesses (Rome — poets in body)

Poets count as **primary ancient** body sources — same `"…"` weave as historians — but they witness **literary memory and legitimation**, not battle chronology. Do not substitute epic for Polybius/Livy on dates, orders of battle, or treaty text.

**Three witness types (classify before QA):**

| Type | Examples | Body job |
|------|----------|----------|
| **Chronicle / oratory** | Polybius, Livy, Appian, Cicero, Plutarch lives | What happened; institutions; turning points |
| **Law / inscription / document** | Twelve Tables refs, *Res Gestae*, official language | Public rule and formula |
| **Epic / literary memory** | Virgil, Horace, Ovid when load-bearing | How Romans **imagined** rivals, foundation, settlement — pairs with chronicle |

**Epic audit triggers** — before humanize QA on Rome `essay-rome-*`, grep body for: *Roman memory* · *memory Rome* · *annihilation* · *readers would* · rival-place mythology · *delenda* / curse / avenger tradition. If triggers fire and no epic/poet quote is woven, check volume map below — do not ship historiography-only when prose claims literary memory.

**Rome volume map (quote homes — dedupe by book, not by author):**

| Material | Primary essay | Notes |
|----------|---------------|-------|
| *Aeneid* **I.1–2** — arms and the man, Troy → Lavinium | `essay-rome-genesis` | Foundation epic frame |
| *Aeneid* **I** — Dido's Carthage / harbor city | `essay-rome-carthage` | Rival place (Book I harbor beat) |
| *Aeneid* **IV** — Dido's curse / avenger | `essay-rome-carthage` | Epic memory of Punic rival; pair with Cato/Appian |
| *Aeneid* **VI** — shield, *imperium sine fine* | `essay-rome-augustus` | Augustan legitimation |
| *Georgics* **I** — renewal / agriculture idiom | `essay-rome-augustus` | Peace idiom |
| Republic § Punic Wars (compress) | `essay-rome-republic` | **No Virgil body** — depth defers to carthage geo-branch |

**Theory pointer (placement law, not quote home):** [`rome-memory.md#faith-spine-mythology`](../../public/civ-state/volumes/rome/rome-memory.md#faith-spine-mythology) · [`faith-history-rome.md`](../../public/civ-state/volumes/rome/essays/faith-history-rome.md) euhemerism boundary — mythic substrate ≠ historiographical claim.

**Embed rules:** one **short** epic quote at a memory or legitimation turn; **swap-don't-pad** at quote band; pair epic with chronicle or oratory (e.g. Dido curse → Cato fig); active intro in authorial voice — avoid meta-only wrappers (*moralized rhetoric*, *One modern analyst*). Optional Notes label: `*(Epic memory — not chronicle SSOT)*`. Reuse PD edition from [`rome-bibliography.md`](../../public/civ-state/volumes/rome/rome-bibliography.md); book-level routing may also live in essay `.meta.yaml` — skill does not duplicate full lattice.


### Essay citation inventory (Rome — downstream of active essays)

**SSOT:** `public/civ-state/volumes/rome/rome-bibliography.md` — flat chronological list of sources **used across active `essay-rome-*` nodes**, with public-domain URL sub-lines (English default; Latin/Greek second line when essays quote heavily in original). **Derived from essays** (body authorial references + `## Notes`) — not imported from the retrieve shelf. **Not** the upstream retrieve shelf — that remains [`sources/rome/bibliography.md`](../../public/civ-state/sources/rome/bibliography.md) (`civ-state` Frame/Retrieve); volume door [`source-shelf.md`](../../public/civ-state/volumes/rome/source-shelf.md).

**Current coverage (v0.2.6):** civic-chain four — genesis · republic · caesar · augustus · geo-branch **carthage**.

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


## Cursor / strategy-codex instance

Cursor-only wiring for [civ-state-essay/SKILL.md](../../../skills/civ-state-essay/SKILL.md). Portable SSOT body stays in `skills/`.

## Instance paths (essay SSOT)

| Topic | Path |
|-------|------|
| Generic essay template | [public/civ-state/templates/civ-state-essay-template.md](../../../public/civ-state/templates/civ-state-essay-template.md) |
| Reader guide | [public/civ-state/docs/reader-guide.md](../../../public/civ-state/docs/reader-guide.md) |
| Cross-volume essays shelf | [public/civ-state/essays/README.md](../../../public/civ-state/essays/README.md) |
| Rome essays README | [public/civ-state/volumes/rome/essays/README.md](../../../public/civ-state/volumes/rome/essays/README.md) |
| Rome registry | [public/civ-state/volumes/rome/essays/essay-rome.registry.yaml](../../../public/civ-state/volumes/rome/essays/essay-rome.registry.yaml) |
| Rome connectivity / essay types | [public/civ-state/volumes/rome/essays/connectivity-rome.md](../../../public/civ-state/volumes/rome/essays/connectivity-rome.md) |
| Rome essay citation inventory | [public/civ-state/volumes/rome/rome-bibliography.md](../../../public/civ-state/volumes/rome/rome-bibliography.md) |
| Hex template | [public/civ-state/volumes/rome/essays/_template-hexagonal-rome.md](../../../public/civ-state/volumes/rome/essays/_template-hexagonal-rome.md) |
| Meta sidecar template | [public/civ-state/volumes/rome/essays/_template-essay-rome.meta.yaml](../../../public/civ-state/volumes/rome/essays/_template-essay-rome.meta.yaml) |

Other volumes: start at `public/civ-state/volumes/{vol}/essays/README.md` before editing.

## QA — civic-chain prose check

**Primary gate:** `scripts/check_civ_state_essay_prose.py`

**Pass → `--class` (see SKILL § Civic-chain pass router):**

| Pass | `--class` | Body | Quoted |
|------|-----------|------|--------|
| Source-bearing (v2 default) | `civic-chain-rome-v2` | 2,400–2,600 | 450–550 |
| Humanizing / light human-prose | `civic-chain-rome-humanize` | 2,400–2,800 | 450–550 |

```powershell
python scripts/check_civ_state_essay_prose.py --rome-civic-chain-four
python scripts/check_civ_state_essay_prose.py --path public/civ-state/volumes/rome/essays/essay-rome-genesis.md --class civic-chain-rome-humanize
python scripts/check_civ_state_essay_prose.py --path public/civ-state/volumes/rome/essays/essay-rome-republic.md --class civic-chain-rome-humanize
python scripts/check_civ_state_essay_prose.py --path public/civ-state/volumes/rome/essays/essay-rome-caesar.md --class civic-chain-rome-humanize
python scripts/check_civ_state_essay_prose.py --path public/civ-state/volumes/rome/essays/essay-rome-augustus.md --class civic-chain-rome-v2
```

Reports: `body_words`, `quoted_words`, `quote_pct`, `authorial_words`, schematic hits, modern-surname violations (Gibbon/Mommsen allowed only inside `"…"`), footnote resolution.

**Essay state (Rome civic-chain four — v0.2.2):** genesis · republic · caesar → **`civic-chain-rome-humanize`**; augustus → **`civic-chain-rome-v2`** until humanized. SSOT table: SKILL § Rome civic-chain essay state · milestones: [release-history.md](../../../public/civ-state/docs/release-history.md).

**Bands (civic-chain-rome-v2):** body 2,400–2,600 · quoted 450–550 · ~18–22% quote ratio.

**Humanizing / light human-prose:** `--class civic-chain-rome-humanize` — body 2,400–2,800 · quoted 450–550 unchanged. Light pass: optional anti-pattern pre-flight; band-floor restore via embodied beats after dedupe (SKILL § Execution order).

**Inline fallback** (one path only, if script unavailable):

```powershell
python -c "import re,sys; p=sys.argv[1]; t=open(p,encoding='utf-8').read(); b=t.split('## Notes')[0]; q=sum(len(re.findall(r'\b\w+\b',s)) for s in re.findall(r'\"([^\"]+)\"',b)); w=len(re.findall(r'\b\w+\b',b)); print(f'body={w} quoted={q} pct={q/w*100:.1f}')" public/civ-state/volumes/rome/essays/essay-rome-genesis.md
```

**Footnotes:** every `[^n]` in body resolves in `## Notes`.

## Validate and publish

```powershell
python scripts/validate_civilizational_statecraft_public.py public/civ-state
python scripts/publish_public_civ_state.py -m "civ-state: …" --push
```

Mirror publish only when operator says **ship**, **publish**, or **VERSION**.

## RLJ cross-links

- [recursive-learning-journal.md](../../../statecraft/recursive-learning-journal.md) — geo-strategic revision law (append on operator `append RLJ` / `log this`); parallel-ban Windows EXECUTE discipline
- After substantive essay ship, offer **`recursive learn`** — do not auto-append

## Related skills (instance)

| Skill | When |
|-------|------|
| [civ-state](../civ-state/SKILL.md) | Essay class unsettled; retrieve / frame |
| [civ-state-volume-architect](../civ-state-volume-architect/SKILL.md) | Volume architecture — not single-essay polish |
| [civilization-part-writer](../civilization-part-writer/SKILL.md) | New civilization part |
| [empire-part-writer](../empire-part-writer/SKILL.md) | New empire part |
| [validator-first](../validator-first/SKILL.md) | Menu pick = run validate same turn |

## Maintenance

```powershell
python scripts/sync_portable_skills.py --skill civ-state-essay
python scripts/sync_portable_skills.py --verify --skill civ-state-essay
python scripts/validate_skills.py
```
