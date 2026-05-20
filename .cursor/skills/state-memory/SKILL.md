---
name: state-memory
description: "Build, mirror, audit, or backfill academy-statecraft civilization memory surfaces from CIV-MEM. Use when the operator says state-memory, asks to convert CIV-MEM into civilization/objects/state-memory.md, mirror state-memory architecture, audit current state carriers, create or refine civilization lenses such as god.md, lit.md, art.md, war.md, or peace.md, demands deep CIV-MEM search/analysis, or wants to prevent biography drift and shallow summary backfills in academy-statecraft lanes."
---

# State Memory

`state-memory` turns CIV-MEM and lane-local statecraft material into the academy-statecraft authority-memory and civilization-lens layers. It keeps the lanes from sliding into biography or shallow summary by enforcing:

> Civilization stores state memory. Empire converts memory into reach. State carries present authority. Objects transmit signals. Transactions test whether authority can become settlement.

## Boundary

- WORK only; not Record.
- Do not edit PH-CIV corpus or CIV-MEM source files from this workflow.
- Do not create transaction files unless the operator separately asks.
- Use lane-local `updates/pending.md` for durable recursive candidates; live analysis proposes, human review decides.
- Preserve unrelated dirty files. State-memory edits should stay inside `codex/academy/statecraft/` unless the operator explicitly expands scope.
- Do not build civilization lens backfills only from existing lane summaries. Use direct CIV-MEM discovery, `MEM CONNECTIONS`, and opened source bodies before drafting.

## Workflow

1. **Ground in repo truth.** Search the target lane and CIV-MEM inputs before drafting:

```powershell
rg -n "state-memory|heads-of-state|authority-structure|objects|CIV-MEM|CIV|STATE" codex/academy/statecraft research/repos/civilization_memory
```

2. **Identify CIV-MEM inputs.** Prefer the target civilization's `CIV-CORE-*` / `CIV–CORE–*`, `CIV-STATE-*` / `CIV–STATE–*`, doctrine / index files, relevance files, and lane-local `civilization/seed-patterns.md`. Cite them in `## CIV-MEM Inputs`; do not rewrite them.
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

## Civilization Lens Backfills

Use this branch when creating or refining lane-local civilization lenses such as:

- `civilization/god.md`
- `civilization/lit.md`
- `civilization/art.md`
- `civilization/war.md`
- `civilization/peace.md`

These backfills must be cognitively dense and source-supported. Existing statecraft summaries may guide the question, but they are not enough.

### Required CIV-MEM Pass

Before drafting a major state-memory or civilization lens backfill, use a three-stage retrieval path. CIV-MEM is the deep civilizational memory graph; academy-statecraft is the operational command surface. Do not let urgency collapse the graph into summary.

1. **Fix the lane, object, and civilization id.**
   - America -> `AMERICA`
   - Russia -> `RUSSIA`
   - China -> `CHINA`
   - Iran -> `PERSIA`
2. **Check the object-aware retrieval matrix.** Open `codex/academy/statecraft/sheets/civ-mem-object-retrieval-matrix.md` when it exists. Use the row for the target object, such as `russia-god`, `china-art`, `iran-peace`, or `america-war`, to set seed terms, required source classes, connection expansion, and counterweight expectations.
3. **Run or emulate direct lane discovery.** Prefer:

```powershell
python scripts/suggest_civ_mem_from_relevance.py <CIV_ID>
```

If the relevance script is missing, exits nonzero, or lacks the needed domain, use targeted `rg` over `research/repos/civilization_memory/content/civilizations/<CIV_ID>` with the lens terms.

4. **Run or emulate lens discovery.** Search for terms specific to the object:
   - `state-memory.md`: continuity, authority, state, dynasty, republic, party, empire, rupture, restoration, succession, sovereignty.
   - `god.md`: sacred, religion, divine, mandate, Heaven, Orthodox, Islam, Shi, Asha, Druj, martyr, righteous, covenant, rights, oath.
   - `lit.md`: LIT, poetry, epic, classic, witness, dissent, sage, story, language, conscience.
   - `art.md`: ART, music, architecture, monument, sculpture, painting, calligraphy, garden, shrine, museum, performance.
   - `war.md`: WAR, battle, invasion, civil war, martyr, sacrifice, deterrence, humiliation, blockade.
   - `peace.md`: treaty, diplomacy, settlement, recognition, reconstruction, restraint, neutrality, verification.
