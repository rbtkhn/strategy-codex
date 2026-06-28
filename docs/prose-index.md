# Prose Index

work only; not Record.

This is the canonical chooser for repo-root prose output classes.

Use it when the question is not yet "which file?" but rather "what kind of prose object do I need?"

If a shelf README and this index ever seem to compete, this index wins on prose-class routing and the shelf README should be read as the **canonical local entrypoint** for that shelf.

For one compact live comparison of how cluster behavior changes across `essays/`, `notes/`, and `docs/skill-work/`, see [prose-cluster-placement-comparison.md](prose-cluster-placement-comparison.md).

## Core Split

`notes/` and `essays/` are first-class prose output classes. They are not doctrine, not sheets, not bridges, not transactions, not journals, and not source archives.

- `notes/` preserve **bounded interpretive objects** — channel-scoped only (`statecraft/notes/`, `singularity/notes/`)
- `essays/` carry **stand-alone synthesized arguments** — **primary shelf:** repo-root [`essays/`](../essays/README.md); channel `*/essays/` folders are compatibility holdings for pre-root material

`synthesis/` is adjacent but different. It is a domain-specific extraction layer, not a general prose class. In practice:

- use `synthesis/` when the main job is month-scale extraction from a canonical source spine
- use `notes/` or `essays/` when the result has become a reusable prose object in its own right

Fast distinction:

- if the object is one seam, mechanism, route question, audit, comparison, session-governance contract, or promoted local insight, open a **note**
- if the object has become a thesis that should travel on its own, open an **essay**

Speaker-shelf carveout:

- `statecraft/voices/` is a continuity-and-retrieval layer, not a general prose shelf
- speaker-derived bounded prose should route to `notes/` once it becomes reusable beyond shelf support
- speaker-derived thesis-bearing prose should route to repo-root [`essays/`](../essays/README.md)

Short boundary rule: `source-lattice` governs retrieval order; prose-index
doctrine governs prose-class placement.

## Quick Placement Rule

Use this order:

1. If the object is still month-scale extraction from a live source spine, use the domain's `synthesis/` layer.
2. If the object is reusable but still bounded to one seam, mechanism, route question, audit, or comparison, use `notes/`.
   This also covers compact session-governance or operating-contract notes that remain local prose objects rather than doctrine.
3. If the object now carries a stand-alone thesis that should travel outside the original routing context, use repo-root [`essays/`](../essays/README.md) (including cross-channel theses).
4. If it is actually doctrine, a kernel, a sheet, a bridge, a transaction, or an archive object, do not force it into a prose shelf.

For speaker-derived objects, apply one extra test:

- if the file mainly helps you understand or enter a speaker, keep it in the speaker shelf
- if the file is now a reusable bounded prose destination, route it to `notes/`
- if the file has become a transportable stand-alone argument, route it to repo-root [`essays/`](../essays/README.md)

## When To Open A Note

Open a note when you need:

- a bounded seam
- a mechanism packet
- a route or threshold distinction
- an audit-shaped interpretive object
- a comparison that should stay local rather than widen into doctrine
- a compact operating or session-governance contract that should remain below doctrine

Notes usually preserve one reusable object without pretending to become the final argument above it.

## When To Open An Essay

Open an essay when you need:

- a thesis-bearing stand-alone argument
- a broader framing document
- a synthesis that rises above one local seam
- a prose output that can travel without depending on the original routing context

Essays should carry the argument, not just point toward it.

**Essay voice (how essays sound):** [essay-voice.md](essay-voice.md) — tri-blend transport synthesis, light apparatus (Band A default). When promoting from a note, **compress apparatus**; do not copy note pin-cite density into the essay body.

Example cross-channel entries on the primary shelf: [from-accumulation-to-governed-interpretive-machine.md](../essays/from-accumulation-to-governed-interpretive-machine.md), [ai-and-the-expansion-of-human-consciousness.md](../essays/ai-and-the-expansion-of-human-consciousness.md) — full index at [essays/README.md](../essays/README.md).

Some essays are also **evidence-bearing research syntheses**. When claim
density is high and the evidence base is heterogeneous, prefer:

- a support cluster
- an evidence matrix
- a short evidence posture near the end of the essay

## Canonical Routes

Need a **thesis-bearing synthesized argument**:

- **primary (default)** — cross-channel or stand-alone essay -> [essays](../essays/README.md) at repo root
- statecraft-heavy legacy holdings -> [statecraft essays](../statecraft/essays/README.md) (compatibility; migrate to root `essays/` in bounded passes)
- singularity-heavy legacy holdings -> [singularity essays](../singularity/essays/README.md) (compatibility; migrate to root `essays/` in bounded passes)

Need a **bounded interpretive object** (channel-scoped only — do not split across channels at note layer):

- statecraft route / mechanism / comparison / audit / threshold object -> [statecraft notes](../statecraft/notes/README.md)
- singularity promoted seam / substrate / control-plane / source-hygiene object -> [singularity notes](../singularity/notes/README.md)

Need a **month-scale extraction layer rather than a prose shelf**:

- singularity month-scale source extraction -> [singularity synthesis](../singularity/synthesis/README.md)
- statecraft day/month archive compression -> [state synthesis](../README.md)

## What These Shelves Are Not

Do not confuse prose shelves with:

- **doctrine**: kernels, constitutional notes, and method owners
- **patterns**: reusable laws extracted from recursive learning
- **journals**: chronological learning or continuity logs
- **sheets**: operating passes, workshop scaffolds, or compact execution surfaces
- **bridges**: routing or retrieval-conditioning systems
- **transactions**: reusable statecraft instruments
- **source archives**: canonical full-source preservation layers

They are also not:

- **legacy compatibility lanes**: older surfaces such as `docs/skill-work/work-strategy/` may still hold useful doctrine, but they are not canonical prose-shelf owners
- **constitutional kernels**: files like `statecraft/statecraft.md` or root domain READMEs may contain strong prose without thereby becoming essay shelves

## Stability Note

This index points to shelf roles and canonical entry surfaces first.

Stability rule:

- repo-root [`essays/README.md`](../essays/README.md) is the canonical entrypoint for new thesis-bearing prose
- channel `notes/` READMEs remain canonical for channel-scoped bounded objects
- channel `*/essays/` READMEs index compatibility holdings only until bounded migration
- prefer `shelf-native` items and README-curated entry points over assuming every file inside a shelf is equally canonical prose authority

Later cleanup may remove or rewrite some mirrored or review-needed items, but this index should remain stable because it routes through shelf authority first rather than through raw folder contents.

For the preferred citation pattern for literature-backed notes and essays, open
[citation-evidence-pattern.md](citation-evidence-pattern.md).
