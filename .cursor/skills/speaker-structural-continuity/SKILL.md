---
name: speaker-structural-continuity
description: Verify that a speaker shelf's front door, speaker object, arc, thread atlas, and month-support surfaces agree on route stack, month ladder, and maturity progression. Use when auditing structural continuity, checking for drift between canonical speaker surfaces, or confirming that setup/bridge/dense-core segment doctrine stays aligned across a speaker shelf.
---

# Speaker Structural Continuity

Use this skill when the question is not "is this month mature?" but "do the canonical speaker surfaces still agree with each other?"

This skill audits **structural continuity across a speaker shelf**:

- front door / README
- speaker object
- native arc
- thread atlas
- month-support shelves
- migration boundary between `statecraft/speakers/` and `codex/speakers/` when present

It is for **agreement checks**, **drift detection**, and **route-stack coherence**.

It is not for:

- discovering new raw-input
- transcript cleanup
- ranking thin captures inside a month
- deciding initial month maturity from scratch unless that judgment is already materially present on the shelf
- deciding whether a month deserves support in the first place when the shelf has not already expressed that judgment

For month-status classification, repair ranking, or `mature every segment` doctrine, use [`speaker-shelf-hygiene`](../speaker-shelf-hygiene/SKILL.md).

## What To Check

Audit these continuity surfaces in order:

1. `README` or shelf front door
2. `speaker-object` note
3. `*-arc.md`
4. `*-arc-threads.md` or equivalent atlas
5. month-support shelves
6. codex-side compatibility fronts and stubs if the speaker has migrated into `statecraft/speakers/`

Check for agreement on:

- the canonical route stack
- whether the shelf is stream-native, helix-first, or host-led
- whether the shelf is host-led, speaker-synthesis-led, or speaker-chronology-led at the month layer
- month ladder ordering
- month-status labels
- the relation between setup, bridge, dense-core, and frontier months
- whether the atlas and month shelves tell the same phase story
- whether codex-side compatibility surfaces point cleanly to the same canonical statecraft-side shelf

## Continuity Questions

Use these tests:

- `front-door continuity`
  - can a future agent enter the shelf from the README and reach the correct canonical surfaces without being pushed into compatibility residue?
- `route-stack continuity`
  - do README, speaker object, arc, and atlas point to the same primary ladder?
- `segment continuity`
  - do adjacent month shelves form a real progression rather than a set of isolated pages?
- `status continuity`
  - do month labels agree across surfaces?
- `month ownership continuity`
  - do the surfaces agree on whether monthly files are bounded synthesis or chronology-owning?
- `thread continuity`
  - does the atlas preserve the same phase progression the month shelves claim?
- `boundary continuity`
  - are compatibility files still demoted, or have they silently become quasi-canonical again?
- `migration continuity`
  - if the speaker moved into `statecraft/speakers/`, do the codex-side pointer fronts and compatibility stubs still resolve without preserving dual authority?

## Common Failure Modes

- speaker object says one month is bridge while arc says another
- month shelves exist, but the arc does not acknowledge them
- support spine still says "no native monthly shelf" after bounded synthesis shelves were introduced
- thread atlas stops carrying the ladder after one or two months
- README still routes to old compatibility surfaces after canonical shelves mature
- codex-side stubs exist, but thread/transcript residue still points to removed or contradictory core files
- frontier months use old generic templates while earlier months use explicit month-status doctrine
- dense-core claims appear in one surface but not the others

## Output Format

Start with a continuity verdict:

- `structurally continuous`
- `mostly continuous with minor seams`
- `material drift present`

Then report:

- what agrees
- what diverges
- the smallest next fix that would restore full continuity

Prefer concise findings like:

- `May shelf still uses old frontier template, so dense-core ladder is doctrinally asymmetric.`
- `Arc and speaker-object agree on February as bridge, but atlas does not yet carry the same month-phase wording.`
- `Statecraft-side monthly shelves are bounded synthesis, but the support spine still describes the shelf as if no native month layer exists.`
- `Codex-side front door demotes correctly, but one compatibility residue file still routes as if the old shelf were canonical.`

## Editing Guidance

If you repair continuity:

- prefer the smallest canonical surface that can restore agreement
- do not duplicate month summaries into the atlas
- do not turn the README into a second speaker-object note
- keep compatibility residue explicitly demoted
- preserve existing maturity judgments unless the shelf already clearly contradicts itself
- if a statecraft-side migration is in progress, prefer restoring one canonical authority path plus thin codex compatibility stubs rather than maintaining two rich front doors

## Success Condition

The shelf is continuous when:

- a future agent can enter from the front door
- reach the correct arc and thread surfaces
- follow the month ladder in order
- understand whether the month layer is synthesis-only or chronology-owning
- and see one consistent story about setup, bridge, dense-core, and frontier progression
- while codex-side compatibility surfaces, if any, remain clearly subordinate to the same canonical shelf

without reconstructing the doctrine from fragments.
