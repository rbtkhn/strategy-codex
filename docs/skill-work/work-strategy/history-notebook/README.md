# History Notebook

**Discoverability:** Linked from **`SELF-LIBRARY/history-notebook`** (repo-relative symlink when created). **LIB:** [LIB-0156](../../../../self-library.md#operator-analytical-books) (operator-authored chapters) Ãƒâ€šÃ‚Â· [LIB-0158 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Bookshelf (self-library-bookshelf)](../../../../self-library.md#self-library-bookshelf) (owned print `HNSRC-*` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [BOOKSHELF.md](research/BOOKSHELF.md) vs [operator books](../../../../self-library.md#operator-analytical-books)) in [`self-library.md`](../../../../self-library.md).

**Operator-authored compressed chapters** distilling civilizational patterns into strategy-ready reference. Five temporal volumes; **target 20 chapters per volume (100 main-era chapters)**; each chapter ~500ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“1000 words. **Curated fact base:** [SELF-LIBRARY](../../../../self-library.md) (governed shelf entries) is the **curated fact base** for history-notebook ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the operator and agent should ground factual discipline and lookup in that index (with [CIV-MEM / LIB-0157](../../../../self-library.md#operator-analytical-books) as the MEM-reservoir layer where indexed), not the undifferentiated open web as default. Not a wholesale mirror of CIV-MEM ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â an independent analytical layer the operator writes and the agent reads.

### Model (chapter-first)

Book identity and chapter IDs remain **SSOT** in [book-architecture.yaml](book-architecture.yaml) and PH wiring in [cross-book-map.yaml](cross-book-map.yaml). History notebook uses a **traditional chapter model** with deliberate variation: **problem-led Volume I** (comparative ancient evidence), five temporal volumes, [STYLE-GUIDE.md](STYLE-GUIDE.md) prose targets, and optional **civilization threads** as longitudinal scratchpads ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **not** a separate legacy history-page file layer. (Strategy-notebook **daily judgment** pages, LIB-0153, are unrelated.)

| Piece | Location | Role |
|-------|----------|------|
| **Chapters** | [chapters/](chapters/) + YAML ids | Primary deliverable: comparative chapters (~500ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“1000w); cite **chapter ids** (`hn-i-v1-04`, ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦) from strategy-notebook **`### History resonance`** |
| **Distillation queue** | [STATUS.md](STATUS.md) | **Single SSOT** for next `hn-*` to draft; strategy **`meta.md`** links here ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see [STRATEGY-NOTEBOOK-ARCHITECTURE Ãƒâ€šÃ‚Â§ Parallel to History notebook](../strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#parallel-to-history-notebook-lib-0156) |
| **Bookshelf** / **self-library-bookshelf** | [research/BOOKSHELF.md](research/BOOKSHELF.md) | **Enhanced bib** for the operatorÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢s **physical** collection ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not full text; [LIB-0158 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â self-library-bookshelf](../../../../self-library.md#self-library-bookshelf); distinct from operator-authored [books in self-library](../../../../self-library.md#operator-analytical-books) |
| **Bookshelf catalog** (optional) | [research/bookshelf-catalog.yaml](research/bookshelf-catalog.yaml) + [research/BOOKSHELF-RUNBOOK.md](research/BOOKSHELF-RUNBOOK.md) | Machine-readable `HNSRC-*` rows (the **self-library-bookshelf** list); **informs** drafting; not chapter SSOT. After edits: `python3 scripts/validate_bookshelf_catalog.py` and `python3 scripts/build_hn_bookshelf_bibliography.py` |
| **Generated shelf bibliography** | [research/bibliography/](research/bibliography/) | Chicago *authorÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“date* (simplified) from the catalog; **read-only** exports ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not chapter SSOT |
| **Shelf anchors by `hn-*`** | [research/SHELF-ANCHORS-BY-CHAPTER.md](research/SHELF-ANCHORS-BY-CHAPTER.md) + `python3 scripts/hn_shelf_anchors.py` | Inverted index: which **HNSRC** rows list each chapter in `candidate_hn_chapters`; `--stub-line`, `--hnsrc`, `--chapter` for drafting |
| **Agentic MVP outputs** | [research/QUEUE-AUTOPRIORITY.md](research/QUEUE-AUTOPRIORITY.md), [research/PROVENANCE-PACKETS.md](research/PROVENANCE-PACKETS.md), [research/REDTEAM-FINDINGS.md](research/REDTEAM-FINDINGS.md) | Queue, claim provenance packets, and red-team challenge matrix generated across all `hn-*` chapters |
| **Agentic MVP command guide** | [research/AGENTIC-MVP-RUNBOOK.md](research/AGENTIC-MVP-RUNBOOK.md) + [research/AGENTIC-MVP-CONFIG.yaml](research/AGENTIC-MVP-CONFIG.yaml) | Scoring, confidence, and classification config + one-command regen/check flow for all generated artifacts |
| **Vol I library scaffold** (optional) | [research/VOL-I-LIBRARY-SCAFFOLD.md](research/VOL-I-LIBRARY-SCAFFOLD.md) | Maps **HNSRC-*** rows to `hn-i-v1-01`ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦`20` for problem-spine drafting; see also [VOL-I-PROBLEM-CHAPTERS.md](research/VOL-I-PROBLEM-CHAPTERS.md). |
| **Civilization threads** (optional) | [threads/](threads/) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `history-civ-*.md` | 9-section governed **longitudinal** threads (continuity, contradictions, MC ladder, polyphony, bridges, ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **scaffolding** for drafting, not a parallel codex |

### Work, Record, and the Strategy notebook

- **History notebook `history-civ-*` threads and `hn-*` chapters** are **operator WORK** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â analytical surfaces for drafting and strategy alignment. They are **not** the [Record](../../../../AGENTS.md) (`self.md` / companion identity) unless a fact is explicitly promoted through the **recursion-gate** pipeline; do not treat thread scratch as Voice truth.
- **One-way interface:** [Strategy notebook](strategy-notebook/README.md) may **draw** from History notebook: **`### History resonance`** with `hn-*` chapter id(s) + a thin mechanism or warrant line (see [STRATEGY-NOTEBOOK-ARCHITECTURE Ãƒâ€šÃ‚Â§ Parallel to History notebook](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#parallel-to-history-notebook-lib-0156)). **No** automatic path the other way ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this book is **not** updated *because* `days.md`, page notes, or daily judgment said so. **Operator-originated** edits in `docs/skill-work/work-strategy/history-notebook/` (and governed thread files) are the only authorized path from ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œtodayÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢s gapÃƒÂ¢Ã¢â€šÂ¬Ã‚Â to HN change.
- **Governed civilization threads:** All `history-civ-*.md` files use the same 9-section template. **Russia** remains the **annotated salience pilot** in [book-architecture.yaml](book-architecture.yaml) (`governed_pilot` on the Russia arc) with **phase-1 exit** criteria: [threads/README.md](threads/README.md#russia-salience-pilot-phase-1).

Flow: **SELF-LIBRARY (curated fact base) + CIV-MEM (MEM reservoir) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ distill into HN chapters (`hn-*`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ strategy-notebook** cites ids + mechanisms in **`### History resonance`** (tiers + optional **`HN gap:`** back-pressure ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [STATUS.md](STATUS.md)). Threads optional before drafting. Retired experiment: see [threads/README.md](threads/README.md).

- **Chapter format:** See [STYLE-GUIDE.md](STYLE-GUIDE.md)
- **Polyphonic drafting (operator):** [POLYPHONY-WORKFLOW.md](POLYPHONY-WORKFLOW.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â CIV-MIND passes on a neutral spine, then public translation (no mind names in chapter prose)
- **Architecture SSOT:** [book-architecture.yaml](book-architecture.yaml) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â all chapters, volumes, sub-groups, arcs
- **PH wiring SSOT:** [cross-book-map.yaml](cross-book-map.yaml) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â sole source of truth for Predictive History ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Â History Notebook links
- **Growth model:** One volume at a time ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â design ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ write ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ validate
- **Strategy notebook (fast judgment):** [../strategy-notebook/README.md](../strategy-notebook/README.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â daily **`### History resonance`** cites HN **chapter ids** and mechanism lines; see [STRATEGY-NOTEBOOK-ARCHITECTURE Ãƒâ€šÃ‚Â§ Parallel to History notebook](../strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#parallel-to-history-notebook-lib-0156). Do not duplicate full chapters in `days.md`.

---

## Volume structure

| Volume | Era | Chapters |
|--------|-----|----------|
| **I ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ancient Empires** (to 476 AD) | Twenty **problem-led** chapters (comparative ancient evidence); see [research/VOL-I-PROBLEM-CHAPTERS.md](research/VOL-I-PROBLEM-CHAPTERS.md) | `hn-i-v1-01` ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ `hn-i-v1-20` (legacy civ draft: [chapters/vol-i/persia.md](chapters/vol-i/persia.md)) |
| **II ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Medieval** (476 ADÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“1453 AD) | Post-Roman reconfigurations: Islam, Byzantium, Mongol disruption | islam, rome-byzantine, persia-islamic, mongol, china-medieval |
| **III ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Colonial** (1453ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“1815) | Ottoman peak, maritime expansion, continental consolidation through the Napoleonic settlement | ottoman, anglia, france, russia |
| **IV ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Industrial** (1815ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“1945) | Post-Vienna order, total war, imperial collapse | america, germany, russia-imperial, anglia-imperial |
| **V ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Modern** (1945ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“present) | Cold War, unipolarity, current crisis landscape | america-hegemonic, china-modern, russia-modern, persia-modern |
| **Appendix** | Methodology | method |

---

## Civilization arcs

Civilizations that span multiple volumes. The arc registry lives in `book-architecture.yaml`; chapters in each arc connect with cross-volume bridge prose (see [STYLE-GUIDE.md](STYLE-GUIDE.md#cross-volume-bridges-style-convention)).

**Phase 1 thread files** (operator roster): eight longitudinal surfaces in [threads/](threads/) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `history-civ-persia`, `russia`, `china`, `rome`, `islam`, `america`, `germania`, `india`. **Folds:** Francia and France are folded into the **Rome** thread; **Anglia** is folded into the **America** thread (no standalone `history-civ-anglia`).

| Arc | Chapters | Thread |
|-----|----------|--------|
| **Persian** | Vol I (`hn-i-v1-19`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ II ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ V | [history-civ-persia.md](threads/history-civ-persia.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â tolerance ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ compression ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ siege governance. |
| **Roman / Latin West** | Vol I (`hn-i-v1-04`, `hn-i-v1-05`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ II | [history-civ-rome.md](threads/history-civ-rome.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â administration and expansion; **Francia and France** live in this lane where analytically relevant. |
| **Islamic** | Vol II (`hn-ii-islam`) and related | [history-civ-islam.md](threads/history-civ-islam.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â civilizational-religious continuity. |
| **Indian** | Comparative Vol I (e.g. `hn-i-v1-12`, `hn-i-v1-16`, `hn-i-v1-18`) | [history-civ-india.md](threads/history-civ-india.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â plural incorporation and civilizational depth. |
| **Chinese** | Vol I (`hn-i-v1-16` ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ `hn-i-v1-18`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ II ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ V | [history-civ-china.md](threads/history-civ-china.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cyclical reunification ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ bureaucratic maturity ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ patience as strategy. |
| **Russian** | III ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ IV ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ V | [history-civ-russia.md](threads/history-civ-russia.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â marginal resilience ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ rupture-regeneration ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ temporal compression. |
| **Germania** | IV (`hn-iv-germany`) and adjacent | [history-civ-germania.md](threads/history-civ-germania.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â continental strategic continuity. |
| **American / Anglian** | III (`hn-iii-anglia`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ IV ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ V | [history-civ-america.md](threads/history-civ-america.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â constitutional republic ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ industrial hegemon ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ overextension; **Anglia** (maritime hegemony ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ managed decline) folded here. |

---

## PH wiring ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "addresses all of Jiang's theories"

`cross-book-map.yaml` maps all 8 PH theses and 20 concepts to HN chapters. Validate coverage with:

```bash
python3 scripts/validate_cross_book.py
```

### Volume wiring checklist

When starting a new volume:

1. **Pre-map** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Open `cross-book-map.yaml` and assign the volume's chapters to the theses and concepts they will address. Set `coverage: partial` (or leave `stub` for concepts the volume doesn't touch).
2. **Write** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Draft chapters per [STYLE-GUIDE.md](STYLE-GUIDE.md). Formation dimensions are natural anchors for PH concepts: education-narrative ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ education, religious-legitimacy ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ religion, financialization-empire ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ economics.
3. **Validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Run `validate_cross_book.py`. Review coverage gaps and orphan chapters.
4. **Update** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Promote coverage values in `cross-book-map.yaml` as chapters are completed. Update chapter `status` in `book-architecture.yaml`.

One file to edit for wiring: `cross-book-map.yaml`. No changes to PH metadata; no operator-facing fields in chapter prose.

---

## Current chapters

| ID | Volume | Title | Status |
|----|--------|-------|--------|
| `hn-i-v1-01` | I | Legitimacy After Conquest | planned |
| `hn-i-v1-02` | I | Civilizational Endurance Under Defeat | planned |
| `hn-i-v1-03` | I | When Power Changes Shape | planned |
| `hn-i-v1-04` | I | Administration, Law, and the Long Run | planned |
| `hn-i-v1-05` | I | Expansion Ceilings, Glory, and Consolidation | planned |
| `hn-i-v1-06` | I | Sea Roads and Circulation Empires | planned |
| `hn-i-v1-07` | I | Inclusion, Occupation, Annihilation | planned |
| `hn-i-v1-08` | I | Institutions Against Genius | planned |
| `hn-i-v1-09` | I | Copying, Standardization, Selective Absorption | planned |
| `hn-i-v1-10` | I | From Subjects to Stakeholders | planned |
| `hn-i-v1-11` | I | Territorial Maximum, Strategic Maximum, Overreach | planned |
| `hn-i-v1-12` | I | Geography of Origin and Permanence | planned |
| `hn-i-v1-13` | I | Mechanism Failure at the Frontier | planned |
| `hn-i-v1-14` | I | Elite Defection and the Shape of Defeat | planned |
| `hn-i-v1-15` | I | Deflection and Ambivalence Toward Outside Orders | planned |
| `hn-i-v1-16` | I | Non-Native Rule, Hybridity, Peak, Exhaustion | planned |
| `hn-i-v1-17` | I | Fragmentation and Monopoly of Authority | planned |
| `hn-i-v1-18` | I | Corridors, Exchange, Legibility, Aftermath of Conquest | planned |
| `hn-i-v1-19` | I | Parity, Buffers, Exhaustion, Third Shock | planned |
| `hn-i-v1-20` | I | Collapse, Vacancy, Succession | planned |
| `hn-ii-islam` | II | Islam ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Rashidun to Abbasid Caliphate | planned |
| `hn-ii-rome-byzantine` | II | Byzantium ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Eastern Roman Survival | planned |
| `hn-ii-persia-islamic` | II | Persia ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Post-Conquest to Timurid | planned |
| `hn-ii-mongol` | II | Mongol ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Steppe Cycle and Disruption | planned |
| `hn-ii-china-medieval` | II | China ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Tang to Ming | planned |
| `hn-iii-ottoman` | III | Ottoman ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Rise to Stagnation | planned |
| `hn-iii-anglia` | III | England ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Tudor to Colonial Order | planned |
| `hn-iii-france` | III | France ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Old Regime through 1815 | planned |
| `hn-iii-russia` | III | Russia ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Muscovy to Catherine | planned |
| `hn-iv-america` | IV | America ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Republic to Global Hegemony | planned |
| `hn-iv-germany` | IV | Germany ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Unification to Catastrophe | planned |
| `hn-iv-russia-imperial` | IV | Russia ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 1815 to Soviet | planned |
| `hn-iv-anglia-imperial` | IV | England ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Pax Britannica to World Wars | planned |
| `hn-v-america-hegemonic` | V | America ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Cold War to Overreach | planned |
| `hn-v-russia-modern` | V | Russia ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Soviet Collapse to Putin | planned |
| `hn-v-persia-modern` | V | Persia ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Islamic Republic to War Phase | planned |
| `hn-v-china-modern` | V | China ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PRC to Belt and Road | planned |
| `hn-app-method` | Appendix | How Jiang Thinks ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Methodology | planned |

---

## Conventions

- **Operator-authored**, not auto-generated ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the value is in the compression and judgment
- **Independent growth** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â adding a chapter does not require updating CIV-MEM; CIV-MEM growth does not require updating chapters (though it may prompt revision)
- **Inline pattern tags** (`[pattern:X]`) enable future script extraction of an axiom deck without building one now
- **WORK only** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not Record, not Voice knowledge unless gated
- **Public / operator boundary** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â chapter prose is public; metadata lives in YAML only (see [STYLE-GUIDE.md](STYLE-GUIDE.md))

