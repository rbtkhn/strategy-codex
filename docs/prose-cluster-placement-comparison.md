# Prose Cluster Placement Comparison

This is a small live comparison note for one recurring placement question:

`how should a doctrine cluster behave differently when it lives in essays/, notes/, or docs/skill-work/?`

The goal is not to create a new taxonomy. The goal is to make future placement decisions faster.

**Primary essay shelf (2026-06):** repo-root [`essays/`](../essays/README.md). Channel `*/essays/` folders are compatibility holdings; notes remain channel-scoped only.

## Core Distinction

The same subject can appear in all three places, but it should behave differently in each one:

- repo-root [`essays/`](../essays/README.md) (primary) or channel `*/essays/` (compatibility) carries the **thesis-bearing owner**
- `singularity/notes/` carries the **bounded promoted object**
- `docs/skill-work/` carries the **operator doctrine or legacy compatibility layer**

If one file is trying to do all three jobs at once, the placement is probably wrong.

## 1. When A Cluster Lives In repo-root `essays/`

Here the cluster exists to support a carriage-bearing argument.

What should be true:

- the main essay can stand on its own
- support notes exist to keep the main essay cleaner, not to replace it
- the cluster is subordinate to a thesis-bearing surface above it
- return paths point upward to the main essay and sideways to the essay shelf

What should not be true:

- the cluster is treated like active workshop procedure
- the support notes behave like open-ended accumulation bins
- the essay depends on local routing lore to make sense

Live example:

- [essays/interpretive-machine.md](../essays/interpretive-machine.md)
- [essays/interpretive-machine/README.md](../essays/interpretive-machine/README.md)

The interpretive-machine cluster now behaves correctly here. The essay owns the transportable claim. The cluster holds lineage, workflow proof, and product extrapolation without pretending to become the main argument.

## 2. When A Cluster Lives In `singularity/notes/`

Here the object is promoted and reusable, but still bounded.

What should be true:

- the note preserves one seam, mechanism, packet, or promoted local argument
- the note still depends somewhat on the originating month, sheet, or route
- the local shelf explains the singularity-specific version of note-class behavior
- promotion to essay remains a real future threshold rather than a rhetorical flourish

What should not be true:

- the note claims broader thesis authority than it can honestly carry
- the note becomes a hidden essay because no one wants to promote it properly
- the note tries to become a doctrine owner

Live examples:

- [singularity/notes/compute-political-currency-control-plane-substrate.md](../singularity/notes/compute-political-currency-control-plane-substrate.md)
- [singularity/notes/may-2026-control-plane-compression.md](../singularity/notes/may-2026-control-plane-compression.md)

These are reusable, but they are still bounded promoted seams rather than stand-alone theses.

## 3. When A Cluster Lives In `docs/skill-work/`

Here the object is not primarily a prose shelf item at all.

What should be true:

- the file helps the operator work
- the file may contain doctrine, procedure, compatibility residue, or transition logic
- the file can remain useful without claiming canonical prose ownership
- if a stronger canonical home appears elsewhere, this layer should degrade gracefully into pointer, redirect, or operator-only support

What should not be true:

- the file silently continues owning a concept after that concept has been re-homed
- a legacy lane is mistaken for the canonical prose shelf because the writing is strong
- compatibility residue and live ownership stay mixed for too long

Live example:

- [docs/skill-work/work-strategy/README.md](skill-work/work-strategy/README.md)

The recent interpretive-machine relocation is the model case. Once the cluster had a real singularity essay home, the old `work-strategy` files no longer needed to own the doctrine. Their honest role became compatibility redirects.

## Fast Placement Test

Ask these in order:

1. Is this object mainly helping the operator work, route, or preserve compatibility?
   If yes, it probably belongs in `docs/skill-work/`.
2. Is it a reusable but still bounded seam, packet, comparison, or promoted local argument?
   If yes, it probably belongs in `notes/`.
3. Is it now a stand-alone thesis that should travel outside the original route?
   If yes, it probably belongs in `essays/`.

If the answer changes over time, move the object and let the old home become thinner rather than pretending all homes are equally canonical.

## Best Short Rule

Use this compression:

```text
essays own transportable arguments
notes own bounded promoted objects
docs/skill-work owns operator doctrine, procedure, and compatibility residue
```

## Return Path

- Return to [Prose Index](prose-index.md) for the canonical class chooser.
- Return to [Essays (repo root)](../essays/README.md) for the primary thesis-bearing essay shelf.
- Return to [Singularity Essays](../singularity/essays/README.md) for singularity compatibility essay holdings.
- Return to [Singularity Notes](../singularity/notes/README.md) for bounded promoted singularity objects.
