---
name: periodic-statecraft-review
description: Compose time-windowed statecraft review passes from last30days through framework and multi-lens.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - last30days
  - monthly-deepening
  - statecraft-framework
  - statecraft-multi-lens
outputs:
  - bounded review memo or watchlist upgrade
authority: advisory_only
verification_level: receipt_required
risk_tier: medium
---

# Periodic Statecraft Review

## Purpose

Run a periodic review chain selecting time window (30-day vs month-scale) then judgment enhancers.

## Trigger

**Operator phrases:** `runbook periodic review`, `runbook last30`, `runbook monthly deepen`.

**Use when:**

- operator wants structured review, not ad-hoc chat synthesis
- wire or archive receipts exist for the window

**Do not use when:**

- archive land incomplete — run intake first
- single-object lens suffices — use one skill only

## Skills Composed

| Mode | Skills | When |
|------|--------|------|
| Fast | `last30days` → `statecraft-framework` | Rolling 30-day scan |
| Month | `monthly-deepening` → `statecraft-framework` | Calendar month closure |
| Compare | prior output → `statecraft-multi-lens` | Multi-preset comparison on live object |

## Inputs Required

- Topic or theater scope
- Date window anchor
- Links to archive/synthesis surfaces when available

## Workflow Steps

1. Pick mode (30-day vs month vs compare).
2. Run window skill (`last30days` or `monthly-deepening`).
3. Run **`statecraft-framework`** on findings.
4. Optionally run **`statecraft-multi-lens`** when comparison adds value.
5. Report receipts and falsifiers; do not auto-promote synthesis.

## Human Approval Points

- Before promoting findings to daily/monthly shelf
- Before public copy

## Stop Conditions

Stop if:

- evidence for window is thin — state downgrade explicitly
- operator declines comparison pass

## Verification / Proof Standard

Do not call this runbook complete unless:

- window skill produced bounded output
- framework pass applied to that output
- links/receipts cited or gaps named

Evidence to report:

- output paths or chat summary
- falsifier lines
- mode selected

## Outputs

- Review memo (chat or notebook candidate)
- Optional multi-lens comparison block

## Return Paths

- [skills/runbooks/README.md](README.md)
- [skills/README.md](../README.md)
