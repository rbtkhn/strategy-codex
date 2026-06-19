# Current Machine Map - 2026-06-01

work only; not Record.

This is a human-readable map of the current `strategy-codex` machine.

Use it on cold re-entry when you do not need every doctrine surface back in your
head at once. The goal is to answer:

```text
what are the main layers,
what is each one for,
and where should I go next?
```

## The Short Map

The current machine has six main layers:

1. `source-archive/` - preserves source truth
2. `statecraft/` and `singularity/` - turn source and reasoning into reusable interpretation
3. membrane law - says what class of artifact something is allowed to be
4. prose routing - says where prose objects belong once they exist
5. validators and audits - test the parts stable enough to check
6. recursive learning - records what the machine has learned about improving itself

If you only remember one thing, remember this:

```text
archive preserves
domains interpret
membrane governs
prose routes
validators test
recursive learning improves
```

## Layer 1: Archive

The archive layer is where source truth is supposed to stay closest to the
thing itself.

Main path:

- [source-archive/](/C:/dev/strategy-codex/source-archive/README.md)

Important split:

- `archive/` = preserved legacy snapshots and older freezes
- `source-archive/` = canonical full-source capture layer for live downstream use

What this layer does:

- stores transcript-bearing or source-bearing objects
- preserves provenance and day/month inventories
- gives downstream interpretation something stable to stand on

What it does **not** do:

- make the final judgment
- carry the main interpretive thesis
- decide prose class

If the source floor is noisy, the whole machine inherits that noise later.

## Layer 2: Domain Interpretation

This is where the repo turns material into reusable judgment.

Main paths:

- [statecraft/](/C:/dev/strategy-codex/statecraft/README.md)
- [singularity/](/C:/dev/strategy-codex/singularity/README.md)

### `statecraft`

`statecraft` is the machine for **bounded analytical objects**.

Typical outputs:

- daily synthesis notes
- monthly synthesis notes
- companion notes
- mechanism comparisons
- lane notes
- bridge and civ-state retrieval surfaces

Its main question is:

```text
what is the object?
```

### `singularity`

`singularity` is the machine for **bounded architectural doctrine**.

Typical outputs:

- notes
- essays
- synthesis shelves
- design and substrate doctrine

Its main question is:

```text
what is the system?
```

## Layer 3: Membrane Law

The membrane answers a harder question:

```text
what kind of thing is this artifact allowed to be?
```

Main paths:

- [docs/work-membrane-v2.md](/C:/dev/strategy-codex/docs/work-membrane-v2.md)
- [statecraft/work-membrane.md](/C:/dev/strategy-codex/statecraft/work-membrane.md)
- [singularity/work-membrane.md](/C:/dev/strategy-codex/singularity/work-membrane.md)

The key classes are:

- `Record`
- `governed adjacent`
- `instrumental work`
- `runtime / derived`
- `external complements`

Why this matters:

before this layer hardened, many surfaces were only described negatively as
"not Record."

Now the repo can distinguish:

- durable but non-Record synthesis
- active work surfaces
- rebuildable helper outputs
- transport or interop bundles

That makes the machine more honest and easier to maintain.

## Layer 4: Prose Routing

The prose router answers:

```text
what kind of prose object do I need?
```

Main path:

- [docs/prose-index.md](/C:/dev/strategy-codex/docs/prose-index.md)

The key split is:

- `notes/` = bounded interpretive objects
- `essays/` = stand-alone synthesized arguments
- `synthesis/` = month-scale extraction layer, not a general prose class

Why this matters:

without a shared prose chooser, every local README starts quietly inventing its
own taxonomy. That creates hesitation, duplicate law, and drift.

The current rule is:

```text
centralize class law
localize shelf flavor
```

## Layer 5: Validators And Audits

These are the surfaces that ask:

```text
which parts of the machine are now stable enough to test?
```

Examples:

- state synthesis validator
- civ-state validators
- transcript audit and repair scripts
- speaker trust or accuracy audits

What they do:

- catch regressions
- make structural contracts explicit
- reduce the amount of quality control that lives only in operator memory

What they do **not** do:

- replace judgment
- prove every interpretive claim
- decide truth in domains that are still too fluid for deterministic checks

## Layer 6: Recursive Learning

This is the layer where the machine learns from its own use.

Main path:

- [statecraft/recursive-learning-journal.md](/C:/dev/strategy-codex/statecraft/recursive-learning-journal.md)

This layer asks:

```text
what reusable law did one object, seam, or failure teach us,
and where did we apply it elsewhere?
```

Examples of what it has learned from:

- speaker and corpus patterns
- source-stack difficulty
- instruction drift
- phase shifts in how the machine itself is developing

This is what makes the repo more than:

- a source archive
- a set of notes
- a pile of doctrine

It is how the machine improves its own interpretive structure over time.

## How The Layers Fit Together

Here is the simplest current flow:

```text
source truth
-> domain interpretation
-> membrane classification
-> prose routing
-> validation where possible
-> recursive learning from the result
```

And here is the most important correction to that simple flow:

```text
later layers do not make earlier layers less important
they make them more important
```

Once the upper layers become more exact, noise in the archive floor matters
more, not less.

## Best Cold Re-Entry Paths

If you are cold and want the fastest honest path back in:

### For domain judgment

- open [statecraft/README.md](/C:/dev/strategy-codex/statecraft/README.md)
- or [singularity/README.md](/C:/dev/strategy-codex/singularity/README.md)

### For artifact class confusion

- open [docs/work-membrane-v2.md](/C:/dev/strategy-codex/docs/work-membrane-v2.md)

### For prose placement confusion

- open [docs/prose-index.md](/C:/dev/strategy-codex/docs/prose-index.md)

### For "what has the machine learned lately?"

- open [statecraft/recursive-learning-journal.md](/C:/dev/strategy-codex/statecraft/recursive-learning-journal.md)

### For the broader recent shift in plain language

- open [essays/from-accumulation-to-governed-interpretive-machine.md](/C:/dev/strategy-codex/essays/from-accumulation-to-governed-interpretive-machine.md)

## The Current Weak Flank

The cleanest architecture pressure point right now is this:

```text
the governance and routing layers have advanced faster than part of the archive substrate
```

Use the dedicated companion surfaces when that seam is the real object:

- [Archive Truth-Floor Repair Routing](/C:/dev/strategy-codex/statecraft/notes/archive-truth-floor-repair-routing-2026-06-01.md) for tranche shape and opening order
- [Why Archive Truth Now Matters More](/C:/dev/strategy-codex/docs/why-archive-truth-now-matters-more-2026-06-01.md) for the plain-language consequence

## One Sentence Summary

`strategy-codex` currently works as a layered machine that preserves source
truth, turns it into reusable interpretation, governs artifact class and prose
placement, validates stable contracts, and then learns from its own successes
and failures so the next pass is cleaner than the last.
