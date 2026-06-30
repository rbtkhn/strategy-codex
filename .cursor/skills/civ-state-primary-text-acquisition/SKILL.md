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
portable_source: skills/civ-state-primary-text-acquisition/SKILL.md
synced_by: sync_portable_skills.py
---
# Deprecated — civ-state-primary-text-acquisition

**Status:** Deprecated as a standalone entry. Do not invoke this skill directly for new work.

**Use instead:** [`skills/runbooks/civ-state-primary-text.runbook.md`](../../skills/runbooks/civ-state-primary-text.runbook.md) after **`civ-state`** entry.

## Legacy activation

When the operator names primary-text acquisition without the runbook phrase, redirect once to **`runbook civ state primary text`**.

## No independent entry surface

Acquisition methodology executes inside the runbook workflow. Do not treat this file as a separate operator entrypoint.


## Cursor / strategy-codex instance

**strategy-codex instance notes**

- Canonical doctrine note for this skill: [statecraft/states/primary-text-architecture.md](../../../statecraft/states/primary-text-architecture.md)
- Canonical structured layers:
  - [source-records](../../../statecraft/states/source-records/README.md)
  - [source-excerpts](../../../statecraft/states/source-excerpts/README.md)
  - [source-sidecar](../../../statecraft/states/source-sidecar/README.md)
- Current pilot records live under:
  - [statecraft/states/source-records/pilot](../../../statecraft/states/source-records/pilot)

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill civ-state-primary-text-acquisition
python scripts/sync_portable_skills.py --verify --skill civ-state-primary-text-acquisition
python scripts/validate_skills.py
```
