---
name: state-synthesis
preferred_activation: state synthesis
description: "Turn a landed statecraft archive day batch into a bounded daily synthesis note on the statecraft side. Use when the source captures for a day already exist and the next job is to identify the dominant crisis object, lane pressure, and speaker-by-function comparisons. Includes same-object mechanism comparison as a built-in subroutine."
portable: true
version: 0.3.1
scope_class: repo-governed
tags:
  - operator
  - statecraft
  - synthesis
  - daily
  - monthly
---

# State synthesis

**Preferred activation (operator):** say **`state synthesis`**.

**Legacy activation (compatibility):** `state synthesis` — same skill; prefer **`state synthesis`**.

Use this skill when a day-batch or month-batch of statecraft source captures is already real and the next need is a bounded synthesis note on the `statecraft/` side.

This skill is for **downstream synthesis**, not archive capture and not synthetic intelligence-essay writing. Its job is to read the landed archive batch, identify the governing object, and write a compact, durable interpretation surface without pretending to replace the underlying transcript authority.

## Use this skill when

- the day archive is already materialized
- the month archive slice is already materially real and the operator wants a month-bound synthesis
- the operator wants a daily synthesis report
- the operator wants a monthly synthesis report built from speaker shelves and archive receipts
- the operator wants a bounded read of lane pressure, crisis object, and tensions
- a same-object, different-mechanism comparison would clarify the batch

## Do not use this skill when

- the day batch does not yet exist in `source-archive/statecraft/`
- the operator is still uploading transcripts and the archive layer is incomplete
- the task is only archive intake
- the task is a lane-direct doctrinal memo rather than a day-batch synthesis
- the task is a paired essay, civilizational perception essay, or other synthetic singularity-statecraft intelligence surface
- the operator wants archive-informed prose where the archive should disappear into authored intelligence rather than remain visible in the note

If the operator wants a synthetic essay rather than a synthesis note, stop this skill and route to `statecraft intelligence essay`.

## Core law

This skill starts **after** archive truth is already grounded.

Read the stack in this order:

`Statecraft Archive -> Statecraft Synthesis -> lane / bridge / civ-state judgment`

This skill operates on the middle of that stack.

## Form law

Daily and monthly synthesis notes remain **visibly archive-grounded**.

That means the prose should usually show its speaker shelf:

- who contributed the strongest mechanism
- who supplied the enabling carrier
- who clarified bargaining consequence
- where the archive genuinely splits

These notes may quote, paraphrase, compare, and shelf speakers directly when that improves traceability.

What they must **not** do is disguise themselves as synthetic civilization-statecraft intelligence. If the speaker shelf should disappear from the prose, this is the wrong skill.

## Output law

The default output is a bounded synthesis note under `statecraft/`, not in the archive.

It should usually do four things:

1. identify the dominant crisis object
2. assign primary and secondary lane pressure
3. name the most useful speakers and why
4. preserve tensions, falsifiers, and next moves

## Daily register vs daily synthesis

Same default path: `statecraft/synthesis/day/YYYY-MM-DD.md`.

- **Daily register** — archive grounded; dominant object named in brief form; companion weaves/matrices linked; **Register Completion Checklist**; header `Status: register`. Write this when captures land before a full executive pass.
- **Daily synthesis** — register shape expanded (dominant themes, lane read, CIV-STATE, speaker value). No `Status: register` line when synthesis tier is complete.

