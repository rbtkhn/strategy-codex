---
name: recursive-learning
preferred_activation: recursive learning
description: "Governed session review and journal entry for reusable machine laws. SSOT journal: statecraft/recursive-learning-journal.md."
portable: true
version: 0.2.0
tags:
  - operator
  - statecraft
  - work-strategy
  - architecture
---

# Recursive Learning

**WORK only; not Record.**

**Activation:** `recursive learning` · `RLJ` · `recursive-learning` · `review this session through recursive learning`

**SSOT (open first — do not repo-grep):** [statecraft/recursive-learning-journal.md](../../statecraft/recursive-learning-journal.md)

Extract **reusable drafting, routing, or architectural law** from a session — not source intake, not speaker shelves, not operator rhythm elicitation.

**Default trigger:** `problem encountered → fix applied → recursive learning`. RLJ runs **after** the fix is in place (code, doctrine, routing, validator), not while debugging.

## When to use

| # | Scenario | When | Mode |
|---|----------|------|------|
| 1 | **Problem → fix** | Fix landed; extract prevention law | Session review |
| 2 | **Elicitation → encode → RLJ** | Operator judgments shipped as doctrine/structure | Session review |
| 3 | **Conductor arc close** | `verdict=held`; stance logged; machine law still implicit | Session review |
| 4 | **Cross-lane proof** | Same pattern family on 2nd/3rd distinct object | Session review or promotion review |
| 5 | **Dense week close** | Multi-lane week ending; law scattered in chat/cadence | Session review |
| 6 | **Promotion review** | Law reused twice; pattern or skill wire may be due | Promotion review |

| Fix depth | RLJ value |
|-----------|-----------|
| One-off typo / obvious mistake | Thin — skip unless a guardrail emerges |
| Repeated misroute, validator fail, sync drift, plan/implementation seam | **High** |
| Architectural ship (multi-file encoding, new pattern) | **High** — full five-section session review |

**Thin invokes (usually skip):** one-off typo, restated plan prose, conductor ritual with no behavior change, productivity praise.

**Not for:** [elicit-knowledge](../../.cursor/skills/elicit-knowledge/SKILL.md) · [skill-elicitation](../../.cursor/skills/skill-elicitation/SKILL.md) · [conductor](../../.cursor/skills/conductor/SKILL.md) execution (outcomes may feed RLJ).

## Elicitation pipeline

```text
skill-elicitation (rank/judgment BEFORE encoding)
  → plan/implement
  → recursive-learning (machine law AFTER encoding)
```

Cross-link [skill-elicitation](../../.cursor/skills/skill-elicitation/SKILL.md) — RLJ does not replace elicitation MCQs.

**Anti-pattern:** Do not invoke RLJ when operator judgment is still unlocked — use elicitation or plan MCQs first. RLJ runs after encoding, not instead of it.

## Promotion ladder

| Stage | Home | Gate |
|-------|------|------|
| Session review | chat only | five sections drafted |
| Journal entry | `recursive-learning-journal.md` | operator confirms append; no duplicate law |
| Pattern promotion | `statecraft/patterns/` | adaptive reuse on a second distinct object ([patterns/README.md](../../statecraft/patterns/README.md) use rule) |
| Skill/validator wire | `.cursor/skills/` or scripts | law reduces misrouting measurably ([skill-refinement-scorecard](../../statecraft/notes/skill-refinement-scorecard.md)) |

**Defer paths:** opportunity-map (rank only), law-extraction checkpoint (carry to close).

**Supersede / cross-link (append gate):** Before append, search full journal for overlapping law (see CURSOR_APPENDIX duplicate grep). If overlap exists: **cross-link** (same law, new reapplication), **narrow** (scope restriction), or **supersede** (dated note + pointer to prior entry) — never silent duplicate.

Promoted pattern examples: [lane-hardening-law.md](../../statecraft/patterns/lane-hardening-law.md), [doctrine-hardening-law.md](../../statecraft/patterns/doctrine-hardening-law.md).

## Known homes

| Artifact | Path |
|----------|------|
| Journal SSOT | [statecraft/recursive-learning-journal.md](../../statecraft/recursive-learning-journal.md) |
| Pattern promotion target | [statecraft/patterns/README.md](../../statecraft/patterns/README.md) |
| Skill-wire gate | [statecraft/notes/skill-refinement-scorecard.md](../../statecraft/notes/skill-refinement-scorecard.md) |
| Conductor arc journal | [conductor-arc-impact-journal.md](../../docs/skill-work/work-strategy/conductor-arc-impact-journal.md) |
| Cadence receipts | [work-cadence-events.md](../../docs/skill-work/work-cadence/work-cadence-events.md) |
| Repair receipt pattern | [archive-truth-floor-audit-receipt-pattern.md](../../docs/archive-truth-floor-audit-receipt-pattern.md) |
| Lineage memo | [interpretive-machine-lineage.md](../../docs/skill-work/work-strategy/interpretive-machine-lineage.md) |

Preflight: read journal entry shape + last 2–3 entries before proposing a new law. Cursor agents: see CURSOR_APPENDIX for preflight commands.

## Entry shape (required)

1. **Trigger** — what taught the lesson
2. **Extracted law** — reusable rule (plain + optional arrow form)
3. **Reapplication** — where it applies next
4. **Structural changes** — files, validators, skills, routing that moved
5. **Guardrail** — prevents template repetition / decorative learning

Optional: **Current lesson** (one line).

### Paste template

```markdown
## YYYY-MM-DD - Short title

### Trigger
…

### Extracted law
…

### Reapplication
…

### Structural changes
…

### Guardrail
…

### Current lesson
…
```

