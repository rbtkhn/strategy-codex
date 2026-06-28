---
name: statecraft-helix-synthesis
description: Archived judgment-method skill. Not used for current strategy-codex work.
preferred_activation: statecraft helix synthesis
activation: statecraft helix synthesis
portable: true
version: 0.2.0
category: judgment-enhancement
status: archived
scope_class: repo-governed
review_date: 2026-12-31
tags:
- operator
- archived
- statecraft
portable_source: skills/statecraft-helix-synthesis/SKILL.md
synced_by: sync_portable_skills.py
---
# Archived — statecraft-helix-synthesis

**Status:** Archived. Do not use this skill for new work.

This file remains for historical reference and legacy trigger clarity only.

## No active invocation

If this method is needed again, revive it through the normal skill path:

```text
skills/skill-candidates.md
→ skills/_drafts/<name>/SKILL.md
→ tested in real use
→ promoted back to active status
```

## No independent methodology

Do not extend this archived file. If current work needs this pattern, create or update an active runbook or active skill instead.


## Cursor / strategy-codex instance

## strategy-codex instance

- Root working area for this skill: [codex/academy/statecraft](../../../codex/academy/statecraft) with the main control plane under [civ-state/migration](../../../statecraft/states/migration).
- Preferred source stack for synthesis work:
  - lane helixes such as [America helix](../../../codex/academy/statecraft/america/helix.md)
  - first-wave strand objects under each lane's `civilization/` and `empire/`
  - migration control-plane notes in [civ-state/migration](../../../statecraft/states/migration)
- Preferred generator command after edits:

```powershell
python scripts/build_civ_emp_migration_inventory.py
```

- Preferred validation commands after listed-skill edits:

```powershell
python scripts/sync_portable_skills.py --skill statecraft-helix-synthesis
python scripts/sync_portable_skills.py --verify --skill statecraft-helix-synthesis
python scripts/validate_skills.py
```

- Keep this skill scoped to the statecraft synthesis layer. Do not let it drift into PH-CIV authoring, raw CIV-MEM backfill, or Record-bearing surfaces unless the operator explicitly asks.
