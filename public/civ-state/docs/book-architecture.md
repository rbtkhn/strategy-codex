# Book Architecture

How *Civilizational Statecraft* is organized after the v0.1.12 theory reshape and v0.1.13 sources consolidation.

This page is a **map of shelves**, not a file inventory. For the reader-facing table of contents, open [Table of Contents](table-of-contents.md). For reading doctrine, open [Reader Guide](reader-guide.md).

## What the book is

**Civilizational Statecraft** is a five-volume comparative work for the general statesman reader. Each volume is one civilization-state case. Whole-work shelves supply governing vocabulary, evidence discipline, and comparative retrieval without replacing volume prose.

The governing **civilizational motion**:

```text
civilization beautifies → empire amplifies → entropy degrades
```

Whole-work retrieval movement:

```text
memory → legitimacy → carrier → pressure → settlement
```

## Layer map

| Layer | Path | Role |
|-------|------|------|
| **Front door** | repo root | Book title (`README.md`, `LICENSE`) |
| **Docs** | `docs/` | Opening essay, reader guide, TOC, glossary, index, meta, contracts |
| **Theory** | `theory/` | Six governing terms (rhythm and era law on [Memory](../theory/memory.md)) |
| **Sources** | `sources/` | Source-lattice law and per-civilization evidence shelves |
| **Volumes** | `volumes/{civ}/` | Interpretive doors: introduction, civilization and empire essays, sub-lenses, shelf-reader, sacred grammar |
| **Essays** | `essays/` | Bounded cross-case or live-seam essays — not mixed into the theory term shelf |
| **Skills** | `skills/` | Operator-facing retrieval recipes (optional for general readers) |
| **Archive** | `archive/` | Legacy public cuts preserved for lineage — not the active reading path |

## Front door

Start at [README.md](../README.md), then the docs shelf:

1. [Civilization and Empire](introduction.md) — opening essay; **not** the book title
2. [Reader Guide](reader-guide.md) — how to read correctly
3. [Table of Contents](table-of-contents.md) — five-volume map and appendix apparatus

Supporting reference in `docs/`: [Glossary](glossary.md), [Hybrid References](hybrid-references.md), [Index](index.md), [Founding Provenance](FOUNDING-PROVENANCE.md).

## Theory shelf

**SSOT:** `theory/`

Six **governing terms** — open the term that is load-bearing first:

- [Civilization](../theory/civilization.md) · [Empire](../theory/empire.md) · [Entropy](../theory/entropy.md)
- [Faith](../theory/faith.md) · [Science](../theory/science.md) · [Memory](../theory/memory.md) — includes [civilizational rhythm](../theory/memory.md#civilizational-rhythm) and [era law](../theory/memory.md#era-law)

Cross-case pattern library is **retired from the public theory shelf** (v0.1.12). Reader-facing replacement: [Cross-case recurrence and sovereignty](../essays/cross-case-recurrence-and-sovereignty.md).

**Volume-local theory** (`volumes/{civ}/theory/`) is forthcoming — case-specific causal history through the same six filenames. Until those shelves ship, use whole-work [theory](../theory/README.md) for comparative grammar.

## Sources shelf

**SSOT:** `sources/`

- Governing law: [Source-Lattice](../sources/source-lattice.md)
- Per case: `sources/{civ}/bibliography.md`, `primary/{era}.md`, `secondary/{era}.md`

Volumes **do not** own canonical evidence paths. Volume README, shelf-reader, and essays **link up** to `sources/{civ}/`. Open primary shelves first; use secondary only when difficulty appears; ascend to civilization and empire essays after the shelf problem is clarified.

See [Sources](../sources/README.md) for the civilization-state shelf index.

## Volume layer

**SSOT for interpretive prose:** `volumes/{civ}/`

Constitutional read order within each volume:

```text
volume introduction → civilization chapter → empire chapter
```

Optional sub-lenses: geo-strategy, secret-history, game-theory.

Each volume also carries:

- **Doorway:** README, introduction, `shelf-reader.md`
- **Deep grammar:** `sacred-grammar.md` when legitimacy or truth-order governs
- **Evidence links:** upward to `sources/{civ}/` (not nested under the volume tree)

Five volumes in sovereignty-chain order: [China](../volumes/china/README.md) → [Persia](../volumes/persia/README.md) → [Rome](../volumes/rome/README.md) → [Russia](../volumes/russia/README.md) → [America](../volumes/america/README.md).

## Essays

**SSOT:** `essays/`

Whole-work essays that are comparative or live-seam but should not sit on the theory term shelf. Current set includes cross-case recurrence, high-skill labor compression, and Hormuz recognition / transit restraint.

## Docs shelf (detail)

**SSOT:** `docs/` — see [Docs index](README.md) for the full list.

Contract pages:

- [Book architecture](book-architecture.md) (this page)
- [Names and titles](names-and-titles.md)
- [Era spine](era-spine.md)
- [Release history](release-history.md)

## What not to collapse

| Do not merge | Because |
|--------------|---------|
| Book title vs opening essay | **Civilizational Statecraft** ≠ **Civilization and Empire** |
| Theory terms vs law pages | Governing diagnosis vs motion/era placement |
| Sources vs volume essays | Evidence spine vs interpretive judgment |
| Whole-work theory vs volume theory (forthcoming) | Comparative grammar vs case-specific causal history |
| Repo slug vs reader title | **civ-state** is GitHub only — not a reader-facing name |

## Typical reading paths

**Civilization-first** (which case owns this inheritance?):

1. Volume map → volume introduction → Civilization → Empire
2. Source-lattice when chronology or attribution trouble appears
3. Theory shelf when the governing term is unclear

**Governing-layer-first** (which term is load-bearing?):

1. Theory README → one governing term page
2. Rhythm or Time when motion or era governs
3. Descend to volume or sources as needed

## Return paths

- [Volume Map](../volumes/README.md)
- [Theory shelf](../theory/README.md)
- [Sources](../sources/README.md)
- [Docs index](README.md)
