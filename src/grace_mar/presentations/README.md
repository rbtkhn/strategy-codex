# Presentations

`grace_mar.presentations` is the local-first deck generation surface for two content families:

- `ph-civ`: public reader-facing learning decks
- `civ-emp`: operator-facing strategy decks

The product surface is not "send markdown to Presenton." The product surface is:

- choose a `family`
- choose a `subsurface`
- choose an `intent`
- render an editable deck

## Families

### `ph-civ`

Public learning and navigation decks.

- `ph-civ`: civilization orientation
- `ph-apo`: apocalypse / crisis application
- `ph-mus`: museum / exhibit routes

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

`packet -> family/subsurface -> intent -> deck`

## Interfaces

- bundle contract: `family`, `subsurface`, `intent`, `source_items`, policy, provenance
- render API: `POST /v1/bundles/render`
- output: editable `pptx` plus web-view path
- example packets: [artifacts/presentations/examples/README.md](/C:/dev/strategy-codex/artifacts/presentations/examples/README.md)

## Operator Language

Prefer product-surface language over infrastructure language.

Say:

- "generate a `ph-civ` lesson deck"
- "generate a `ph-mus` museum deck"
- "generate a `ce-emp` briefing deck"
- "generate a `ce-mus` exhibit deck"

Avoid defaulting to:

- "build a bundle and submit it to the render service"

That wiring still exists, but it is implementation detail rather than the primary story.

## Symmetry Examples

The checked-in examples make the two museum lanes feel parallel rather than hypothetical:

- `ph-mus-gt16.packet.json`: public museum route -> reader-facing museum deck
- `ce-mus-hormuz.packet.json`: WORK-safe strategic object sequence -> operator-facing exhibit deck
