# Strategy-codex template - raw-input
<!-- word_count: canonical scaffold -->

WORK only; not Record.

**Purpose:** Canonical raw-input template for strategy-codex. This file owns the literal capture scaffold below refined pages, strategy pages, chapters, and books.

**Companion contracts:** [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md) · [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md)

## Raw-input role

- **Raw-input** = literal SSOT for captured words and source material
- **Refined pages** = quoted/cited support with local reflection
- **Strategy pages / chapters / books** = composed notebook judgment and continuity

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
kind: transcript | paste-bundle | rss-item | x-post-text | mixed
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

## Body expectations

- Start with a human-readable title.
- Preserve the full literal body after the title.
- Optional light headings are fine only when they preserve source clarity.
- Do not pre-summarize, condense into notebook judgment, or rewrite the source into page prose here.

## Relationship to other raw-input docs

- Use this file for **shape**: folder/date convention, frontmatter, and literal-body expectations.
- Keep **capture-type policy**, **backfill source families**, **automation workflows**, and **pruning** in the raw-input docs under `2026/raw-input/`.
