# Speaker arc orthogonality template


Purpose: define a reusable scaffold for comparing **how two expert arc outputs differ in explanatory frame**, not just whether they reach the same conclusion.

System grammar:

- **Person arc:** `<speaker>-arc.md` for one speaker's continuity across hosts, contexts, and time.
- **Relational arc:** `<host>-<speaker>-arc.md` for what a specific host repeatedly elicits from that speaker.
- **Tension note:** `<speaker-a>-vs-<speaker-b>-<window>.md` for a bounded disagreement or interpretive split.
- **Arc orthogonality note:** `<speaker-a>-<speaker-b>-orthogonality-<window>.md` for evaluating whether two arc outputs are complementary, redundant, or merely differently phrased.

Ownership rule:

- Choose a **tension note** when the main question is "where do they disagree?"
- Choose an **arc orthogonality note** when the main question is "how distinct are their explanatory contributions, even if they overlap on outcome?"

## Arc orthogonality note

# `<speaker-a> x <speaker-b> orthogonality - <window>`


Use this note when two speaker outputs need to be compared for **frame separation**, **evidence separation**, and **conclusion overlap**.

**Naming rule:**

- Use a concrete time, event, or prompt window, for example `2026-05`, `iran-war-question`, or `china-russia-alliance`.
- Keep the filename plain: `<speaker-a>-<speaker-b>-orthogonality-<window>.md`.

**Recommended shape:**

- `Scope`
- `Question`
- `Arc A`
- `Arc B`
- `Orthogonality audit`
- `Composite use`
- `Notebook use`

## Scope

List the local anchors that substantiate the comparison.

- [{source-1}]({source-1-path})
- [{source-2}]({source-2-path})
- [{optional-source-3}]({optional-source-3-path})

State the bounded claim:

- what prompt or issue generated the comparison
- what surfaces are being compared
- what this note does **not** try to adjudicate

## Question

State the comparison question in one sentence.

Example:

- "How differently do Freeman-arc and Mearsheimer-arc explain Russia's value to China?"

## Arc A

`{speaker-a}-arc` emphasizes:

- {frame-a-1}
- {frame-a-2}
- {frame-a-3}

Its typical causal language:

- {keywords / mechanisms / preferred abstractions}

## Arc B

`{speaker-b}-arc` emphasizes:

- {frame-b-1}
- {frame-b-2}
- {frame-b-3}

Its typical causal language:

- {keywords / mechanisms / preferred abstractions}

## Orthogonality audit

Score or describe each dimension explicitly.

### Frame orthogonality

Are the two outputs working at different explanatory layers, or just rephrasing the same one?

### Evidence orthogonality

Do they rely on different examples, receipts, or recurring source habits?

### Conclusion overlap

Do they converge on the same bottom-line judgment?

### Net relation

Classify the pair:

- `highly orthogonal`
- `moderately orthogonal`
- `mostly redundant`
- `same conclusion, different mechanism`
- `different conclusion, shared frame`

Include a one-paragraph justification.

## Composite use

If the two outputs are combined, what stronger synthesis becomes possible?

Use a compact shape:

- `{speaker-a}` contributes: {what it uniquely adds}
- `{speaker-b}` contributes: {what it uniquely adds}
- `Combined`: {the stronger composite claim}

## Notebook use

Use this note when the notebook needs:

- a check on whether two expert outputs are actually distinct
- a guard against flattening complementary experts into one line
- a way to compose multiple arcs without losing method differences
- a quick answer to "are these two analyses redundant or additive?"

## Boundary

Do not use an arc orthogonality note for:

- basic disagreement mapping that belongs in a tension note
- one speaker's continuity surface that should remain an arc
- a verdict memo claiming which speaker is correct
- a generic comparison with no bounded prompt or window

Treat this as a comparison of explanatory shape. It measures distinctness and composability, not truth.
