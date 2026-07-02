# Source Archive

This is the repo-root canonical **source-truth** layer shared by the live top-level systems.

It exists partly to stop namespace relapse: new source work should not be framed through legacy `strategy-notebook`, `raw-input`, or `codex` ownership assumptions when the live consumers are repo-root `statecraft/` and `singularity/`.

This folder is distinct from root [`archive/`](../archive/README.md):

- `source-archive/` stores canonical full source objects meant for active downstream use
- `archive/` stores preserved non-live holdings, freezes, and legacy residues

At the repo-root level, the stack is:

- [`archive/`](../archive/README.md) for preserved legacy snapshots and non-live holdings
- `source-archive/` for canonical full-source capture intended for active downstream use
- [`continuity/`](../continuity/README.md) for chronology, accumulation, and continuity (legacy redirect: [`codex/`](../codex/README.md))
- [`statecraft/`](../statecraft/README.md) and [`singularity/`](../singularity/README.md) for live interpretation, routing, synthesis, notes, essays, and downstream judgment

Direct consumer namespaces:

- `source-archive/statecraft/` for statecraft-facing dated source capture
- `source-archive/singularity/` for singularity-facing full source capture

Archive law:

- `source-archive/` stores full source objects only
- `archive/` stores preserved non-live holdings only
- `statecraft/` consumes `source-archive/statecraft/...` for routing, continuity, and drafting
- `singularity/` consumes `source-archive/singularity/...` for workshop and academy synthesis

What belongs here:

- full transcripts
- cleaned transcripts
- operator-pasted full captures
- source-first essays, newsletters, and posts
- workshop-native full source captures

What does not belong here:

- routing notes
- bridge adapters
- continuity shelves
- control sheets
- transaction drafts
- workshop synthesis

Those downstream surfaces belong under `statecraft/` or `singularity/` by constitutional role.
