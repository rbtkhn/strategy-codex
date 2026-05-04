# Strategy-codex template - page
<!-- word_count: canonical scaffold -->

WORK only; not Record.

**Purpose:** Canonical page template for strategy-codex. This file owns the two page-shaped analytical surfaces:

- **refined page** = standalone source-support page under `experts/<expert_id>/`
- **strategy page** = thread-embedded analytical page inside a month thread

**Companion contracts:** [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md) · [THREAD-CONTRACT.md](THREAD-CONTRACT.md)

## Page family

Use this naming split consistently:

- **Page** = the general analytical unit in strategy-codex.
- **Refined page** = the standalone citation/support page for one primary capture.
- **Strategy page** = the thread-embedded analytical page composed during the strategy session.

Raw wording lives in `raw-input/`; pages are the first analytical layer above literal capture.

---

## Refined page -> `experts/<expert_id>/<expert_id>-page-YYYY-MM-DD.md`

# Cognition stream refined page - `<expert_id>`

WORK only; not Record.

Use this when the page should stand on its own outside the thread while preserving a direct citation handle back to `raw-input/`.

**Surface rules:**

- `### Verbatim` = curated quote body from `raw-input/`
- `### Reflection` = operator analysis grounded in that capture
- `### Predictive Outlook` = tracked expectations, status, and short forecast notes for the stream
- `### Appendix` = machinery only

**Skeleton:**

```markdown
# <Stream / author> refined page - YYYY-MM-DD
WORK only; not Record.

**Cognition stream:** `<expert_id>` · **Published:** YYYY-MM-DD · **Artifact:** refined page.

---

### Verbatim

### Reflection

### Predictive Outlook

---

### Appendix
```

**Rule of use:** refined pages are source/verbatim support and durable citation handles for `thread`, `days.md`, and later synthesis. They do not replace the main analytical role of `strategy-page` blocks.

---

## Strategy page -> thread-fence page

# Cognition stream strategy page - `<expert_id>`

WORK only; not Record.

Use this inside `experts/<expert_id>/<expert_id>-thread-YYYY-MM.md` or legacy `thread.md`.

**Surface rules:**

- `### Chronicle` = curated quote body or distilled evidentiary line
- `### Reflection` = operator analysis
- `### Predictive Outlook` = tracked expectations, status, and short forecast notes for the stream
- `### Appendix` = machinery only

**Skeleton:**

```markdown
<!-- strategy-page:start id="<kebab-id>" date="YYYY-MM-DD" watch="<optional-watch-slug>" -->
### Page: <human title>

### Chronicle

### Reflection

### Predictive Outlook

---

### Appendix
<!-- strategy-page:end -->
```

**Rule of use:** the strategy page is the notebook's primary composed analytical unit. Use refined pages to support and cite it, not to compete with it.

---

## Relationship to other templates

- Month continuity and chapter rhythm belong to [strategy-codex-template-book.md](strategy-codex-template-book.md) and [strategy-codex-template-chapter.md](strategy-codex-template-chapter.md).
- Legacy file-contract references to `strategy-expert-template.md` may persist while links are being updated.