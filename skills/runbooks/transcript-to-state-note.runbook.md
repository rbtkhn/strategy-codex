---
name: transcript-to-state-note
description: Convert a landed transcript or daily synthesis wedge into one bounded statecraft note.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - statecraft-source-intake
  - state-note
outputs:
  - statecraft/notes bounded note
authority: advisory_only
verification_level: receipt_required
risk_tier: low
---

# Transcript to State Note

## Purpose

Convert a landed transcript or daily synthesis wedge into **one** bounded statecraft note under `statecraft/notes/`.

## Trigger

**Operator phrases:** `runbook state note`, `promote to statecraft note` with a single argument identified.

**Use when:**

- archive or daily parent exists
- one method-bearing argument should survive outside chat

**Do not use when:**

- archive land incomplete — `statecraft-source-intake` first
- whole-day synthesis still needed — `state-synthesis` first
- multiple unsettled claims — `statecraft-multi-lens` or daily synthesis
- essay-class prose intended — `docs/prose-index.md` route
- lane intake unresolved — `statecraft-lane-intake-router` or `state-deploy`

## Skills Composed

| Step | Skill | Role |
|---:|---|---|
| 1 | `statecraft-source-intake` | Verify archive floor or complete land |
| 2 | `state-note` | Promote one bounded argument to `statecraft/notes/` |

## Inputs Required

- Archive path or parent daily/synthesis link
- Single argument to promote
- Falsifier or revisit trigger (required for note)

## Workflow Steps

1. Confirm archive or daily parent exists and is linked.
2. Extract **one** argument — mechanism, seam, or threshold distinction.
3. Run **`state-note`** promotion discipline — note-shaped, not daily-shaped.
4. Link archive or parent daily in note frontmatter/body.
5. Add falsifier or revisit trigger line.

## Human Approval Points

- Before creating note file (operator explicit or clear promote intent)
- Before any cross-lane or essay promotion

## Stop Conditions

Stop if:

- more than one competing argument remains unsettled
- note would mirror full daily synthesis or essay class
- archive anchor missing

## Verification / Proof Standard

Do not call this runbook complete unless:

- note contains **one** argument only
- note links archive or parent daily
- note includes falsifier or revisit trigger
- note is under `statecraft/notes/` and is not pretending to be full daily or essay

Evidence to report:

- note path
- parent archive/daily link
- falsifier line quoted or summarized

## Outputs

- Single file under `statecraft/notes/`

## Return Paths

- [skills/runbooks/README.md](README.md)
- [skills/state-note/SKILL.md](../state-note/SKILL.md)
- [skills/_schema.md](../_schema.md)
