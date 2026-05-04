# Notebook contract - strategy-codex
<!-- word_count: 372 -->

WORK only; not Record.

**Purpose:** Shared hub for the canonical bundle. Normative detail lives in the files below; do not duplicate long excerpts here.

## Center of gravity

- **Cognition streams** are the top-level analytical scaffold; **pages** are the primary composed unit; legacy **`thread:<expert_id>`** handles remain routing/provenance joins; **raw-input** is the literal SSOT.
- The canonical page and scaffold shapes now live in [strategy-codex-template-page.md](strategy-codex-template-page.md), [strategy-codex-template-chapter.md](strategy-codex-template-chapter.md), and [strategy-codex-template-book.md](strategy-codex-template-book.md). Legacy `strategy-expert-template.md` anchors remain compatibility redirects while links are updated.
- Month continuity in the thread journal layer is a short bookended synthesis of that month's `strategy-page` set. See [COGNITION-STREAMS.md](COGNITION-STREAMS.md), [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology), and the thread section of [strategy-expert-template.md](strategy-expert-template.md#thread-template).

## Compatibility naming

Use this naming split consistently:

- **strategy-codex** = the active public name for the notebook/workspace.
- **strategy-notebook** = the legacy path and file-contract name still present on disk and in some tooling.
- **strategy-author** = the active public name for the author lane / analytical voice tracked in the codex.
- **strategy-expert** = the legacy filename, parser, and marker contract still present in templates, scripts, and tests.

Editing rule:

- Prefer the new names in prose and operator-facing guidance.
- Preserve the old names where they are part of a live contract: paths, filenames, markers, regexes, fixtures, and generated artifacts.

If a document needs both names, make the compatibility status explicit rather than silently swapping terms.

**Why this matters:** Future agents need one clean distinction before they write: use raw-input and refined pages to preserve and cite what was said; use cognition streams to choose the interpretive lane; use thread-embedded `strategy-page` blocks to compose what the notebook thinks. That split keeps evidence, routing, continuity, and judgment from collapsing into one ambiguous file.

**Brief advisory:** Before composing a major strategy page or public-facing synthesis, write or infer a WORK job brief: audience, objective, evidence surface, success criteria, and acceptance check. This is a drift-control aid, not a requirement for every page and not a substitute for the page/thread contract.

**Watch / worry:** Do not let the brief become a mandatory ceremony for ordinary page edits. The brief exists to clarify ambiguous, public-facing, or delegation-shaped work; when the page shape is already obvious from raw-input, thread context, and operator direction, proceed with the page contract.

**Elicitation checkpoint:** When stream ownership, raw-input routing, page shape, contrapuntal relation, or civ-mem lens choice is unclear, use `skill-elicitation` as an optional bounded checkpoint before writing. It should surface operator judgment and then return to the existing page/thread contract; it is not a new compose path and not an automatic coffee or dream action.

## Page-thread binding

**Author surfaces are siblings, not a hierarchy:** **Thread / Continuity** tracks temporal narrative and analytical continuity; **Pages / Work Product** are focused author-associated analytical objects. Keep a small bidirectional index, but do not duplicate the page.

**Standalone refined pages** use these continuity bullets in `### Appendix`:

```markdown
- **Thread file:** [experts/<expert_id>/<expert_id>-thread-YYYY-MM.md](experts/<expert_id>/<expert_id>-thread-YYYY-MM.md)  <!-- or legacy thread.md -->
- **Thread month:** `YYYY-MM`
- **Thread role:** `new-thesis` | `update` | `contradiction` | `falsifier` | `synthesis` | `carry-forward`
- **Continuity delta:** One sentence naming what this page changes, clarifies, or carries forward in the author continuity.
```

**Thread month segments** should carry a compact page index when adopted:

```markdown
### Pages / Work Product

- YYYY-MM-DD - [Page title](<page path>)
  role: carry-forward
  delta: One sentence saying what the page contributes to continuity.
```

The thread index **does not duplicate** the page. It answers: *why does this page matter to this author's temporal continuity?*

