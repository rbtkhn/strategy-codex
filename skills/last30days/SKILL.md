---
name: last30days
description: Deprecated legacy judgment-review skill. Use the periodic-statecraft-review runbook for new work.
preferred_activation: last30days
activation: last30days
portable: true
version: 0.2.0
category: legacy-redirect
status: deprecated
replacement: periodic-statecraft-review
scope_class: repo-governed
review_date: 2026-12-31
tags:
  - operator
  - deprecated
  - statecraft
---
# Deprecated — last30days

**Status:** Deprecated. Do not use this skill for new work.

**Use instead:** [`skills/runbooks/periodic-statecraft-review.runbook.md`](../runbooks/periodic-statecraft-review.runbook.md).

This file remains only for legacy trigger compatibility.

## Legacy activation

When the operator says `last30days`, route to the `periodic-statecraft-review` runbook if a time-window review is still intended.

## No independent methodology

This file must not contain independent judgment-review doctrine. Put workflow composition in the runbook and current methodology in active skills.
