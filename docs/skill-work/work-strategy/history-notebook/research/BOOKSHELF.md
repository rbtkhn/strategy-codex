# Bookshelf

**WORK only;** not Record.

**Collection name:** **self-library-bookshelf** â€” the operatorâ€™s **physical print library** (300-title-class scale), cataloged under this heading and in [`bookshelf-catalog.yaml`](bookshelf-catalog.yaml) as `HNSRC-*` rows. Same thing as â€œBookshelfâ€ / [LIB-0158](../../../../self-library.md#bookshelf) in the self-library index; the name **self-library-bookshelf** stresses **self-library** as the home for the **shelf** list.

**Bookshelf** is the operatorâ€™s **owned print library** expressed as an **enhanced bibliography**: **title-level metadata** (and optional planning hints) for physical books you keep â€” **not** full text, not a reading corpus, and **not** an operator-authored â€œbookâ€ in the [Operator analytical books](../../../../self-library.md#operator-analytical-books) sense.

## Distinct from operator books

| | **Bookshelf (this doc)** | **Operator analytical books** (e.g. [LIB-0156](../../../../self-library.md#operator-analytical-books) History notebook, [LIB-0153](../../../../self-library.md#operator-analytical-books) strategy notebook) |
|---|-------------------------|----------------------------------|
| **What it is** | Third-party print you own; bibliographic rows + optional `HNSRC-*` hooks to drafting | **Operator-authored** structured corpora (chapters, journals, multivolume spines) under grace-mar |
| **Grain** | Citation / shelf / era / tags â€” *enhanced bib*, not a repository of page content | Prose, meta, and README SSOTs meant for **analysis, judgment, and synthesis** |
| **Self-library** | [LIB-0158 â€” Bookshelf](../../../../self-library.md#bookshelf) Â· `shelf_intent: working_reference` (not `operator_book`) | `shelf_intent: operator_book` + `operator_analytical` scope where applicable |

**Rule of thumb:** If it would live in a zotero row or a library catalog card, it belongs on **Bookshelf**. If *you* are writing the â€œbookâ€ in-repo, it belongs under **Operator analytical books**.

## Machine-readable SSOT (the actual list)

The **full, enumerated Bookshelf** (every volume row) is **only** in:

- [`bookshelf-catalog.yaml`](bookshelf-catalog.yaml) â€” `HNSRC-*` items (title, author, era, tags, optional `candidate_hn_chapters`, etc.).

This file is the **bibliography database**. It does **not** store scanned text; optional `content_path` in schema is for a future **phase 2** (see comments in the YAML header).

**Formal bibliography (generated, not a second hand-maintained list):** [research/bibliography/](bibliography/) â€” Chicago *authorâ€“date* (simplified) Markdown built from this YAML by `python3 scripts/build_hn_bookshelf_bibliography.py`. Optional fields (`place`, `publisher`, â€¦) in the header comment; sparse `year` rows show as `n.d.`

**Writer ergonomics (inverse index + lookups):** [SHELF-ANCHORS-BY-CHAPTER.md](SHELF-ANCHORS-BY-CHAPTER.md) â€” `hn-*` chapter id â†’ HNSRC list. Regen: `python3 scripts/hn_shelf_anchors.py`. One-line **card** for a shelf id: `python3 scripts/hn_shelf_anchors.py --hnsrc HNSRC-0001`. **Paste line** for a chapter draft: `--stub-line hn-i-v1-01`. **Cited fragment** (subset bib): `python3 scripts/build_hn_bookshelf_bibliography.py --cited-ids â€¦` â€” see [.cursor/skills/hn-bookshelf-lookup/SKILL.md](../../../../.cursor/skills/hn-bookshelf-lookup/SKILL.md).

**Agentic drafting outputs:** [QUEUE-AUTOPRIORITY.md](QUEUE-AUTOPRIORITY.md), [PROVENANCE-PACKETS.md](PROVENANCE-PACKETS.md), and [REDTEAM-FINDINGS.md](REDTEAM-FINDINGS.md), regenerated with scripts in [AGENTIC-MVP-RUNBOOK.md](AGENTIC-MVP-RUNBOOK.md).

**Runbook** (batches, era rules, upload order): [BOOKSHELF-RUNBOOK.md](BOOKSHELF-RUNBOOK.md).

## How it connects to History Notebook

Bookshelf rows **inform** [History Notebook](../README.md) chapter drafting (which problems, which primary arcs) â€” they do **not** replace [`book-architecture.yaml`](../book-architecture.yaml) or the **`hn-*`** deliverables. Treat the catalog as a **shelf-ordered, enriched bibliography** behind your judgment, not a chapter dump.

## See also

- [History Notebook â€” STYLE-GUIDE Â§ Bookshelf era buckets](../STYLE-GUIDE.md#bookshelf-era-buckets) â€” era vocabulary in prose.
- [artifacts/library-index.md](../../../../../artifacts/library-index.md) â€” operator dashboard; includes **LIB-0158** in entry summaries, not the HNSRC title list.