**Drafting flow:** before picking the excerpt body for a refined page, reduce the prior month thread files into a bounded context packet. The packet is a compose aid only: it orients quote selection and synthesis, while `raw-input/` remains the literal SSOT.

**Source-first ingest:** `raw-input/` may hold transcripts, essays, posts, bundles, or other captures even when the speaker or outlet does **not** map to an existing author folder. Keep it unthreaded unless later routing assigns it to an existing lane.

**Selective backfill rule:** When using archive or feed discovery to populate `raw-input/`, treat the archive as a discovery index, not a completeness mandate. Backfill the substantial items you want preserved; leave light, repetitive, or low-signal archive-visible items out when that is the better editorial choice.

## Where the rules live

Use this file as the routing hub. If another notebook document appears to duplicate a rule, prefer the narrower owner below: template syntax in `strategy-expert-template.md`, operational architecture in `STRATEGY-NOTEBOOK-ARCHITECTURE.md`, script receipts in the trace contract, and source-capture policy in `raw-input/README.md` plus `raw-input/BACKFILL-SOURCES.md`. Keep this hub short rather than copying those rules here.

| Topic | Document / tool |
|-------|-----------------|
| Cognition stream scaffold | [COGNITION-STREAMS.md](COGNITION-STREAMS.md) |
| Fence syntax, page template | [strategy-codex-template-page.md#strategy-page---thread-fence-page](strategy-codex-template-page.md#strategy-page---thread-fence-page) |
| Refined page scaffold | [strategy-codex-template-page.md#refined-page---expertsexpert_idexpert_id-page-yyyy-mm-ddmd](strategy-codex-template-page.md#refined-page---expertsexpert_idexpert_id-page-yyyy-mm-ddmd) |
| Chapter scaffold | [strategy-codex-template-chapter.md](strategy-codex-template-chapter.md) |
| Book scaffold | [strategy-codex-template-book.md](strategy-codex-template-book.md) |
| Thread layers (journal vs machine), parse contract | [STRATEGY-NOTEBOOK-ARCHITECTURE.md Â§ Thread](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) |
| Backfill source-family routing | [raw-input/BACKFILL-SOURCES.md](raw-input/BACKFILL-SOURCES.md) |
| `watch=` and multi-author duplicate pages | [watches/README.md](watches/README.md) (page format) |
| Validation | From repo root: `python3 scripts/validate_strategy_pages.py` - [validate_strategy_pages.py](../../../../scripts/validate_strategy_pages.py) |
| Machine **`### Page references`** | [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) (machine layer) |
| Bundled read-only multi-author snapshots | [compiled-views/README.md](compiled-views/README.md) - **derived**, not SSOT |
| Trace and receipts (script runs) | [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](STRATEGY-NOTEBOOK-TRACE-CONTRACT.md) |
| Page update operations (script / propose) | [STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md](STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md) |
| Derived graph (rebuild) | [GRAPH-SCHEMA.md](GRAPH-SCHEMA.md), `build_strategy_notebook_graph.py` |

## Multi-author pages

When several authors address the same page, the **same `id=`** appears in each author's **thread file for that month** (see [watches/README.md](watches/README.md)). This is **intentional** duplication for per-lane reading; **not** multiple competing sources of truth.

## Refined pages (standalone `*-page-*.md`)

**Standalone refined pages** use the canonical section in [strategy-codex-template-page.md](strategy-codex-template-page.md#refined-page---expertsexpert_idexpert_id-page-yyyy-mm-ddmd). They are **source/verbatim support and citation handles** for `thread` / `days.md` / analysis, not the primary composed analysis unit. Keep **`### Verbatim`** as the quote body, with **`### Reflection`** / **`### Predictive Outlook`** available for local judgment on that capture. Target is **~3000** words, with **~70-80%** in `### Verbatim`.

**Primary composed analysis** lives in thread-embedded **`strategy-page`** blocks during the EOD strategy session. Refined pages should make the evidence easier to cite and route; they do not replace the `strategy-page` fence as the notebook's analytical unit.

**Rule of shape:** one file per publication day by default, with `-<slug>` splitting when needed. Keep `### Appendix` for machinery only. The raw file under `raw-input/` remains the full capture.
