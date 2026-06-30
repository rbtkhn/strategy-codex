# CIV-EMP Source Retrieval Matrix


## Purpose

Use this matrix before creating or upgrading academy-statecraft civilization, empire, helix, or state-memory objects from CIV-EMP.

CIV-EMP is the local Civilization and Empire source base for academy-statecraft. It replaces active CIV-MEM reliance in this workshop while preserving CIV-MEM as legacy provenance where older lane objects already cite it.

## Retrieval Contract

For each arc-lens or empire instrument, run four retrieval layers:

1. **CIV-EMP source retrieval** - open the relevant CIV-EMP source object, volume map, or index entry once present.
2. **Lane retrieval** - open the lane's `civilization/`, `empire/`, `state/`, `helix.md`, and seed-pattern surfaces where present.
3. **Lens retrieval** - search for the object-specific seed terms below.
4. **Counterweight retrieval** - find at least one source or lane object where the pattern degrades, reverses, overreaches, or becomes unusable.

During migration, older CIV-MEM files may serve as provenance for CIV-EMP objects, but statecraft outputs should cite the CIV-EMP object or lane-local translation whenever one exists.

## Arc-Conditioned Retrieval

Some live claims arrive through speaker arcs before they are mature enough for direct transaction routing. In those cases, use the quiet bridge layer in [academy-statecraft bridges](../../bridges/README.md) to choose the right retrieval profile before opening lane surfaces.

Current pilot adapters:

- [Marandi CIV-EMP retrieval adapter](../../bridges/marandi-civ-emp-retrieval-adapter.md) for recognition, legitimacy, sovereignty, and leverage-meaning claims
- [Parsi CIV-EMP retrieval adapter](../../bridges/parsi-civ-emp-retrieval-adapter.md) for guarantees, sequencing, architecture, and settlement-durability claims

## Citation Preference

Prefer the narrowest source that can carry the claim:

1. Cite a lane-local object when the claim is already translated into statecraft use.
2. Cite a CIV-EMP source object when the claim needs source-base authority.
3. Cite PH-CIV or legacy CIV-MEM only as upstream provenance or when no CIV-EMP object exists yet.

Do not cite a broad public source or legacy graph file merely because it is impressive. The goal is faster operational retrieval with enough provenance to remain honest.

## Arc-Lens Contract

Every major civilization object is an arc-lens, not a topic page. The lens side names what the object helps the operator see in the present. The arc side explains how that perception was formed through civilizational memory.

Gather evidence for each component:

- **Origin** - the earliest or clearest formation point of the pattern.
- **Continuity** - the carriers that let the pattern survive rupture.
- **Transformation** - the moments that mutate the pattern under defeat, conquest, reform, revolution, technology, or institutional pressure.
- **Current carrier** - the present authority, transmitter, institution, or implementation surface that bears the pattern now.
- **Failure mode** - the way the arc hardens, degrades, becomes false, or turns against the civilization it claims to protect.
- **Transaction use** - the clause, routing, objection, carrier, or recursive-candidate test the arc enables.

Mark an object `Provisional` if it cannot identify origin, transformation, failure mode, and transaction use.

## Object Matrix

| Object | CIV-EMP lane | Source classes | Seed terms | Counterweight requirement |
|---|---|---|---|---|
| `state-memory` | America, Russia, China, Iran | CIV-EMP source object, lane civilization, lane state, helix | continuity, succession, legitimacy, geography, state form, collapse, restoration | Find where continuity becomes coercion, personalism, paralysis, or imperial overreach. |
| `god` | America, Russia, China, Iran | CIV-EMP sacred grammar, lane civilization, state-memory | covenant, providence, Orthodoxy, mandate, Asha, Druj, Shia, legitimacy, sacred order | Find where sacred grammar becomes domination, broken mandate, instrumentalized faith, or martyrdom lock. |
| `lit` | America, Russia, China, Iran | CIV-EMP narrative/language, lane civilization, speaker-state use | conscience, suffering, classics, poetry, dignity, memory, witness, face | Find where narrative becomes paralysis, grievance capture, warning suppression, or hollow moral theater. |
| `art` | America, Russia, China, Iran | CIV-EMP form/beauty, lane civilization, empire instrument | landscape, icon, calligraphy, monument, garden, spectacle, architecture | Find where beauty becomes nostalgia, spectacle, coercive form, or prestige demand. |
| `geo` | America, Russia, China, Iran | CIV-EMP geography, lane civilization, lane empire, transaction route | continent, steppe, river, plateau, Gulf, ports, water, food, energy, chokepoint | Find where geography becomes scarcity, expansion trap, ecological pressure, or corridor exposure. |
| `war` | America, Russia, China, Iran | CIV-EMP war memory, lane civilization, lane empire, current carrier | civil war, invasion, humiliation, martyrdom, sacrifice, deterrence, blockade | Find where coercion exceeds authority, sacrifice becomes unlimited claim, or deterrence substitutes for settlement. |
| `peace` | America, Russia, China, Iran | CIV-EMP settlement memory, lane civilization, state carrier, transaction object | treaty, recognition, neutrality, relief, verification, restraint, guarantees | Find where peace becomes domination, humiliation, creditor leverage, or endless enforcement. |
| `empire-instrument` | America, Russia, China, Iran | CIV-EMP empire volume, lane empire, lane helix | force, finance, alliance, chokepoint, law, infrastructure, dependency, sanctions | Find where amplification degrades the civilization or traps the state in overreach. |

## Output Benchmarks

A full-strength object should improve statecraft retrieval over direct search alone:

- It gives one named pattern and one named counterweight.
- It links civilization memory to an empire instrument or state carrier.
- It produces at least one transaction hook.
- It can be cited from a treaty, memo, negotiation brief, or crisis route without reopening the entire upstream corpus.

## Membrane Rule

CIV-EMP retrieval can propose durable lane improvements, but it cannot absorb them automatically.

Route durable discoveries as:

`CIV-EMP signal -> named statecraft pattern -> lane-local update candidate -> human review -> accepted lane change`

Use `<lane>/updates/pending.md` for candidates. Do not directly rewrite transactions, PH-CIV, CIV-MEM, Record surfaces, raw-input, speaker sources, or current state carrier files unless the operator separately requests that implementation.

## Upstream-Candidate Rule

When downstream Civilizational Statecraft work exposes a durable source insight, classify it before editing anything:

1. **Send upstream to `civ-emp`** when the discovery changes:
   - source pattern
   - retrieval logic
   - historical counterweight
   - source-object contract
2. **Keep downstream in Civilizational Statecraft** when the discovery changes:
   - menu or deployer behavior
   - lane-local routing
   - helix judgment
   - objection handling
   - transaction or clause design
3. **When both layers are implicated**
   - draft the live downstream instrument first
   - then stage one explicit upstream candidate rather than silently mutating both layers

Default test:

- `Would another lane benefit from this as source memory or retrieval discipline?` Send it upstream.
- `Is this mainly about how we route, phrase, or carry an instrument here?` Keep it downstream.
