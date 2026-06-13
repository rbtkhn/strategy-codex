WORK only; not Record.

# Statecraft Voices

**Disambiguation:** **`voices/`** = analyst registers (interview, essay, social) in WORK — not Grace-Mar **Record Voice** (`bot/prompt.py`).

**Agent dispatch:** For analyst/source-index routing, open [INDEX.md](INDEX.md). For repo-wide LLM routing, open [LLM-ROUTING.md](../../LLM-ROUTING.md).

Purpose: hold the canonical speaker-state continuity surfaces that feed repo-root `statecraft/`.

This subtree is the canonical home of **Statecraft Synthesis** for speaker-state work.

For the canonical archive/synthesis pair, open [Statecraft Archive and Statecraft Synthesis](../archive-synthesis-law.md).
For the compact naming grammar, open [Speaker-Shelf Vocabulary](speaker-shelf-vocabulary.md).

This subtree is speaker-organized rather than lane-organized so the same speaker-state object can feed multiple lanes, bridge adapters, and `civ-state` indexes without being forced into one national bench too early.

## Canonical Rule

- `statecraft/voices/` is the canonical home for speaker-state surfaces that belong to live statecraft work.
- canonical migrated shelf paths take the form `statecraft/voices/<speaker>/`
- the long-run target is the whole live speaker corpus, not only a pilot subset
- `codex/speakers/` remains compatibility residue, non-statecraft speaker storage, or upstream archive material during migration and after cutover
- Do not silently duplicate authority. If a surface has been migrated here, the legacy `codex/speakers/` path should be a compatibility pointer only.
- `statecraft/speakers/` is also compatibility-only after the namespace move; its front door should redirect here rather than carry parallel shelf authority.

Short constitutional split:

- `source-archive/statecraft/` = **Statecraft Archive**, the canonical source-bearing layer
- `statecraft/voices/` = **Statecraft Synthesis**, the canonical live speaker continuity layer above that archive
- `statecraft/speakers/` = namespace-redirect stub only, retained to keep old links legible during migration
- `statecraft/hosts/` = canonical live host-family continuity for migrated hosts
- `codex/speakers/` = compatibility, archive residue, or not-yet-migrated legacy storage

Boundary law:

- Statecraft Archive preserves source truth.
- Statecraft Synthesis interprets that truth into arcs, routing, crossing, support, and bounded synthesis shelves.
- Host law, bridge conditioning, CIV-STATE retrieval, and lane drafting remain downstream.

## What Belongs Here

- speaker arc
- month-support pages
- segment-maturity ladders
- thread atlases
- routing notes
- bridge-facing intake notes
- theme and activation surfaces when they are part of statecraft retrieval
- host-conditioned continuity surfaces
- retrieval-facing shelf tools

## What Does Not Belong Here

- lane judgment
- transaction authority
- provenance itself
- silent `civ-state` mutation
- reusable bounded prose whose main job is analytical preservation rather than speaker retrieval
- stand-alone transportable arguments

Speaker-state continuity lives here as Statecraft Synthesis, not as source-bearing archive. Bridge adapters still live in [statecraft/bridges/](../bridges/), `civ-state` still owns retrieval memory, and lanes still own substantive drafting.

## Source Vocabulary

Use the source-layer terms in this order:

- **`source-index`** = the named file and canonical route surface
- **`source bench`** = the retrieval/breadth job that surface performs inside a shelf
- **`provenance bench`** = optional emphasis when the point is evidentiary breadth rather than the public file name

Default rule:

- name the file as `source-index`
- describe its ordinary shelf role as the `source bench`
- preserve `provenance bench` only where the prose is specifically stressing source breadth, archive-facing truth, or lower-interpretation evidentiary character

This avoids three kinds of drift:

- treating the file name and the function as if they were separate competing surfaces
- leaving older `raw-input` naming pressure alive inside newly normalized shelves
- using `provenance bench` as a casual synonym when the text is really just naming the canonical route surface

