# Prose Index

work only; not Record.

This is the canonical chooser for repo-root prose output classes.

Use it when the question is not yet "which file?" but rather "what kind of prose object do I need?"

If a shelf README and this index ever seem to compete, this index wins on prose-class routing and the shelf README should be read as the **canonical local entrypoint** for that shelf.

For one compact live comparison of how cluster behavior changes across `essays/`, `notes/`, and `docs/skill-work/`, see [prose-cluster-placement-comparison.md](/C:/dev/strategy-codex/docs/prose-cluster-placement-comparison.md).

## Core Split

`notes/` and `essays/` are first-class prose output classes. They are not doctrine, not sheets, not bridges, not transactions, not journals, and not source archives.

- `notes/` preserve **bounded interpretive objects**
- `essays/` carry **stand-alone synthesized arguments**

`synthesis/` is adjacent but different. It is a domain-specific extraction layer, not a general prose class. In practice:

- use `synthesis/` when the main job is month-scale extraction from a canonical source spine
- use `notes/` or `essays/` when the result has become a reusable prose object in its own right

Fast distinction:

- if the object is one seam, mechanism, route question, audit, comparison, or promoted local insight, open a **note**
- if the object has become a thesis that should travel on its own, open an **essay**

Speaker-shelf carveout:

- `statecraft/civ-lens/` is a continuity-and-retrieval layer, not a general prose shelf
- speaker-derived bounded prose should route to `notes/` once it becomes reusable beyond shelf support
- speaker-derived thesis-bearing prose should route to `essays/`

Short boundary rule: `source-lattice` governs retrieval order; prose-index
doctrine governs prose-class placement.

## Quick Placement Rule

Use this order:

1. If the object is still month-scale extraction from a live source spine, use the domain's `synthesis/` layer.
2. If the object is reusable but still bounded to one seam, mechanism, route question, audit, or comparison, use `notes/`.
3. If the object now carries a stand-alone thesis that should travel outside the original routing context, use `essays/`.
4. If it is actually doctrine, a kernel, a sheet, a bridge, a transaction, or an archive object, do not force it into a prose shelf.

For speaker-derived objects, apply one extra test:

- if the file mainly helps you understand or enter a speaker, keep it in the speaker shelf
- if the file is now a reusable bounded prose destination, route it to `notes/`
- if the file has become a transportable stand-alone argument, route it to `essays/`

## When To Open A Note

Open a note when you need:

- a bounded seam
- a mechanism packet
- a route or threshold distinction
- an audit-shaped interpretive object
- a comparison that should stay local rather than widen into doctrine

Notes usually preserve one reusable object without pretending to become the final argument above it.

## When To Open An Essay

Open an essay when you need:

- a thesis-bearing stand-alone argument
- a broader framing document
- a synthesis that rises above one local seam
- a prose output that can travel without depending on the original routing context

Essays should carry the argument, not just point toward it.

Some essays are also **evidence-bearing research syntheses**. When claim
density is high and the evidence base is heterogeneous, prefer:

- a support cluster
- an evidence matrix
- a short evidence posture near the end of the essay

## Canonical Routes

Need a **bounded interpretive object**:

- statecraft route / mechanism / comparison / audit / threshold object -> [statecraft notes](/C:/dev/strategy-codex/statecraft/notes/README.md)
- singularity promoted seam / substrate / control-plane / source-hygiene object -> [singularity notes](/C:/dev/strategy-codex/singularity/notes/README.md)

Need a **thesis-bearing synthesized argument**:

- statecraft framing or cross-lane argument -> [statecraft essays](/C:/dev/strategy-codex/statecraft/essays/README.md)
- singularity thesis about agency, acceleration, substrate, alignment, labor, or authority -> [singularity essays](/C:/dev/strategy-codex/singularity/essays/README.md)

Need a **month-scale extraction layer rather than a prose shelf**:

- singularity month-scale source extraction -> [singularity synthesis](/C:/dev/strategy-codex/singularity/synthesis/README.md)
- statecraft day/month archive compression -> [statecraft daily synthesis](/C:/dev/strategy-codex/statecraft/daily/README.md)

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

- shelf READMEs are the canonical entrypoints for their local prose shelves
- some shelf contents remain mirrored compatibility material while taxonomy settles
- prefer `shelf-native` items and README-curated entry points over assuming every file inside a shelf is equally canonical prose authority

Later cleanup may remove or rewrite some mirrored or review-needed items, but this index should remain stable because it routes through shelf authority first rather than through raw folder contents.

For the preferred citation pattern for literature-backed notes and essays, open
[citation-evidence-pattern.md](/C:/dev/strategy-codex/docs/citation-evidence-pattern.md).
