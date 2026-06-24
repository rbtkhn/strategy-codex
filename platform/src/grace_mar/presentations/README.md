# Presentations

`grace_mar.presentations` is the local-first deck generation surface for two content families:

- `ph-civ`: public reader-facing learning decks
- `civ-emp`: operator-facing strategy decks

The product surface is not "send markdown to Presenton." The product surface is:

- choose a `family`
- choose a `subsurface`
- choose an `artifact_class`
- choose an `intent`
- render an editable deck

## Families

### `ph-civ`

Public learning and navigation decks.

- `ph-civ`: civilization orientation
- `ph-apo`: apocalypse / crisis application

Typical jobs:

- `lesson`
- `summary`
- `comparison`

### `civ-emp`

WORK-safe strategy and briefing decks.

- `ce-civ`: civilization-side pattern decks
- `ce-emp`: empire / statecraft briefings
- `ce-mus`: exhibit-style strategic object decks

Typical jobs:

- `briefing`
- `summary`
- `roadmap`
- `comparison`

## Mental Model

The render service is the shared engine.

- `ph-civ` helps people learn, navigate, and share
- `civ-emp` helps people brief, compare, and decide

Short formula:

`packet -> family/subsurface/artifact_class -> intent -> deck`

## Comparison Boundary

`comparison` currently means a comparison deck **inside one bundle family**.

Supported now:

- `ph-civ` vs `ph-civ`
- `ph-apo` route vs route
- `ce-emp` decision path vs decision path
- `ce-mus` artifact set vs artifact set

Not supported yet:

- one render bundle that compares `ph-civ` and `civ-emp` directly
- composite left/right bundle comparison payloads

The current contract is intentionally `bundle_type=single_bundle` only. If cross-family comparison becomes a real product need, it should land as a higher-order composite bundle type rather than stretching a single-family bundle until it lies.

## Interfaces

- bundle contract: `bundle_type`, `family`, `subsurface`, `artifact_class`, `intent`, `source_items`, policy, provenance
- render API: `POST /v1/bundles/render`
- output: editable `pptx` plus web-view path
- example packets: [runtime/artifacts/presentations/examples/README.md](/C:/dev/strategy-codex/runtime/artifacts/presentations/examples/README.md)

## Operator Language

Prefer product-surface language over infrastructure language.

Say:

- "generate a `ph-civ` lesson deck"
- "generate a `ph-apo` application deck"
- "generate a `ce-emp` briefing deck"
- "generate a `ce-mus` exhibit deck"

Avoid defaulting to:

- "build a bundle and submit it to the render service"

That wiring still exists, but it is implementation detail rather than the primary story.

## Symmetry Examples

The checked-in example shows a WORK-safe exhibit deck path:

- `ce-mus-hormuz.packet.json`: WORK-safe strategic object sequence -> operator-facing exhibit deck

Legacy public museum packet example (`ph-mus-gt16.packet.json`) remains in the examples folder for archaeology only; the `ph-mus` subsurface was retired. See [`public/ph-civ/docs/archive/ph-mus-retired.md`](../../../public/ph-civ/docs/archive/ph-mus-retired.md).
