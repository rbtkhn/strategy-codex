---
name: "singularity-note-promotion"
description: "Promote one bounded argument from a singularity monthly synthesis into a reusable note without overpromoting it into a broad essay. Use when a month memo contains one route-worthy claim that should become a stand-alone singularity note with source anchors, action wedges, and return paths."
portable: true
version: "0.1.0"
tags:
  - "operator"
  - "singularity"
  - "synthesis"
  - "notes"
  - "promotion"
portable_source: "skills-portable/singularity-note-promotion/SKILL.md"
synced_by: "sync_portable_skills.py"
---
# Singularity Note Promotion

Use this skill when one argument inside a singularity synthesis memo has become reusable enough to stand alone as a **note**, but not yet broad or settled enough to become an essay.

## Boundary

- WORK only; not Record.
- Promote one bounded argument, not the whole month.
- Keep the note argument-shaped, not archive-shaped.
- Do not use note promotion to smuggle in a broad doctrine that still belongs in synthesis.

## When to use

Use this skill when all of the following are true:

- a month memo already exists
- one claim or wedge is clearly stronger than the rest
- the claim can travel beyond the month while still staying bounded
- the operator would benefit from a reusable argument surface

If the month still has multiple competing candidate claims, stay in synthesis first.

## Workflow

### 1. Pick exactly one promotable claim

Choose one object such as:

- a substrate claim
- a control-plane claim
- a labor-compression claim
- a trust/provenance claim
- a route-to-statecraft claim

If you find yourself drafting "the whole month," narrow further.

### 2. Preserve the parent-child relationship

The new note should remain visibly downstream of the synthesis month:

- the note points back to the parent month
- the parent month points to the promoted note
- the notes shelf index gains an entry

Do not let the promotion sever provenance.

### 3. Use the bounded-note shape

A strong promoted note usually includes:

- `Purpose`
- `Core claim`
- `Why this matters`
- `Pattern` or `Control-plane read`
- `Failure modes`
- `Action wedges`
- `Best pairings`
- `Source anchors`
- `Next use`

Do not bloat the note into a pseudo-essay.

### 4. Preserve source anchors

Name the exact month sources or source sheets carrying the argument.

Prefer:

- source-sheet anchors
- a small number of raw checkpoints
- the parent synthesis memo

Do not widen the source base just to make the note sound more authoritative.

### 5. Keep the note reusable

The note should answer:

- what is the bounded argument?
- what operator problem does it help with?
- when should someone reach for it again?

If it cannot be reused outside the original month, it is not ready for promotion.

### 6. Guard against overpromotion

Before finalizing, ask:

1. Is this still one argument?
2. Could this live comfortably inside `notes/` rather than `essays/`?
3. Does the note still need the parent month to explain everything?
4. Did the promotion make the route clearer than before?

If `2` is no, move toward essay work instead.
If `3` is yes, the note is not yet mature enough.

## Success condition

The new note becomes a reusable singularity argument with clear source anchors and clear return paths, while the parent month remains the owning context for everything that was not promoted.



## Cursor / grace-mar instance

**strategy-codex instance notes**

- Parent synthesis shelf: [singularity/synthesis](/C:/dev/strategy-codex/singularity/synthesis)
- Notes shelf: [singularity/notes](/C:/dev/strategy-codex/singularity/notes/README.md)
- Current promoted example: [compute-political-currency-control-plane-substrate.md](/C:/dev/strategy-codex/singularity/notes/compute-political-currency-control-plane-substrate.md)
- Parent month example: [2026-05.md](/C:/dev/strategy-codex/singularity/synthesis/2026-05.md)
- Notes index: [singularity/notes/README.md](/C:/dev/strategy-codex/singularity/notes/README.md)

**Repo notes**

- Promotion in this repo should be bidirectional: the new note links back to the month, and the month records the completed `promote_to_note` route.
- Use source sheets and a few raw checkpoints as anchors; do not restate the entire month.
- If the argument starts absorbing too many fronts at once, stop and keep it in synthesis.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill singularity-note-promotion
python scripts/sync_portable_skills.py --verify --skill singularity-note-promotion
python scripts/validate_skills.py
```