## Thread Vocabulary

Use the thread-layer terms in this order:

- **`thread atlas`** = the named surface that maps recurring continuity families across a speaker shelf or bounded run
- **`arc-threads`** = the recurring strands that a bounded arc, month surface, or host-local arc braids together

Default rule:

- name the surface as a `thread atlas`
- describe the internal strands it names as `arc-threads`
- preserve `arc-threads` as the surface label only when quoting a legacy filename or compatibility path

This keeps the surface class distinct from the internal strand grammar and avoids treating a recurring atlas like just another bounded arc.

For the compact `surface name / surface role / surface interior` table behind these rules, open [Speaker-Shelf Vocabulary](speaker-shelf-vocabulary.md).

## Speaker-Shelf Prose Boundary

`statecraft/voices/<speaker>/` is a continuity-and-retrieval layer, not a general prose shelf.

Its canonical job is to preserve:

- speaker identity and arc
- routing and first-open discipline
- source indexes / source benches
- helix and support-spine logic
- host-conditioned continuity
- retrieval-facing shelf tools

It should **not** silently accumulate canonical bounded prose authority when a
file's main job is a reusable analytical object rather than speaker retrieval.

Decision rule:

- if a file is mainly about understanding, entering, or retrieving a speaker, keep it in `voices`
- if it is a reusable bounded analytical object, its canonical prose home is [statecraft/notes/](../notes/README.md)
- if it has become a transportable thesis, its canonical prose home is [statecraft/essays/](../essays/README.md)

Examples:

- [barnes-routing.md](barnes/barnes-routing.md) stays in `voices` because it is retrieval architecture
- [barnes-on-ai.md](barnes/barnes-on-ai.md) is the canonical example of a speaker-derived bounded prose object that may later be recanonicalized into `statecraft/notes/`

Pointer law for future migrations:

- when a speaker-derived file is recanonicalized into `statecraft/notes/` or `statecraft/essays/`, the originating speaker shelf should keep only routing pointers or curated index mentions
- do not maintain duplicate full-authority prose copies in both places

When the real question is host-law rather than speaker identity, open [statecraft/hosts/](../hosts/README.md) instead of treating retired `codex/speakers/<host>/...` surfaces as live authority.

## Speaker profile law

A **speaker profile** (`<speaker>-profile.md`) is the identity-and-voice hub: expert_id, role, pairing tags, voice fingerprint, convergence/tension stubs, and links — not transcript provenance, arc motion, or load-bearing synthesis.

**Shape contract:** [voices-profile-template.md](voices-profile-template.md) — required sections, seed vs mature tiers, migration checklist. Upstream minimal scaffold: [strategy-codex-template-profile.md](../../codex/strategy-codex-template-profile.md).

Canonical placement:

- **Migrated canonical shelf** → `statecraft/voices/<speaker>/<speaker>-profile.md` (SSOT). List it in the shelf `README.md` **Open first** block before arc/routing when identity or voice tier is the job.
- **Migrated canonical host** → `statecraft/hosts/<host>/<host>-profile.md` (SSOT) when the live host shelf has moved under `statecraft/hosts/`.
- **Profile-only / commentator-thread lane** (no first-class shelf yet) → `codex/profiles/<speaker>-profile.md` until real on-disk continuity warrants a shelf.
- **Legacy paths** (`codex/profiles/`, `codex/speakers/<speaker>/`) → thin compatibility redirects after migration; **do not** duplicate the profile corpus in both places.

Current migrated profiles: [Barnes](barnes/barnes-profile.md), [Mercouris](mercouris/mercouris-profile.md), [Pape](pape/pape-profile.md), [Crooke](crooke/crooke-profile.md), [Ritter](ritter/ritter-profile.md), [Parsi](parsi/parsi-profile.md), [Diesen](diesen/diesen-profile.md), [Weichert](weichert/weichert-profile.md) (seed). Host profiles: [Davis](../hosts/davis/davis-profile.md), [Nima](../hosts/nima/nima-profile.md). Profile-only lanes: [codex/profiles/README.md](../../codex/profiles/README.md).

