# Postmortem To Skill Feedback Loop

Use this loop when a session reveals a repeated failure pattern that should become active guidance instead of remaining only a dated note.

## Goal

Promote a real mistake into the smallest durable correction:

- a skill rule
- a doctrine update
- or a lightweight tooling / observability guardrail

The test is whether a future agent working from active repo surfaces becomes less likely to repeat the same error.

## Minimal loop

1. Name the failure pattern plainly.
2. Identify the active surface that should have prevented it.
3. Choose the lightest durable fix:
   - skill rule
   - doctrine note
   - helper or observability nudge
4. Add the rule where future work will actually route through it.
5. Leave the original postmortem as evidence, not as the only fix.

## Promotion test

Promote the lesson when most of these are true:

- the mistake cost real time or operator trust
- the same class of error could recur in adjacent tasks
- the preventive rule can be stated simply
- the fix can live in an active workflow surface without adding ritual bloat

## Seed examples from this session

- **Encoded workflow recognition**
  - Failure: freeform elicitation replaced an existing bookshelf MCQ -> strictness -> gate ritual.
  - Durable fix: add an encoded-workflow-first rule to active operator skills.

- **No fake compatibility trees**
  - Failure: path drift was answered by inventing a compatibility directory instead of fixing root-layout assumptions.
  - Durable fix: state that migrations should repair path assumptions, not create shadow structure, unless doctrine explicitly requires it.

- **Mixed-churn detection**
  - Failure: unrelated local edits made cleanup families harder to isolate.
  - Durable fix: classify cleanup families early and treat mixed files as holdouts unless intentionally disentangled.

- **Environment bottleneck escalation**
  - Failure: a broken `rg` workflow was tolerated as shell annoyance even though it imposed a compounding throughput tax.
  - Durable fix: treat degraded core tools as setup problems when the fix is local and high leverage.

## What not to do

- Do not create a new doctrine layer for every minor mistake.
- Do not leave important lessons only in a dated postmortem if an active skill or README can carry the rule.
- Do not "solve" a recurring problem with a workaround that hides the underlying control surface.

## Related session notes

- [bookshelf-mcq-root-layout-repair-2026-05-04.md](dev-notebook/work-dev/bookshelf-mcq-root-layout-repair-2026-05-04.md)
- [root-vs-users-migration-audit-2026-05-05.md](dev-notebook/work-dev/root-vs-users-migration-audit-2026-05-05.md)
- [tree-shaping-audit-2026-05-06.md](dev-notebook/work-dev/tree-shaping-audit-2026-05-06.md)
- [validation-family-close-2026-05-06.md](dev-notebook/work-dev/validation-family-close-2026-05-06.md)
