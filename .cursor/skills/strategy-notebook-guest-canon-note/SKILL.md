---
name: strategy-notebook-guest-canon-note
preferred_activation: speaker arc
description: Create a host-stream guest speaker arc from repeated host x guest raw inputs: rank the key episodes, explain the lane, place the note inside the host stream, and wire lattice or thread surfaces to cite it without inventing a new category.
portable: true
version: 0.2.0
tags:
- operator
- strategy-codex
- strategy-notebook-legacy
- speaker-arc
- guest-lane
portable_source: skills-portable/strategy-notebook-guest-canon-note/SKILL.md
synced_by: sync_portable_skills.py
---
# Strategy-codex guest speaker arc

**Preferred activation (operator):** say **`speaker arc`**.

**Compatibility note:** The portable skill slug remains `strategy-notebook-guest-canon-note` for manifest and sync stability. In live strategy-codex language, use **speaker arc**; `strategy-notebook` is legacy compatibility language only.

Use this skill when a recurring guest run inside a host stream has become important enough to deserve a compact, reusable note that future routing can cite.

Model: a guest speaker arc is a **host-local arc**, and an arc is a bounded helix of arc-threads. Use the arc note for the bounded host x guest braid; use a thread atlas when recurring strands cross months or hosts; use a speaker helix when comparing multiple host-local arcs.

## Required host equivalents

| Purpose | Portable placeholder |
|---------|----------------------|
| Canonical host x guest raw inputs | `<stream-raw-input>` |
| Host-stream routing surface | `<speaker-routing>` |
| Lattice or speaker index surface | `<lattice-surface>` |
| Thread roster or expert continuity surface | `<thread-surface>` |

## When to run

- A host stream now has several raw inputs with the same guest.
- The guest lane is clearly useful, but not a new lattice category by itself.
- The notebook needs a durable answer to:
  - why this guest run matters
  - which episodes anchor the arc
  - which file to open first
  - how the lane should be routed or paired
- A lattice row or thread handle should cite a compact note instead of re-explaining the lane each time.

## Workflow

1. **Confirm the ontology first**
   - Identify the **host stream** and the **guest run**.
   - Default to a **stream-local** note inside the host stream.
   - Do not invent a new top-level category just because the guest matters.
   - Do not place the note under shelves like `supporting-voices` unless the host already uses that as a real taxonomy.

2. **Collect the ground set**
   - Find the canonical raw-input files for the host x guest run.
   - Make sure the run is real, not just a one-off appearance.
   - Prefer files already materialized in canonical raw input over pointers or loose references.

3. **Rank by strategic value**
   - Rank the episodes by reusable notebook value, not by length or recency alone.
   - Favor:
     - the strongest single anchor
     - the best biographical or architectural file
     - the clearest application file
     - the best paired read
   - Say plainly why each ranked file matters.

4. **Write the speaker arc**
   - Keep it compact and reusable.
   - Use this shape:
     - title
     - `WORK only; not Record.`
     - purpose paragraph
     - `## Why this guest run matters`
     - `## Arc set`
     - `## Arc-thread braid`
     - `## Open first`
     - `## Routing use`
     - `## Boundaries`
   - In the arc table, include:
     - rank
     - date
     - title
     - why it matters most
   - In the arc-thread braid, name the recurring strands that make the arc more than chronology.

5. **Preserve stream-local logic**
   - The note should read as **Host x Guest**, not as a standalone worldview bucket.
   - Keep the host stream explicit in the title and purpose.
   - If the guest also appears elsewhere, that does not change the default placement of this note.

6. **Wire the notebook surfaces**
   - Add a citation from the guest row in the host's lattice surface when the guest belongs there.
   - Add or refine the `thread:<expert_id>` row in the host's thread surface when appropriate.
   - Point those surfaces at the speaker arc instead of duplicating the long explanation everywhere.

7. **Run a fullness-before-closure check**
   - Before calling the arc finished, ask:
     - does it give a clean entry for a future operator?
     - is it explicit about what the arc owns versus what the lattice or thread roster owns?
     - does it point toward the right next surface instead of acting like a substitute for a missing speaker route?
     - if the guest run has grown beyond stream-local usefulness, should a fuller year index, speaker folder, or other route now exist?
     - is this arc actually mature enough to absorb stronger synthesis, or is it still the honest stopping point?
   - If those answers are weak, the note may still be useful, but it is not yet a strong reusable arc.

## Skill closure rule

Use the host's shared skill-closure doctrine as the maturity test.

For this skill, stronger synthesis belongs only when the host-local arc can clearly carry it. If the run still mainly needs routing help, stop at the compact arc and point toward the fuller destination.

## Keep boundaries honest

- Say what the guest lane is good for.
- Say what it is not the right tool for.
- If the underlying files are auto-caption normalizations or otherwise imperfect, say so clearly.

## Placement rule

- Preferred home: the host's stream-local note path for `<host>-<guest>-speaker-arc.md`
- The note belongs to the **host stream**.
- The lattice and thread surfaces may cite the note.
- The note itself should not silently redefine the lattice.

## Guardrails

- Do not create a new ontology shelf just because a guest feels important.
- Do not confuse a guest speaker arc with a raw input, profile, or corpus boundary.
- Do not rank by charisma, novelty, or word count alone.
- Do not overclaim certainty; if the lane is speculative or high-variance, say so.
- Do not flatten the guest into a generic ideology label when a more precise lane description is available.
- Do not let a good stream-local note become an excuse to avoid building the fuller routed surface once recurrence is thick enough.
- Do not promote a host-local arc into Record-bearing truth, permanent taxonomy, or a cross-host canon claim without an explicit human decision.

## Success condition

The result is a compact host-stream speaker arc that future routing can cite directly, plus any needed lattice or thread pointers, without creating taxonomic drift or false closure.


## Cursor / grace-mar instance

Grace-mar paths and commands for this repository (from `.cursor/skills/strategy-notebook-guest-canon-note/`).

| Topic | Path |
|--------|------|
| Existing stream-local speaker arcs | [codex/speakers/diesen/stream/](../../codex/speakers/diesen/stream/) |
| Lattice speakers roster | [codex/speaker-lattice.md](../../codex/speaker-lattice.md) |
| Thread handle roster | [codex/strategy-commentator-threads.md](../../codex/strategy-commentator-threads.md) |
| Portable skill manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- In this repo, guest speaker arcs belong to the **host stream** unless an existing taxonomy explicitly says otherwise.
- Current reference pattern:
  - [diesen-matlock-speaker-arc.md](../../codex/speakers/diesen/stream/diesen-matlock-speaker-arc.md)
  - [diesen-jiang-speaker-arc.md](../../codex/speakers/diesen/stream/diesen-jiang-speaker-arc.md)
- The lattice and `thread:` roster may cite the speaker arc, but the note itself should not invent a new shelf or corpus boundary.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill strategy-notebook-guest-canon-note
python scripts/sync_portable_skills.py --verify
python scripts/validate_skills.py
```
