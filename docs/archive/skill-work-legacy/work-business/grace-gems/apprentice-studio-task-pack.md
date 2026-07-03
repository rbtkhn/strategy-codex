# Apprentice Studio Task Pack - Grace Gems

non-authoritative. Review-gated. No live customer action without operator approval.

## Purpose

This task pack defines apprentice-safe Grace Gems work for the `Apprentice Studio` 30-day pilot.

Use it when `cici-ai` participants are completing real business tasks under operator review. This pack should be read alongside:

- [Grace Gems README](README.md)
- [Agent Encoding](agent-encoding.md)
- [Workflow reminders](workflow-reminders.md)

It references those docs rather than restating all policies from scratch.

## Month-One Rule

Start `back-office first`.

Approved task types:

- listing validation
- stone/provenance QA
- policy consistency checks
- message drafts
- market research summaries
- workflow cleanup notes

Disallowed early tasks:

- live sends to customers
- pricing decisions
- order promises
- refunds or compensation offers
- new sourcing claims
- policy changes
- any customer-facing truth change without review

## Standard Workflow

1. Assign one task only.
2. Apprentice produces one artifact.
3. Operator reviews against this pack and `agent-encoding`.
4. Reviewer marks artifact as `accepted`, `accepted with edits`, or `not yet reusable`.
5. Progress surface records proof packet and weekly count.

Do not batch multiple customer messages, listings, or business decisions into one assignment.

## Task Menu

### 1. Listing QA

Deliverable:

- short checklist or markdown note naming any mismatch, ambiguity, or missing fact in one listing

Check for:

- stone/provenance consistency
- terminology misuse
- policy mismatch
- unsupported claims

### 2. Stone / provenance QA

Deliverable:

- one note comparing a listing or draft against the provenance table in [agent-encoding.md](agent-encoding.md)

Check for:

- valid region match
- unsupported origin claims
- uncertainty that should be flagged instead of guessed

### 3. Policy consistency check

Deliverable:

- one note comparing customer-facing copy against documented Grace Gems policies

Check for:

- shipping wording
- returns wording
- repair warranty wording
- custom-order boundaries

### 4. Draft-only customer message support

Deliverable:

- one draft reply only

Requirements:

- friendly, accurate, simple
- one concrete fact per reply
- no invented policy or sourcing detail
- no direct send by apprentice

### 5. Market research summary

Deliverable:

- one short summary of a narrow market question with evidence pointer(s)

Examples:

- competitor listing patterns
- common customer questions
- repeated confusion around natural versus lab-grown stones

### 6. Workflow cleanup note

Deliverable:

- one short note proposing a clearer checklist, rubric, or operator reminder based on observed confusion

This is the preferred path when the apprentice notices friction in the workflow itself.

## Prompt Skeleton

Use this structure when assigning work:

```text
Task type:
One artifact only:
Source docs to use:
What to check:
What not to do:
Output format:
Escalate if:
```

Example:

```text
Task type: Listing QA
One artifact only: review one Grace Gems listing draft
Source docs to use: Grace Gems README, agent-encoding provenance table, terminology glossary
What to check: unsupported provenance, terminology mismatch, policy inconsistency
What not to do: do not rewrite shop policy, do not invent sourcing facts, do not publish anything
Output format: markdown with findings and one suggested correction path
Escalate if: you need a fact not already documented
```

## Reviewer Checklist

Mark every artifact with one reviewer status:

- `accepted`
- `accepted with edits`
- `not yet reusable`

Use this checklist:

- grounded in documented Grace Gems facts
- follows `agent-encoding` rules where relevant
- stays within the assigned task boundary
- avoids invention and unsafe live action
- useful enough to save operator time or improve clarity

## Escalate Instead Of Guessing

Escalate when:

- a fact is missing from the docs
- a listing implies unsupported provenance
- a customer question requires a policy not already documented
- the task drifts into pricing, promises, refunds, or legal/compliance territory

The correct move is to flag uncertainty, not smooth over it.

## What Counts As A Good Month-One Output

- one clear artifact
- one narrow scope
- one reviewable business question
- one decision-ready operator handback

The goal is not brilliance. The goal is safe, reviewable, repeatable usefulness.
