---
name: speaker-shelf-hygiene
description: Deprecated speaker shelf helper — use speaker-shelf-maintenance runbook (hygiene mode) for new work.
preferred_activation: speaker shelf
activation: speaker shelf
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
# Deprecated — speaker-shelf-hygiene

**Status:** Deprecated. Do not invoke this skill for new work.

**Use instead:** [`skills/runbooks/speaker-shelf-maintenance.runbook.md`](../../../skills/runbooks/speaker-shelf-maintenance.runbook.md) — **hygiene** mode.

## Legacy activation

When the operator says **`speaker shelf`** or asks for arc/month/citation hygiene on a speaker folder, route once to **`runbook speaker shelf`** (hygiene mode unless continuity or membrane is clearly the ask).

## No independent entry surface

Shelf audit doctrine executes inside the runbook. Do not treat this file as a separate operator entrypoint.
