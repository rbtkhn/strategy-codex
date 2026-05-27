---
name: "memory"
preferred_activation: "memory"
description: "Build, mirror, audit, or backfill repo-root statecraft state-memory and civilization arc-lens surfaces from CIV-MEM. Use when the operator says memory or legacy state-memory, asks to convert CIV-MEM into civilization/objects/state-memory.md, mirror state-memory architecture, audit current state carriers, create or refine god.md, lit.md, art.md, geo.md, war.md, or peace.md, or wants deep CIV-MEM search without biography drift."
portable: true
version: "0.1.0"
tags:
  - "operator"
  - "statecraft"
  - "civ-mem"
  - "state-memory"
  - "civilization"
portable_source: "skills-portable/memory/SKILL.md"
synced_by: "sync_portable_skills.py"
---
# Memory

**Preferred activation (operator):** say **`memory`**.

Use this skill to build, mirror, audit, or backfill repo-root statecraft **state-memory** and civilization arc-lens layers from CIV-MEM and lane-local statecraft material.

Compatibility note: older references to **`state-memory`** as a skill mean this skill. The **skill name** is now `memory`; the **statecraft object family** remains `state-memory`.

This skill is the lane-local implementation surface for the CIV-EMP **evidence-spine law** and the `MEM CONNECTIONS` quantitative default.

Inside the active **Civilizational Statecraft Framework**, `memory` is the thickness-restoring tool mainly for:

- **civilization** surfaces
- **faith** surfaces
- **memory** surfaces

It is not a catch-all skill for all six layers. Its main job remains rebuilding continuity-bearing and legitimacy-bearing substrates when they are thin, stale, or contested.

The **Civilizational Statecraft Framework** governs interpretation first. Older families such as `god`, `lit`, `art`, `geo`, `war`, and `peace` remain useful only as **secondary retrieval-and-expression families** chosen after the governing layer has been identified. Build them as subordinate arc-lenses, not as primary ontology.

It keeps the lanes from sliding into biography or shallow summary by enforcing:

> Civilization stores state memory. Empire converts memory into reach. State carries present authority. Objects transmit signals. Transactions test whether authority can become settlement.

Second rule: every major civilization object is an arc-lens, not a topic page. A lens reads the present; an arc carries the civilizational development that makes the reading legitimate. In this workflow the two are one object: memory becomes perception, perception becomes judgment, and judgment becomes a possible update. These arc-lenses are downstream expression surfaces, not coequal doctrine. Every arc-lens must trace origin, continuity, transformation, current carrier, failure mode, and transaction use.

## Boundary

- WORK only; not Record.
- Do not edit PH-CIV corpus or CIV-MEM source files from this workflow.
- Do not create transaction files unless the operator separately asks.
- Use lane-local `updates/pending.md` for durable recursive candidates; live analysis proposes, human review decides.
- Preserve unrelated dirty files. Memory-skill edits should stay inside `statecraft/` unless the operator explicitly expands scope.
- Do not build civilization arc-lens backfills only from existing lane summaries. Use direct CIV-MEM discovery, `MEM CONNECTIONS`, and opened source bodies before drafting.

## Workflow

1. **Ground in repo truth.** Search the target lane and CIV-MEM inputs before drafting:

```powershell
rg -n "state-memory|heads-of-state|authority-structure|objects|CIV-MEM|CIV|STATE" statecraft research/repos/civilization_memory
```

2. **Identify CIV-MEM inputs.** Prefer the target civilization's `CIV-CORE-*`, `CIV-STATE-*`, doctrine / index files, relevance files, and lane-local `civilization/seed-patterns.md`. Cite them in `## CIV-MEM Inputs`; do not rewrite them.
3. **Name the continuity pattern.** State what survives regime, dynasty, party, constitutional, or leadership changes.
4. **Shape the arc-lens.** Name what the object helps read in the present, then name origin, continuity, transformation, current carrier, failure mode, and transaction use. If these cannot be identified, mark the object `Provisional` rather than padding the file with citations.
5. **Separate authority forms from current carriers.** Historical authority forms belong in `civilization/objects/state-memory.md`; present carriers belong directly in `state/`.
6. **Classify people and offices.**
   - historical authority memory -> `civilization/objects/state-memory.md`
   - current state carrier -> `state/<carrier>.md`
   - diplomatic / ministerial / institutional signal transmitter -> `state/objects/<object>.md`