Doctrine: [statecraft/synthesis/METHOD.md § Daily register vs daily synthesis](../../statecraft/synthesis/METHOD.md#daily-register-vs-daily-synthesis).

**Do not** use **stub** for register-tier dailies.

## Workflow

1. **Open the landed day archive**
   - Start from the touched day `README.md`.
   - Confirm the batch is materially real and source-bearing.
   - Identify the highest-signal captures in the batch.
   - For Mario Nawfal sources tagged `opening_tier: host-monologue`, start chronology at the **first guest mechanism block** (first sustained guest answer to a falsifiable question), not Mario's optimistic deal loop — unless Mario's read is itself the seam under test.
   - For Dialogue Works / Nima sources tagged `opening_tier: full-scaffold` (or still carrying a separable mid-intro Substack CTA before the first crisis question), start chronology at the first `let me start with` / `I want to start with` falsifiable crisis read — not the Substack or book promo block. For `solo-brief`, keep the spoken date/timezone anchor; do not skip Brazil vs US East Coast dating when it governs the archive day.

2. **Name the governing object**
   - Ask what the day is really about:
     - command failure
     - settlement breakdown
     - blockade/coercion
     - recognition threshold
     - alliance entrapment
     - escalation psychology
   - Prefer one dominant object and one secondary object over a flat summary.

3. **Assign lane pressure**
   - Name the primary owning lane.
   - Name secondary lane pressure only when it materially changes the read.
   - Do not force every day into cross-lane symmetry.

4. **Compare speakers by explanatory function**
   - Do not collapse speakers into generic agreement/disagreement.
   - Ask what each speaker contributes best:
     - mechanism
     - enabling carrier
     - bargaining consequence
     - settlement architecture
     - threshold/clock/falsifier
   - Preserve differences in explanatory power.

5. **Write the bounded report**
   - Put the note on the `statecraft/` side.
   - Keep it compact, decision-bearing, and traceable back to the source day or month slice.
   - Let the archive remain visible in the writing: speaker shelves, quote anchors, and function comparisons are allowed and often preferred.
   - Include best next moves rather than pretending the batch already settled everything.

### Source-dense war-object inquiry-ladder deepener

Use this optional deepener when a day-batch or month-batch is dominated by one war object and the archive clearly supports a staged climb.

Preferred sequence:

1. battlefield geometry
2. hinge
3. supporting arm
4. campaign theory
5. speaker-function adjudication

Use this deepener only when:

- the batch is genuinely centered on one war object
- each step materially changes the question
- the archive supports the climb without speculative stretching
- the speaker bench is strong enough that explanatory responsibility can be divided rather than blended

Do not use this deepener when:

- the batch is still multi-object and fragmented
- the map does not actually reveal a real hinge or supporting arm
- campaign theory would have to be invented rather than extracted
- the ladder would only restate the same battlefield claim in hotter language

Short rule:

`use the ladder only when the climb clarifies the object more than a flat executive read would`

6. **Update the smallest live synthesis surfaces**
   - Update the relevant daily shelf index.
   - Link statecraft mechanism notes when they become durable enough to reuse.

7. **Check the surface class before closing**
   - Ask whether the note is still visibly a synthesis note rather than a disguised essay.
   - If the writing no longer needs speaker shelves, archive-grounded attribution, or quote-bearing traceability, route the job to `statecraft intelligence essay` instead of finishing under this skill.

## Mechanism-comparison subroutine

Use this subroutine when multiple speakers are reading the **same object** through different logics.

Default comparison sequence:

1. state the shared object
2. identify each speaker's strongest mechanism
3. identify the enabling carrier if one speaker supplies it
4. identify the opponent-side bargaining effect if one speaker supplies it
5. compress the result into a reusable line

Example shape:

- `Pape` = trap logic
- `Freeman` = strategic backfire
- `Sachs` = enabling carrier
- `Marandi` = adversary-side hardening

Short rule:

`do not ask only who is right; ask where explanatory responsibility is divided`

## Week hinge subroutine (not weekly synthesis)

**Activation:** operator says **`week hinge`** or **`start-here`** + month/week.

This is **navigation + object-migration** between daily and monthly synthesis — **not** a third full synthesis contract (no five-volume block, no functional-convergence grid).

**Month-aligned partition** (not ISO/Sunday; no cross-month weeks):

| weekN | Days |
|-------|------|
| week1 | 1 – 7 |
| week2 | 8 – 14 |
| week3 | 15 – 21 |
| week4 | 22 – EOM |

**When to write or refresh:** month-week close, object migrates within month-week (refresh same `YYYY-MM-weekN-start-here.md`), or operator invocation. Header: `partial through YYYY-MM-DD` while open.

**Doctrine:** [statecraft/synthesis/METHOD.md § Week Hinge](../../statecraft/synthesis/METHOD.md#week-hinge-contract) · template: [`_templates/week-hinge-start-here.md`](../../statecraft/synthesis/day/_templates/week-hinge-start-here.md).

**After daily synthesis:** if dominant object migrated within the active month-week, offer or refresh the week hinge; intake-readiness should point to the hinge for post-daily re-entry.

**Monthly feed:** only on explicit **`statecraft monthly synthesis`** — lift object-migration lines into `Month Arcs`; no dream auto-merge.

## Guardrails

- Never write the daily synthesis into `source-archive/statecraft/`.
- Never write the monthly synthesis into `source-archive/statecraft/`.
- Never let a polished summary replace transcript authority.
- Never flatten multiple speakers into one blended commentary voice.
- Never force lane certainty when the day still has a real split.
- Never let one elegant mechanism pretend to explain the entire object if the batch clearly shows carrier, leverage, and bargaining layers separately.
- Never mistake a synthetic intelligence essay for a synthesis note just because both are downstream from the same archive batch.
- Never force every war batch through the inquiry ladder.
- Never claim a hinge, supporting arm, or campaign theory unless the archive itself makes that level of distinction supportable.

## Receipt ledger (optional)

When companions or transaction rows add receipt IDs (e.g. `AMER-224-RCPT-03`), optional subsection on intake-readiness or daily companion notes:

```markdown
## Receipt ledger (optional)
| ID | File | Status |
|----|------|--------|
| AMER-224-RCPT-03 | statecraft/america/transactions/... | wired |
```

Agent-filled when wire-ins land; no script required in v1.

## Related operations

| Operation | Relationship |
|-----------|--------------|
| **civ-state** | When civilizational layer unsettled after synthesis — offer wire-bridge handoff (see below) |
| **state-note** | One promotable wedge after synthesis when method-bearing |
| **statecraft-multi-lens** | Live comparison before synthesis when speakers unsettled |

## After synthesis close

When dominant crisis object is named but **governing term / case / primary shelf** is still unsettled, or mechanism comparison needs cross-case placement, offer **one line** (do not auto-run civ-state):

```text
Civilizational layer unsettled — say civ-state for wire-bridge (term → case → primary shelf).
```

## Success condition

The day or month ends with a bounded, reusable synthesis note under `statecraft/` that is grounded in the archive batch, clear about lane pressure, and explicit about which speakers explain which part of the object best.

## Verification / Proof Standard

Do not call this complete unless:

- day batch exists under `source-archive/statecraft/<day>/` with at least one landed source
- synthesis output path under `statecraft/synthesis/day/` (or explicit month surface) is named
- crisis object is stated in one line in the synthesis
- synthesis does not mirror verbatim archive bodies

Evidence to report:

- archive day path and source count
- synthesis file path
- one-line crisis object
- optional receipt ledger rows when wire-ins applied

If verification cannot be completed:

- state whether archive batch or synthesis file is missing
- downgrade to candidate-only language; do not claim daily promotion
