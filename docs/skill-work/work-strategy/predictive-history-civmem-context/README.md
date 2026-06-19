# Predictive History CIV-MEM context transfer package

WORK only; not Record. This folder is a **transfer-ready handoff package**
prepared inside `strategy-codex` for later application in the external
`rbtkhn/ph-workshop` repo.

> In cross-repo handoffs, specify the intended experience transformation first,
> then define the structural contracts that preserve it. This package therefore
> begins not from implementation alone, but from the change it is meant to
> create in first contact with the target object: what the reader or operator
> notices, how the object is framed, and how it can be re-entered later with
> greater coherence. The structures that follow are not ends in themselves, but
> the smallest durable contracts needed to preserve that better encounter across
> surfaces, tools, and later revisions.

## Purpose

This package defines a CIV-MEM contextualization system whose job is:

- to help the Predictive History developer historically-civilizationally frame
  each lecture/chapter
- to make that framing visible to readers through a substantial
  `CIV-MEM Context` block
- to keep the **context structure stable** while allowing the **voice** to be
  tuned later

Because the canonical Predictive History repo is **not directly accessible**
from this workspace, the right deliverable here is a **handoff package**, not a
file-specific implementation patch against unseen PH paths.

## Package contents

| File | Role |
|------|------|
| [implementation-handoff.md](implementation-handoff.md) | Consolidated direct-transfer implementation spec for the future PH repo. |
| [civmem-context-doctrine.md](civmem-context-doctrine.md) | Core doctrine: what the layer is for, payload vs rendering, substantial-by-default rule, and low-fit honesty. |
| [pack-payload-template.md](pack-payload-template.md) | Canonical structured payload template for PH archive/placeholders/evidence/media packs. |
| [reader-context-block-template.md](reader-context-block-template.md) | Reader-facing `## CIV-MEM Context` template for lectures/chapters. |
| [house-default-voice.md](house-default-voice.md) | Initial contextual voice doctrine (`house-default`) plus modulation rules. |
| [calibration-examples.md](calibration-examples.md) | Golden example bundle: strong-fit, medium-fit, lower-fit, and alternate cooler render. |

## Transfer model

The package assumes one stable split:

- **context payload** lives in the PH **archive/placeholders/evidence/media pack**
- **rendered context block** lives in the PH **lecture/chapter presentation**

That split keeps the conceptual content stable while making the prose easy to
modulate later.

## Recommended integration order in the future PH repo

1. Start from [implementation-handoff.md](implementation-handoff.md) as the
   direct-transfer spec.
2. Add the **pack payload** section to the archive/placeholders/evidence/media pack format.
3. Add the reader-facing **`## CIV-MEM Context`** block to lecture/chapter
   templates.
4. Adopt **`house-default`** as the active initial voice profile.
5. Use the examples in
   [calibration-examples.md](calibration-examples.md) as the golden set while
   tuning local PH surfaces.

## Acceptance check

The package is complete if a future PH implementer can answer, without new
design work:

- what CIV-MEM contextualization is supposed to do
- what structured payload fields must exist
- what visible block readers should see
- what voice that block should use
- how structure and voice remain separable
- how low-fit cases remain honest without disappearing