7. **Use the template.** Follow `statecraft/templates/state-memory.md`: `Continuity Pattern`, `Arc Shape`, `Authority Forms`, `Current Carriers`, `Transaction Test`, `Failure Mode`, `CIV-MEM Inputs`.
8. **Wire the layer.** Link state-memory to current carriers, current carriers back to state-memory, and transmitter objects to both.
9. **Expose the evidence spine.** For major objects, make the construction auditable:
   - `Seed MEM`
   - `MEM CONNECTIONS cluster`
   - `Overview corroborators`
   - `Counterweight`
   - `Current-carrier bridge`
10. **Sweep stale links.** After moving files, search for old paths and biography drift:

```powershell
rg -n "heads-of-state|head-of-state.md|head-of-state pattern|biography" statecraft/<lane>
```

11. **Validate.** Run `python scripts/validate_skills.py`. If skill files were not touched, still use the stale-link search and a manual path check.

## Civilization Arc-Lens Backfills

Use this branch when creating or refining lane-local civilization arc-lenses such as:

- `civilization/god.md`
- `civilization/lit.md`
- `civilization/art.md`
- `civilization/geo.md`
- `civilization/war.md`
- `civilization/peace.md`

These backfills must be cognitively dense and source-supported. Existing statecraft summaries may guide the question, but they are not enough.

Use them only after the governing pair inside the **Civilizational Statecraft Framework** is clear. The backfill question is not "which lens is sovereign?" It is "which secondary object family best expresses the already-identified governing layer?"

### Required CIV-MEM Pass

Before drafting a major state-memory or civilization arc-lens backfill, use a three-stage retrieval path. CIV-MEM is the deep civilizational memory graph; repo-root statecraft is the operational command surface. Do not let urgency collapse the graph into summary.

1. **Fix the lane, object, and civilization id.**
   - America -> `AMERICA`
   - Russia -> `RUSSIA`
   - China -> `CHINA`
   - Iran -> `PERSIA`
2. **Check the object-aware retrieval matrix.** Open `statecraft/sheets/civ-mem-object-retrieval-matrix.md` when it exists. Use the row for the target object, such as `russia-god`, `china-art`, `iran-peace`, or `america-war`, to set seed terms, required source classes, connection expansion, and counterweight expectations.
3. **Run or emulate direct lane discovery.** Prefer:

```powershell
python scripts/suggest_civ_mem_from_relevance.py <CIV_ID>
```

If the relevance script is missing, exits nonzero, or lacks the needed domain, use targeted `rg` over `research/repos/civilization_memory/content/civilizations/<CIV_ID>` with the lens terms.

4. **Run or emulate lens discovery.** Search for terms specific to the object. This is the lens side of the arc-lens:
   - `state-memory.md`: continuity, authority, state, dynasty, republic, party, empire, rupture, restoration, succession, sovereignty.
   - `god.md`: sacred, religion, divine, mandate, Heaven, Orthodox, Islam, Shi, Asha, Druj, martyr, righteous, covenant, rights, oath.
   - `lit.md`: LIT, poetry, epic, classic, witness, dissent, sage, story, language, conscience.
   - `art.md`: ART, music, architecture, monument, sculpture, painting, calligraphy, garden, shrine, museum, performance.
   - `geo.md`: geography, ecology, terrain, river, sea, ocean, mountain, plateau, steppe, canal, strait, port, water, food, energy, climate, resource, route, chokepoint.
   - `war.md`: WAR, battle, invasion, civil war, martyr, sacrifice, deterrence, humiliation, blockade.
   - `peace.md`: treaty, diplomacy, settlement, recognition, reconstruction, restraint, neutrality, verification.
5. **Run or emulate graph retrieval through `MEM CONNECTIONS`.** Use connection expansion to find adjacent evidence, counterweights, analogies, rupture points, and transaction constraints. Prefer:

