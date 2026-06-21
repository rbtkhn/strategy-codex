---
name: cognition-streams
preferred_activation: cognition streams
description: Legacy alias for check-sources (formerly check-streams). Use when the operator says cognition streams, daily streams, main streams, or asks for the daily YouTube roster with speaker-folder routing.
portable: true
version: 0.3.0
tags:
  - operator
  - strategy
  - raw-input
  - youtube
  - daily
  - legacy-alias
portable_source: skills/cognition-streams/SKILL.md
synced_by: sync_portable_skills.py
---

# Cognition streams

`cognition streams` is a legacy compatibility activation. Treat **`check sources`** as the canonical skill name and operator-facing command.

Use the canonical [check-sources](../check-sources/SKILL.md) workflow for the actual roster pass:

- load roster from `channel-index.json` (main index; misc excluded)
- discover today's uploads for watchlist or full main scope
- filter likely clips / highlights into a secondary bucket
- list main uploads first
- wait for operator selection
- hand approved URLs to **`source-intake`** for archive land
- suggest speaker-folder routing hints after land

Do not maintain a separate ingest doctrine here. When this alias triggers, say that you are using **`check sources`** and follow that skill's instructions.

## Cursor / strategy-codex instance

Legacy alias shim for this repository.

- Canonical skill: [.cursor/skills/check-sources/SKILL.md](../check-sources/SKILL.md)
- Canonical portable source: [skills/check-sources/SKILL.md](../../../skills/check-sources/SKILL.md)
- Legacy operator phrases: `cognition streams`, `check streams`
- Canonical operator phrase: `check sources`

When this alias triggers, follow **`check sources`**. Do not duplicate roster, clip-filter, or source-intake doctrine here.
