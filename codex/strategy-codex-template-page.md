# Strategy-codex template - strategy-page
<!-- word_count: canonical scaffold -->


**Purpose:** Canonical template for a standalone **strategy-page**: a stream-level analytical object that can be read as public-draft prose while retaining source receipts.

**Companion contracts:** [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md) · [THREAD-CONTRACT.md](THREAD-CONTRACT.md)

## Glossary

- **Strategy-page:** a standalone analytical object for one cognition stream.
- **Strategy-chapter:** a daily synthesis across relevant cognition streams and strategy-pages.
- **Strategy-book:** a month-level synthesis and coordination surface.
- **Source capture:** literal source material; it is evidence, not a strategy-page.

## Location and naming

Store new strategy-pages as standalone files:

```text
codex/<year>/<stream>/<stream>-page-YYYY-MM-DD[-slug].md
```

Examples:

- `statecraft/voices/mercouris/mercouris-page-2026-05-01.md`
- `statecraft/voices/pape/pape-page-2026-05-01-escalation-trap.md`

The old distinction between `codex-page` and thread-fenced `strategy-page` is legacy compatibility only. Existing files and `<!-- strategy-page:start ... -->` blocks remain readable/importable, but new writing should use the standalone strategy-page shape above.

## Public-draft body rules

The body should be readable by an outside audience. Avoid backend jargon in body prose, including `civ-mem`, `WORK`, `Record`, `raw-input`, `source_mode`, `strategy-codex`, and internal path talk. Internal paths and process terms belong only in `### Sources`, examples, or tooling docs.

Prefer bullet-point argumentation supported by source material:

- `### Signal` and major `### Judgment` bullets should be supported by a verbatim quote, explicit source fact, or explicit inference.
- When quoting, use 1-3 full sentences.
- If no source text exists, do not fabricate quotes; use prompt premises or source facts and label them plainly.

Every strategy-page should use historical-pattern reasoning, but it should appear as public analysis rather than backend language. A brief argument bullet can satisfy this when the analogy is not load-bearing; use the phrase "historical pattern" only when it improves clarity.

## Required sections

- `### Signal` = evidence-rich threshold section: what made the page worth writing.
- `### Judgment` = argument-step reasoning, with live tensions preserved.
- `### Prediction` = up to three revisitable loops when claims are separable.
- `### Sources` = source links or receipts only.

Prediction loops use this shape:

```markdown
- **Prediction:** <falsifiable expectation or interpretive claim>
- **Falsifier:** <what would weaken or overturn it>
- **Revisit:** <date, event, or threshold>
```

## Skeleton

```markdown
# <Public title>

**Date:** YYYY-MM-DD
**Status:** Draft strategy-page
**Stream:** <stream>

### Signal

- <Source claim or observation that crossed the threshold. Include a 1-3 sentence quote when source text exists.>

### Judgment

- <Argument step supported by quote, source fact, or explicit inference.>
- <Historical-pattern reasoning in public prose, if it sharpens the judgment.>
- <Tension, mismatch, or weakest part of the claim.>

### Prediction

- **Prediction:** <falsifiable expectation or interpretive claim>
- **Falsifier:** <what would weaken or overturn it>
- **Revisit:** <date, event, or threshold>

### Sources

- <source link or receipt>
```

## Relationship to chapters and books

Strategy-pages carry stream-level analysis. Strategy-chapters synthesize multiple strategy-pages across the day. Strategy-books coordinate the month.
