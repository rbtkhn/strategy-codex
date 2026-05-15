---
name: cognition-streams
preferred_activation: cognition streams
description: Legacy alias for check-streams. Use when the operator says cognition streams, daily streams, main streams, or asks for the Davis, Diesen, Dialogue Works, and Mercouris daily YouTube roster with speaker-folder routing.
portable: true
version: 0.2.0
tags:
- operator
- strategy
- raw-input
- youtube
- daily
- legacy-alias
portable_source: skills-portable/cognition-streams/SKILL.md
synced_by: sync_portable_skills.py
---
# Cognition streams

`cognition streams` is a legacy compatibility activation. Treat **`check streams`** as the canonical skill name and operator-facing command.

Use the canonical [check-streams](../check-streams/SKILL.md) workflow for the actual daily roster pass:

- discover today's Davis, Diesen, Dialogue Works, and Mercouris uploads
- filter likely clips / highlights into a secondary bucket
- list main uploads first
- wait for operator selection
- hand approved URLs down to the lower-layer `youtube transcript` workflow for materialization
- suggest speaker-folder routing hints after materialization

Do not maintain a separate ingest doctrine here. When this alias triggers, say that you are using **`check streams`** and follow that skill's instructions.


## Cursor / grace-mar instance

Legacy alias shim for this repository.

- Canonical skill: [.cursor/skills/check-streams/SKILL.md](../check-streams/SKILL.md)
- Canonical portable source: [skills-portable/check-streams/SKILL.md](../../../skills-portable/check-streams/SKILL.md)
- Legacy operator phrase: `cognition streams`
- Canonical operator phrase: `check streams`

When this alias triggers, follow **`check streams`**. Do not duplicate daily roster, clip-filter, or transcript materialization doctrine here.