For anchor-and-satellite routing after Pape, Ritter, Parsi, or Crooke, open [speaker-cluster-map.md](speaker-cluster-map.md).

Transcript-first evidence, arc-first interpretation.

When live statecraft work names a speaker or needs speaker-grounded analysis, use this routing order unless the speaker's object shape explicitly says otherwise:

1. open the strongest available actual transcript or transcript-bearing provenance capture
2. extend through the transcript-derived host-local arc when the task needs host-conditioned interpretation
3. extend through routing notes, helixes, support spines, or month-support synthesis only after the transcript and host-arc layer
4. preserve the seam between transcript-backed and synthesized claims whenever analysis extends beyond transcript truth

Derived speaker arcs, routing notes, helixes, and support spines are Statecraft Synthesis surfaces downstream of the Statecraft Archive, not substitutes for transcript authority.

Carveout rule: transcript-first is the default for transcript-bearing relational arcs and transcript-backed routing notes. Authored-first, stream-native, profile-only, or mixed-provenance speakers should state their carveout explicitly and keep the first-open surface that matches the real shelf shape.

## Migration Shape

The migration is phased, but the constitutional target is already fixed:

1. whole-corpus doctrine and compatibility law
2. active migration fronts such as [Freeman](freeman/README.md), [Mercouris](mercouris/README.md), [Crooke](crooke/README.md), [Macgregor](macgregor/README.md), [Ritter](ritter/README.md), [Barnes](barnes/README.md), [Marandi](marandi/README.md), and [Pape](pape/README.md)
3. support-spine shelf exemplars
4. remaining active statecraft speakers
5. long-tail archive cleanup

During migration:

- live synthesis authority should move here
- bridge adapters stay in [statecraft/bridges/](../bridges/)
- lane judgment stays in lanes
- provenance stays in the Statecraft Archive, outside speaker folders
- latest namespace verification receipt: [migration-verification-2026-05-29.md](migration-verification-2026-05-29.md)

## Normalized 2026 Shelf Level

The current normalized shelf level is the `Macgregor / Ritter` grammar:

- canonical home under `statecraft/voices/<speaker>/`
- `README.md` and `index.md` front doors
- speaker arc, routing note, source index, and crossing surface
- speaker-owned support spine
- bounded monthly synthesis ladder for `2026-01` through `2026-05`
- historical audit and `themes/README.md`
- codex front doors reduced to compatibility pointers

The active normalized 2026 shelf set is:

- [Freeman](freeman/README.md)
- [Crooke](crooke/README.md)
- [Mercouris](mercouris/README.md)
- [Macgregor](macgregor/README.md)
- [Ritter](ritter/README.md)
- [Johnson](johnson/README.md)

Canonical cross-context exception shelves now also include:

- [Parsi](parsi/README.md)

Canonical lighter first-pass shelves now also include:

- [Barnes](barnes/README.md)
- [Marandi](marandi/README.md)
- [Postol](postol/README.md)
- [McGovern](mcgovern/README.md)
- [Martyanov](martyanov/README.md)
- [Sachs](sachs/README.md)

## Shelf classes

The repo now recognizes four shelf classes.

### 1. Normalized month-ladder shelves

These use the full canonical statecraft speaker grammar:

- `README.md` and `index.md`
- arc
- routing
- source index
- crossing surface
- support spine
- bounded `2026-01` through `2026-05` synthesis ladder
- historical audit
- `themes/README.md`

Current examples:

- [Freeman](freeman/README.md)
- [Crooke](crooke/README.md)
- [Mercouris](mercouris/README.md)
- [Macgregor](macgregor/README.md)
- [Ritter](ritter/README.md)
- [Johnson](johnson/README.md)

### 2. Cross-context exception shelves

