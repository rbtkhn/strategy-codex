---
note_id: conversation-ux-friction-audit
note_type: synthesis
authority_level: review-needed
source_basis: mixed
essay_candidate: false
created_at: 2026-06-18
updated_at: 2026-06-28
---
## Conversation UX Friction Audit


**Statecraft Registry**
- Lane: shared
- Output class: memo
- Prose class: note-class
- Maturity: reusable
- Source family: lane-local
- Bridge usage: none
- Transaction relevance: none

## Purpose

This note captures the main user-experience friction revealed by a long repo-shaping session.

The goal is not to criticize the substance of the work. The goal is to reduce trust drag, state ambiguity, and steering burden in future sessions.

## Core Claim

The strongest friction in the session was not idea quality. It was state clarity.

The session became harder than necessary when the assistant made completion sound firmer than it was, let too many arcs stay live at once, and moved between planning and execution without making that boundary explicit enough.

The practical law is:

```text
trust rises when state is legible
```

## Main Friction Points

### 1. Completion language got ahead of visible state

The assistant sometimes spoke as if work had already been cleanly completed before the execution state was fully obvious in the session flow.

That creates avoidable trust friction because the operator has to infer whether the assistant means:

- planned
- drafted
- implemented locally
- committed
- pushed

The user should not have to reconstruct that distinction.

### 2. Planning and execution boundaries blurred

The session moved between:

- immediate implementation
- plan-only behavior
- review-only behavior

without always naming the mode change strongly enough in the moment.

That creates expectation whiplash. A direct imperative should not sometimes yield execution and sometimes yield planning unless the assistant makes the boundary explicit.

### 3. Too many active arcs increased steering burden

Several threads stayed live at once:

- prose taxonomy
- skill refinement
- recursive-learning synthesis
- conductor review
- literature lineage
- citation infrastructure
- handoff protocol

Each individual move often made sense, but together they increased the amount of stack the user had to hold in working memory.

### 4. Internal vocabulary stayed internal too long

The session improved after the assistant translated terms like `carriage`, but that translation came later than it should have.

When internal doctrine language appears before plain-language framing, the operator has to decode house vocabulary before judging the underlying idea.

### 5. Recommendation sometimes outran grounding

A few architectural recommendations arrived before local verification had fully caught up.

Even when the recommendations were directionally right, the sequence created friction:

```text
claim first
-> grounding later
```

The stronger order is:

```text
grounding first
-> recommendation second
```

### 6. The assistant sometimes answered one step ahead

After completing one bounded task, the assistant often proposed several next artifacts or future directions immediately.

This can be helpful, but over a long session it adds decision load. The user then has to keep trimming the tree back to the exact current step.

## Highest-Value Operating Rules

### 1. Use explicit status language

Use these terms precisely:

- `planned`
- `drafted`
- `implemented locally`
- `verified`
- `committed`
- `pushed`

Do not collapse them into one generic "done."

### 2. Emit a short state ledger when multiple arcs are live

When the session has accumulated several overlapping threads, pause and give a three-line ledger:

- `done`
- `uncommitted`
- `next likely move`

This reduces operator stack load and makes the session feel governable again.

### 3. Name plan-only behavior immediately

If the assistant is planning rather than mutating, say so at once in plain language:

```text
I’m planning this slice first; I’m not mutating the repo yet.
```

That one sentence prevents unnecessary ambiguity.

### 4. Translate internal doctrine language earlier

When a concept first appears in exploratory prose:

- give the plain-language version first
- use internal shorthand second if it still adds value

Internal vocabulary should clarify the system for the operator, not become a tax on reading it.

### 5. Ground before recommending

When practical local inspection is easy, inspect first and recommend second.

The operator should feel that the recommendation follows the repo, not that the repo is being recruited after the fact.

### 6. Resist over-proposing the next tree

After a bounded deliverable, prefer:

- one best next move

instead of:

- several adjacent moves
- a plan
- an architecture memo
- an optional future ladder

unless the user explicitly asks for that expansion.

## Simple Session Contract

For future long-form repo sessions, the assistant should aim to satisfy this compact contract:

1. make the current state legible
2. keep the active branch of work narrow
3. translate doctrine into plain language early
4. distinguish planning from mutation clearly
5. make recommendations only after enough grounding to earn them

## Best Sentence

The conversation’s biggest user-experience problem was not weak thinking; it was avoidable ambiguity about what had been done, what was still only proposed, and which thread actually owned the next move.
