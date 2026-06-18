# Release History

Public reshape milestones for [rbtkhn/civ-state](https://github.com/rbtkhn/civ-state). Full publisher lineage: [Founding Provenance](FOUNDING-PROVENANCE.md).

## Current release

**v0.1.21** — Rome volume-local theory flat layout (`rome-{term}.md`).

## Timeline

### Founding cut (helix-lane v1)

- Exported as `rbtkhn/civ-emp` — helix-first operator corpus (lanes, strands, transactions, orientation routers).
- Preserved under [archive/helix-lane-v1](../archive/helix-lane-v1/README.md).

### Repo rename

- `civ-emp` → **civ-state** — public slug aligned with civilization-**state** book architecture.

### Reshape v0.2 (book-first export)

- Replaced helix-first navigation with the book-first export.
- Five-volume whole work (China, Persia, Rome, Russia, America).
- Source-lattice per volume (later moved to whole-work `sources/` — see v0.1.13).
- Comparative and sacred-grammar apparatus in the appendix.

### v0.1.12 — theory shelf migration

Whole-work theory **SSOT:** `theory/`

| Retired | Replacement |
|---------|-------------|
| `theory/form.md` | `theory/civilization.md` · `theory/empire.md` |
| `theory/truth.md` | `theory/faith.md` · `theory/science.md` |
| `theory/continuity.md` | [Cross-case recurrence essay](../essays/cross-case-recurrence-and-sovereignty.md) |
| `theory/patterns/*` | Same essay; pattern library retired from public shelf |
| Governing term **desire** | **entropy** (behavioral overreach in `theory/entropy.md`) — **superseded v0.1.15** → [empire](../theory/empire.md) |

Each term page carries a **Causal connections** section. Pattern library retired from the public shelf.

### v0.1.15 — entropy theory rebuild

Whole-work **entropy** SSOT: [`theory/entropy.md`](../theory/entropy.md)

| Retired | Replacement |
|---------|-------------|
| structural / behavioral entropy | Removed |
| entropy as divergence mechanics | civilization · empire · rhythm |
| desire → entropy (behavioral) | desire → empire |

Historical causes and manifestations: war, revolution, disease, famine, ecological disaster, compound shocks.

### v0.1.21 — Rome theory flat layout

| Change | Detail |
|--------|--------|
| `volumes/rome/rome-{term}.md` | Moved from `theory/` subdirectory; `rome-` prefix |
| `volumes/rome/rome-theory.md` | Shelf door |

### v0.1.20 — Rome theory Roman law mirror

| Change | Detail |
|--------|--------|
| `volumes/rome/theory/*.md` | Each term page expanded from whole-work cross-cutting Roman law row |
| `volumes/rome/theory/README.md` | Mirror table + navigation |

### v0.1.19 — Rome volume-local theory (skeleton)

| Change | Detail |
|--------|--------|
| `volumes/rome/theory/` | Six term stubs + README — thin bridge to whole-work theory and Rome essays |
| Navigation | Volume README, volume map, book architecture, TOC wired |

### v0.1.18 — cross-cutting objects

Whole-work theory **SSOT:** [`theory/README.md`](../theory/README.md#cross-cutting-objects)

| Change | Detail |
|--------|--------|
| Cross-cutting objects | Law, treaty, constitution, corridor regime — all six lenses; govern one first |
| Worked example | Roman law — one row per governing term |
| `faith.md` · `science.md` | Symmetric See also; cross-cutting pointer |
| `civilization.md` | Pointer from science/codification link |

### v0.1.17 — theory causal-connection mesh

Whole-work theory **SSOT:** six files in `theory/` — cross-term links deepened; rhythm, era law, and retrieval movement promoted to `##` sections on [`memory.md`](../theory/memory.md).

| Change | Detail |
|--------|--------|
| Boundary | `statecraft/states/` is **not** upstream/workshop for `public/civ-state/` — orthogonal operator substrate |
| `memory.md` | `#civilizational-rhythm`, `#era-law`, `#retrieval-movement` as top-level sections |
| `faith.md` · `science.md` | Causal connections to empire, memory, civilization, entropy |
| `civilization.md` · `empire.md` | Missing cross-links added |

### v0.1.16 — rhythm and time under memory

Whole-work theory **SSOT:** six files in `theory/` — rhythm and era law on [`memory.md`](../theory/memory.md).

| Retired | Replacement |
|---------|-------------|
| `theory/rhythm.md` | [memory.md#civilizational-rhythm](../theory/memory.md#civilizational-rhythm) |
| `theory/time.md` | [memory.md#era-law](../theory/memory.md#era-law) |

### v0.1.13 — sources shelf consolidation

Whole-work sources **SSOT:** `sources/`

| Retired | Replacement |
|---------|-------------|
| `source-lattice.md` (repo root) | `sources/source-lattice.md` |
| `volumes/{civ}/sources/primary\|secondary/` | `sources/{civ}/primary\|secondary/` |
| `volumes/{civ}/bibliography.md` (canonical) | `sources/{civ}/bibliography.md` (volume stubs redirect) |
| Volume-owned evidence paths | Volume doors link up to `sources/{civ}/` |

### v0.1.14 — docs shelf consolidation

Whole-work reader apparatus and publish meta **SSOT:** `docs/`

| Retired (repo root) | Replacement |
|---------------------|-------------|
| `introduction.md`, `reader-guide.md`, `table-of-contents.md` | `docs/` same names |
| `glossary.md`, `hybrid-references.md`, `index.md` | `docs/` same names |
| `CONTRIBUTING.md`, `FOUNDING-PROVENANCE.md`, `EXPORT-RECEIPT.md` | `docs/` same names |
| `manifest.yaml`, `VERSION`, `MIRROR-RECEIPT.md` | `docs/` same names |

Root keeps **`README.md`** and **`LICENSE`**.

Thin **redirect stubs** remain at retired repo-root paths (e.g. `introduction.md`, `glossary.md`) pointing into `docs/` for legacy bookmarks.

## Maintenance rule

| Ship-bound surface | Edit here |
|--------------------|-----------|
| Theory prose | `theory/` |
| Source shelves | `sources/` |
| Volume interpretive prose | `volumes/{civ}/` |
| Docs contracts | `docs/` |

Edit ship-bound prose in `public/civ-state/` only. Publish to [rbtkhn/civ-state](https://github.com/rbtkhn/civ-state) from tagged releases on the public tree.

## Export

Generated by the public export pipeline. Receipt: [EXPORT-RECEIPT.md](EXPORT-RECEIPT.md).

## Return paths

- [Founding Provenance](FOUNDING-PROVENANCE.md)
- [Book architecture](book-architecture.md)
- [Docs index](README.md)