5. **Run or emulate graph retrieval through `MEM CONNECTIONS`.** Use connection expansion to find adjacent evidence, counterweights, analogies, rupture points, and transaction constraints. Prefer:

```powershell
python scripts/route_civ_mem_topic.py "<lane> <object> <topic>" --bfs-mem-target 25 --bfs-max-depth 3 --bfs-neighbors-per-hop 12 --no-focus
```

Use `PYTHONIOENCODING=utf-8` if PowerShell cannot print CIV-MEM dashes. If the router profile is too generic for the object, manually open promising MEM files and follow their `MEM CONNECTIONS` sections.

6. **Open source bodies, not only filenames.** For baseline heavy backfills, read:
   - `CIV-CORE-*` or `CIV–CORE–*`, when present;
   - `CIV-STATE-*` or `CIV–STATE–*`, when present;
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
9. **Cite every opened source that materially shaped the lens** in `## CIV-MEM Inputs`. Do not cite paths that were not opened unless clearly marked as pointers for later.
10. **Preserve the membrane.** If graph retrieval reveals a durable new lane insight, stage it only as a candidate in `<lane>/updates/pending.md`. Do not directly rewrite transaction files, CIV-MEM, PH-CIV, Record surfaces, or current state carrier files unless the operator separately requests that work.

### Lens-Specific Search Terms

Use the target lens to seed direct CIV-MEM search. These terms supplement the object-aware matrix; they do not replace it.

- `god.md`: `god`, `religion`, `sacred`, `divine`, `mandate`, `Heaven`, `Orthodox`, `Islam`, `Shi`, `Asha`, `Druj`, `martyr`, `righteous`, `covenant`, `rights`, `oath`.
- `lit.md`: `LIT`, author names, `poetry`, `epic`, `classic`, `witness`, `dissent`, `sage`, `story`, `language`.
- `art.md`: `ART`, `music`, `architecture`, `monument`, `sculpture`, `painting`, `calligraphy`, `garden`, `shrine`, `museum`, `performance`.
- `war.md`: `WAR`, `battle`, `invasion`, `civil war`, `martyr`, `sacrifice`, `deterrence`, `humiliation`, `blockade`.
- `peace.md`: `treaty`, `diplomacy`, `settlement`, `recognition`, `reconstruction`, `restraint`, `neutrality`, `verification`.

### Backfill Output Rule

Every civilization lens backfill should include:

- `Purpose`
- `Civilizational Function`
- `Statecraft Signals`
- one lens-specific boundary section when needed, such as `Sacred Boundary` for `god.md`;
- `Failure Mode`
- `CIV-MEM Inputs`
- `Transaction Use`

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
- the lens cannot answer what would make a bargain forbidden, humiliating, disorder-producing, coercive, unserious, or illegitimate.

## Default Shapes

Use a flattened `state/` carrier layout for lanes where the operator has chosen the new structure:

```text
<lane>/civilization/objects/state-memory.md
<lane>/state/<current-carrier>.md
<lane>/state/objects/<transmitter>.md
```

For civilization lenses, use:

```text
<lane>/civilization/<lens>.md
```

where `<lens>` is `god`, `lit`, `art`, `war`, or `peace`.

## Transaction Test

Every state-memory object and civilization lens should make transactions more usable. Include questions that test:

- whether the clause preserves the durable state interest;
- which current carrier must authorize, implement, sell, or restrain it;
- which historical wound, dignity claim, legitimacy grammar, sacred boundary, or continuity burden the wording touches;
- what makes the settlement look like collapse, humiliation, overreach, profanation, disorder, or managed dependency;
- what observable mechanism proves implementation after the headline moment.

## Output

When answering without file edits, provide a compact architecture recommendation. When implementing, modify the lane files, run validation, and summarize:

- state-memory object or civilization lens added/refined;
- CIV-MEM discovery method used;
- source bodies opened and patterns extracted;
- carrier files moved or linked, if relevant;
- stale links checked;
- validation result.
