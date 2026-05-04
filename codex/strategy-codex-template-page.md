# Strategy-codex template - page
<!-- word_count: canonical scaffold -->

WORK only; not Record.

**Purpose:** Canonical page template for strategy-codex. This file owns the two page-shaped analytical surfaces:

- **codex-page** = standalone source-support page in the owning year/channel folder
- **strategy-page** = thread-embedded analytical page inside a month thread

**Companion contracts:** [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md) · [THREAD-CONTRACT.md](THREAD-CONTRACT.md)

## Page family

Use this naming split consistently:

- **Page** = the general analytical unit in strategy-codex.
- **codex-page** = the standalone citation/support page for one primary capture.
- **strategy-page** = the thread-embedded analytical page composed during the strategy session.

Never use bare **page** where the contrast matters. In those cases, say **codex-page** or **strategy-page** explicitly.

Raw wording lives in `raw-input/`; pages are the first analytical layer above literal capture.

## Judgment loop

Every substantive analytical page should leave behind a compact, revisitable judgment loop:

1. make or refine a call
2. name a falsifier
3. name a revisit trigger or horizon
4. later record whether the call held, weakened, broke, or remains open

This is the notebook's defense against `T + C` drift: evidence alone is not enough if the page leaves no way to revisit what it claimed.

---

## codex-page -> `codex/<year>/<channel>/<expert_id>-page-YYYY-MM-DD.md`

# Cognition stream codex-page - `<expert_id>`

WORK only; not Record.

Use this when the standalone page should stand on its own outside the thread while preserving a direct citation handle back to `raw-input/`.

**Location and naming rules:**

- Store the file in the owning year/channel folder, for example `codex/2026/mercouris/mercouris-page-2026-05-01.md`.
- Keep expert-first basenames: `<expert_id>-page-YYYY-MM-DD.md`.
- When more than one same-day page is needed, use `<expert_id>-page-YYYY-MM-DD-<slug>.md`.
- One raw-input capture usually feeds one primary codex-page, but multiple codex-pages may cite the same raw-input file when host/guest or channel ownership splits are intentional.

**Surface rules:**

- `### Verbatim` = curated excerpts from one primary raw-input source
- `### Reflection` = operator analysis grounded in that capture
- `### Predictive Outlook` = the compact judgment-loop surface for the stream
- `### Appendix` = source wiring and continuity machinery

**Predictive Outlook minimum:** use a short three-line block:

```markdown
- **Call:** <one short expectation / interpretation / warning>
- **Falsifier:** <one observation that would weaken or overturn the call>
- **Revisit:** <one date, event trigger, or condition>
```

This block is required for substantive codex-pages. Keep it compact; codex-pages remain mostly evidence-forward.

**Readable-body balance:** target roughly `~70-80%` of readable body weight in `### Verbatim`. This is a guidance band, not a hard fail threshold.

**Skeleton:**

```markdown
# <Stream / author> codex-page - YYYY-MM-DD
WORK only; not Record.

**Cognition stream:** `<expert_id>` · **Published:** YYYY-MM-DD · **Artifact:** codex-page.

---

### Verbatim

### Reflection

### Predictive Outlook

- **Call:** <one short expectation / interpretation / warning>
- **Falsifier:** <one observation that would weaken or overturn the call>
- **Revisit:** <one date, event trigger, or condition>

---

### Appendix

- **Primary raw-input:** [raw-input/YYYY-MM-DD/<slug>.md](...)
- **Supporting raw-input:** [raw-input/YYYY-MM-DD/<slug>.md](...)  <!-- optional; keep the set small -->
```

**Rule of use:** codex-pages are source/verbatim support and durable citation handles for `thread`, `days.md`, and later synthesis. They do not replace the main analytical role of `strategy-page` blocks.

---

## strategy-page -> thread-fence page

# Cognition stream strategy-page - `<expert_id>`

WORK only; not Record.

Use this inside `experts/<expert_id>/<expert_id>-thread-YYYY-MM.md` or legacy `thread.md`.

**Surface rules:**

- `### Chronicle` = curated quote body or distilled evidentiary line
- `### Reflection` = operator analysis
- `### Predictive Outlook` = the required judgment-loop surface
- `### Appendix` = machinery only

**Predictive Outlook minimum:** use the same short three-line block:

```markdown
- **Call:** <one short forward-looking or interpretive claim>
- **Falsifier:** <what would weaken or overturn it>
- **Revisit:** <date, event, or threshold that should trigger review>
```

This block is required for normal strategy-page writing. It should not be replaced by vague future-looking filler.

**Skeleton:**

```markdown
<!-- strategy-page:start id="<kebab-id>" date="YYYY-MM-DD" watch="<optional-watch-slug>" -->
### Page: <human title>

### Chronicle

### Reflection

### Predictive Outlook

- **Call:** <one short forward-looking or interpretive claim>
- **Falsifier:** <what would weaken or overturn it>
- **Revisit:** <date, event, or threshold that should trigger review>

---

### Appendix
<!-- strategy-page:end -->
```

**Rule of use:** the strategy-page is the notebook's primary composed analytical unit. Use codex-pages to support and cite it, not to compete with it. If a page truly carries no live call, keep it transcript-only / codex-page-only or state a minimal call such as "this frame remains tentative pending X."

---

## Relationship to other templates

- Month continuity and chapter rhythm belong to [strategy-codex-template-book.md](strategy-codex-template-book.md) and [strategy-codex-template-chapter.md](strategy-codex-template-chapter.md).
- Legacy file-contract references to `strategy-expert-template.md` may persist while links are being updated.
