# Speaker surface orthogonality review template

WORK only; not Record.

Purpose: define a reusable audit scaffold for checking whether a set of **speaker arcs** and **threads inside those arcs** are distinct enough to justify their separate existence.

System grammar:

- **Arc template** = how to write one arc surface
- **Thread template** = how to write one thread surface
- **Arc orthogonality note** = how to compare two expert outputs
- **Surface orthogonality review** = how to audit a local cluster of arcs and threads for redundancy, collapse pressure, and composability

Use this review when the main question is not "what is this arc?" but "is this family of surfaces partitioned well enough to produce cognitive depth, breadth, and connectivity without waste?"

## Surface orthogonality review

# `<speaker-or-cluster> surface orthogonality review - <window>`

WORK only; not Record.

Use this note when a speaker shelf, host cluster, or topical cluster has grown enough that the notebook should explicitly test whether the arcs and threads are still partitioned well.

**Naming rule:**

- Use the narrowest cluster name that still makes sense, for example:
  - `<speaker>-surface-orthogonality-2026-05.md`
  - `<host>-cluster-orthogonality-iran-war-window.md`
  - `<speaker>-threads-orthogonality-deterrence-window.md`

**Recommended shape:**

- `Scope`
- `Surfaces under review`
- `Arc audit`
- `Thread audit`
- `Redundancy findings`
- `Recommended actions`
- `Notebook use`

## Scope

List the local surfaces being reviewed.

- [{surface-1}]({surface-1-path})
- [{surface-2}]({surface-2-path})
- [{surface-3}]({surface-3-path})

State the bounded claim:

- what cluster is under review
- why redundancy or overlap is suspected
- what this review can and cannot settle

## Surfaces under review

Separate the cluster into:

- **arcs under review**
- **threads under review**
- **comparison-only notes** such as tension notes or orthogonality notes that should not be mistaken for continuity surfaces

## Arc audit

For each arc, answer:

- What continuity does this arc own?
- What explanatory frame does it add?
- What source habit or host transformation makes it distinct?
- What operator use would justify opening it instead of a neighboring arc?

### Arc distinctness table

| Arc | Owned continuity | Distinct frame | Distinct evidence habit | Distinct use | Status |
|---|---|---|---|---|---|
| `{arc-1}` | TBD | TBD | TBD | TBD | keep / merge / rename / collapse |
| `{arc-2}` | TBD | TBD | TBD | TBD | keep / merge / rename / collapse |

## Thread audit

For each thread, answer:

- What recurring strand does this thread isolate?
- How is its object different from neighboring threads?
- How is its causal grammar different?
- What retrieval or citation use does it support that the parent arc or another thread does not?

### Thread distinctness table

| Thread | Object | Mechanism | Source spine | Retrieval use | Status |
|---|---|---|---|---|---|
| `{thread-1}` | TBD | TBD | TBD | TBD | keep / merge / rename / collapse |
| `{thread-2}` | TBD | TBD | TBD | TBD | keep / merge / rename / collapse |

## Redundancy findings

Classify any overlap explicitly.

Possible tags:

- `same conclusion, different mechanism`
- `same source spine, different use`
- `same frame, different host transformation`
- `near-duplicate thread`
- `arc should absorb thread`
- `thread should split`
- `comparison note mistaken for continuity surface`

Give a short explanation for each finding.

## Recommended actions

Use compact operator language:

- `keep as is`
- `rename for clearer ownership`
- `merge into neighboring arc`
- `collapse back into parent arc`
- `split one thread into two`
- `move comparison material into tension note or orthogonality note`

Prefer the smallest change that increases distinctness.

## Notebook use

Use this review when the notebook needs:

- a direct audit of whether a speaker shelf has become redundant
- a way to preserve depth and breadth without surface sprawl
- a check that threads inside an arc are genuinely different
- a basis for future cleanup, renaming, or consolidation work

## Boundary

Do not use this review for:

- ordinary source summary
- disagreement mapping between two experts
- a claim that one surface is truer than another
- raw-input provenance checking

This is a partition audit. It tests whether the notebook’s explanatory surfaces are arranged well enough to stay sharp as the shelf grows.
