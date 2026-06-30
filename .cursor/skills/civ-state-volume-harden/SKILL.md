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
portable_source: skills/civ-state-volume-harden/SKILL.md
synced_by: sync_portable_skills.py
---
# Deprecated — civ-state-volume-harden

**Status:** Deprecated as a standalone entry. Do not invoke this skill directly for new work.

**Use instead:** [`skills/runbooks/civ-state-volume-hardening.runbook.md`](../../skills/runbooks/civ-state-volume-hardening.runbook.md) after **`civ-state`** entry.

## Legacy activation

When the operator names volume hardening without the runbook phrase, redirect once to **`runbook civ state harden`**.

## No independent entry surface

Volume hardening methodology executes inside the runbook workflow. Do not treat this file as a separate operator entrypoint.


## Cursor / strategy-codex instance

**strategy-codex instance notes**

- Canonical front-door doctrine surface: [statecraft/states/README.md](../../../statecraft/states/README.md)
- Canonical volume map: [statecraft/states/volumes/README.md](../../../statecraft/states/volumes/README.md)
- Volume surfaces to harden:
  - [Vol I - China](../../../README.md)
  - [Vol II - Persia](../../../README.md)
  - [Vol III - Rome](../../../README.md)
  - [Vol IV - Russia](../../../README.md)
  - [Vol V - America](../../../README.md)
- Use `civilization_memory` only as evidence for this skill; CIV-STATE surfaces remain the operator-facing layer.
- Keep volume passes bounded to CIV-STATE architecture surfaces unless the operator explicitly widens scope into lane, transaction, or source-memory files.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill civ-state-volume-harden
python scripts/sync_portable_skills.py --verify --skill civ-state-volume-harden
python scripts/validate_skills.py
```
