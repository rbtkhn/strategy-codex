# Speaker Map

WORK only; not Record.

`speaker-map/` is the navigation and route-map layer over the canonical speaker memory shelf.

It does not replace the parent [`statecraft/voices/`](../). Speaker folders remain the durable accumulation layer for speaker objects, host-local arcs, helixes, cross-year notes, and routing notes. Speaker-map files should help agents decide what to open next, compare routes, and see cross-host reinforcement without moving interpretation out of the speaker folders.

For the storage-side SSOT and the canonical raw-input-side version of the wiring rule, see [provenance/README.md](../../years/2026/provenance/README.md).

This README is the governing speaker-routing doctrine. Speaker folders, year indexes, and lattice surfaces should implement this contract rather than restate it.

For the compact speaker-shelf naming table that this routing doctrine assumes, see [Speaker-Shelf Vocabulary](/C:/dev/strategy-codex/statecraft/voices/speaker-shelf-vocabulary.md).

## Layer Contract

- `raw-input/` = provenance
- `appearance` = one host/speaker/date/source event derived from verified raw-input
- `speaker arc` = host-local interpretation
- `speaker object` = durable speaker orientation
- `speaker helix` / cross-host note = comparative memory
- `speaker-map/` = navigation, maps, adjacency, and open-first routes
- `lattice` = lookup pointer, not the main interpretive surface

Benchmark pin:

- `raw-input/` decides provenance, publication day, materialization status, and primary ownership
- speaker and host routing surfaces decide downstream visibility, route shape, and whether wiring is complete after materialization

## Routing Ladder

When a speaker has appearances beyond one stable host lane, prefer a three-tier ladder instead of ad hoc channel-by-channel doctrine:

- `core host lane`: a stable host transformation with its own route surface
- `non-core appearance bench`: materialized transcript-bearing appearances outside those core lanes
- `discovery memory`: found or operator-pasted appearances that still help routing but are not yet materialized raw-input

Use this ladder when cross-host spread becomes thick enough to matter. Once needed, it should replace repeated source-name exceptions in prose.

The ladder is intentionally sparse:

- the corpus-wide raw-input master index handles global lookup
- the speaker source index handles a real `non-core appearance bench`
- the arc handles interpretation

Do not add a separate index surface for every arc by default.

## Source Vocabulary

Inside speaker routing doctrine, use the terms this way:

- **`source-index`** = the named speaker route surface
- **`source bench`** = the retrieval role that surface performs
- **`provenance bench`** = optional emphasis when the point is evidentiary breadth rather than file naming

Map rule:

- when naming the surface, say `source-index`
- when describing the routing job, say `source bench`
- preserve `provenance bench` only where the route contract needs to stress archive-facing breadth or lower-interpretation evidence coverage

## Thread Vocabulary

Inside speaker routing doctrine, use the thread terms this way:

- **`thread atlas`** = the named recurring-strand route surface
- **`arc-threads`** = the recurring strands that a bounded arc or host-local arc braids together

Map rule:

- when naming the surface, say `thread atlas`
- when describing what sits inside a bounded arc, say `arc-threads`
- preserve `arc-threads` as a surface label only when a legacy filename or compatibility path still uses it

## Route Contract

Use the ladder this way:

- `core host lane` = the appearance belongs to a stable host transformation and should be entered through that host-local route surface
- `non-core appearance bench` = the appearance is valid and materialized, but does not belong to a stable host transformation
- `discovery memory` = the appearance is found, mentioned, or operator-pasted, but not yet materialized as raw-input

Governance rule:

- `speaker-map` owns the route contract
- `speaker-lattice` may signal that a fuller route is needed, but it does not decide ownership or completion
- local speaker folders implement the ladder as applications of this contract, not as parallel doctrine

## Orthogonality Invariant

Speaker memory should strive for **orthogonality across surfaces**.

This applies at two levels:

- **between arcs**: different person arcs, relational arcs, or host-local arcs should contribute materially different explanatory value rather than restating the same continuity in slightly different wording
- **between threads inside an arc**: each topical thread should isolate a genuinely distinct recurring strand, not a near-duplicate of a neighboring thread

Working rule:

