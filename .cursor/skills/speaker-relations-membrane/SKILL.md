---
name: speaker-relations-membrane
description: Deprecated speaker shelf helper — use speaker-shelf-maintenance runbook (membrane mode) for new work.
preferred_activation: speaker membrane
activation: speaker membrane
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
  - membrane
---
# Deprecated — speaker-relations-membrane

**Status:** Deprecated. Do not invoke this skill for new work.

**Use instead:** [`skills/runbooks/speaker-shelf-maintenance.runbook.md`](../../../skills/runbooks/speaker-shelf-maintenance.runbook.md) — **membrane** mode.

## Legacy activation

When the operator says **`speaker membrane`** or asks whether a note belongs in one speaker shelf vs `statecraft/notes/` (cross-speaker compare), route once to **`runbook speaker membrane`**.

## No independent entry surface

Relations membrane workflow executes inside the runbook. Do not treat this file as a separate operator entrypoint.
