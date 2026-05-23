# cici-ai Daily Brief Control-Plane Pilot

WORK only; not Record.

## Purpose

This pilot turns the `cici-ai` daily Telegram brief into a real control-plane test.

The question is not only whether we can generate a better brief. The question is whether one partially automated team surface can make authority clearer under automation:

- what the generator may do on its own
- what still requires operator review
- what evidence counts
- what receipt proves the brief was honest
- what rollback condition stops the flow from bluffing momentum

This is the first tractable build surface for the broader singularity-workshop roadmap: `agent control-plane maturity` leads the build queue even if `compute / substrate governance` leads the map.

## Scope

Workflow under test:

1. bounded source read
2. internal digest generation
3. Telegram-ready message generation
4. operator review
5. final post or narrow/hold decision

Current generator:

- [generate_cici_ai_daily_brief.py](../../../scripts/generate_cici_ai_daily_brief.py)
- [cici-ai Daily Telegram Brief](cici-ai-daily-telegram-brief.md)

## Agent Actions Allowed

The generator may:

- read bounded `work-cici` sources
- summarize visible movement
- classify confidence using the existing `A / B / C` ladder
- propose one primary ask and one secondary ask
- name who needs action when the source basis supports it
- produce an internal digest and a Telegram-ready draft

The generator may not:

- invent progress
- convert weak self-report into proof
- make payment, scholarship, employment, or governance commitments
- speak as if `work-cici` were Cici's governed instance
- post directly to Telegram without operator review

## Human Gate Points

### Gate 1. Source sufficiency

The operator decides whether the source basis is strong enough for a public brief.

If the evidence is thin, the correct action is:

- narrow the brief
- switch to a follow-up ask
- or hold the public post

### Gate 2. Public wording

The operator decides whether the Telegram draft outruns the digest.

No public line should be stronger than the internal evidence summary that produced it.

### Gate 3. Escalation or silence

The operator decides whether a blocker, ambiguity, or confidence downgrade should be surfaced publicly, routed privately, or left out until better evidence exists.

## Receipt Format

Each daily run should leave a compact receipt, even if nothing is posted.

Minimum receipt fields:

- date
- mode: `intake`, `setup`, `proof`, `public-output`, or `review/reset`
- source set used
- confidence ceiling: `A`, `B`, or `C`
- post status: `posted`, `narrowed`, or `held`
- primary ask
- main reason for any hold or narrowing

Suggested receipt shape:

```text
cici_ai_daily_brief_receipt
date=YYYY-MM-DD
mode=proof
confidence_ceiling=B
post_status=posted
sources=dashboard,progress,telegram,evidence,profiles
primary_ask=post one artifact from your first task
note=public brief stayed inside visible evidence
```

## Rollback Condition

Stop treating the flow as healthy if any of the following appears:

- public copy repeatedly sounds more certain than the digest
- the brief rewards noise more than proof
- the generator keeps naming action for members without current evidence
- the operator routinely rewrites most of the message by hand
- the group stops responding with the requested proof shape

If one of these persists, rollback means:

- reduce automation scope
- simplify the brief shape
- or return to operator-written briefs until the source layer improves

## Failure Modes

### 1. Motion theater

The brief makes the lane sound active while the evidence remains thin.

### 2. Quiet authority drift

The generator starts deciding what counts as meaningful movement without enough operator scrutiny.

### 3. Proof collapse

The group learns that enthusiasm and greetings are enough to earn mention.

### 4. Overpersonalized routing

The brief names individuals too aggressively when the source basis is weak or stale.

### 5. Doctrine without embodiment

The control-plane language is sound, but no visible receipt or hold behavior exists in practice.

## Pilot Test

### Build

Use the current generator and brief spec as the implementation base.

### Test

Run the flow for a small sequence of real days and inspect:

- whether the public brief stays inside the digest
- whether reply asks become more concrete
- whether proof-bearing replies rise
- whether the operator spends less time correcting authority drift

### Success signal

The flow is useful if it makes the lane easier to re-enter and easier to trust at the same time.

### Failure signal

The flow is not useful if it creates more polished summaries without improving proof, routing, or operator clarity.

## Next Use

- Pair this note with [cici-ai Daily Telegram Brief](cici-ai-daily-telegram-brief.md) when evolving the generator or the posting routine.
- Use it with [Future Roadmap Implications](../../../codex/academy/singularity/workshop/sheets/future-roadmap-implications.md) as the first live test of `agent control-plane maturity`.
- If this pilot works, use the same shape for other automated report surfaces before broadening the doctrine.
