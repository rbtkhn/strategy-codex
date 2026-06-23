# Authority ambiguity vs file abundance

## Purpose

Give future stewardship and cleanup passes a better first diagnosis when the root tree feels noisy or dangerous.

The recurring mistake is to say:

- "there are too many files"

when the sharper truth is often:

- "there are too many files whose **authority relationship** is not legible enough"

This note exists to keep those diagnoses separate.

## Core rule

**File abundance is only a secondary problem. Authority ambiguity is the primary membrane problem.**

A repo can contain many root-level files and still be healthy if each one is clearly one of:

- canonical
- optional but legitimate
- compatibility-only
- derived
- transitional

The membrane becomes dangerous when that classification is unclear, inconsistent, or split across multiple naming grammars.

## Why this matters

When operators or assistants misread abundance as the main issue, they reach for the wrong remedies:

- broad deletion
- surface consolidation
- flattening distinct roles into one file
- cleanup that improves aesthetics but weakens governance clarity

The actual governance risk is usually different:

- a compatibility pointer mistaken for canon
- a derived file mistaken for a merge surface
- a transitional file treated as permanent truth
- a naming contract that makes two legitimate surfaces feel like duplicates

## The Strategy-codex lesson

The recent root-surface audit showed that the sharpest hazard was not simply the number of files.

The deeper issue was:

- continuity was being preserved faster than legible authority was being reasserted

That produced a tree where several surfaces could be read incorrectly even when they were individually defensible.

Examples of this pattern:

- `self-archive.md` versus `self-evidence.md`
- `self-library.md` versus ``
- `skill-think.md` / `skill-write.md` / `skill-steward.md` versus `self-skill-*` language in doctrine

These are not all "duplicates" in the same sense.
The danger is that the repo can make them *feel* equivalent when they are not.

## Membrane-first diagnostic sequence

Before calling a surface cluster "duplicate" or "too large," ask:

1. Is each surface canonical, optional, derived, compatibility-only, or transitional?
2. Is that status stated clearly in one place the operator can actually find?
3. Do docs, scripts, and filenames teach the same authority story?
4. Is the danger semantic, not numerical?

If the answers are unclear, stop diagnosing abundance and start diagnosing authority ambiguity.

## What abundance really means

Abundance becomes a real problem only when it creates one of these downstream failures:

- slower orientation
- wrong merge intuition
- false duplicate anxiety
- higher cleanup cost
- easier boundary mistakes

So abundance is best treated as a **multiplier** of authority ambiguity, not its root cause.

## Naming and triadic risk

Naming ambiguity is especially dangerous when it changes the *felt ontology* of the system.

In this repo, the `skill-*` versus `self-skill-*` ambiguity does more than create search friction.
It risks inviting a system-first reading in which the triad feels like a modular toolkit rather than a governed authority structure.

That is a membrane problem, not a tidiness problem.

## Practical steward rule

When a cleanup pass encounters apparent duplicates:

- do **not** begin with deletion
- do **not** begin with consolidation
- begin by writing the authority classification down

Only after the authority map is legible should you decide:

- track
- rename
- deprecate
- pointerize
- derive
- archive
- remove

## Short steward heuristic

Use this sentence as a check:

**"Is this dangerous because there are many files, or because I cannot tell which file has the right to mean what?"**

If the second clause is doing the real work, the pass is a membrane clarification problem, not a file-count problem.

## Relationship to the recent audit

Companion note:

- [duplicate-canonical-surfaces-audit-2026-05-12.md](dev-notebook/work-dev/duplicate-canonical-surfaces-audit-2026-05-12.md)

That audit is the concrete case.
This note is the durable steward doctrine extracted from it.
