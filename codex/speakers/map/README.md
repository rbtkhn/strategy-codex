# Speaker Map

WORK only; not Record.

`speaker-map/` is the navigation and route-map layer over the canonical speaker memory shelf.

It does not replace the parent [`codex/speakers/`](../). Speaker folders remain the durable accumulation layer for speaker objects, host-local arcs, helixes, cross-year notes, and routing notes. Speaker-map files should help agents decide what to open next, compare routes, and see cross-host reinforcement without moving interpretation out of the speaker folders.

For the storage-side SSOT and the canonical raw-input-side version of the wiring rule, see [raw-input/README.md](../../years/2026/raw-input/README.md).

This README is the governing speaker-routing doctrine. Speaker folders, year indexes, and lattice surfaces should implement this contract rather than restate it in local variants.

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

Use this ladder as a reusable doctrine for all speakers when cross-host spread becomes thick enough to matter. It is optional for thin or single-stream objects, but once needed it should replace repeated source-name exceptions in prose.

## Route Contract

Use the ladder this way:

- `core host lane` = the appearance belongs to a stable host transformation and should be entered through that host-local route surface
- `non-core appearance bench` = the appearance is valid and materialized, but does not belong to a stable host transformation
- `discovery memory` = the appearance is found, mentioned, or operator-pasted, but not yet materialized as raw-input

Governance rule:

- `speaker-map` owns the route contract
- `speaker-lattice` may signal that a fuller route is needed, but it does not decide ownership or completion
- local speaker folders may implement the ladder, but they should do so as applications of this contract, not as parallel doctrine

## Wiring Invariant

No valid speaker raw-input should remain unwired from the correct speaker surface.

That means:

- if a raw-input clearly belongs to a speaker's stable host transformation, wire it into the relevant `core host lane`
- if it is valid and materialized but does not belong to a stable host transformation, wire it into that speaker's `non-core appearance bench`
- if it is only found, mentioned, or partially pasted and not yet materialized as raw-input, keep it in `discovery memory` until it can be either materialized or discarded

An unwired valid raw-input is a routing defect, not a harmless omission.

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

The closeout owner is the routing stack, not storage. If speaker-map cannot name the correct routed surface, the appearance has not ended its life well enough to call the task complete.

## Audit Posture

Speaker-map does not own provenance, but it does own the routing-side completion check after materialization.

Ask:

1. Which speaker surface exposes this capture now?
2. Is that surface a `core host lane` or a `non-core appearance bench`?
3. Is any item still sitting in `discovery memory` even though the raw-input has already been materialized?
4. Is the route complete for the touched speaker, or only mentioned in passing somewhere nearby?

If the map can name the speaker but cannot name the correct routed surface, the work is not complete.

Speaker-map may point to speaker memory. It should not become the authority for a speaker's meaning. If a map and a speaker object disagree, open the speaker object and repair the map later.

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
