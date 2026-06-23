---
name: cognition-streams
description: Legacy alias for check-sources. Redirect to check sources for roster discovery and source-intake handoff.
preferred_activation: cognition streams
activation: cognition streams
portable: true
version: 0.4.0
category: legacy-redirect
status: redirect
replacement: check-sources
scope_class: repo-governed
review_date: 2026-12-31
tags:
- operator
- legacy-alias
- youtube
portable_source: skills/cognition-streams/SKILL.md
synced_by: sync_portable_skills.py
---
# Cognition streams (legacy alias)

**Superseded by:** [check-sources](../check-sources/SKILL.md)

**Activation:** `cognition streams`, `check streams`, and `daily streams` remain valid **compatibility triggers** — execute [check-sources](../check-sources/SKILL.md) procedure.

**Preferred name (new work):** **`check sources`** · **`check-sources`**


## Cursor / strategy-codex instance

Legacy alias shim for this repository.

- Canonical skill: [.cursor/skills/check-streams/SKILL.md](../check-streams/SKILL.md)
- Canonical portable source: [skills/check-streams/SKILL.md](../../../skills/check-streams/SKILL.md)
- Legacy operator phrase: `cognition streams`
- Canonical operator phrase: `check streams`

When this alias triggers, follow **`check streams`**. Do not duplicate daily roster, clip-filter, or transcript materialization doctrine here.
