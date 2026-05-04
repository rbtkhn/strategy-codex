# Strategy-codex template - chapter
<!-- word_count: canonical scaffold -->

WORK only; not Record.

**Purpose:** Canonical chapter template for strategy-codex. A **chapter** is the day-bounded continuity unit inside a book/month.

**Companion contracts:** [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md) · [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md)

## Chapter role

- **Book** = month-level synthesis and index surface.
- **Chapter** = daily composition surface.
- **Page** = analytical unit cited or composed within the chapter's day.

The chapter file is normally the active month's `chapters/YYYY-MM/days.md`, with one or more dated sections inside it.

## Chapter block -> `chapters/YYYY-MM/days.md`

# Chapter block - `YYYY-MM-DD`

WORK only; not Record.

Use this for the daily continuity block composed during the strategy session.

**Minimum sections:**

- `### Chronicle`
- `### Reflection`
- `### References`

**Optional sections when the day genuinely needs them:**

- `### Open`
- `### Bets`
- `### Jiang`
- `### History resonance`

**Skeleton:**

```markdown
## YYYY-MM-DD

### Chronicle

### Reflection

### References
```

**Rule of use:** chapters hold chronology and continuity. They should point toward page-level work, not duplicate whole page bodies.

## Relationship to pages and books

- Pull evidence from `raw-input/` and page work.
- Name or link page ids when a page is load-bearing for the day.
- Let the month/book layer summarize the chapter set rather than bloating the chapter with month-scale recap.