```powershell
python scripts/route_civ_mem_topic.py "<lane> <object> <topic>" --bfs-mem-target 25 --bfs-max-depth 3 --bfs-neighbors-per-hop 12 --no-focus
```

Use `PYTHONIOENCODING=utf-8` if PowerShell cannot print CIV-MEM dashes. If the router profile is too generic for the object, manually open promising MEM files and follow their `MEM CONNECTIONS` sections.

6. **Open source bodies, not only filenames.** For baseline heavy backfills, read:
   - `CIV-CORE-*`, when present;
   - `CIV-STATE-*`, when present;
   - one index, doctrine, relevance, or seed file if present;
   - **8-12 opened MEM bodies** relevant to the object when doing a major backfill;
   - at least **two connection-discovered counterweight MEMs** that complicate the first pattern.
7. **Use the quantitative default.** Direct retrieval should create the first 8-12 candidate MEMs. `MEM CONNECTIONS` should expand the candidate pool to roughly **20-35** before final selection. Mark the object `Provisional` if no useful connection path or counterweight can be found.
8. **Extract, do not summarize.** For each opened source, pull one statecraft-useful pattern:
   - legitimacy claim;
   - sacred or moral boundary;
   - humiliation / disorder / sacrifice trigger;
   - authority or carrier implication;
   - failure mode;
   - transaction constraint.
9. **Shape the arc.** Convert the extracted patterns into origin, continuity, transformation, current carrier, failure mode, and transaction use. This is the arc side of the arc-lens. A source list without an arc is still shallow.
10. **Cite every opened source that materially shaped the arc-lens** in `## CIV-MEM Inputs`. Do not cite paths that were not opened unless clearly marked as pointers for later.
11. **Preserve the membrane.** If graph retrieval reveals a durable new lane insight, stage it only as a candidate in `<lane>/updates/pending.md`. Do not directly rewrite transaction files, CIV-MEM, PH-CIV, Record surfaces, or current state carrier files unless the operator separately requests that work.

### Evidence-Spine Rule

For major backfills, the final object should expose:

- **Seed MEM**
- **MEM CONNECTIONS cluster**
- **Overview corroborators**
- **Counterweight**
- **Current-carrier bridge**

Treat one-file doctrine as shallow by default. An object is not full-strength if it was built from one `CIV-CORE-*` overview alone or if it cannot name a counterweight and current-carrier relation.

### Lens-Specific Search Terms

Use the target lens to seed direct CIV-MEM search. These terms supplement the object-aware matrix; they do not replace it.

- `god.md`: `god`, `religion`, `sacred`, `divine`, `mandate`, `Heaven`, `Orthodox`, `Islam`, `Shi`, `Asha`, `Druj`, `martyr`, `righteous`, `covenant`, `rights`, `oath`.
- `lit.md`: `LIT`, author names, `poetry`, `epic`, `classic`, `witness`, `dissent`, `sage`, `story`, `language`.
- `art.md`: `ART`, `music`, `architecture`, `monument`, `sculpture`, `painting`, `calligraphy`, `garden`, `shrine`, `museum`, `performance`.
- `geo.md`: `GEO`, `geography`, `ecology`, `terrain`, `river`, `sea`, `ocean`, `mountain`, `plateau`, `steppe`, `canal`, `strait`, `port`, `water`, `food`, `energy`, `climate`, `resource`, `route`, `chokepoint`.
- `war.md`: `WAR`, `battle`, `invasion`, `civil war`, `martyr`, `sacrifice`, `deterrence`, `humiliation`, `blockade`.
- `peace.md`: `treaty`, `diplomacy`, `settlement`, `recognition`, `reconstruction`, `restraint`, `neutrality`, `verification`.

### Backfill Output Rule

Every civilization arc-lens backfill should include:

- `Purpose`
- `Civilizational Function`
- an arc-bearing continuity or pattern section when useful, naming origin, continuity, transformation, current carrier, failure mode, and transaction use;
- `Statecraft Signals`
- one lens-specific boundary section when needed, such as `Sacred Boundary` for `god.md`;
- `Failure Mode`
- `CIV-MEM Inputs`
- `Transaction Use`

