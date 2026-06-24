---
name: periodic-statecraft-review
description: Compose time-windowed statecraft review passes using active synthesis and judgment skills (replaces deprecated last30days/monthly-deepening and archived framework/multi-lens).
portable: true
version: 0.2.0
scope_class: repo-governed
skills:
  - state-synthesis
  - primary-overhearing-analysis
  - statecraft-intelligence-essay
outputs:
  - bounded review memo or watchlist upgrade
authority: advisory_only
verification_level: receipt_required
risk_tier: medium
---

# Periodic Statecraft Review

## Purpose

Run a periodic review chain for a named time window using **active** statecraft skills — not retired judgment-method stubs.

## Trigger

**Operator phrases:** `runbook periodic review`, `runbook last30`, `runbook monthly deepen`.

**Legacy triggers:** `last30days`, `monthly deepening` — route here (deprecated skill stubs redirect to this runbook).

**Use when:**

- operator wants structured review, not ad-hoc chat synthesis
- wire or archive receipts exist for the window

**Do not use when:**

- archive land incomplete — run intake first
- single-day synthesis suffices — use **`state-synthesis`** only

## Skills Composed

| Mode | Active chain | When |
|------|--------------|------|
| Fast | archive/wire scan → **`state-synthesis`** for window | Rolling ~30-day scan |
| Month | month batch under `source-archive/statecraft/` → **`state-synthesis`** | Calendar month closure |
| Compare | prior synthesis → **`primary-overhearing-analysis`** or **`statecraft-intelligence-essay`** | Layered comparison when object unsettled |

Do **not** invoke `last30days`, `monthly-deepening`, `statecraft-framework`, `statecraft-multi-lens`, or `statecraft-helix-synthesis` — those skills are retired.

## Inputs Required

- Topic or theater scope
- Date window anchor
- Links to archive/synthesis surfaces when available

## Workflow Steps

1. Pick mode (30-day vs month vs compare).
2. Name the window and list archive/synthesis inputs for that window.
3. Run **`state-synthesis`** (or bounded chat review if archive batch incomplete — state gap explicitly).
4. Optionally run **`primary-overhearing-analysis`** or **`statecraft-intelligence-essay`** when comparison or register work adds value.
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

- time window and scope are named
- synthesis or bounded review output is produced or deferral is stated
- links/receipts cited or gaps named

Evidence to report:

- output paths or chat summary
- falsifier lines
- mode selected

## Outputs

- Review memo (chat or notebook candidate)
- Optional comparison block from active judgment skills

## Return Paths

- [skills/runbooks/README.md](README.md)
- [skills/README.md](../README.md)
