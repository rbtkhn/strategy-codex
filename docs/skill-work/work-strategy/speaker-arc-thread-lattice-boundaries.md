# Speaker Arc vs Thread vs Lattice Row


If you only half-remember the `speaker arc` stack, start here. This is the fastest re-entry point because it tells you which notebook object you are actually looking for.

This note distinguishes three notebook objects that are adjacent but not interchangeable:

- **speaker arc**
- **thread**
- **lattice row**

The short rule is:

- **speaker arc** = why a recurring host x guest run matters
- **thread** = who said what over time
- **lattice row** = who this recurring figure is in the notebook

## One-line distinctions

| Object | Primary question | Main job | Typical location |
|---|---|---|---|
| **Speaker arc** | Why does this recurring host x guest lane matter? | Compact stream-local reuse note for future routing | `codex/<year>/<host-stream>/<host>-<guest>-speaker-arc.md` |
| **Thread** | What did this named voice say across dates? | Provenance join and continuity lane | `thread:<expert_id>` in inbox plus thread/transcript surfaces |
| **Lattice row** | Who is this recurring speaker in the notebook? | Alphabetical roster identity and cross-stream lookup | [speaker-lattice.md](../../../codex/speaker-lattice.md) |

## Speaker arc

A **speaker arc** is a compact host-stream note about a recurring guest run.

Use it when the notebook needs:

- a ranked arc set
- an open-first recommendation
- a paired-read recommendation
- a concise statement of what this guest lane is good for
- a boundary statement about what it is not good for

A speaker arc is:

- **stream-local**
- interpretive
- compact
- downstream of raw-input accumulation

A speaker arc is not:

- a provenance ledger
- a roster entry by itself
- a new ontology shelf
- a substitute for raw-input or thread continuity

## Thread

A **thread** is the continuity and provenance join for a named voice.

Use it when the notebook needs:

- date-separated accumulation
- drift or pivot detection
- grep-friendly routing from `daily-strategy-inbox.md`
- machine-assisted extraction and continuity

A thread is:

- keyed by **`thread:<expert_id>`**
- longitudinal
- provenance-bearing
- script-aware

A thread is not:

- a ranking note
- a compact lane summary
- a host x guest arc by itself

If a shared episode contains both host and guest value, the thread layer still tracks the named speaker via `thread:<expert_id>`. The speaker arc sits above that layer and explains why the repeated host x guest run is worth caring about.

## Lattice row

A **lattice row** is the notebook's stable roster identity for a recurring speaker.

Use it when the notebook needs:

- alphabetical lookup
- a one-line role note
- cross-stream positioning
- a quick jump to thread or speaker-arc surfaces

A lattice row is:

- sparse
- roster-like
- cross-stream
- identity-oriented

A lattice row is not:

- the full continuity object
- a ranked reading path
- a place to restate the whole lane every time

## How they relate

The normal relationship is:

1. **Raw-inputs** accumulate.
2. **Threads** carry dated continuity and provenance.
3. **Speaker arcs** compress the recurring host x guest lane into a reusable routing note.
4. **Lattice rows** point at the right deeper surfaces without re-explaining them.

That means a lattice row may cite a speaker arc, but it does not become one. A thread may feed a speaker arc, but it does not replace one.

## Routing rule

If the question is:

- **"Who is this recurring figure?"** -> open the **lattice row**
- **"What has this voice been saying over time?"** -> open the **thread**
- **"Why does this recurring host x guest run matter, and where should I start?"** -> open the **speaker arc**

## Common mistakes

- Treating a speaker arc as if it were the provenance source.
- Treating a thread as if it were already a ranked reading note.
- Stuffing too much lane explanation into the lattice row.
- Inventing a new shelf when a stream-local speaker arc is enough.
- Using `thread:<expert_id>` as if it were a worldview label rather than a routing join.

## Default hierarchy

When all three exist:

- **lattice row** = shortest identity layer
- **thread** = continuity layer
- **speaker arc** = compact interpretive lane layer

That hierarchy should keep future routing clean.

## Further gloss

If you want the philosophical layer rather than the structural distinction, read [speaker-arc-conversational-form.md](speaker-arc-conversational-form.md).

If you need the boundary between `speaker arc` host-locality and raw-input ingest ownership, read [raw-input-ownership-vs-speaker-arc.md](raw-input-ownership-vs-speaker-arc.md).