## Modes

### Session review (default)

1. Open journal SSOT; scan recent entries.
2. Run falsification pass (below) before drafting.
3. Draft all five sections in reply — **do not append** without confirmation.
4. Offer: append to journal, promote to `statecraft/patterns/`, or wire into skill/validator.

### Journal entry

On operator confirm (`append RLJ`, `log this`, `add to recursive learning journal`):

1. Complete session review draft.
2. Duplicate grep across full journal; apply supersede/cross-link/narrow if needed.
3. Append `## YYYY-MM-DD - Title` block to journal.
4. Offer pattern promotion — do not auto-promote.

### Law extraction (checkpoint)

Mid-session: state **Extracted law** + **Guardrail** only; full entry at close when fix lands.

### Falsification pass (before append)

Ask: what would prove this law false or decorative? If falsified → soften claim or split authority layers; do not append co-primary claims without cash-out.

### Opportunity map (no append)

Rank 3–7 candidate laws from a corpus/session; **no adoption** until reuse proven. Output rank + guardrail per candidate.

### Promotion review

When law may be ready for pattern or skill wire (canonical #4, #6, or operator request):

- Checklist: two reuses on distinct objects? routing/repair/stopping/priority/architecture change? duplicate of existing journal/pattern law?
- Output: `append` | `defer` | `promote to patterns` | `wire skill/validator`

## Cadence integration

RLJ is **post-encoding consolidation** (conductor is **mid-day pressure**). Standalone activation by name — not coffee hub letter E. Coffee/dream hub seeds and handoff detail: **CURSOR_APPENDIX** (Cursor) or [work-coffee README](../../docs/skill-work/work-coffee/README.md).

| Job | Primary surface | RLJ role |
|-----|-----------------|----------|
| **Continuity** | `dream_coffee_rollup.py`, `last-dream.json` | Handoff only — note deferred law in prose hints |
| **Observability** | `build_conductor_ledger.py`, cadence events | None — do not duplicate `coffee_pick` / `coffee_conductor_outcome` |
| **Durable learning** | `conductor-arc-impact-journal.md`, **`recursive-learning-journal.md`** | **Owns machine-law extraction and journal append** |

| Surface | Owns | Does not own |
|---------|------|--------------|
| **Coffee hub (A–D)** | Confirm / Test / Deepen / Reframe | Journal append, conductor movement |
| **Conductor** | Stance, `coffee_conductor_outcome`, ship discipline | Machine-law checklist, pattern promotion |
| **RLJ skill** | Five-section review, append gate, promotion ladder | Hub letter, auto_dream.py mutations |
| **Dream** | Night maintenance, `tomorrow_inherits` | Full RLJ pass inside scripts |
| **conductor-arc-impact-journal** | Conductor arc scoring windows | Cross-surface encoding law |

**Dual receipt:** conductor close first → optional RLJ. `coffee_conductor_outcome` = stance/verdict/falsify; RLJ session review = extracted machine law, reapplication, guardrails.

## Agent workflow

1. Open [statecraft/recursive-learning-journal.md](../../statecraft/recursive-learning-journal.md) — not repo-wide search.
2. Name one trigger object.
3. Extract falsifiable, reusable law.
4. Show at least one concrete reapplication.
5. List structural changes (or note review-only).
6. State guardrail.
7. Append only on explicit request.

## Related operations

| Operation | Relationship |
|-----------|--------------|
| Conductor | Sequencing may *be* the lesson; cadence logs separately; close before RLJ |
| skill-elicitation | Locks operator judgment **before** encoding |
| recursive-learning | Locks machine law **after** encoding |
| repo-hygiene-pass | Structural changes section after bucketed ship |
| statecraft-source-intake | Closeout / sync-check laws after intake fix |

## Worked example (illustration only — not yet appended)

*Rome v0.1.26 fractured-sovereignty chain encoding.*

**Trigger:** Operator elicitation locked Republic opener, co-primary carriers (papacy, France, HRE), colonial `instrument` tier, and shared rupture primaries; plan executed across six `rome-{term}.md` files + theory links + validator pass.

**Extracted law:** Fractured-sovereignty chains need **memory spine + term segments**: one cross-term index (`rome-memory#chain-spine`) plus per-lens segments; shared ruptures get one primary home + cross-refs elsewhere; colonial empires are instruments, not chain heads.

**Reapplication:** Next civilization with split sovereignty (e.g. Persia dual centers, China tributary layers) — elicit co-primary tiers before encoding; never promote colonial branches to chain-head without operator cash-out.

**Structural changes:** Six `rome-*.md`, theory Volume depth links, `governing-term-first.md`, VERSION v0.1.26, validator strict-theory pass.

**Guardrail:** Do not copy Rome tier labels to other civs without elicitation; `instrument` vs `co-primary` is judgment, not template.

## Quality test

Must change at least one of: routing · repair boundaries · stopping rules · priority · architecture.

**Fail:** productivity praise, restated plan prose, template copy without adaptation, conductor ritual with no behavior change.

## Guardrails

```text
recursive learning ≠ template repetition
```

- Phase/conductor language must cash out in routing, repair, or priority.
- No duplicate journal laws without cross-link/supersede.
- WORK journal ≠ Record truth.
- **Do not repo-grep** for this operation.

## Done when

- **Review:** five sections in reply; append offered.
- **Entry:** dated block in journal; no silent duplicate.
- **Checkpoint:** law + guardrail stated; full entry deferred.
- **Promotion review:** explicit output (`append` | `defer` | `promote` | `wire`).
