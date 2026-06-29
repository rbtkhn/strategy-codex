WORK only; not Record.

# Speaker routing doctrine

This file is the navigation and route-map layer over the canonical speaker memory shelf.

It does not replace the parent [`statecraft/voices/`](README.md). Speaker folders remain the durable accumulation layer for speaker objects, host-local arcs, helixes, cross-year notes, and routing notes. This doctrine should help agents decide what to open next, compare routes, and see cross-host reinforcement without moving interpretation out of the speaker folders.

For the storage-side SSOT and the canonical raw-input-side version of the wiring rule, see [provenance/README.md](../../README.md).

Speaker folders, year indexes, and lattice surfaces should implement this contract rather than restate it.

For the compact speaker-shelf naming table that this routing doctrine assumes, see [Speaker-Shelf Vocabulary](speaker-shelf-vocabulary.md).

## Layer Contract

- `raw-input/` = provenance
- `appearance` = one host/speaker/date/source event derived from verified raw-input
- `speaker arc` = host-local interpretation
- `speaker object` = durable speaker orientation
- `speaker helix` / cross-host note = comparative memory
- `speaker-routing-doctrine` = navigation, maps, adjacency, and open-first routes (this file)
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

## Route Contract {#route-contract}

Use the ladder this way:

- `core host lane` = the appearance belongs to a stable host transformation and should be entered through that host-local route surface
- `non-core appearance bench` = the appearance is valid and materialized, but does not belong to a stable host transformation
- `discovery memory` = the appearance is found, mentioned, or operator-pasted, but not yet materialized as raw-input

Governance rule:

- this file owns the route contract
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

This is the speaker-routing application of the repo's `Fullness Before Closure` doctrine: do not multiply index surfaces until the extra route is functionally necessary.

## Wiring Invariant

No valid speaker raw-input should remain unwired from the correct speaker surface.

That means:

- if a raw-input clearly belongs to a speaker's stable host transformation, wire it into the relevant `core host lane`
- if it is valid and materialized but does not belong to a stable host transformation, wire it into that speaker's `non-core appearance bench`
- if it is only found, mentioned, or partially pasted and not yet materialized as raw-input, keep it in `discovery memory` until it can be either materialized or discarded

An unwired valid raw-input is a routing defect.

Enforcement rule:

- do not treat a materialized capture as fully processed if routing doctrine cannot name its correct routed surface
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

The closeout owner is the routing stack, not storage. If this doctrine cannot name the correct routed surface, the task is not complete.

## Audit Posture

This file does not own provenance, but it does own the routing-side completion check after materialization.

Ask:

1. Which speaker surface exposes this capture now?
2. Is that surface a `core host lane` or a `non-core appearance bench`?
3. Is any item still sitting in `discovery memory` even though the raw-input has already been materialized?
4. Is the route complete for the touched speaker, or only mentioned in passing somewhere nearby?

If routing doctrine can name the speaker but not the correct routed surface, the work is not complete.

This file may point to speaker memory, but it is not the authority for speaker meaning. If a map table and a speaker object disagree, repair the map later.

## Host map {#host-map}

First-pass map of host shelves that carry host-local speaker arcs. Navigation aid, not a replacement for the arcs themselves.

### Active Host Shelves

| Host shelf | Role | Open first |
|---|---|---|
| [`alkhorshid/`](alkhorshid/) | Nima Alkhorshid voice shelf · cross-host guest · [Dialogue Works host](../channels/dialogue-works/dialogue-works-channel-index.md) | [`alkhorshid-profile.md`](alkhorshid/alkhorshid-profile.md) |
| [`davis/`](davis/) | Daniel Davis voice shelf · cross-host guest · [Deep Dive host](../channels/daniel-davis/daniel-davis-channel-index.md) | [`davis-thread.md`](davis/davis-thread.md) |
| [`diesen/`](diesen/) | Glenn Diesen host-local arcs | [`diesen-thread.md`](diesen/diesen-thread.md) |
| [`mercouris/`](mercouris/) | Alexander Mercouris stream shelf | [`mercouris-thread.md`](mercouris/mercouris-thread.md) |
| [`reason-resist/`](../channels/reason-resist/) | Reason to Resist · **Dimitri Lascaris host-only** (no `voices/lascaris/`) | [`reason-resist-channel-index.md`](../channels/reason-resist/reason-resist-channel-index.md) |
| [`napolitano/`](../channels/judging-freedom/) | Judging Freedom / Judge Andrew Napolitano host-local arcs | [`napolitano-thread.md`](../channels/judging-freedom/napolitano-thread.md) |

