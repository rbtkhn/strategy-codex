---
name: monthly-deepening
description: Handle bounded month-by-month deepening for speaker or stream corpora. Use when the operator wants a month inventory, missing-list, URL recovery pass, full-transcript vs stub classification, high-value target selection, month-shelf extension, or a commit limited to one month slice. Do not use for one-off transcript intake, direct YouTube caption fetch, or broad cross-month synthesis. Transcript uploads from the operator imply month-slice materialization unless the operator explicitly says inventory-only, classification-only, or do-not-write.
portable: true
version: 0.1.0
tags:
  - operator
  - strategy
  - statecraft
  - monthly
  - transcript
  - inventory
---

# Monthly Deepening

## Overview

Use this workflow to keep monthly deepening truthful and request-shaped. The core rule is simple: first determine whether the user wants a report, a recovery pass, a classification pass, a shelf-building pass, or a commit. Do not jump from one mode to another without explicit user intent.

## Operator Transcript Convention

If the operator pastes or uploads a full transcript during monthly deepening work, treat that as an implicit request to materialize the capture into the canonical repo surface for that month.

Default behavior after a transcript upload:

- create the canonical capture file in the appropriate archive location
- classify it accurately
- include it in the month inventory on subsequent passes
- refresh only the bounded generated surfaces needed for that speaker or month when practical

Do not wait for a separate `please materialize this` instruction unless the operator explicitly says:

- `inventory only`
- `classification only`
- `do not write files`
- or otherwise limits the task to reporting

This convention applies to uploaded or pasted transcripts, not to mere mentions of titles or URLs.

## Workflow

### 1. Classify the request before doing work

Put the request in exactly one of these buckets first:

- `inventory`: list what exists for a month
- `missing`: list what is absent or unresolved for a month
- `url-recovery`: provide or recover direct watch URLs
- `classification`: split full transcripts from stubs or mirrors
- `selection`: choose the highest-value remaining targets
- `shelf-build`: create or extend monthly shelf files and wiring
- `commit`: isolate and commit only the bounded month slice

If the user asked for URLs or a list, stay in `inventory`, `missing`, `url-recovery`, or `classification`. Do not start editing files.

Exception:

- if the operator has pasted or uploaded a transcript body, classify the surrounding request normally but treat the transcript itself as materialization work unless the operator explicitly restricted the turn to reporting only

### 2. Build the month inventory from local evidence

Use local repo evidence first:

- canonical source-archive date folders
- any relevant speaker raw-input index or speaker arc
- local receipts in cognition-stream or observability artifacts
- legacy raw-input or provenance paths when current archive surfaces are incomplete

Before counting items, fix the scope:

- `speaker-only`: the named speaker's own channel or canonical thread items only
- `speaker-adjacent`: interviews, panels, or host-crossovers where the speaker appears but is not the primary channel owner
- `mixed`: both, but labeled separately

Do not silently convert `speaker-adjacent` material into `speaker-only` coverage.

For each discovered item, separate it into:

- `present with URL`
- `present but URL missing`
- `mentioned in legacy or receipts only`
- `uncaptured but direct URL known`
- `not recoverable from local evidence`

Do not silently merge these categories.

### 3. Answer the exact question asked

Answer shape rules:

- If asked for `all entries and URLs`, return the month list with URLs if available.
- If asked for `full transcripts vs stubs`, classify only.
- If asked for `5 high-value missing`, give only the missing candidates, not present ones.
- If local evidence cannot support `5` truthful candidates, say so directly and provide the largest defensible set.
- If a watch URL is still unknown, say `URL unrecovered locally` rather than guessing.

### 4. Choose high-value targets carefully

When choosing high-value missing items, prioritize:

- bridge value between nearby confirmed captures
- transcript-bearing or likely transcript-bearing episodes
- cross-host reinforcement that compounds speaker reuse
- hinge episodes that clarify the month's dominant themes
- unresolved URL or transcript gaps that block routing later

Do not recommend already-captured items as `missing`.

### 5. Only build shelves when explicitly asked

When the user explicitly asks to deepen a month into repo artifacts:

- derive the month shape from actual captures, not symmetry
- assign an honest month status such as `prehistory setup`, `hinge`, `thin month`, or similar
- wire only the minimum supporting surfaces needed
- keep chronology ownership with the native stream or raw-input layer
- verify links locally before presenting the result

Materializing transcript uploads is not the same as shelf-building. Transcript materialization should happen by default under the operator transcript convention even when the user did not ask for a shelf.

### 6. Commit bounded slices only

If the user asks to commit:

- inspect the full worktree first
- stage only the files for the single requested month slice
- confirm the staged diff is bounded
- leave unrelated dirty state untouched

### 7. Failure-mode guardrails

Do not:

- convert a URL request into shelf-building
- convert a classification request into a commit
- imply there are `5` missing items when local evidence only proves `1` or `2`
- flatten `present but URL missing` into `missing`
- overstate confidence about dates or watch IDs

Preferred recovery language:

- `I can confirm these are present.`
- `This item exists locally but its direct YouTube watch URL is still unrecovered.`
- `I cannot truthfully produce five exact missing Mercouris February URLs from local evidence.`
