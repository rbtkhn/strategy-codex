---
name: strategy-notebook-guest-canon-note
description: Legacy alias for strategy-codex guest speaker arc. Redirect to codex guest-arc placement rules.
preferred_activation: speaker arc
activation: speaker arc
portable: true
version: 0.3.0
category: legacy-redirect
status: redirect
replacement: strategy-codex-guest-canon-note
scope_class: repo-governed
review_date: 2026-12-31
tags:
- operator
- strategy-codex
- strategy-notebook-legacy
- speaker-arc
portable_source: skills/strategy-notebook-guest-canon-note/SKILL.md
synced_by: sync_portable_skills.py
---
# Strategy-codex guest speaker arc (legacy slug)

**Legacy slug:** `strategy-notebook-guest-canon-note` (manifest compatibility only).

**Active concept:** **strategy-codex guest speaker arc** — compact host x guest lane note for lattice/thread citation.

**SSOT:** [codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md) · host-stream placement in codex speaker shelves.

**Activation:** `speaker arc`, `guest canon note` — follow codex guest-arc workflow; cite raw-input receipts; no new lattice category without operator approval.

**Preferred name (new work):** **`speaker arc`** in strategy-codex / codex surfaces.


## Cursor / strategy-codex instance

Grace-mar paths and commands for this repository (from `.cursor/skills/strategy-notebook-guest-canon-note/`).

| Topic | Path |
|--------|------|
| Existing stream-local speaker arcs | [statecraft/voices/diesen/](../../../statecraft/voices/diesen) |
| Lattice speakers roster | [codex/speaker-lattice.md](../../../codex/speaker-lattice.md) |
| Thread handle roster | [codex/strategy-commentator-threads.md](../../../codex/strategy-commentator-threads.md) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- In this repo, guest speaker arcs belong to the **host stream** unless an existing taxonomy explicitly says otherwise.
- Current reference pattern:
  - [arc-matlock-diesen-host.md](../../../statecraft/notes/arc-matlock-diesen-host.md)
  - [arc-jiang-diesen-host.md](../../../statecraft/notes/arc-jiang-diesen-host.md)
- The lattice and `thread:` roster may cite the speaker arc, but the note itself should not invent a new shelf or corpus boundary.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill strategy-notebook-guest-canon-note
python scripts/sync_portable_skills.py --verify
python scripts/validate_skills.py
```
