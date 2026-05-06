# work-jiang Layer Audit

**Purpose:** Name the distinct functions currently bundled inside `research/external/work-jiang/` so later doctrine can point to the right **sub-template** instead of treating the whole tree as one reusable shape.

**Bottom line:** Jiang is a valid **corpus-first exception**, but `work-jiang` is **not** a clean one-piece template for future lane promotion. It bundles multiple layers that should be conceptually separated even when they live in one tree.

## Layer map

| Layer | What it does | Canonical examples |
|---|---|---|
| **Corpus** | Holds the source world and the structured research surfaces needed to work it over time. | `lectures/`, `substack/essays/`, `analysis/`, `metadata/`, `claims/`, `verbatim-transcripts/`, `prediction-tracking/`, `divergence-tracking/`, `chronology` |
| **Book / editorial** | Turns the corpus into a publishable multivolume line with chapter order, evidence packs, and release discipline. | `BOOK-ARCHITECTURE*.md`, `CHAPTER-QUEUE*.md`, `book/`, `evidence-packs/`, `PREFACE.md`, `INTRODUCTION.md` |
| **Pedagogy / voice** | Defines how Jiang’s material should be taught or explained in a Jiang-like classroom register. | `docs/templates/JIANG–VOICE.md`, `docs/skill-work/work-jiang/jiang-voice.md`, pedagogy tasks in `MULTI-AGENT.md` |
| **Site / publication surface** | Presents the corpus and books to readers as a public-facing Jiang-first gateway. | `site/README.md`, `site/index.html`, `site/volume-01.html` |
| **Workflow / orchestration** | Coordinates tasks, review queues, and promotion of agent/operator work inside the lane. | `MULTI-AGENT.md`, `tasks.jsonl`, `review-queue/`, promotion scripts, context-pack assembly |

## What makes Jiang a true exception

Jiang is not just another commentator lane with heavy reuse. The corpus justifies dedicated external treatment because it has:

- sustained high-volume source material
- multiple primary corpora under one intellectual line
- explicit claims, prediction, and divergence machinery
- strong payoff from chronology and cross-episode continuity
- a stable research problem that extends beyond single captures

That is enough to make Jiang a clean **exception to the shared-intake default**.

## Why Jiang is not a clean template

The mistake would be to infer:

- `Jiang has a dedicated corpus`
- therefore
- `future promoted lanes should look like work-jiang`

That is too broad.

`work-jiang` is not only a corpus. It is also:

- a **book-production system**
- a **pedagogical emulation system**
- a **reader-site surface**
- a **multi-agent production workflow**

Those functions are all legitimate, but they are not all part of the minimal reusable pattern for a promoted strategy-codex lane.

## Reusable vs non-reusable parts

### Reusable core for future lane promotion

These are the parts that should inform future dedicated external corpora for lanes like `mercouris`, `davis`, or `diesen` if they ever cross the threshold:

- source-text layer
- curated analysis layer
- minimal metadata/source registry
- recurring-judgment surface such as claims or equivalent notes
- optional chronology / quote / prediction / divergence layers only when workflow pressure justifies them

### Non-default extras

These should **not** be imported automatically when another lane is promoted:

- full multivolume book architecture
- chapter queue and evidence-pack machinery
- Jiang-style teaching-voice contract
- dedicated public-facing site
- task manifest + review-queue production workflow

Those are second-order systems that belong only when the lane is also becoming a publication program, pedagogy program, or production operation.

## Recommended doctrine use

When strategy-codex policy needs to reference Jiang, use these rules:

- cite Jiang as the **corpus-first exception**
- do **not** cite the entire `work-jiang` tree as the default promotion template
- when discussing future lane promotion, point to the **Corpus** layer first
- treat the **Book / editorial**, **Pedagogy / voice**, **Site**, and **Workflow** layers as optional expansions that require separate justification

## Practical implication for lane promotion

If a future lane is promoted:

- the target is a **minimal dedicated external corpus**
- not a mini-`work-jiang`
- later additions such as publication, pedagogy, or site layers should be proposed separately

That keeps Jiang legible as:

- a true exception to the eight-lane shared-intake default
- but only a **partial template** for future corpus promotion
