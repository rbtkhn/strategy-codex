# Codex Goal Mode Playbook

**Status:** work-layer operator doctrine. Not Record. Not EVIDENCE.

Purpose: explain how to use Codex goal mode as a campaign runner for strategy-codex work that is larger than a single turn, larger than a single edit, or vulnerable to drift.

Goal mode is most useful when the work has:

- a concrete objective
- multiple steps
- a real done state
- a real blocked state
- a tendency to sprawl unless the mission stays explicit

It is **not** a substitute for the gated merge rule, not a second governance path, and not a reason to treat vague aspirations as executable objectives.

## What Goal Mode Changes

In ordinary turn-by-turn use, Codex can still do excellent work, but each turn must recover or restate the mission in conversation.

Goal mode turns the mission itself into a tracked object.

Relevant primitives in this environment:

- `create_goal`
- `get_goal`
- `update_plan`
- `update_goal`

This means Codex can hold onto:

- the objective
- the current plan
- whether the campaign is still active
- whether it is complete
- whether it is genuinely blocked

The unlock is not unlimited autonomy. The unlock is **disciplined continuity**.

## When To Use Goal Mode

Use goal mode for work that is:

- cross-file
- likely to take more than one substantial turn
- easy to drift away from
- checkable at the end

Good fits in this repo:

- benchmark hardening
- speaker-shelf audit campaigns
- source backfill campaigns
- dirty-worktree split-and-ship campaigns
- migration waves with clear boundaries

Do **not** use goal mode for:

- tiny one-file edits
- casual questions
- vague standing ambitions
- permanent stewardship with no clear finish line

## Good Goal Shapes

Good goals are:

- specific
- finite
- externally checkable
- narrow enough that completion means something

Examples:

- `Create a goal: make the speaker-memory benchmark family bundle-first and green.`
- `Create a goal: audit and close the January 2025 Freeman transcript gaps, including direct watch URL recovery where possible.`
- `Create a goal: split the current speaker-shelf dirty worktree into coherent commits without touching governed Record surfaces.`
- `Create a goal: backfill the academy-singularity source lane for the last 7 missing issues and rebuild downstream sheets.`

Optional budget shape:

- `Create a goal: calibrate SM-3 and SM-4 on real speaker shelves with a token budget of 12000.`

## Bad Goal Shapes

Avoid goals like:

- `Improve the repo`
- `Make the system smarter`
- `Keep helping with speaker shelves`
- `Do strategy better`

These are domains, not missions. They do not provide honest completion criteria.

## Recommended Campaign Shapes

### 1. Benchmark campaigns

Use a goal when:

- a benchmark family needs new fixtures
- the scorer needs new support
- the harness must become runnable in the bundled runtime
- calibration examples need to be added and linked

Template:

`Create a goal: make the <benchmark-family> fully runnable and green in the bundled Codex runtime.`

### 2. Speaker-shelf campaigns

Use a goal when:

- a shelf needs a completeness audit
- URL recovery is missing
- object, helix, thread, and routing surfaces need reconciliation
- a real comparison set needs calibration

Template:

`Create a goal: audit the <speaker> shelf for density, completeness, coherence, and maturity, then close the highest-value gaps.`

### 3. Source backfill campaigns

Use a goal when:

- a month or lane of captures is missing
- transcript bodies must be materialized
- source-note quality must be normalized
- downstream derived artifacts depend on the backfill

Template:

`Create a goal: backfill <lane/date-range>, materialize missing transcript-bearing captures, and rebuild dependent artifacts.`

### 4. Dirty-tree cleanup campaigns

Use a goal when:

- unrelated work has accumulated in the index or worktree
- commit boundaries have become unclear
- you need a safe split rather than broad landing

Template:

`Create a goal: split the current dirty worktree into coherent commit wedges and leave unrelated work unstaged.`

### 5. Conductor stewardship campaigns

Use a goal when:

- a conductor pass has revealed repeated structural issues
- a workflow loop needs implementation, verification, and ship discipline
- the work is bigger than one stylistic pass

Template:

`Create a goal: implement the next conductor-driven workflow improvement and verify it end to end before shipping.`

## Practical Prompting Pattern

Best sequence:

1. create the goal with one sentence
2. let Codex hold or refine a plan
3. let Codex execute until the objective is complete or truly blocked
4. close the goal explicitly

Minimal operator pattern:

```text
Create a goal: make the speaker-memory benchmark family fully runnable and green in the bundled runtime.
```

Then let Codex:

- inspect local state
- update the plan
- execute
- verify
- report completion or blockage honestly

## Bounded Arc Goal Template

Use this when you want a new goal-mode session to stay strictly inside one arc-shaped mission such as `freeman-arc`, `crooke-arc`, or `baud-arc`.

```text
New goal-mode session.
Workspace: `C:\dev\strategy-codex`.

Boundary:
This session is strictly bounded to `<arc-name>`.

Interpret `<arc-name>` as the sole mission container for this session.
It does not authorize:
- broader shelf work
- neighboring speaker cleanup
- general benchmark work
- repo-wide cleanup
- opportunistic adjacent fixes
- absorption of unrelated dirty-worktree material

Operating rule:
Before any action, apply this filter:
"Does this directly serve the bounded `<arc-name>` mission?"
If no, leave it alone.

Goal-mode rule:
Keep the objective explicit, the plan explicit, and the execution bounded.
Do not declare completion early.
Do not declare blockage unless real progress is impossible without operator input or external state change.

Scope rule:
Neighboring inconsistencies are out of scope unless they directly affect `<arc-name>`.
Unrelated files are not in scope.
No broadening by implication.

Repo rule:
The worktree may be noisy.
Do not touch unrelated files.
Preserve narrow commit boundaries if commits become appropriate.
Governed Record surfaces remain governed.

Prime directive:
Maintain strict scope discipline.
Protect the integrity, coherence, and boundedness of `<arc-name>`.
```

Optional strengthening line for multi-surface arcs:

```text
Arc-local surfaces are in scope only if they are part of the same arc object; adjacent shelf doctrine is not in scope unless the arc cannot be stabilized without it.
```

Good uses:

- `freeman-arc`
- `crooke-arc`
- `baud-arc`
- `johnson-arc`

## Completion Discipline

A goal should be marked complete only when:

- the objective has actually been achieved
- required verification has been run when feasible
- no required work remains inside the stated objective

For this repo, “complete” often means:

- code or docs are changed
- the relevant validator or smoke path has passed
- the commit boundary is clean, if shipping was part of the goal

## Blocked Discipline

A goal should be considered blocked only when:

- the same blocking condition keeps recurring
- Codex cannot make meaningful progress without operator input or external state change

Examples of real blockers:

- missing source material that cannot be recovered locally or from allowed sources
- required user preference on a genuinely consequential split
- network or permission constraints that prevent the next mandatory step

Not blockers:

- work is hard
- the campaign is large
- more polish would be nice
- a side quest looks tempting

## Why This Matters For Strategy-Codex

This repo is unusually campaign-shaped.

A lot of valuable work here is not:

- one edit
- one answer
- one script run

It is:

- audit + repair + verification
- backfill + normalization + routing
- doctrine + scorer + harness + calibration
- split + commit + verify

Goal mode is therefore a force multiplier because it turns those chains into explicit missions instead of relying on conversational momentum alone.

## First Recommended Uses

If you want to build fluency quickly, start with goals in this order:

1. benchmark hardening campaigns
2. speaker-shelf audits
3. source backfill wedges
4. dirty-tree split-and-ship passes

These are the places where the gain from explicit mission continuity is highest.
