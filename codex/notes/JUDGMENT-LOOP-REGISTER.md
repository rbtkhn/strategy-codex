# Judgment loop register
<!-- word_count: 220 -->


**Purpose:** Optional stronger tracking surface for consequential calls, recurring theses, or especially important warnings that deserve more than the lightweight page-level loop.

**Use this only when needed.** The canonical minimum remains the compact **Call / Falsifier / Revisit** block inside `codex-page` and `strategy-page`. This register is an escalation surface, not a second mandatory compose path.

## Entry scaffold

```markdown
## YYYY-MM-DD - <short label>

- **Reference:** [page or day block](...)
- **Call:** <one short claim or warning>
- **Falsifier:** <what would weaken or overturn it>
- **Revisit:** <date, event trigger, or threshold>
- **Status:** `open` | `held` | `weakened` | `broke` | `superseded`
- **Outcome note:** <one short line on what changed or what still has to happen>
```

## Rules

- Prefer one entry per consequential call, not one entry per page.
- Update `Status` only when reality materially clarifies the call.
- Use `superseded` when a later thesis replaces the earlier one without the earlier one cleanly holding or breaking.
- Keep the note short; if the real continuity work belongs in `days.md`, record it there and link back here.

## Relationship to the notebook

- `raw-input/` preserves the literal source layer.
- `codex-page` and `strategy-page` carry the lightweight judgment loop.
- `days.md` records whether a call held, weakened, broke, or stayed open.
- This file is for the subset of calls that deserve stronger operator visibility across sessions.
