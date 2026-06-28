# Notebook contract - strategy-codex
<!-- word_count: 372 -->

WORK only; not Record.

**Purpose:** Shared hub for the canonical bundle. Normative detail lives in the files below; do not duplicate long excerpts here.

## Center of gravity

- **Cognition streams** are the top-level analytical scaffold; **strategy-pages** are standalone stream-level analytical objects; **strategy-chapters** are daily synthesis across streams; legacy **`thread:<expert_id>`** handles remain routing/source-archive joins; **source-archive** is the literal SSOT for full source capture.
- The canonical scaffold shapes now live in [strategy-codex-template-raw-input.md](strategy-codex-template-raw-input.md), [strategy-codex-template-page.md](strategy-codex-template-page.md), [strategy-codex-template-chapter.md](strategy-codex-template-chapter.md), and [strategy-codex-template-book.md](strategy-codex-template-book.md). Legacy `strategy-expert-template.md` anchors remain compatibility redirects while links are updated.
- Month continuity in the thread journal layer is a short bookended synthesis and index of that month's standalone strategy-page set. See [COGNITION-STREAMS.md](COGNITION-STREAMS.md), [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology), and [speakers/_templates/speaker-thread-template.md](../statecraft/voices/_templates/speaker-thread-template.md).

## Compatibility naming

Use this naming split consistently:

- **strategy-codex** = the active public name for the notebook/workspace.
- **strategy-notebook** = a deprecated compatibility name still present on disk and in some tooling.
- **strategy-author** = the active public name for the author lane / analytical voice tracked in the codex.
- **strategy-expert** = the legacy filename, parser, and marker contract still present in templates, scripts, and tests.

Editing rule:

- Prefer the new names in prose and operator-facing guidance.
- Preserve the old names where they are part of a live contract: paths, filenames, markers, regexes, fixtures, and generated artifacts.

If a document needs both names, make the compatibility status explicit rather than silently swapping terms.

**Why this matters:** Future agents need one clean distinction before they write: source capture preserves what was said; strategy-pages make stream-level judgment; strategy-chapters synthesize the day. Legacy `codex-page` language and thread-fenced `strategy-page` blocks remain readable/importable, but they are not the preferred shape for new writing.

**Strategy-state model:** strategy-codex uses a four-part state split. **Knowledge** = governed understanding and owned judgment. **Library** = governed reference world and return-to sources. **Memory** = resumable continuity and open-loop state. **Archive** = governed evidence and provenance spine. In notebook terms: source capture is archive-adjacent literal capture, standalone strategy-pages bridge archive toward knowledge, and strategy-chapters are daily memory/synthesis.

**Judgment loop:** strategy-codex should compound durable judgment, not just archive surfaces. Every substantive strategy-page should leave behind a compact loop: **Prediction**, **Falsifier**, and **Revisit**. Later strategy-chapter continuity should say whether the earlier prediction **held**, **weakened**, **broke**, or is **still open**. Legacy **Call / Falsifier / Revisit** loops remain parseable. See [strategy-codex-template-page.md](strategy-codex-template-page.md) and [notes/TCLD-AUDIT-STRATEGY-CODEX.md](notes/TCLD-AUDIT-STRATEGY-CODEX.md).

**Brief advisory:** Before composing a major strategy page or public-facing synthesis, write or infer a WORK job brief: audience, objective, evidence surface, success criteria, and acceptance check. This is a drift-control aid, not a requirement for every page and not a substitute for the page/thread contract.

**Watch / worry:** Do not let the brief become a mandatory ceremony for ordinary page edits. The brief exists to clarify ambiguous, public-facing, or delegation-shaped work; when the page shape is already obvious from source capture, thread context, and operator direction, proceed with the page contract.

**Elicitation checkpoint:** When stream ownership, source-archive routing, page shape, contrapuntal relation, or civ-mem lens choice is unclear, use `skill-elicitation` as an optional bounded checkpoint before writing. It should surface operator judgment and then return to the existing page/thread contract; it is not a new compose path and not an automatic coffee or dream action.

## Page-thread binding

**Author surfaces are siblings, not a hierarchy:** **Thread / Continuity** tracks temporal narrative and analytical continuity; **Pages / Work Product** are focused author-associated analytical objects. Keep a small bidirectional index, but do not duplicate the page.

Standalone strategy-pages may use these continuity bullets in `### Sources` when stream indexing needs them:

```markdown
- **Primary source capture:** [../source-archive/statecraft/YYYY-MM-DD/<slug>.md](...)
- **Supporting source capture:** [../source-archive/statecraft/YYYY-MM-DD/<slug>.md](...)  <!-- optional; keep the set small -->
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

**Drafting flow:** before picking the Signal body for a strategy-page, reduce the prior month thread files into a bounded context packet. The packet is a compose aid only: it orients quote selection and synthesis, while source-archive capture remains the literal SSOT.

**Continuity review rule:** when a later day materially updates an earlier strategy-page or day-level judgment, record whether that earlier prediction **held**, **weakened**, **broke**, or is **still open**. Keep this lightweight and prose-native; do not turn every day into a ledger entry.

**Source-first ingest:** `source-archive/statecraft/` may hold transcripts, essays, posts, bundles, or other captures even when the speaker or outlet does **not** map to an existing author folder. Treat it as archive capture, not knowledge by itself, and keep it unthreaded unless later routing assigns it to an existing lane.

**Selective backfill rule:** When using archive or feed discovery to populate `source-archive/statecraft/`, treat the archive as a discovery index, not a completeness mandate. Backfill the substantial items you want preserved; leave light, repetitive, or low-signal archive-visible items out when that is the better editorial choice.

## Where the rules live

Use this file as the routing hub. If another notebook document appears to duplicate a rule, prefer the narrower owner below: template syntax in `strategy-expert-template.md`, operational architecture in `STRATEGY-NOTEBOOK-ARCHITECTURE.md`, script receipts in the trace contract, and source-capture policy in [`../source-archive/README.md`](../source-archive/README.md) plus `raw-input/BACKFILL-SOURCES.md`. Keep this hub short rather than copying those rules here.

| Topic | Document / tool |
|-------|-----------------|
| Cognition stream scaffold | [COGNITION-STREAMS.md](COGNITION-STREAMS.md) |
| Raw-input scaffold | [strategy-codex-template-raw-input.md](strategy-codex-template-raw-input.md) |
| Strategy-page scaffold | [strategy-codex-template-page.md](strategy-codex-template-page.md) |
| Legacy fenced page parser | [validate_strategy_pages.py](../../scripts/validate_strategy_pages.py) |
| Chapter scaffold | [strategy-codex-template-chapter.md](strategy-codex-template-chapter.md) |
| Book scaffold | [strategy-codex-template-book.md](strategy-codex-template-book.md) |
| Thread layers (journal vs machine), parse contract | [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Thread](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) |
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

## Strategy-pages (standalone `*-page-*.md`)

New strategy-pages use the canonical scaffold in [strategy-codex-template-page.md](strategy-codex-template-page.md). They are standalone stream-level analytical objects with `Signal / Judgment / Prediction / Sources`.

Legacy `codex-page` files and thread-fenced `strategy-page` blocks remain readable/importable. Do not rewrite the existing corpus just to rename those artifacts; prefer the standalone strategy-page shape for new work.

## Optional stronger tracking

For consequential calls, recurring theses, or especially important warnings, use the shared optional register at [notes/JUDGMENT-LOOP-REGISTER.md](notes/JUDGMENT-LOOP-REGISTER.md). It is an escalation surface, not a second mandatory compose path.
