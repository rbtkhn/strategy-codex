# Speakers

Speakers are higher-order strategy-codex objects outside the current eight-stream scaffold. They may carry speaker-arcs, speaker-helixes, cross-year notes, profiles, and other speaker-local materials without becoming first-class cognition streams in this volume.

Do not use this shelf for text-first analyst-writer folders such as `simplicius` or `bigserge`; those belong under [`../writers/`](../writers/).

Promote a speaker into the scaffold only by explicit operator decision.

WORK only; not Record.

## Memory architecture

Speaker folders are the durable accumulation layer for recurring figures. Use them to accumulate judgment about who a speaker is in the notebook, why the speaker matters, where to open first, and what not to overclaim.

Raw-input remains provenance. An **appearance** is one derived host/speaker/date/source event from a verified raw-input capture. Speaker arcs remain host-local interpretation. Speaker objects remain orientation and routing. Speaker helixes and cross-host notes remain comparative surfaces. In this shelf, lattice rows are lookup pointers only; they may cite speaker folders, but they should not become the place where every interpretation lives.

For map-like navigation across the shelf, use [`../speaker-map/`](../speaker-map/). Speaker-map is an index layer over this shelf, not a rename and not a replacement. Durable memory stays here; route views, adjacency maps, and open-first route maps live there.

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
- [speaker helix template](_templates/speaker-helix-template.md)

Existing `*-page-template.md` files are compatibility stubs for older page scaffolds. Do not use them as the speaker-memory templates.

## Speaker object contract

A speaker folder becomes a first-class speaker-object folder when it contains a `*-speaker-object.md` note. That note is an orientation and routing object, not a provenance ledger.

Each speaker-object note should include:

- `WORK only; not Record.`
- `## Object shape`
- `## Open first`
- `## Boundaries`
- one declared object shape, either as an explicit `object_shape: <shape>` line or in the prose of the Object shape section

Allowed object shapes:

- `profile-only` - a light orientation shelf, not yet a mature thread, stream, or helix
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
