# Open-First Routes

WORK only; not Record.

This file gives agents fast entry paths through the speaker map. It is a map of useful first openings, not a ranked canon.

## Default Route

1. Open the relevant speaker folder under [`codex/speakers/`](../).
2. Read the `*-speaker-object.md` if present.
3. If the question is host-specific, open the matching `host x speaker` arc.
4. If the question is cross-host, ask whether the speaker already has a routing ladder:
   `core host lane` / `non-core appearance bench` / `discovery memory`.
5. Open the helix or cross-host note when the question is comparative across stable host transformations.
6. Use raw-input only when provenance or transcript details matter.

## Route Types

| Need | Open first | Then |
|---|---|---|
| "Who is this speaker in the Codex?" | speaker object | best host-local arc |
| "What does this host do with this guest?" | host-local speaker arc | raw-input appearances |
| "What changes across hosts?" | helix or cross-host note | two strongest host-local arcs |
| "Where do non-main-stream but accepted appearances go?" | non-core appearance bench | speaker object or helix |
| "Where do found-but-not-materialized appearances stay?" | discovery memory | materialize or discard later |
| "What should daily ingest update?" | speaker-memory action queue | target speaker arc/object |
| "Where did this come from?" | raw-input | appearance ledger |

## Ladder Rule

When a speaker has enough cross-host spread that routing keeps naming exceptions, normalize it into this ladder:

- `core host lane`: stable host transformation with its own arc
- `non-core appearance bench`: accepted transcript-bearing appearances outside those lanes
- `discovery memory`: found or operator-pasted appearances that remain routing memory only

This should be the default doctrine for all speakers once the problem exists, not a Freeman-only special case.

## Wiring Standard

Treat valid-but-unwired speaker raw-input as a defect.

- A valid materialized raw-input should always land either in a `core host lane` or the speaker's `non-core appearance bench`.
- `discovery memory` is only for not-yet-materialized appearances, not for leaving real raw-input stranded.
- If a daily ingest or cleanup pass finds a valid speaker raw-input that is not visible from the correct speaker surface, the next routing move should repair that.

## Current High-Value Paths

- Napolitano densification: open [`../napolitano/`](../napolitano/), then Freeman, Johnson, Macgregor arcs.
- Freeman: open [`../freeman/index.md`](../freeman/index.md), then the March cross-host arc or matching host-local arc.
- Dialogue Works x Freeman: open [`../alkorshid/stream/alkorshid-freeman-speaker-arc.md`](../alkorshid/stream/alkorshid-freeman-speaker-arc.md), then [`../freeman/freeman-march-2026-cross-host-arc.md`](../freeman/freeman-march-2026-cross-host-arc.md) if the question crosses hosts.
- Davis x Barnes: open [`../davis/stream/davis-barnes-speaker-arc.md`](../davis/stream/davis-barnes-speaker-arc.md), then the Barnes speaker folder if it exists.

## Boundary

Open-first routes are allowed to be practical and provisional. They should be repaired when action queues, speaker objects, or host arcs show that another path has become more useful.
