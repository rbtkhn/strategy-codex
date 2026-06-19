# CIV-MEM Context doctrine for Predictive History

WORK only; transfer package for later use in the external Predictive History
repo.

## What this layer is for

`CIV-MEM Context` is the historical-civilizational framing layer that helps
Predictive History do two jobs at once:

- help the **developer/editor** understand what kind of larger object a
  lecture/chapter is really working on
- help the **reader** enter that lecture/chapter with the right horizon of
  attention

Its purpose is not to replace the transcript, analysis memo, or chapter draft.
Its purpose is to establish the **civilizational reading posture** before the
reader descends into detailed argument or evidence.

## Context payload vs rendered context block

This system has two different objects:

### 1. Context payload

The **context payload** is the stable conceptual content. It should be stored in
the PH **archive/placeholders/evidence/media pack** and treated as the canonical source of truth for
context.

The payload names:

- the primary civilizational object
- the larger historical arc
- the dominant CIV-MEM slots
- the reader orientation
- fit strength
- any limit or mismatch note when needed

This layer should remain stable even if the visible prose changes.

### 2. Rendered context block

The **rendered context block** is the reader-facing prose that appears near the
top of a lecture/chapter under a heading such as `## CIV-MEM Context`.

It is the visible expression of the payload, written in the active house voice.
It may be shortened, tuned, or rephrased later without changing the underlying
payload.

## Why the archive/placeholders/evidence/media pack should own the payload

The pack is the best home for the payload because it already sits between:

- transcript / lecture evidence
- analysis and registries
- chapter construction
- later publishing decisions

If the payload lives there, the developer can stabilize the conceptual content
once and then reuse it for:

- the lecture page
- the chapter opening
- later site or summary surfaces
- future voice revisions

This avoids maintaining two unrelated CIV-MEM drafts in different places.

## Why lecture/chapter pages should display the rendered block

Predictive History is not only a research archive. It is also a reading
experience. The lecture/chapter page is where the reader needs help answering:

- what historical-civilizational object am I entering?
- what arc is this part of?
- what should I pay attention to while reading this unit?

The visible `CIV-MEM Context` block should therefore appear near the top of the
unit, before the reader is immersed in transcript density or chapter detail.

## What "always substantial" means

`Always substantial` does **not** mean every context block must sound equally
grand or equally long. It means every unit should receive a real contextual
layer that does actual work.

In practice, that means:

- the block should never collapse into a decorative label
- it should say more than "this is about empire" or "this concerns religion"
- it should orient the reader toward a larger civilizational frame
- it should guide how the unit is to be read

Substantial means **functionally meaningful**, not necessarily rhetorically
maximal.

## Low-fit honesty

Some PH units fit CIV-MEM more strongly than others. Low fit should not mean the
layer disappears. It should mean the layer becomes more explicit about its
limits.

For low-fit units:

- keep the block shorter
- identify the primary object with less flourish
- use a narrower historical arc
- add a mismatch or limit note if the analogy is partial
- do not force heavy civilizational rhetoric

Rule:

- **always present**
- **not always equally weighty**

## Recommended target integration steps for the future PH repo

When this package is applied in the real Predictive History repo, the
implementer should:

1. add the payload section to the archive/placeholders/evidence/media pack format
2. add the reader-facing `## CIV-MEM Context` block to lecture/chapter
   templates
3. keep the pack as source of truth for payload
4. render the visible block from the payload rather than authoring two unrelated
   versions
5. preserve one active voice profile (`house-default`) while leaving room for
   future voice tuning

