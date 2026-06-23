---
name: speaker-structural-continuity
description: "Verify that a speaker shelf's front door, speaker object, arc, thread atlas, and month-support surfaces agree on route stack, month ladder, and maturity progression. Use when auditing structural continuity, checking for drift between canonical speaker surfaces, or confirming that setup/bridge/dense-core segment doctrine stays aligned across a speaker shelf."
category: domain-pack
status: active
scope_class: repo-governed
---
# Speaker Structural Continuity

Use this skill when the question is not "is this month mature?" but "do the canonical speaker surfaces still agree with each other?"

This skill audits **structural continuity across a speaker shelf**:

- front door / README
- speaker object
- native arc
- thread atlas
- month-support shelves
- migration boundary between `statecraft/voices/` and `codex/speakers/` when present
- canonical outer grammar when a shelf has normalized into `statecraft/voices/`

It is for **agreement checks**, **drift detection**, and **route-stack coherence**.

It is not for:

- discovering new raw-input
- transcript cleanup
- ranking thin captures inside a month
- deciding initial month maturity from scratch unless that judgment is already materially present on the shelf
- deciding whether a month deserves support in the first place when the shelf has not already expressed that judgment

For month-status classification, repair ranking, or `mature every segment` doctrine, use [`speaker-shelf-hygiene`](../speaker-shelf-hygiene/SKILL.md).

## Normalized outer grammar

When a speaker has normalized into `statecraft/voices/`, treat this as the expected outer shelf grammar unless the shelf explicitly says otherwise:

1. `README.md`
2. `index.md`
3. `person arc`
4. `routing`
5. `raw-input bench`
6. `helix / crossing surface`
7. `support spine`
8. `stream/README.md`
9. bounded monthly synthesis ladder for `2026-01` through `2026-05`
10. `historical audit`
11. `themes/README.md`
12. codex compatibility fronts and residue

Short rule:

`canonical statecraft shelf first -> bounded monthly synthesis -> codex compatibility last`

This is an **outer grammar**, not a claim that every speaker has identical inner structure.

Examples of inner variation that still pass continuity:

- `Macgregor / Ritter` = direct canonical template
- `Crooke` = authored plus interview dual-source-class object inside the same outer grammar
- `Mercouris` = stream-native inner core wrapped by the same outer grammar

Do not mistake a shared outer scaffold for a demand that every speaker become the same type of object.

## Exception classes

Outer-grammar normalization does **not** erase legitimate exception classes.

Use these three classes explicitly:

1. `normalized month-ladder shelf`
   - canonical `statecraft/<speaker>/`
   - bounded `2026-01` through `2026-05` synthesis ladder
   - support spine owns month-status law
   - examples: `Macgregor`, `Ritter`, `Freeman`, `Johnson`

2. `cross-context exception shelf`
   - canonical `statecraft/<speaker>/`
   - recurring thread atlas and source-class crossing are structurally primary
   - bounded month support appears only where mature cross-context pressure is real
   - example: `Parsi`

3. `host-led mature-month exception shelf`
   - may still be codex-side or later migrate statecraft-side
   - mature months exist, but they are owned more cleanly by host arcs, reinforcing orbit, or a non-core bench than by speaker-native month shelves
   - support spine and routing own the maturity explanation
   - current main example: `Mearsheimer`

Continuity work must decide which class a shelf belongs to before forcing it toward a migration pattern.

## What To Check

Audit these continuity surfaces in order:

1. `README` or shelf front door
2. `index.md` if present
3. `speaker-object` note if present
4. `*-arc.md`
5. `*-arc-threads.md` or equivalent atlas
6. support spine
7. month-support shelves
8. codex-side compatibility fronts and stubs if the speaker has migrated into `statecraft/voices/`

Check for agreement on:

- the canonical route stack
- the normalized outer grammar when the shelf is statecraft-side canonical
- which shelf class governs the object
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
- `outer-grammar continuity`
  - if this is a normalized `statecraft/voices/` shelf, are `README`, `index`, support spine, monthly ladder, audit, and themes all visibly present and legible?
