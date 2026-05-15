# Speaker Map

WORK only; not Record.

`speaker-map/` is the navigation and route-map layer over the canonical speaker memory shelf.

It does not replace [`../speakers/`](../speakers/). Speaker folders remain the durable accumulation layer for speaker objects, host-local arcs, helixes, cross-year notes, and routing notes. Speaker-map files should help agents decide what to open next, compare routes, and see cross-host reinforcement without moving interpretation out of the speaker folders.

## Layer Contract

- `raw-input/` = provenance
- `appearance` = one host/speaker/date/source event derived from verified raw-input
- `speaker arc` = host-local interpretation
- `speaker object` = durable speaker orientation
- `speaker helix` / cross-host note = comparative memory
- `speaker-map/` = navigation, maps, adjacency, and open-first routes
- `lattice` = lookup pointer, not the main interpretive surface

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

Do not auto-edit speaker-map from daily ingest unless the operator asks for that follow-up.
