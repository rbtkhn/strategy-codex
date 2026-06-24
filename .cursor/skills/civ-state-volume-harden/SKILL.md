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

**Use instead:** [`skills/runbooks/civ-state-volume-hardening.runbook.md`](../runbooks/civ-state-volume-hardening.runbook.md) after **`civ-state`** entry.

## Legacy activation

When the operator names volume hardening without the runbook phrase, redirect once to **`runbook civ state harden`**.

## No independent entry surface

Volume hardening methodology executes inside the runbook workflow. Do not treat this file as a separate operator entrypoint.


## Cursor / strategy-codex instance

**strategy-codex instance notes**

- Canonical front-door doctrine surface: [statecraft/states/README.md](/C:/dev/strategy-codex/statecraft/states/README.md)
- Canonical volume map: [statecraft/states/volumes/README.md](/C:/dev/strategy-codex/statecraft/states/volumes/README.md)
- Volume surfaces to harden:
  - [Vol I - China](/C:/dev/strategy-codex/statecraft/states/volumes/vol-i-china/README.md)
  - [Vol II - Persia](/C:/dev/strategy-codex/statecraft/states/volumes/vol-ii-persia/README.md)
  - [Vol III - Rome](/C:/dev/strategy-codex/statecraft/states/volumes/vol-iii-rome/README.md)
  - [Vol IV - Russia](/C:/dev/strategy-codex/statecraft/states/volumes/vol-iv-russia/README.md)
  - [Vol V - America](/C:/dev/strategy-codex/statecraft/states/volumes/vol-v-america/README.md)
- Use `civilization_memory` only as evidence for this skill; CIV-STATE surfaces remain the operator-facing layer.
- Keep volume passes bounded to CIV-STATE architecture surfaces unless the operator explicitly widens scope into lane, transaction, or source-memory files.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill civ-state-volume-harden
python scripts/sync_portable_skills.py --verify --skill civ-state-volume-harden
python scripts/validate_skills.py
```