These are still canonical `statecraft/voices/` shelves, but their real inner law is not a host-style monthly ladder. Recurring thread continuity and source-class crossing are structurally primary, and month support appears only where mature cross-context pressure is real.

Current example:

- [Parsi](parsi/README.md)
- [Pape](pape/README.md)

### 3. Lighter first-pass canonical shelves

These are canonical `statecraft/voices/` shelves with real speaker identity, routing, provenance, and maturity law, but not yet enough density to justify a bounded month ladder.

For these shelves:

- the arc and routing surfaces do most of the work
- the support spine explains why the shelf remains intentionally lighter
- host arcs and source benches still own most chronology
- extension should be driven by density, not symmetry

Current examples:

- [Barnes](barnes/README.md)
- [Marandi](marandi/README.md)
- [Postol](postol/README.md)
- [McGovern](mcgovern/README.md)
- [Martyanov](martyanov/README.md)
- [Sachs](sachs/README.md)

### 4. Host-led mature-month exception shelves

These have genuinely mature months, but those months are still owned more cleanly by host arcs, reinforcing orbit, or a non-core appearance bench than by speaker-native month shelves.

For these shelves:

- support spine owns the maturity explanation
- routing owns first-open discipline
- source bench and host-local arcs remain the real month-entry layer
- migration should not proceed by symmetry alone

Read this class as a **governed migration exception**, not as a weaker shelf.

Its constitutional pattern is:

- the speaker is fully first-class
- the statecraft-side shelf is canonical
- host-local chronology remains truer than a native month ladder
- heavier support may remain linked from legacy shelves while the statecraft front door and core speaker grammar migrate first

In other words:

`canonical shelf authority can migrate before chronology ownership migrates`

Current deliberate case:

- [Mearsheimer](mearsheimer/README.md)
- [Wilkerson](wilkerson/README.md)

Why they belong together:

- both are mature enough to deserve canonical `statecraft/voices` shelves
- both are best entered through stable host transformations rather than speaker-native month pages
- both widen beyond one host, but not in a way that makes a normalized month ladder the cleanest constitutional form
- both now use the same migration pattern:
  - statecraft-side `README`, `index`, `arc`, and `routing` first
  - then statecraft-side `helix` and support doorway surfaces
  - linked legacy shelf support retained until a fuller transfer pass is genuinely clearer than the current host-led chronology

This is why `Mearsheimer` and `Wilkerson` should be read as a **class**, not as two isolated special pleas.

### 5. Starter exception shelves

These are truthful doorway shelves that have enough density for routing and provenance support, but not yet enough maturity for a full canonical speaker grammar.

For these shelves:

- the README should say explicitly that the shelf is still a starter surface
- routing and provenance are primary
- absent arc, helix, or support-spine layers should not be faked for symmetry
- promotion to a fuller shelf should be driven by real density, not classification pressure

Current example:

- [Hoh](hoh/README.md)

### 6. Mirror-bearing exception shelves

These are canonical speaker shelves whose primary structural role includes an embedded public mirror or corpus bench, so they should not be judged by ordinary month-ladder or ordinary speaker-link expectations alone.

For these shelves:

- the mirror or embedded corpus is part of the shelf's official opening grammar
- shelf-level routing should distinguish mirror-facing entry from ordinary speaker continuity
- generic shelf-health audits should carve the mirror out unless the task is specifically mirror integrity
- month-ladder symmetry is not the right maturity test

Current example:

- [Jiang](jiang/README.md)

## Current constitutional choice

The repo no longer assumes that every mature speaker must collapse into one monthly grammar.

Instead:

- normalize where the shelf truly wants a canonical month ladder
- preserve cross-context shelves where source-class crossing is primary
- preserve host-led mature-month exception shelves where month ownership still belongs to host arcs and the non-core bench
- let canonical statecraft-side authority migrate first, then migrate heavier support only where that second step makes chronology and retrieval cleaner rather than merely more symmetrical
