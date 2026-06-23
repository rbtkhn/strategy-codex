---
name: tufte-data-viz
preferred_activation: tufte viz
description: "Tufte-style chart and dashboard discipline for operator observability: high data-ink, direct labels, log scales when warranted, chart-review mode; inspection-only, not Record merge."
portable: true
version: 0.1.0
tags:
  - operator
  - work-dev
  - observability
  - visualization
---

# Tufte Data Visualization

**Preferred activation (operator):** say **`tufte viz`** or **`tufte review`**.

Use when creating or reviewing charts, dashboards, and metric views for operator observability — cadence pressure, gate snapshots, workflow rollups, integration activity proxies, or (when instrumented) token usage.

## Governance

- Observability visuals are **inspection-only**. They do not merge the Record, approve gate candidates, or substitute for `recursion-gate.md`.
- Label **partial or inferred** metrics honestly (`directional`, `proxy`, `no token instrumentation`).
- Do not treat chart output as EVIDENCE truth.

## When to use

- Cadence + governance pressure views (coffee / dream / bridge vs gate pending).
- Chart review of chat tables, bridge dumps, or derived Markdown dashboards.
- Workflow observability or context-efficiency rollups when JSON exists.
- Token-burn views **only** when non-zero token fields exist or the operator supplies an external usage export.

## Modes

### Generate (`tufte viz`)

1. **Preflight data** — confirm the source exists and is fresh; note empty windows or zero token columns.
2. **Choose chart type** — prefer small multiples, horizontal bars, sparklines, or direct-labeled series over heavy legends.
3. **Apply surface semantics** (legend convention, not canonical Record colors):
   - SELF — knowledge / identity load
   - removed operator-books symlink — reference / library surfaces
   - SKILLS — capability / execution surfaces
   - EVIDENCE — activity / receipt surfaces
4. **Scale** — linear by default; log scale when span exceeds ~2 orders of magnitude and values are strictly positive.
5. **Annotate** — direct labels; mark gate-pending counts, pressure signals, and data staleness inline.
6. **Deliver** — Cursor canvas for interactive prototypes; or concise review prose when canvas is not requested.

### Review (`tufte review`)

Apply this checklist to an existing chart, table, or dashboard:

| Check | Pass criterion |
|-------|----------------|
| Data-ink | No decorative grid, 3D, or redundant legend boxes |
| Labels | Reader knows metric, units, and source without hunting |
| Title | Assertive, specific (not "Metrics") |
| Governance | No implied merge authority from visuals |
| Accessibility | Sufficient contrast; color not sole carrier of meaning |
| Honesty | Partial / proxy / stale data called out |

## Universal Tufte rules (condensed)

- Eliminate chartjunk — no unnecessary spines, grids, or legend boxes when direct labels work.
- Prefer range frames and small multiples over one overloaded panel.
- Use sparklines for continuity; reserve pie charts for simple part-to-whole with few slices.
- Keep typography quiet; let the data carry weight.

## Agent behavior norms

- **Human authority** — Assist; charts do not approve or merge.
- **Abstention** — If sources are empty, say so; use activity proxies only with explicit labeling.
- **No silent overwrite** — Do not replace operator-owned dashboards without consent.

## Provenance

Methodology inspired by Edward Tufte and the open-source `caylent/tufte-data-viz` skill pattern. Adopt principles; do not bulk-copy vendor bodies without license review.

## Related capture skill

For *where* to land repeated observability patterns (Record vs WORK vs portable), see `observability-to-cadence-capture` — orthogonal to this skill's *how to draw* role.