### Reading Rule

Use host shelves to preserve conversational form. A speaker can mean something different under different host pressure. Do not flatten `Napolitano x Freeman`, `Dialogue Works x Freeman`, and `Diesen x Freeman` into one generic Freeman note until the host-local arcs have been read.

### Maintenance Notes

- Add host shelves here only when they carry more than a one-off mini-branch and meet the real-continuity threshold.
- Prefer links to `*-thread.md` or a host README over direct raw-input lists.
- Let generated routing queues propose changes; update this map only after the operator accepts the underlying memory shape.

## Cross-host index {#cross-host-index}

Speakers whose usefulness is strengthened by more than one host surface. Quick map for cross-host reading, not a speaker dossier.

When a speaker's spread includes appearances outside the main host transformations, prefer the shared routing ladder:

- `core host lane`
- `non-core appearance bench`
- `discovery memory`

Do not solve those cases by repeatedly naming acceptable channels in doctrine prose if a bench/discovery split would be clearer.

### Cross-Host Candidates

| Speaker | Durable folder | Comparative surface | Host surfaces to compare |
|---|---|---|---|
| Freeman | [`freeman/index.md`](freeman/index.md) | [`arc-march-2026-cross-host-freeman-host.md`](../notes/arc-march-2026-cross-host-freeman-host.md) | Alkhorshid, Napolitano, Davis, Diesen, non-default March Iran-crisis channels where present |
| Johnson | [`johnson/`](johnson/) | [`johnson-helix.md`](johnson/johnson-helix.md) | Napolitano, Davis, Alkhorshid, Diesen where present |
| Kent | [`kent/`](kent/) | [`kent-helix.md`](kent/kent-helix.md) | Carlson, Davis, Diesen, Nawfal, Barnes quote-surface |
| Macgregor | [`macgregor/`](macgregor/) | [`macgregor-helix.md`](macgregor/macgregor-helix.md) | Napolitano, Davis, Diesen |
| Marandi | [`marandi/`](marandi/) | speaker object / host-local arcs | Alkhorshid, Davis, Diesen |
| Ritter | [`ritter/`](ritter/) | speaker object / host-local arcs | Alkhorshid, Napolitano, Davis, Diesen |
| Wilkerson | [`wilkerson/`](wilkerson/) | [`wilkerson-helix.md`](wilkerson/wilkerson-helix.md) | Napolitano, Alkhorshid |

### Use

Open this section when the question is not "what did one host do with this speaker?" but "what changes as this speaker moves across hosts?"

Good follow-up targets:

- a helix note needs a stronger pair comparison
- a speaker object needs an `object_shape` update
- a host-local arc has enough appearances to become the open-first route
- the speaker-memory action queue proposes `consider-helix`

### Boundary

Do not use this index to make cross-host claims unsupported by speaker folders or raw-input appearances. When in doubt, route the uncertainty back to the speaker object or helix as an operator-reviewable proposal.

## Open-first routes {#open-first-routes}

Fast entry paths through speaker routing. Useful first openings, not a ranked canon.

### Default Route

1. Open the relevant speaker folder under [`statecraft/voices/`](README.md) or host folder under [`statecraft/channels/`](../channels/).
2. Read the `*-speaker-object.md` if present.
3. If the folder exposes a bare `*-thread.md`, do not assume it is a canonical topical thread; check whether it is a legacy continuity surface or a true topic-suffixed thread.
4. If the question is host-specific, open the matching `host x speaker` arc.
5. If the question is cross-host, ask whether the speaker already has a routing ladder:
   `core host lane` / `non-core appearance bench` / `discovery memory`.
6. Open the helix or cross-host note when the question is comparative across stable host transformations.
7. Use raw-input only when provenance or transcript details matter.
8. If the question is explicitly `speaker A versus speaker B`, check whether a cross-speaker compare note already exists under [`../notes/`](../notes/).

