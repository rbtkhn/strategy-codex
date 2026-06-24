---
name: civ-state-primary-text-acquisition
description: Deprecated standalone entry — use civ-state-primary-text runbook for new work.
portable: true
version: 0.2.0
category: legacy-redirect
status: deprecated
replacement: civ-state-primary-text
scope_class: repo-governed
review_date: 2026-12-31
tags:
  - operator
  - deprecated
  - civ-state
  - primary-sources
---
# Deprecated — civ-state-primary-text-acquisition

**Status:** Deprecated as a standalone entry. Do not invoke this skill directly for new work.

**Use instead:** [`skills/runbooks/civ-state-primary-text.runbook.md`](../runbooks/civ-state-primary-text.runbook.md) after **`civ-state`** entry.

## Legacy activation

When the operator names primary-text acquisition without the runbook phrase, redirect once to **`runbook civ state primary text`**.

## No independent entry surface

Acquisition methodology executes inside the runbook workflow. Do not treat this file as a separate operator entrypoint.
