---
name: lane-survey
description: Deprecated domain helper — use domain-lane-survey runbook for new work.
preferred_activation: survey
activation: survey
category: legacy-redirect
status: deprecated
replacement: domain-lane-survey
scope_class: repo-governed
review_date: 2026-12-31
tags:
  - operator
  - deprecated
  - domain-pack
---
# Deprecated — lane-survey

**Status:** Deprecated. Do not invoke this skill for new work.

**Use instead:** [`skills/runbooks/domain-lane-survey.runbook.md`](../../../skills/runbooks/domain-lane-survey.runbook.md).

## Legacy activation

When the operator says **`lane survey`** or **`survey [lane]`**, route once to **`runbook lane survey`**.

## No independent entry surface

Landscape scan methodology executes inside the runbook. Do not treat this file as a separate operator entrypoint.
