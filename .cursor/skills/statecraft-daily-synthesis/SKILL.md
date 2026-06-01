---
name: "statecraft-daily-synthesis"
preferred_activation: "statecraft daily synthesis"
description: "Turn a landed statecraft archive day batch into a bounded daily synthesis note on the statecraft side. Use when the source captures for a day already exist and the next job is to identify the dominant crisis object, lane pressure, and speaker-by-function comparisons. Includes same-object mechanism comparison as a built-in subroutine."
portable: true
version: "0.2.0"
tags:
  - "operator"
  - "statecraft"
  - "synthesis"
  - "daily"
  - "monthly"
portable_source: "skills-portable/statecraft-daily-synthesis/SKILL.md"
synced_by: "sync_portable_skills.py"
---
# Statecraft daily synthesis

**Preferred activation (operator):** say **`statecraft daily synthesis`**.

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

## Workflow

1. **Open the landed day archive**
   - Start from the touched day `README.md`.
   - Confirm the batch is materially real and source-bearing.
   - Identify the highest-signal captures in the batch.

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

6. **Update the smallest live synthesis surfaces**
   - Update the relevant daily shelf index.
   - Link companion comparison notes when they become durable enough to reuse.

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

## Guardrails

- Never write the daily synthesis into `source-archive/statecraft/`.
- Never write the monthly synthesis into `source-archive/statecraft/`.
- Never let a polished summary replace transcript authority.
- Never flatten multiple speakers into one blended commentary voice.
- Never force lane certainty when the day still has a real split.
- Never let one elegant mechanism pretend to explain the entire object if the batch clearly shows carrier, leverage, and bargaining layers separately.
- Never mistake a synthetic intelligence essay for a synthesis note just because both are downstream from the same archive batch.

## Success condition

The day or month ends with a bounded, reusable synthesis note under `statecraft/` that is grounded in the archive batch, clear about lane pressure, and explicit about which speakers explain which part of the object best.


## Cursor / grace-mar instance

**strategy-codex instance notes**

- Canonical source day root for this skill: [source-archive/statecraft](/C:/dev/strategy-codex/source-archive/statecraft)
- Canonical synthesis side for daily reports: [statecraft/daily](/C:/dev/strategy-codex/statecraft/daily/README.md)
- Use the day archive inventory first, then write synthesis downstream.
- Do not place synthesis notes in `source-archive/statecraft/`.

**Current local model example**

- Daily synthesis report:
  - [statecraft/daily/2026-05-29.md](/C:/dev/strategy-codex/statecraft/daily/2026-05-29.md)
- Companion comparison note:
  - [statecraft/daily/2026-05-29-pape-vs-freeman-sachs-marandi.md](/C:/dev/strategy-codex/statecraft/daily/2026-05-29-pape-vs-freeman-sachs-marandi.md)

**Repo notes**

- Archive truth stays upstream in `source-archive/statecraft/`.
- This skill begins only after the archive batch is real.
- The default companion mechanism comparison for this repo is:
  - `Pape` = trap logic
  - `Freeman` = strategic backfire
  - `Sachs` = enabling carrier
  - `Marandi` = adversary-side hardening

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill statecraft-daily-synthesis
python scripts/sync_portable_skills.py --verify --skill statecraft-daily-synthesis
python scripts/validate_skills.py
```
