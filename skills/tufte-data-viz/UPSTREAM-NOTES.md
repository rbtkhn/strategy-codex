# Upstream diff — caylent/tufte-data-viz

**Compared:** 2026-06-08 · upstream `main` @ [caylent/tufte-data-viz](https://github.com/caylent/tufte-data-viz) · local `skills/tufte-data-viz/SKILL.md` v0.1.0

**License:** MIT (Caylent 2026) — selective adoption permitted with copyright notice in substantial copies.

## Summary

| Dimension | Upstream | strategy-codex local |
|-----------|----------|----------------------|
| Size | ~14 KB SKILL + `rules/` (10 files) + `examples/` | ~3 KB portable core + CURSOR_APPENDIX |
| Scope | General chart generation (6 libraries) | Operator observability + chart-review + governance |
| Rules | 22 numbered universal rules | 6 condensed bullets + 6-row review table |
| Validation | 20-item checklist | 6-row review checklist |
| Libraries | Recharts, ECharts, Chart.js, matplotlib, Plotly, D3/SVG | Cursor `cursor/canvas` (appendix); defer Plotly/HTML until committed dashboards |
| Colors | Hex tokens + categorical `#4e79a7` `#f28e2b` `#e15759` `#76b7b2` | Record **semantic** legend + canvas `useHostTheme()` (no hardcoded hex) |
| Workflow | 4 steps: message → rules → library → validate | Preflight → chart type → surface semantics → scale → annotate → deliver |

## What local adds (keep)

- Inspection-only governance; no recursion-gate / Record merge implied by visuals.
- `tufte review` mode independent of generation.
- Cadence-pressure, workflow observability, gate-board data preflight (appendix).
- Token-burn deferral when ledger tokens are zero.
- `observability-to-cadence-capture` boundary cross-link.
- `preferred_activation` + portable schema (`portable: true`, no `allowed-tools`).

## What upstream has that local lacks (adopt selectively)

### High value for next revision (portable core)

1. **Rule 13 — comparison context** — “Compared to what?” reference line/band/second series; fits gate-pending annotations on cadence charts.
2. **Rule 20–22** — assertive finding titles, human number formatting, don’t chart 1–2 numbers (write a sentence).
3. **Rule 11** — no dual y-axes → small multiples (aligns with cadence small-multiples canvas).
4. **Step 1 workflow** — identify message + comparison context before code.
5. **Anti-pattern one-liners** — legend→direct labels, pie→horizontal bar, rainbow→gray+accent (compress into review mode).
6. **Chart-type guidance table** — at least bar/line/sparkline/small-multiples rows for agent routing.

### Medium value (appendix or phase 2)

- Library quick-reference table — link upstream `rules/*.md` when target is Plotly/matplotlib/Recharts HTML (not Cursor canvas).
- Full 20-item validation checklist — optional superset after `tufte review` on shipped HTML/Plotly.
- Rules 15–19 (screen-first: progressive disclosure, WCAG, responsive, motion, dark mode) — canvas skill already enforces host theme; don’t duplicate hex/serif mandates for `.canvas.tsx`.

### Low priority / defer

- Vendor entire `rules/` tree into repo (weight); prefer URL pointers until committed dashboard family exists.
- `allowed-tools` frontmatter — not in strategy-codex portable schema.
- Upstream serif + `#fffff8` palette — conflicts with Cursor canvas token rules; keep host-theme path for canvas, upstream palette for Plotly/HTML exports only.

## Color palette note

Upstream categorical four-color set matches the Grok proposal’s SELF/LIBRARY/SKILLS/EVIDENCE hex list. **Coincidence, not Record canon.** Local skill correctly treats these as optional semantic legend labels, not governed identity colors.

## Recommended revision order (v0.2.0)

1. Add **Identify message** + **comparison context** to Generate mode (rules 1 + 13 + 20–22 compressed).
2. Expand **Review** checklist with upstream anti-pattern rows (legends, pie, dual axis, rainbow).
3. Add **Chart-type routing** subsection (bar / line / sparkline / small multiples).
4. In CURSOR_APPENDIX: pointer block “HTML/Plotly/matplotlib exports → read ONE file from [upstream rules/](https://github.com/caylent/tufte-data-viz/tree/main/rules)”.
5. Do **not** bulk-paste upstream SKILL.md; bump `version` and re-run `sync_portable_skills.py --verify`.

## Attribution (keep in SKILL Provenance)

Inspired by Edward Tufte and [caylent/tufte-data-viz](https://github.com/caylent/tufte-data-viz) (MIT). See this file for adoption boundaries.