### Route Types

| Need | Open first | Then |
|---|---|---|
| "Who is this speaker in the Codex?" | speaker object | best host-local arc |
| "What does this host do with this guest?" | host-local speaker arc | raw-input appearances |
| "What changes across hosts?" | helix or cross-host note | two strongest host-local arcs |
| "Where do non-main-stream but accepted appearances go?" | non-core appearance bench | speaker object or helix |
| "Where do found-but-not-materialized appearances stay?" | discovery memory | materialize or discard later |
| "What should daily ingest update?" | speaker-memory action queue | target speaker arc/object |
| "Where did this come from?" | raw-input | appearance ledger |

### Ladder Rule

When a speaker has enough cross-host spread that routing keeps naming exceptions, normalize it into this ladder:

- `core host lane`: stable host transformation with its own arc
- `non-core appearance bench`: accepted transcript-bearing appearances outside those lanes
- `discovery memory`: found or operator-pasted appearances that remain routing memory only

This should be the default doctrine for all speakers once the problem exists, not a Freeman-only special case.

### Compatibility Rule

Many shelves still carry older `*-thread.md` files that function as distilled continuity or journaled companion surfaces.

- Treat canonical topical threads as files shaped like `<speaker>-thread-<topic>.md`.
- Treat bare `*-thread.md` files as compatibility surfaces unless the local shelf explicitly upgrades them into the newer grammar.
- Do not infer thread multiplicity or thread orthogonality merely from the existence of one legacy `*-thread.md`.
- When opening a compatibility `*-thread.md`, expect it to route you upward to the canonical arc, helix, thread atlas, or light profile-first surface rather than acting as an equal thread authority.

Many host shelves also still carry older relational-arc filenames in the form `<host>-<speaker>-speaker-arc.md`.

- Treat canonical relational arcs as files shaped like `<host>-<speaker>-arc.md`.
- Treat `*-speaker-arc.md` files as compatibility spellings unless the local shelf clearly uses them as the only embodied relational surface.
- If both spellings exist, prefer the canonical `*-arc.md` file and treat the `*-speaker-arc.md` file as an alias rather than a second arc.

### Wiring Standard

Treat valid-but-unwired speaker raw-input as a defect.

- A valid materialized raw-input should always land either in a `core host lane` or the speaker's `non-core appearance bench`.
- `discovery memory` is only for not-yet-materialized appearances, not for leaving real raw-input stranded.
- If a daily ingest or cleanup pass finds a valid speaker raw-input that is not visible from the correct speaker surface, the next routing move should repair that.

### Current High-Value Paths

- Napolitano densification: open [`../notes/`](../notes/), then Freeman, Johnson, Macgregor arcs.
- Freeman: open [`freeman/index.md`](freeman/index.md), then the March cross-host arc or matching host-local arc.
- Dialogue Works x Freeman: open [`../notes/arc-freeman-nima-host.md`](../notes/arc-freeman-nima-host.md), then [`freeman/freeman-march-2026-cross-host-arc.md`](freeman/freeman-march-2026-cross-host-arc.md) if the question crosses hosts.
- Davis x Barnes: open [`../notes/arc-barnes-davis-host.md`](../notes/arc-barnes-davis-host.md), then the Barnes speaker folder if it exists.

### Boundary

Open-first routes are allowed to be practical and provisional. They should be repaired when action queues, speaker objects, or host arcs show that another path has become more useful.

## Update Rule

Use this doctrine after materialization and routing:

1. Verify raw-input exists and is non-stub.
2. Build appearances and route stacks.
3. Review the speaker-memory action queue.
4. Update speaker objects, arcs, or helixes only when explicitly approved.
5. Update host map, cross-host index, and open-first routes after the underlying speaker memory path is clear.

Before considering routing complete, check that every valid speaker raw-input touched by the task has landed in the correct speaker path. If it has not, the work is still incomplete.

If the capture is still stranded in storage, discovery memory, or a thin mention-only surface, the correct closeout is `routing still open`, not `done`.

Do not auto-edit this file from daily ingest unless the operator asks for that follow-up.
