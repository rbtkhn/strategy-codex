# Strategy-codex template - raw-input
<!-- word_count: canonical scaffold -->


**Purpose:** Canonical raw-input template for strategy-codex. This file owns the literal capture scaffold below codex-pages, strategy-pages, chapters, and books.

**Companion contracts:** [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md) · [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md)

## Raw-input role

- **Raw-input** = literal SSOT for captured words and source material
- **codex-pages** = quoted/cited support with local reflection
- **strategy-pages / chapters / books** = composed notebook judgment and continuity

Use `raw-input/` to preserve what was actually said or published. Do not convert the file into notebook analysis.

## On-disk shape

Use this layout consistently:

```text
raw-input/
  _aired-pending/        <- temporary holding area when pub_date is not fixed yet
  YYYY-MM-DD/
    <slug>.md
```

Rules:

- The folder date matches `pub_date`.
- `ingest_date` records when the file entered the tree; it does not control the folder name.
- `_aired-pending/` is a temporary recovery exception only. Move the file into `raw-input/YYYY-MM-DD/` once `pub_date` is known.

## Raw capture scaffold

Use this for a literal capture file:

```markdown
---
ingest_date: YYYY-MM-DD
pub_date: YYYY-MM-DD
source_url: https://...
kind: transcript | paste-bundle | rss-item | x-post-text | shortform-bundle | mixed
thread: expert_id
---

# Human-readable title

Full literal body.
```

## Frontmatter notes

- `ingest_date` = when the file entered this tree
- `pub_date` = when the source went public
- `source_url` = canonical or best available source URL
- `kind` = capture class; keep the detailed kind policy in `raw-input/CAPTURE-TYPES.md`
- `thread` = optional for source-first captures that do not yet belong to a lane

When `thread:` is present for an interview or host-led stream, it should name the owning host/interviewer lane rather than every notable guest.

One raw-input capture usually feeds one primary downstream codex-page. Multiple codex-pages may cite the same raw-input file when ownership splits require separate host/guest or channel readings.

## Body expectations

- Start with a human-readable title.
- Preserve the full literal body after the title.
- Optional light headings are fine only when they preserve source clarity.
- Do not pre-summarize, condense into notebook judgment, or rewrite the source into page prose here.

## Naming discipline for transcript captures

When a raw-input transcript mixes **source-faithful identifiers** with **editorial structure**, keep the two layers distinct:

- **Source-faithful fields** keep the source's own public naming as-is: `channel_slug`, `source_url`, `canonical_url`, quoted `Title (YouTube)` lines, `Channel:` labels, and verbatim quoted transcript content.
- **Editorial fields** may use the notebook's own normalization style: `author`, `host`, `interviewer`, `show`, `slug`, speaker labels, and assistant-added headings.
- For designated stream transcripts where the lane is already the owning cue (for example `transcript-diesen-*`), prefer **surname-style editorial labels** such as `Diesen` in assistant-added metadata and speaker tags unless a stronger local convention already exists.
- If a source title or spoken line itself says `Glenn Diesen`, preserve it when you are quoting the source rather than labeling it.

Before closeout on a transcript capture, do a quick **editorial name drift** pass:

- check that assistant-added labels match the lane's editorial convention
- check that source identifiers were not "normalized" away from their public names
- check that filenames and `channel_slug` still preserve stable routing

## Relationship to other raw-input docs

- Use this file for **shape**: folder/date convention, frontmatter, and literal-body expectations.
- Use this file as the literal source layer for downstream **codex-page** citation and **strategy-page** synthesis.
- Keep **capture-type policy**, **backfill source families**, **automation workflows**, and **pruning** in the raw-input docs under `2026/raw-input/`.
