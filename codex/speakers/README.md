# Speakers

Speakers are higher-order strategy-codex objects outside the current eight-stream scaffold. They may carry speaker-arcs, speaker-helixes, cross-year notes, profiles, and other speaker-local materials without becoming first-class cognition streams in this volume.

Do not use this shelf for text-first analyst-writer folders such as `simplicius` or `bigserge`; those belong under [`../writers/`](../writers/).

Promote a speaker into the scaffold only by explicit operator decision.

WORK only; not Record.

## Memory architecture

Speaker folders are the durable accumulation layer for recurring figures. Use them to accumulate judgment about who a speaker is in the notebook, why the speaker matters, where to open first, and what not to overclaim.

Creation threshold: do **not** create a speaker folder for thin, accidental, or one-off recurrence. A speaker belongs on this shelf only after the notebook has enough real continuity that future routing would otherwise keep rebuilding the same judgment from scratch.

Raw-input remains provenance. An **appearance** is one derived host/speaker/date/source event from a verified raw-input capture. Speaker arcs remain host-local interpretation. Speaker objects remain orientation and routing. Speaker helixes and cross-host notes remain comparative surfaces. In this shelf, lattice rows are lookup pointers only; they may cite speaker folders, but they should not become the place where every interpretation lives.

Layering rule: a **speaker arc** in the speaker shelf is the canonical person-level continuity surface; **host-local arcs** in host shelves are bounded transformations of that speaker under one host's pressure; **bench or month-spine support** in the speaker shelf exists only to route non-core appearances and month-level sequencing without replacing the canonical arc; and **statecraft intake** remains downstream, drawing speaker-state from these surfaces to build country, transaction, or civilizational instruments without becoming the owner of the speaker object itself. Freeman is the model case for this layering.

Cross-speaker disagreement or comparison objects that do not belong to one speaker's continuity ownership should live under [`relations/`](relations/), not inside a single speaker folder by default.

For map-like navigation across the shelf, use [`../speaker-map/`](../speaker-map/). Speaker-map is an index layer over this shelf, not a rename and not a replacement. Durable memory stays here; route views, adjacency maps, and open-first route maps live there.

For the authored/interview subtype, use [authored-pressure-quartet.md](/C:/dev/strategy-codex/codex/speakers/authored-pressure-quartet.md). It clusters Crooke, Ritter, Pape, and Parsi as a repeatable crisis-analysis pass: forecast clock, force constraint, settlement architecture, and structural misreading.

For a wider functional placement of the speaker shelf around that quartet, use [speaker-cluster-map.md](/C:/dev/strategy-codex/codex/speakers/speaker-cluster-map.md).

Default routing order after materialization:

1. verify the raw-input body exists and is not a stub
2. derive the appearance from frontmatter
3. route the appearance to the best primary surface
4. list additional surfaces the same appearance strengthens
5. aggregate routed appearances into an advisory action queue when concrete follow-up proposals are useful
6. update speaker memory only when the operator explicitly asks

The derived speaker-routing queue may point at multiple surfaces. A host-local speaker arc can be the primary route while the same appearance also strengthens a speaker object or cross-host note.

The derived speaker-memory action queue converts route stacks into operator-reviewable proposals: update an existing arc, review an existing object, create a candidate arc/object, or consider a helix. It is still a WORK artifact, not an automatic edit path.

Canonical templates:

- [speaker object template](_templates/speaker-object-template.md)
- [speaker arc template](_templates/speaker-arc-template.md)
- [speaker thread template](_templates/speaker-thread-template.md)
- [speaker helix template](_templates/speaker-helix-template.md)

Existing `*-page-template.md` files are compatibility stubs for older page scaffolds. Do not use them as the speaker-memory templates.

## Thread compatibility rule

The newer `speakers/` taxonomy uses **topical threads** in the form `<speaker>-thread-<topic>.md` as support surfaces beneath an arc.

Some folders still carry older single-file `*-thread.md` continuity artifacts. Unless a folder explicitly says otherwise, treat those as **legacy distilled continuity files**, not as proof that the shelf already has canonical topical threads.

When a legacy `*-thread.md` is retained:

- it should declare itself as a **compatibility continuity surface**
- it should include an explicit **orthogonality guide** that routes upward to the canonical arc, helix, thread atlas, or light profile-first surface that now owns the structure
- it should not silently behave like a second canonical topical-thread system

Do not proliferate new thread files merely because a legacy `*-thread.md` exists. Create a canonical topical thread only when:

- a parent person arc or relational arc already exists or is clearly implicit
- one recurring topic deserves its own reusable surface
- the new thread can defend distinct object, mechanism, and retrieval use under the orthogonality rule

## Arc compatibility rule

The current canonical relational-arc grammar is `<host>-<speaker>-arc.md`.

Some shelves still carry older `<host>-<speaker>-speaker-arc.md` files. Treat those as **compatibility spellings of relational arcs**, not as a second arc class.

When both exist:

- treat `<host>-<speaker>-arc.md` as the canonical continuity-bearing surface
- treat `<host>-<speaker>-speaker-arc.md` as an alias or compatibility stub
- do not count the two filenames as evidence of arc multiplicity or added orthogonality

## Speaker object contract

A speaker folder becomes a first-class speaker-object folder when it contains a `*-speaker-object.md` note. That note is an orientation and routing object, not a provenance ledger.

Minimum invariant: every canonical speaker folder needs a **routeable rationale**. That rationale answers why the folder exists, where a future agent should open first, what evidence or branch currently supports the object, and what maturity claim must not be overstated. A routeable rationale may be a speaker object, profile, native stream map, host-local arc pointer, cross-host note, authored ledger, or helix.

But the stricter shelf rule is now:

- if the speaker does **not** have enough real continuity, do **not** create the folder
- if the speaker does have enough real continuity to justify a folder, the folder should eventually become strong enough to state its own continuity honestly rather than staying permanently skeletal
- if the speaker is a **major speaker** with broad recurrence across hosts, contexts, or time, the shelf should converge toward one canonical **person arc** file: `<speaker>-arc.md`

Use an arc, helix, or authored-pressure ledger only when the evidence warrants it:

- a **host-local speaker arc** is earned by a recurring host x speaker lane
- a **person arc** is earned when one speaker's continuity across hosts, contexts, and time has become a reusable notebook object in its own right
- a **speaker helix** is earned by multiple host-local arcs that are strong enough to compare
- an **authored-pressure ledger** is earned by a substantial authored corpus with interview pressure
- a **profile-only** or **cross-host-reinforced** object is valid only when the speaker already has enough real recurrence to justify the folder, but the continuity is not yet broad enough to consolidate into a person arc or helix

This prevents two opposite errors: creating shelves for speakers who do not yet deserve one, and inflating a real but still-maturing speaker into premature helix/arc language that makes a light or search-backed body look more embodied than it is.

Each speaker-object note should include:

- `WORK only; not Record.`
- `## Object shape`
- `## Open first`
- `## Boundaries`
- one declared object shape, either as an explicit `object_shape: <shape>` line or in the prose of the Object shape section

Allowed object shapes:

- `profile-only` - a light orientation shelf, not yet a mature thread, stream, or helix
- `person-arc-first` - a canonical person arc is the primary way to enter the object, with helix, routing, and bench surfaces supporting it
- `stream-native` - the main body of the object is one native cognition stream
- `stream-anchored` - one native stream is primary, but the object is less stream-native than depth-native
- `stream-anchored-with-cross-host-reinforcement` - one native stream remains primary, while guest appearances materially reinforce the object
- `cross-host-reinforced` - no thick native stream dominates; the object coheres through recurring cross-host usefulness
- `single-helix` - one host-local branch carries helix-like depth
- `double-helix` - two host-local branches are mature enough to read together
- `triple-helix` - three host-local branches are mature enough to read together
- `helix-first` - host transformation is the primary way to enter the object, even if the exact branch count is still being refined

The object shape is a routing claim. It should tell future agents whether to enter through a native stream, a profile, a helix, or a cross-host reinforcement note. It should not flatten host-local speaker arcs into one generic speaker theory.

Validate with:

```bash
python scripts/validate_speaker_objects.py
```

## Speaker state-set manifests

Mature speaker folders may declare a local `state-set.toml` manifest. The manifest makes the shelf's compact state explicit: `compact_state_files` are the current routing/orientation surfaces, while `provenance_roots` remain the raw-input chain of custody. Source sets and guest matrices may then declare exact counts, prefixes, exclusions, and host-arc glob contracts that the validator can enforce.

Use this for mature folders where the current state should be dependable without rereading every capture. Do not use it to replace raw-input, speaker arcs, or ledger source links; it is a compact-state contract over those materials.

Validate with:

```bash
python scripts/validate_speaker_state_sets.py
```
