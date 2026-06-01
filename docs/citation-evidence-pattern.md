# Citation and Evidence Pattern

work only; not Record.

This note defines the preferred citation pattern for literature-backed notes and
essays in this repo.

The goal is not to create a formal scholarly apparatus. The goal is to make
strong claims:

- more inspectable
- more reusable
- more comparable
- harder to overstate

## When Explicit Academic Support Is Needed

Use explicit academic support when a prose object makes one or more of these
moves:

- claims that a design family has precedent or lineage
- claims that a concept is not unique in kind
- compares this repo's architecture to named academic traditions
- relies on empirical or theoretical literature rather than only repo-native
  observation
- would become materially weaker if its evidence base stayed tacit

Do not force this pattern onto every essay. Use it when the argument is
literature-bearing rather than only interpretive or architectural.

## Three Supporting Shapes

### 1. Support notes

Use support notes when one main essay needs separate lines for:

- lineage
- workflow proof
- product extrapolation
- family-separated literature discussion

Support notes help the main essay stay compact without hiding the scaffolding.

### 2. Evidence matrix

Use an evidence matrix when the main need is comparison across sources rather
than one continuous argument.

The default comparison template is:

- **Source claim**
- **Design resemblance**
- **Distance**
- **Boundary**

This is the preferred matrix form for:

- lineage claims
- non-uniqueness claims
- partial ancestry
- adjacent design precedent

### 3. Carriage-bearing essay

Use a carriage-bearing essay when the claim should stand on its own.

The essay may link a support cluster, but it should still carry the main
argument without forcing the reader to open every support note first.

## Preferred Citation Behavior

For literature-backed prose:

- use inline links for core claims
- use a support cluster when the evidence base is too large or heterogeneous
  for one essay
- use an evidence matrix when the real need is comparison across sources
- add one short boundary section naming what the evidence does **not** prove

Primary academic sources should support substantive literature claims whenever
the essay is making:

- lineage claims
- precedent claims
- design-family comparisons
- non-uniqueness claims

Secondary summaries can still be useful for orientation, but they should not be
the main support for those stronger claims.

## Evidence Posture

Research-heavy essays may add a short `Evidence Posture` or `Evidence Basis`
section near the end.

It should answer:

- what literature families support the essay
- whether the evidence base is primary-only or mixed
- what level of claim the evidence can honestly sustain

This section is intentionally lighter than a `Source Support Block`. It is a
prose-native way of making the essay's evidentiary footing explicit.

## Cluster Standard

When the evidence base is too large or heterogeneous for one essay, prefer a
research cluster with this default shape:

- `README.md` as cluster front door
- `evidence-matrix.md` or equivalent annotated bibliography
- family notes or function-separated support notes
- one synthesized essay above the cluster

Use:

- a **single memo** when the claim is bounded and the literature family is
  narrow
- a **cluster** when multiple literature families or support functions need to
  stay distinct
- an **evidence matrix** when comparison across sources is the main need

## Boundary

This pattern is intentionally lightweight in v1.

It does **not** require:

- a validator
- a bibliography database
- artifact-registry schema changes
- file-level citation bureaucracy

If literature-backed essays become common enough later, a more formal evidence
block or registry extension can be added then.
