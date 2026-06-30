---
note_id: assistant-session-state-clarity-contract
note_type: mechanism
authority_level: review-needed
source_basis: mixed
essay_candidate: false
created_at: 2026-06-18
updated_at: 2026-06-28
---
## Assistant Session-State Clarity Contract


This note defines a short operating contract for assistant behavior during long repo sessions. Its purpose is to reduce trust drag by making execution state easy to read, especially when inspection, drafting, implementation, verification, and closeout happen across several turns.

Trust rises when state is legible.

## Session Contract

- Name the mode early. Say plainly whether the current move is `inspecting`, `implementing`, `reviewing`, or `planning-only`.
- Use explicit status labels. Prefer `planned`, `drafted`, `implemented locally`, `verified`, `committed`, and `pushed` over generic completion language.
- Translate plain language first. Give the ordinary meaning before internal doctrine terms when both appear.
- Ground before recommending when local inspection is cheap. Let the repo lead the recommendation order.
- Keep one active branch foregrounded. If adjacent threads exist, make clear which branch owns the current turn.
- Emit a short ledger when multiple arcs are live. Use `done`, `uncommitted`, and `next likely move`.
- Prefer one best next move. Do not widen into a branching next-step tree unless the operator asks for options.
- Close with exact state. Say what was done, what was not done, and whether the work was verified, committed, or pushed.

## Quick Checklist

- mode named
- current branch named
- status words precise
- recommendation grounded
- ledger emitted if stack is crowded
- closeout states exact

The audit explains the friction; this note defines the corrective operating behavior.
