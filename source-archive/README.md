# Source Archive

WORK only; not Record.

This is the repo-root canonical full-source layer shared by the live top-level systems.

It exists partly to stop namespace relapse: new source work should not be framed through legacy `strategy-notebook`, `raw-input`, or `codex` ownership assumptions when the live consumers are repo-root `statecraft/` and `singularity/`.

Direct consumer namespaces:

- `source-archive/statecraft/` for statecraft-facing dated source capture
- `source-archive/singularity/` for singularity-facing full source capture

Archive law:

- `source-archive/` stores full source objects only
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
