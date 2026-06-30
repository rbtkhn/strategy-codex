# Strategy-codex template - strategy-chapter
<!-- word_count: 258 -->
<!-- word_count: canonical scaffold -->


**Purpose:** Canonical template for a **strategy-chapter**: the daily synthesis across relevant cognition streams and strategy-pages.

**Companion contracts:** [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md) · [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md)

## Chapter role

- **Strategy-page** = stream-level analytical object.
- **Strategy-chapter** = daily synthesis across streams.
- **Strategy-book** = month-level synthesis and coordination surface.
- **Source capture** = literal source material, not a page.

The chapter file remains:

```text
continuity/<year>/chapters/<YYYY-MM>/days.md
```

Each `## YYYY-MM-DD` block is one strategy-chapter. Default length is 1200-2000 words when the day synthesizes many pages.

## Public-draft body rules

The body should be readable by an outside audience. Avoid backend jargon in body prose, including `civ-mem`, `WORK`, `Record`, `raw-input`, `source_mode`, `strategy-codex`, and internal path talk. Internal paths and process terms belong in `### References`.

Prefer bullet-point synthesis supported by the pages being synthesized:

- Quote from already-captured strategy-page or source material when a quotation clarifies the signal.
- Use 1-3 full sentences when quoting.
- Do not re-quote large source blocks in the chapter.

## Required sections

- `### Signal` = 3-7 top cross-stream signals, deduped and thresholded.
- `### Judgment` = synthesis plus seams; preserve contradictions between streams rather than smoothing them away.
- `### Prediction` = carry forward only the 1-3 most important page predictions, contradictions, or open loops.
- `### References` = compact "Pages synthesized" list plus source links.

Prediction loops use this shape:

```markdown
- **Prediction:** <falsifiable expectation or interpretive claim>
- **Falsifier:** <what would weaken or overturn it>
- **Revisit:** <date, event, or threshold>
```

## Skeleton

```markdown
## YYYY-MM-DD

**Status:** Draft strategy-chapter

### Signal

- <Top cross-stream signal, with a short quote if it sharpens the point.>
- <Second signal.>

### Judgment

- <Daily synthesis across streams.>
- <Seam or contradiction that should remain visible.>

### Prediction

- **Prediction:** <most important carried-forward expectation or interpretive claim>
- **Falsifier:** <what would weaken or overturn it>
- **Revisit:** <date, event, or threshold>

### References

**Pages synthesized:**

- [<strategy-page title>](../../<stream>/<stream>-page-YYYY-MM-DD.md)

**Sources:**

- <source link or receipt>
```

## Relationship to pages and books

Strategy-chapters coordinate the day. They should synthesize strategy-pages, not duplicate each page body. Let the strategy-book summarize the month rather than bloating the chapter with month-scale recap.
