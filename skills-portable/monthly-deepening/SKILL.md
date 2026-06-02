---
name: monthly-deepening
description: Handle bounded month-by-month deepening for speaker or stream corpora. Use when the operator wants a month inventory, missing-list, URL recovery pass, full-transcript vs stub classification, high-value target selection, month-shelf extension, month-route judgment, or a commit limited to one month slice. Do not use for one-off transcript intake, direct YouTube caption fetch, or broad cross-month synthesis. Transcript uploads from the operator imply month-slice materialization unless the operator explicitly says inventory-only, classification-only, or do-not-write.
portable: true
version: 0.3.0
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

Use this workflow to keep monthly deepening truthful and request-shaped. The core rule is simple: first determine whether the user wants a report, a recovery pass, a classification pass, a shelf-building pass, or a commit. Then determine what kind of month object the evidence actually supports. Do not jump from one mode to another without explicit user intent, and do not force a month into the wrong shelf class just because it feels important.

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

### 1a. Route the month object before writing shelf prose

When the request moves beyond list-making into month interpretation or shelf-building, choose exactly one month route first:

- `closure-audit`: use when the month has a finite contradiction queue or a bounded completeness claim that can be falsified, repaired, or closed
- `watchlist`: use when the real question is archive representation, thinness, or backfill priority rather than closure
- `benchmark`: use when the month is already dense and coherent enough to preserve for later comparison, not to reopen by default

Choose the route from local evidence, not from intuition about which month feels important.

Short rules:

- if the month has a small, URL-backed candidate queue and an unsafe completeness claim, choose `closure-audit`
- if the month mainly needs present/thin/backfill judgment, choose `watchlist`
- if the month already has stable meaning across existing shelves and the best use is later comparison, choose `benchmark`

Do not hybridize these by default. If the month wants two jobs, pick the dominant one and name the other as a later promotion or companion note.

### 1b. Consult the month routing infrastructure before drafting

Before drafting or extending month prose, check these support surfaces:

- human-facing registry: `statecraft/notes/month-maturity-routing-registry.md`
- machine-readable registry: `statecraft/data/month-maturity-routing-registry.json`
- generated routing metadata: `statecraft/data/month-routing-metadata.json`

If the month is already registered, treat that route as the current persisted truth unless new local evidence clearly forces a repair.

Use the standard month templates when creating new month notes:

- `statecraft/templates/month-benchmark-note-template.md`
- `statecraft/templates/month-watchlist-note-template.md`
- `statecraft/templates/month-closure-audit-template.md`
- `scripts/scaffold_statecraft_month_note.py` when you want a registry-aware starter draft instead of building a month note by hand

The registry is the persistence layer for month routing decisions already made. The month note still owns the month's substantive local argument.

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
- decide whether the month artifact is a `closure-audit`, `watchlist`, or `benchmark` before drafting
- wire only the minimum supporting surfaces needed
- keep chronology ownership with the native stream or raw-input layer
- verify links locally before presenting the result

Materializing transcript uploads is not the same as shelf-building. Transcript materialization should happen by default under the operator transcript convention even when the user did not ask for a shelf.

### 5a. Use the correct month output contract

If the month artifact is a `closure-audit`, it should usually include:

- current on-disk baseline
- contradiction or candidate queue
- candidate status with direct URLs when known
- explicit month verdict such as `audited and confirmed complete`, `needs contradiction repair`, or `needs backfill attention`

If the month artifact is a `watchlist`, it should usually include:

- exact month window
- clear statement that the judgment is about local archive coverage
- three buckets such as `healthy coverage`, `thin but acceptable`, and `needs backfill attention`
- any label-normalization caveat that materially affects counting

If the month artifact is a `benchmark`, it should usually include:

- what the month is at month scale
- which existing speaker or bridge surfaces make the month reusable
- what the month is good for in later comparisons
- what the month still needs without reopening a capture campaign

Prefer the standard template paths above rather than recreating the section order from scratch.

Do not let a `benchmark` quietly acquire a missing-candidate queue, and do not let a `watchlist` pretend it has already earned closure.

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
- convert a benchmark month into a backfill campaign without a real finite queue
- convert a watchlist month into a closure claim without a bounded contradiction object
- imply there are `5` missing items when local evidence only proves `1` or `2`
- flatten `present but URL missing` into `missing`
- overstate confidence about dates or watch IDs

Preferred recovery language:

- `I can confirm these are present.`
- `This item exists locally but its direct YouTube watch URL is still unrecovered.`
- `I cannot truthfully produce five exact missing Mercouris February URLs from local evidence.`