- `shelf-class continuity`
  - is the shelf being described as the same class everywhere, or are different surfaces half-describing different constitutional types?
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
  - if the speaker moved into `statecraft/voices/`, do the codex-side pointer fronts and compatibility stubs still resolve without preserving dual authority?
- `inner-shape continuity`
  - does the normalized outer scaffold preserve the speaker's real inner shape rather than forcing a fake one?

## Stream-native wrapper rule

Some speakers normalize into the same outer grammar while keeping a different inner core.

Use `Mercouris` as the main example:

- the outer shelf still needs `README`, `index`, routing, raw-input bench, crossing surface, support spine, month ladder, audit, and themes
- but the inner continuity core may still be a native stream arc and arc-thread atlas

Continuity passes if:

- the outer statecraft shelf clearly owns the canonical opening path
- the inner stream-native logic remains legible and unflattened
- the support spine explains how bounded monthly synthesis relates to stream-owned chronology

Continuity fails if:

- the wrapper implies a fake helix-first or host-led identity the inner shelf does not support
- the month ladder silently takes chronology ownership without saying so
- the codex-side stream residue keeps behaving like co-equal canon

## Common Failure Modes

- speaker object says one month is bridge while arc says another
- month shelves exist, but the arc does not acknowledge them
- support spine still says "no native monthly shelf" after bounded synthesis shelves were introduced
- thread atlas stops carrying the ladder after one or two months
- README still routes to old compatibility surfaces after canonical shelves mature
- statecraft-side shelf has normalized, but lacks `index.md`, support spine, or `stream/README.md`
- codex-side stubs exist, but thread/transcript residue still points to removed or contradictory core files
- frontier months use old generic templates while earlier months use explicit month-status doctrine
- dense-core claims appear in one surface but not the others
- outer grammar is normalized, but the speaker-object or inner core still describes an older incompatible route stack
- a codex transcript or thread still routes to codex-side arc / routing / helix after statecraft-side canon is live
- a host-led mature-month exception shelf is being migrated as if it already wanted a native monthly ladder
- a cross-context exception shelf is being flattened into host-style month law for symmetry alone

## Output Format

Start with a continuity verdict:

- `structurally continuous`
- `mostly continuous with minor seams`
- `material drift present`

Then report:

- what agrees
- what diverges
- the smallest next fix that would restore full continuity

When useful, name both:

- `outer-grammar verdict`
- `inner-shape verdict`

Prefer concise findings like:

- `May shelf still uses old frontier template, so dense-core ladder is doctrinally asymmetric.`
- `Arc and speaker-object agree on February as bridge, but atlas does not yet carry the same month-phase wording.`
- `Statecraft-side monthly shelves are bounded synthesis, but the support spine still describes the shelf as if no native month layer exists.`
- `Codex-side front door demotes correctly, but one compatibility residue file still routes as if the old shelf were canonical.`
- `Outer scaffold is normalized, but the stream-native inner core is still being described as if it were a cross-host helix.`
- `Month ladder is present, but the support spine still has not claimed month-status law.`

## Editing Guidance

If you repair continuity:

- prefer the smallest canonical surface that can restore agreement
- fix statecraft-side canonical wording before widening codex residue
- do not duplicate month summaries into the atlas
- do not turn the README into a second speaker-object note
- keep compatibility residue explicitly demoted
- preserve existing maturity judgments unless the shelf already clearly contradicts itself
- if a statecraft-side migration is in progress, prefer restoring one canonical authority path plus thin codex compatibility stubs rather than maintaining two rich front doors
- if the shelf already has the normalized outer grammar, repair codex residue by updating compatibility notes rather than rebuilding codex-side doctrine
- if the shelf is still in an unresolved exception class, fix the doctrinal classification first rather than forcing a migration shape by momentum

## Success Condition

The shelf is continuous when:

- a future agent can enter from the front door
- see the normalized outer grammar if the shelf is statecraft-side canonical
- reach the correct arc and thread surfaces
- follow the month ladder in order
- understand whether the month layer is synthesis-only or chronology-owning
- and see one consistent story about setup, bridge, dense-core, and frontier progression
- while codex-side compatibility surfaces, if any, remain clearly subordinate to the same canonical shelf

without reconstructing the doctrine from fragments.
