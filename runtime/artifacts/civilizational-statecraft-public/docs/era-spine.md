# Era Spine

Shared chronology anchors for source shelves and era-matched reading in *Civilizational Statecraft*.

Era **law** (how eras govern retrieval) lives on [Memory — era law](../theory/memory.md#era-law). This page is the **spine table** and per-volume coverage notes.

## Shared era table

| Era | Anchor | Typical use |
|-----|--------|-------------|
| **Ancient** | → 476 | Classical and late-antique continuity |
| **Medieval** | → 1453 | Sacred-imperial and post-classical orders |
| **Colonial** | → 1815 | Expansion, encounter, and early modern state formation |
| **Industrial** | → 1991 | Mass industrial state, world wars, Cold War closure |
| **Cybernetic** | post-1991 | Networked order, algorithmic governance, present carrier |

Anchors are **reading boundaries**, not claims that every civilization "begins" in Ancient. Russia and America enter the set on later rungs (see below).

## Per-volume coverage

| Volume | Ancient primary | Medieval | Colonial | Industrial | Cybernetic | Notes |
|--------|-----------------|----------|----------|------------|------------|-------|
| [China](../volumes/china/README.md) | yes | yes | yes | yes | yes | Full five-era spine |
| [Persia](../volumes/persia/README.md) | yes | yes | yes | yes | yes | Full five-era spine |
| [Rome](../volumes/rome/README.md) | yes | yes | yes | yes | yes | Full spine; some shelves still maturing — see volume README |
| [Russia](../volumes/russia/README.md) | — | yes | yes | yes | yes | No Ancient primary shelf |
| [America](../volumes/america/README.md) | — | — | yes | yes | yes | Opens at Colonial; no Ancient or Medieval primary shelf |

**Secondary shelves** may exist for eras where primary orientation is thin or where attribution trouble requires bounded support. Governing rule: primary first, secondary only when difficulty appears.

## How to use the spine

1. **Inside one case:** Open `sources/{civ}/bibliography.md`, then the era file that matches the live object (`sources/{civ}/primary/{era}.md`).
2. **Cross-era pressure:** When the object spans a boundary (e.g. Industrial → Cybernetic), read [Memory — era law](../theory/memory.md#era-law) before stacking era files.
3. **Cross-volume comparison:** Use the same era label across cases only after each case's shelf is open — analogies across eras still require case-specific legitimacy reads.

## File naming

Era files use lowercase era slugs:

```text
sources/{civ}/primary/ancient.md
sources/{civ}/primary/medieval.md
sources/{civ}/primary/colonial.md
sources/{civ}/primary/industrial.md
sources/{civ}/primary/cybernetic.md
```

Matching secondary files live under `sources/{civ}/secondary/` when present.

## Return paths

- [Source-Lattice](../sources/source-lattice.md)
- [Sources index](../sources/README.md)
- [Volume Map](../volumes/README.md)
- [Memory — era law](../theory/memory.md#era-law)
