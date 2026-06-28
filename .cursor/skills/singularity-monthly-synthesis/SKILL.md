---
name: singularity-monthly-synthesis
description: Deepen a dated singularity month into a synthesis-first monthly memo with actionable ideas, route decisions, and minimal typed support notes. Use when the operator wants an Innermost Loop or similar month scaffold generated, deepened, reviewed, or extended without sliding back into issue-by-issue commentary.
portable: true
version: 0.1.0
category: judgment-enhancement
status: active
scope_class: repo-governed
tags:
- operator
- singularity
- synthesis
- monthly
- longitudinal
portable_source: skills/singularity-monthly-synthesis/SKILL.md
synced_by: sync_portable_skills.py
---
# Singularity Monthly Synthesis

Use this skill to build or deepen a **monthly synthesis layer** over a dated singularity corpus.

The primary unit is the **month memo**, not the individual issue. Use issue-level notes only when they materially improve provenance, chronology, counterweight, or action extraction.

## Boundary

- WORK only; not Record.
- Archive truth stays upstream in raw captures and deterministic longitudinal surfaces.
- Do not turn the month into equal-weight commentary on every issue.
- Do not overgenerate support notes.
- Do not promote the month into an essay just because the source month is rich.

## Preconditions

Use this skill when most of the following are already true:

- raw captures for the month exist
- a dated spine or equivalent chronology already exists
- the operator wants synthesis, not archive recovery
- the output surface is `monthly synthesis`, not a one-off strategy note

If raw capture or chronology is still missing, use a source-intake or backfill skill first.

## Core rule

`Archive -> Spine -> Minimal support -> Monthly synthesis -> Promotion or route-away`

The month memo is the main analytical object. Support notes exist to help the month memo stay honest, not to become a second archive.

## Workflow

### 1. Ground the month before writing

Read the month scaffold, the relevant dated spine window, and the strongest source anchors for the month.

Prefer:

- the month synthesis scaffold
- source sheets already built for the month
- a few raw checkpoints that show the month bend

Do not pretend the final cluster is the whole month if earlier signals materially changed the story.

### 2. Name the month's real object

Decide what the month actually is, for example:

- inflection month
- control-plane compression month
- substrate-legitimacy month
- workflow substitution month
- agent-governance month

If you cannot state the month object in one sentence, keep reading before drafting.

### 3. Keep support notes minimal and typed

Support notes should exist only when one of these is true:

- the issue is a **first-front anchor**
- the issue is a **chronology anomaly** or deterministic ambiguity that changes the month read
- the issue already has a **source sheet** and is carrying a major action wedge

Preferred support-note roles:

- `chronology_clarifier`
- `counterweight`
- `misreading_correction`
- `substrate_anchor`
- `action_wedge_seed`

Do not create support notes for ordinary issue density, generic importance, or because the month has many interesting items.

### 4. Deepen the month memo, not the archive

Every deepened month should fill these sections with real analysis:

- `Source Support Block`
- `Month in one paragraph`
- `What materially changed`
- `Control-plane shifts`
- `Actionable ideas`
- `Open tensions`
- `Route decisions`
- `Failure-mode check`

Favor:

- strongest patterns over exhaustive recap
- control-plane consequences over benchmark narration
- reusable wedges over elegant summary

### 5. Make action wedges mandatory

Each month should produce 2-5 concrete wedges tagged such as:

- `monitor`
- `prepare`
- `contain`
- `build`
- `route_to_statecraft`
- `route_to_work_dev`
- `route_to_work_cici`
- `promote_to_note`
- `promote_to_essay`

Every wedge should name the anchor issues, source sheets, or support notes that justify it.

### 6. Route the month honestly

At the end of the pass, decide whether the strongest next move is:

- stay in synthesis
- promote one bounded note
- promote an essay
- route to statecraft
- route to work-dev
- route to work-cici

Do not leave route decisions as decorative prose.

### 7. Review against failure modes

Check the memo against:

- `hype_smoothing`
- `substrate_erasure`
- `action_theater`
- `cross_front_blur`
- `counterweight_failure`
- `overpromotion`
- `commentary_inflation`

If the month fails one of these, say so directly and narrow the claim.

## Promotion rule

Promote to `notes/` when one argument from the month becomes reusable on its own.

Promote to `essays/` only when the month's claim can carry a larger stand-alone argument without depending on month-bound scaffolding.

## Success condition

The month reads as a governed analytical machine:

- source-bound
- route-bearing
- action-yielding
- resistant to commentary sprawl



## Cursor / strategy-codex instance

**strategy-codex instance notes**

- Canonical synthesis shelf: [singularity/synthesis](../../../singularity/synthesis)
- Canonical support-note shelf: [singularity/synthesis/support](../../../singularity/synthesis/support)
- Canonical month example: [2026-05.md](../../../singularity/synthesis/2026-05.md)
- Deterministic spine: [singularity/workshop/longitudinal/innermost-loop.md](../../../singularity/workshop/longitudinal/innermost-loop.md)
- Structured spine index: [innermost-loop-signals.json](../../../singularity/workshop/longitudinal/innermost-loop-signals.json)
- Source-sheet anchors: [singularity/workshop/sheets](../../../singularity/workshop/sheets)
- Raw archive: [source-archive/singularity/innermost-loop](../../../source-archive/singularity/innermost-loop)
- Generator: [scripts/build_innermost_loop_synthesis.py](../../../scripts/build_innermost_loop_synthesis.py)

**Repo notes**

- In this repo, Innermost Loop monthly work is explicitly **synthesis-first**, not commentary-first.
- The month memo is the primary object; support notes should stay scarce and typed.
- The current support-note rule for this shelf is intentionally narrow: first-front anchors, chronology anomalies, or source-sheet-backed action wedges.
- Promotion targets live at [singularity/notes](../../../singularity/notes) and [singularity/essays](../../../singularity/essays).

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill singularity-monthly-synthesis
python scripts/sync_portable_skills.py --verify --skill singularity-monthly-synthesis
python scripts/validate_skills.py
python scripts/build_innermost_loop_synthesis.py
```
