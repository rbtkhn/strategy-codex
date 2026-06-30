---
name: chapter-seeding
description: Compose arc-to-chapter-seeds with PH/book writer skills for chapter spine work.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - arc-to-chapter-seeds
outputs:
  - chapter seed candidates under predictive-history or civ-state trees
authority: advisory_only
verification_level: receipt_required
risk_tier: medium
surfaces:
  - continuity/predictive-history/BOOK-ARCHITECTURE.md
---

# Chapter Seeding

## Purpose

Turn a bounded arc into chapter seeds and optional PH-CIV spine extensions.

## Trigger

**Operator phrases:** `runbook chapter seed`, `seed chapters from arc`.

## Skills Composed

| Step | Skill / surface | Role |
|---:|---|---|
| 1 | `arc-to-chapter-seeds` | Extract chapter seeds from arc |
| 2 | `predictive-history-chapter-spine` (Cursor) | Extend PH chapter spine when PH lane active |
| 3 | `civilization-part-writer` / `empire-part-writer` (Cursor) | Part writers when drafting |

## Inputs Required

- Arc source (essay, synthesis, operator outline)
- Target book/volume id
- Public vs internal boundary decision

## Workflow Steps

1. Run **`arc-to-chapter-seeds`** on bounded arc.
2. When PH lane active, invoke **`predictive-history-chapter-spine`** (Cursor).
3. Route drafts to part writers only on explicit operator pick.
4. Stop before public publish — edit and push `rbtkhn/predictive-history`; optional inbound sync in strategy-codex.

## Human Approval Points

- Before promoting seeds to canonical chapter list
- Before public PH-CIV publish

## Stop Conditions

Stop if:

- arc scope ambiguous
- public boundary violated

## Verification / Proof Standard

Do not call this runbook complete unless:

- seed list produced with source links
- target volume/path named
- publish boundary stated

## Outputs

- Chapter seed list (markdown candidate)
- Optional spine diff path

## Return Paths

- [skills/runbooks/README.md](README.md)
- [continuity/predictive-history/BOOK-ARCHITECTURE.md](../../continuity/predictive-history/BOOK-ARCHITECTURE.md)
