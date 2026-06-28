---
name: civ-state-volume-harden
description: Deprecated standalone entry — use civ-state-volume-hardening runbook for new work.
portable: true
version: 0.2.1
category: legacy-redirect
status: deprecated
replacement: civ-state-volume-hardening
scope_class: repo-governed
review_date: 2026-12-31
tags:
  - operator
  - deprecated
  - civ-state
  - doctrine
---
# Deprecated — civ-state-volume-harden

**Status:** Deprecated as a standalone entry. Do not invoke this skill directly for new work.

**Use instead:** [`skills/runbooks/civ-state-volume-hardening.runbook.md`](../../skills/runbooks/civ-state-volume-hardening.runbook.md) after **`civ-state`** entry.

## Legacy activation

When the operator names volume hardening without the runbook phrase, redirect once to **`runbook civ state harden`**.

## No independent entry surface

Volume hardening methodology executes inside the runbook workflow. Do not treat this file as a separate operator entrypoint.