### Arc-Lens Output Contract

Every major arc-lens must make four claims explicit:

1. **Lens side:** what the object detects in a present crisis, transaction, clause, or policy question.
2. **Arc side:** origin, continuity, transformation, current carrier, failure mode, and transaction use.
3. **Orthogonality side:** what the object must not steal from neighboring objects once the governing six-part layer has already been identified:
   - `god.md` owns sacred boundary and forbidden bargain;
   - `lit.md` owns narrative, moral language, witness, dissent, and memory;
   - `art.md` owns form, beauty, spectacle, ceremony, architecture, music, and public image;
   - `geo.md` owns terrain, ecology, routes, resource constraints, climate stress, food/water/energy base, chokepoints, and settlement geography;
   - `war.md` owns coercion, sacrifice, deterrence, command, and escalation;
   - `peace.md` owns settlement, restraint, recognition, verification, and off-ramp legitimacy.
4. **Membrane side:** when the object discovers a durable lane rule, it stages a recursive candidate in `<lane>/updates/pending.md`; it does not directly rewrite transactions, CIV-MEM, PH-CIV, Record, raw-input, or current carrier files.

If any side is missing, mark the object `Provisional` or revise before finishing. An arc-lens should answer both "what does this help us see now?" and "what civilizational development gives that reading authority?"

Add a short working provenance habit while drafting: what was searched, what was opened, and what pattern each source contributed. The final file does not need a long audit log, but the answer to the operator must be able to trace the CIV-MEM use honestly.

For major backfills, the operator-facing answer must include:

- direct CIV-MEM sources opened;
- `MEM CONNECTIONS` expansion run or manually emulated;
- connected MEMs used;
- the counterweight source that complicated the thesis;
- the named statecraft pattern extracted from each used source;
- whether the object is full-strength or `Provisional`.

### Shallow Backfill Rejection Test

Do not finish a backfill if any of these are true:

- it could have been written from lane summaries alone;
- `## CIV-MEM Inputs` contains sources not opened or not used;
- all sources point in one direction and no counterweight source was checked;
- `MEM CONNECTIONS` were ignored on a major object backfill;
- the file names themes but does not convert them into transaction constraints;
- the arc-lens cannot answer what would make a bargain forbidden, humiliating, disorder-producing, coercive, unserious, or illegitimate.

## Default Shapes

Use a flattened `state/` carrier layout for lanes where the operator has chosen the new structure:

```text
<lane>/civilization/objects/state-memory.md
<lane>/state/<current-carrier>.md
<lane>/state/objects/<transmitter>.md
```

For civilization arc-lenses, use:

```text
<lane>/civilization/<lens>.md
```

where `<lens>` is `god`, `lit`, `art`, `geo`, `war`, or `peace`.

## Transaction Test

Every state-memory object and civilization arc-lens should make transactions more usable. Include questions that test:

- whether the clause preserves the durable state interest;
- which current carrier must authorize, implement, sell, or restrain it;
- which historical wound, dignity claim, legitimacy grammar, sacred boundary, or continuity burden the wording touches;
- what makes the settlement look like collapse, humiliation, overreach, profanation, disorder, or managed dependency;
- what observable mechanism proves implementation after the headline moment.

## Output

When answering without file edits, provide a compact architecture recommendation. When implementing, modify the lane files, run validation, and summarize:

- state-memory object or civilization arc-lens added/refined;
- CIV-MEM discovery method used;
- source bodies opened and patterns extracted;
- carrier files moved or linked, if relevant;
- stale links checked;
- validation result.


## Cursor / grace-mar instance

**strategy-codex instance notes**

- Preferred operator invocation: `memory`
- Legacy alias note: older references to `state-memory` as a skill mean this skill
- Keep `state-memory` as the canonical statecraft object family:
  - `civilization/objects/state-memory.md`
  - `statecraft/templates/state-memory.md`
  - migration and inventory object-class keys
- Do not blur this skill with repo meanings such as `self-memory`, runtime memory, or speaker-memory.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill memory
python scripts/sync_portable_skills.py --verify --skill memory
python scripts/validate_skills.py
```
