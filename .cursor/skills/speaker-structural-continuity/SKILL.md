---
name: speaker-structural-continuity
description: Deprecated speaker shelf helper — use speaker-shelf-maintenance runbook (continuity mode) for new work.
preferred_activation: speaker continuity
activation: speaker continuity
category: legacy-redirect
status: deprecated
replacement: speaker-shelf-maintenance
scope_class: repo-governed
review_date: 2026-12-31
tags:
  - operator
  - deprecated
  - strategy-codex
  - speakers
---
# Deprecated — speaker-structural-continuity

**Status:** Deprecated. Do not invoke this skill for new work.

**Use instead:** [`skills/runbooks/speaker-shelf-maintenance.runbook.md`](../../../skills/runbooks/speaker-shelf-maintenance.runbook.md) — **continuity** mode.

## Legacy activation

When the operator asks whether canonical speaker surfaces **agree** (route stack, month ladder, maturity labels), route once to **`runbook speaker shelf`** with continuity mode.

## No independent entry surface

Structural continuity checks execute inside the runbook. Do not treat this file as a separate operator entrypoint.
