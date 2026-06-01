---
name: "statecraft-intelligence-essay"
preferred_activation: "statecraft intelligence essay"
description: "Write synthetic singularity-statecraft intelligence essays from archive-grounded statecraft material without visible speaker-shelf scaffolding in the prose. Use for paired essays, actor-perception essays, and strategic-historical interpretation surfaces where the archive remains substrate rather than the visible frame."
portable: true
version: "0.1.0"
tags:
  - "operator"
  - "statecraft"
  - "essay"
  - "intelligence"
  - "synthesis"
portable_source: "skills-portable/statecraft-intelligence-essay/SKILL.md"
synced_by: "sync_portable_skills.py"
---
# Statecraft intelligence essay

**Preferred activation (operator):** say **`statecraft intelligence essay`**.

Use this skill when the archive is already grounded and the next need is a synthetic singularity-statecraft essay rather than a speaker-shelf synthesis note.

This skill is for **authored intelligence prose**. It uses the archive as substrate, but the finished essay should not read like a transcript comparison, quote stack, or elevated paraphrase of named speakers.

## Use this skill when

- the operator wants a paired essay, civilizational perception essay, actor-perception note, or strategic-historical interpretation surface
- the archive batch or supporting source shelf is already materially real
- the essay should sound like singularity-statecraft intelligence rather than an archive report
- the archive should inform the writing without remaining the visible frame

## Do not use this skill when

- the task is source intake
- the task is a daily synthesis note
- the task is a monthly synthesis note
- the operator explicitly wants speaker-by-speaker comparison, quote-bearing traceability, or a shelf-led report

If the operator wants a bounded archive-grounded report with visible speakers and direct quote anchors, stop this skill and route to `statecraft daily synthesis`.

## Core law

This skill starts **after** archive truth is already grounded.

Read the stack in this order:

`Statecraft Archive -> Statecraft Synthesis / lane notes -> Intelligence Essay`

The essay may be informed by the archive directly, but it should not pretend the archive layer is optional. It should simply stop showing its scaffolding in the prose.

## Form law

An intelligence essay is **synthetic, authored, and non-speaker-led**.

That means:

- the archive remains the substrate, not the visible frame
- named speakers do not carry the argumentative spine
- direct quotes are usually omitted
- shelf comparisons recede into the intelligence rather than appearing as the main prose structure

The test is simple:

`If the piece still reads like "speaker A says, speaker B says," it is not yet an intelligence essay.`

## Output law

The default output is a durable essay surface under the relevant downstream `statecraft/` shelf.

It should usually do five things:

1. name the live object clearly
2. render the actor, civilization, or strategic grammar at work
3. explain what the actor thinks is being threatened or tested
4. identify the rationality and the distortion inside that perception
5. return to the present object rather than drifting into abstraction

## Workflow

1. **Confirm the substrate is real**
   - Make sure the source day, month, or supporting notes are materially grounded.
   - Do not generate free-floating intelligence prose from a thin archive surface.

2. **Name the essay class**
   - Decide what kind of essay this is:
     - paired civilizational essay
     - actor-perception essay
     - strategic-historical interpretation
     - legitimacy or order-transition essay
   - Keep the class narrow enough that the essay does real work.

3. **Identify the governing perception**
   - Ask what this actor thinks the event really is.
   - Prefer one governing perception and one secondary tension over a flat list of themes.

4. **Build the hidden archive spine**
   - Determine which archive observations actually support the essay.
   - Use those observations to stabilize the claims, but do not make speaker names the visible skeleton unless there is a special reason.

5. **Write authored intelligence prose**
   - Let the essay sound like singularity-statecraft intelligence, not transcript commentary.
   - Use historical memory, strategic grammar, and current mechanism together.
   - Preserve the actor's internal rationality before naming its blind spots.

6. **Check for disguised synthesis**
   - Remove visible speaker-led scaffolding.
   - Remove quote clusters unless a rare anchor is indispensable.
   - Make sure the archive remains legible only as substrate.

7. **Close on the live object**
   - Return to the current crisis object, threshold, or settlement problem.
   - End with present-tense relevance rather than broad theory alone.

## Guardrails

- Never treat an intelligence essay as a substitute for source intake.
- Never let synthetic prose outrun archive truth.
- Never build the body around speaker-by-speaker scaffolding unless the essay type explicitly requires an exception.
- Never leave the essay as elevated paraphrase of the source shelf.
- Never let civilizational depth become an excuse for losing the live strategic object.

## Success condition

The result is a durable downstream essay that reads as singularity-statecraft intelligence, remains anchored to real archive substrate, and explains the live object without visible speaker-shelf scaffolding.


## Cursor / grace-mar instance

**strategy-codex instance notes**

- Canonical daily shelf for downstream statecraft essays: [statecraft/daily](/C:/dev/strategy-codex/statecraft/daily/README.md)
- Canonical archive substrate for these essays: [source-archive/statecraft](/C:/dev/strategy-codex/source-archive/statecraft)
- Use archive-grounded notes and day/month synthesis surfaces as substrate, but do not leave speaker-shelf scaffolding visible in the essay prose.

**Current local model examples**

- Parent day with linked essay pair:
  - [statecraft/daily/2026-06-01.md](/C:/dev/strategy-codex/statecraft/daily/2026-06-01.md)
- Paired intelligence essays:
  - [statecraft/daily/2026-06-01-persia-hormuz-lebanon-strategic-memory.md](/C:/dev/strategy-codex/statecraft/daily/2026-06-01-persia-hormuz-lebanon-strategic-memory.md)
  - [statecraft/daily/2026-06-01-america-hormuz-lebanon-strategic-memory.md](/C:/dev/strategy-codex/statecraft/daily/2026-06-01-america-hormuz-lebanon-strategic-memory.md)

**Repo notes**

- Daily and monthly synthesis documents remain the quote-bearing, speaker-shelf-based surfaces.
- Intelligence essays remain synthetic, authored, and non-speaker-led.
- Use the archive as substrate rather than visible frame.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill statecraft-intelligence-essay
python scripts/sync_portable_skills.py --verify --skill statecraft-intelligence-essay
python scripts/validate_skills.py
```
