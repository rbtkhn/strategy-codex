---
name: elicit-knowledge
preferred_activation: elicit knowledge
description: Topic-anchored history MCQ workflow that converts validated answers into merge-ready IX-A knowledge candidates in recursion-gate (no methodology framing, no placeholder suggested_entry). Use when the user asks to elicit knowledge and stage gate candidates.
---

# Elicit Knowledge -> Gate

Use this skill when the operator wants to elicit historical knowledge from `self-library-bookshelf` and stage `recursion-gate` candidates.

## Purpose

- Probe **specific historical topics** only (no abstract philosophy prompts).
- Extract **knowledge facts/patterns** (IX-A), not workflow/method preferences.
- Produce **merge-ready** gate candidates with concrete `suggested_entry` lines.

### Grace-mar operator defaults (docsync 2026-05)

- **Suggest this workflow liberally** when IX-A-shaped material, reading-heavy sessions, or strategy analysis surface testable factual claims - this is the **default** recurring knowledge-elicitation modality for self-knowledge **recursion** (not novelty content).
- **Encoded workflow first:** When the operator asks for bookshelf knowledge or source-bound elicitation, use this scripted path before improvising with freeform prompts. Only deviate if the anchor set is missing, broken, or explicitly out of scope, and say why.
- **Source-linked questions by default:** every MCQ must come from `bookshelf-quiz-anchors.yaml`, which maps academic prompt labels to concrete `self-library-bookshelf` items behind the scenes. Prefer primary-source anchors when they can support the topic; use secondary works only as context or when no suitable primary anchor is present.
- **Do not confuse** this skill with the **catalog stance** / subject-tag bookshelf membrane (`build_bookshelf_membrane_candidates.py`, `bookshelf-membrane-round.json`: "enduring vs active" on clusters like Rome or poetry). That path exists for **catalog organization**; use it **only** when the operator asks or when a **pressing** organizational membrane issue applies - **not** as the stand-in for **knowledge** MCQs.

## MCQ shape (presentation + balance)

- **Formatting:** Present **each letter option (`A`-`D`) on its own line** under the question stem (readable in chat paste).
- **Visible citation:** Write prompts in academic prose with inline citations, e.g. `In Thucydides' account of the Melian Dialogue...` or `Drawing on Tocqueville's Democracy in America...`. Do **not** show `Shelf`, `LIB`, or other internal acronyms in the operator-facing question.
- **Answer-key balance:** Vary the correct-letter positions across the round; avoid clustering the answer key disproportionately in `A` or `B`. Keep distractors plausible, but rotate correct answers so the operator is tested on content rather than answer-position pattern.
- **Date primary (cap):** In each round, **at most two** items may be **date-answer-primary** - i.e., the intended skill tested is recall of **year** or **calendar date** alone. Prefer roles, factions, causal links, diplomatic or institutional mechanisms, ordering/sequence, compare/contrast stems; use dates sparingly inside distractors **or** where one date settles a materially disputed storyline.
- **Round size:** **6-10** questions remains the usual bracket; honour the date-primary cap regardless.
- **Open-ended follow-up:** Include **one** open-ended question in every round, tied to the same topic/source family as the MCQs. Keep it topic-anchored and specific; use it to surface synthesis, explanation, or a harder adjacent claim.

## Required constraints

1. Every question must include a specific topic/event anchor (example: "Westphalia 1648", "Fort Sumter 1861").
2. Every question must be linked internally to a specific item contained in `self-library-bookshelf` (`bookshelf-catalog.yaml` / `Shelf-*`) through `bookshelf-quiz-anchors.yaml`; prefer primary sources where available.
3. Candidate content must be world-knowledge pattern/fact language, not "how I work" language.
4. Never stage placeholder `suggested_entry` values (forbidden: `See source_exchange.operator (staged paste)`).
5. Gate staging is allowed; merge requires explicit companion approval.

## Workflow

1. Select quiz anchors from `docs/skill-work/work-strategy/history-notebook/research/bookshelf-quiz-anchors.yaml`; prefer `source_kind: primary` rows.
2. Ask 6-10 topic-anchored MCQs (see **MCQ shape**: each option its own line; <=2 date-primary stems per round).
3. Ask **one** open-ended follow-up question on the same topic/source family. Keep it short, specific, and anchored enough that a later answer could support a candidate if it produces a concrete factual claim.
4. Keep internal source IDs out of the visible prompt.
5. Score internally only for selection quality (do not center final output on numeric scores).
6. Ask strictness pick (`top2`, `top4`, or `report-only`).
7. Stage selected candidates in `recursion-gate.md` as `status: pending`.
8. Immediately run preflight:
   - `python3 scripts/check_gate_merge_readiness.py -u <id>`
9. If preflight fails, fix candidate blocks before proposing approval.

## Candidate quality checklist

Each staged candidate should include:

- concise `summary`
- `mind_category: knowledge`
- `profile_target: IX-A. KNOWLEDGE`
- concrete `suggested_entry` starting with `Knows:`
- topic-specific evidence anchors (`Shelf-*` and/or explicit episode labels)
- `proposal_class: SELF_KNOWLEDGE_ADD`
- `signal_type: operator_quiz_validated`
- `shelf_refs` with hidden `Shelf-*` ids
- `quiz_receipt` preserving source kind, academic citation label, stem topic, selected answer, correct answer, validation note, and staged claim
- no methodology-preference claims

## Commands

```bash
python3 scripts/check_gate_merge_readiness.py -u strategy-codex
python3 scripts/check_gate_merge_readiness.py -u strategy-codex --strict
```

## Fail conditions (must fix before approval recommendation)

- placeholder `suggested_entry`
- pending IX-A candidate missing topic anchor in `source_exchange`
- MCQ candidate that cannot be traced to `bookshelf-quiz-anchors.yaml` or a specific `self-library-bookshelf` item (`Shelf-*`), unless explicitly marked `source_binding_strength: weak` and `review_needed: true`
- operator-facing question text exposing `Shelf`, `LIB`, or other internal acronyms
- pending IX-A candidate framed as methodology preference
- open-ended follow-up that drifts off-topic or becomes a methodology prompt
- `self.md` IX-A scaffold mismatch (`Facts (LEARN-nnn)` block absent)