- if two arcs produce the same conclusion, check whether they arrive there by different mechanisms, source habits, or explanatory layers
- if two threads sit inside one arc, check whether they differ in object, causal grammar, or retrieval use
- if a proposed surface cannot defend its distinctness, collapse it, rename it, or keep the material inside the parent arc

The target is not maximal fragmentation. The target is **maximum cognitive depth, breadth, and connectivity with minimum redundant surface area**.

Operational tests:

1. **Frame test** - does this surface see something differently, or only repeat it?
2. **Evidence test** - does it rely on a distinct source spine or recurring receipt pattern?
3. **Use test** - would an operator open this surface for a meaningfully different reason than a neighboring one?

When the answer is no, do not add another surface just because it is possible.

## When an arc deserves its own index

An arc-specific index is exceptional and should only be created when all of the following are true:

1. **Front-door test** - the parent arc is no longer a practical front door for the material it now contains.
2. **Retrieval-domain test** - the items being indexed form a distinct retrieval domain rather than just a chronology, month run, or reading order.
3. **Question-difference test** - the proposed index answers a meaningfully different operator question than the neighboring speaker source index, host lane, or arc.
4. **Completion-role test** - the surface has a stable ownership story and a real completion role in the routing stack.

If those tests are not all satisfied, keep the material in:

- the corpus-wide raw-input master index for global lookup
- the speaker source index for `non-core appearance bench` retrieval
- the arc itself for interpretation

This is the speaker-map application of the repo's `Fullness Before Closure` doctrine: do not multiply index surfaces until the extra route is functionally necessary.

## Wiring Invariant

No valid speaker raw-input should remain unwired from the correct speaker surface.

That means:

- if a raw-input clearly belongs to a speaker's stable host transformation, wire it into the relevant `core host lane`
- if it is valid and materialized but does not belong to a stable host transformation, wire it into that speaker's `non-core appearance bench`
- if it is only found, mentioned, or partially pasted and not yet materialized as raw-input, keep it in `discovery memory` until it can be either materialized or discarded

An unwired valid raw-input is a routing defect.

Enforcement rule:

- do not treat a materialized capture as fully processed if the map cannot name its correct routed surface
- do not let discovery-memory mentions, lattice mentions, or passing prose references count as routed visibility

## Lifecycle Closure

For speaker appearances, the lifecycle question is: where does this appearance properly end its life once it is valid and materialized?

Valid terminal states:

- `core host lane`
- `non-core appearance bench`
- `both`, when host-owned routing and speaker-side visibility are both required
- `discarded after review`, when the item turns out not to be a valid routed speaker capture

False terminal states:

- `raw-input only`
- `discovery memory only`
- `lattice mention only`
- `passing prose only`
- `cross-host note only` when no correct routed surface exists underneath it

The closeout owner is the routing stack, not storage. If speaker-map cannot name the correct routed surface, the task is not complete.

## Audit Posture

Speaker-map does not own provenance, but it does own the routing-side completion check after materialization.

Ask:

1. Which speaker surface exposes this capture now?
2. Is that surface a `core host lane` or a `non-core appearance bench`?
3. Is any item still sitting in `discovery memory` even though the raw-input has already been materialized?
4. Is the route complete for the touched speaker, or only mentioned in passing somewhere nearby?

If the map can name the speaker but not the correct routed surface, the work is not complete.

Speaker-map may point to speaker memory, but it is not the authority for speaker meaning. If a map and a speaker object disagree, repair the map later.

## Initial Views

- [Host map](host-map.md) - which host shelves carry which speaker arcs.
- [Cross-host index](cross-host-index.md) - which speakers appear across more than one host surface.
- [Open-first routes](open-first-routes.md) - recommended first paths through the map.

## Update Rule

Use speaker-map after materialization and routing:

1. Verify raw-input exists and is non-stub.
2. Build appearances and route stacks.
3. Review the speaker-memory action queue.
4. Update speaker objects, arcs, or helixes only when explicitly approved.
5. Update speaker-map indexes after the underlying speaker memory path is clear.

Before considering routing complete, check that every valid speaker raw-input touched by the task has landed in the correct speaker path. If it has not, the work is still incomplete.

If the capture is still stranded in storage, discovery memory, or a thin mention-only surface, the correct closeout is `routing still open`, not `done`.

Do not auto-edit speaker-map from daily ingest unless the operator asks for that follow-up.
