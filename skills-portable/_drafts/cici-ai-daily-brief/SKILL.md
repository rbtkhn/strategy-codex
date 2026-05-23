---
name: cici-ai-daily-brief
preferred_activation: cici daily brief
description: "Generate a daily Telegram-ready operating brief for a beginner-heavy cohort: bounded sources, confidence-tagged movement, digest layer versus public layer, one concrete reply ask, and graceful narrowing when evidence is thin."
portable: true
version: 0.1.0
tags:
  - operator
  - reporting
  - telegram
  - cohort
  - beginner-onboarding
  - confidence
---

# cici-ai daily brief

**Preferred activation (operator):** say **`cici daily brief`**. **Aliases:** **`team daily brief`**, **`Telegram operating brief`**, **`cohort brief`**.

## Purpose

Generate a short daily message for a cohort or team chat that does four things:

1. names what actually moved,
2. states what matters today,
3. routes who needs action,
4. ends with one concrete reply format.

This is an operating brief, not a newsletter.

When the host is building future proof assets, treat the brief as a workflow receipt surface first and a public message second.

## When to use

- A beginner-heavy group needs a daily coordination message.
- The source base is mixed: artifacts, progress notes, chat evidence, and self-report.
- The operator needs a private digest plus a public message.
- The message must reward real proof rather than passive membership.

Do not use this skill when the task is a weekly review, a governance memo, or a broad promotional update.

## Core rule

The brief should become simpler as evidence gets weaker.

Do not compensate for thin evidence with stronger tone.

## Source order

Use the strongest available sources in this order:

1. direct artifact or repo-visible evidence
2. operator-observed evidence with a pointer
3. member self-report
4. explicit follow-up ask when proof is missing

If a higher-confidence source contradicts a lower-confidence one, preserve the mismatch.

## Output layers

Always produce two layers:

### 1. Operator digest

Internal object or note containing:

- date
- current mode
- source set used
- strongest movements
- confidence tags
- people or subgroup slices needing action
- primary ask
- final draft message

### 2. Public message

Telegram-ready or chat-ready copy that is:

- shorter
- cleaner
- still evidence-disciplined

The public layer may be simpler than the digest, but it must not be stronger.

## Message shape

Use five blocks:

1. **Pulse**
2. **What moved**
3. **What matters today**
4. **Who needs action**
5. **Reply format**

Keep it short enough for a phone screen. Prefer one or two asks, not a stack.

## Workflow

1. **Choose the operating mode**
   - intake
   - setup
   - proof
   - public-output
   - review/reset

2. **Collect bounded sources**
   - use the host's equivalents for:
     - community dashboard
     - progress lane
     - team-chat lane
     - evidence notes
     - member or contributor profiles

3. **Extract movement**
   - count only signals that change the funnel:
     - joined
     - introduced
     - goal stated
     - setup proof
     - first task completed
     - issue / PR / artifact
     - helper behavior
     - public-output movement

4. **Preserve confidence**
   - attach the host's equivalent confidence tier to each movement line
   - if a signal is only self-report, keep it visibly weaker than artifact-backed proof

5. **Choose the wedge**
   - identify the single most useful ask for the next 24 hours
   - prefer:
     - one URL
     - one screenshot
     - one artifact
     - one one-line status format

6. **Route action**
   - name who needs to act:
     - specific people
     - subgroup slices
     - blocked members
   - avoid shame language

7. **Draft the public message**
   - produce the final five-block message
   - trim anything that does not change behavior

8. **Preserve downstream proof value**
   - if the brief may later feed a receipt, case study, or proof packet, keep the movement language specific enough to survive reuse
   - separate:
     - setup
     - proof
     - public output
     - helper behavior

## Good source classes

Good:

- dashboards with evidence rules
- progress notes with explicit next action
- lane READMEs with open loops
- evidence notes with movement and follow-up sections
- standardized member profiles

Weak unless corroborated:

- vague chat enthusiasm
- generic "we are growing" language
- self-report without a linked artifact
- old dashboards treated as if they were current

## Proof chain note

This brief may become upstream evidence for:

- workflow receipts
- case studies
- proof packets
- offer validation surfaces

That does not make the brief itself market proof.

Preserve the distinction between:

- internal workflow proof
- cohort motion
- public seed credibility
- client proof

## Graceful constraint rule

If the source base is weak:

- reduce the number of movement claims
- stop short of proof language
- shift the message toward artifact collection
- make the reply ask narrower

Do not:

- inflate setup into activation
- count interest as completion
- turn self-report into proof
- keep the same confident voice after the evidence base has thinned

## Minimal public template

```text
Daily brief - {DATE}

Pulse
{one sentence}

What moved
- {movement} [{confidence}]
- {movement} [{confidence}]

What matters today
- {primary ask}
- {secondary ask, optional}

Who needs action
- {name or subgroup}: {next step}
- {name or subgroup}: {next step}

Reply format
- Reply with: {artifact format}
```

## Never do

- Do not turn the brief into motivation copy.
- Do not hide confidence differences.
- Do not list every signal when only two matter.
- Do not let the public message outrun the operator digest.
- Do not create scholarship, payment, or employment commitments through summary language.
- Do not write setup motion in a way that will be misread later as proof or activation.

## Success condition

The next day's replies contain more usable artifacts, more members move from setup to proof, and the operator spends less time reconstructing what the group should do next.
