---
name: check-streams
preferred_activation: check streams
description: DEPRECATED 2026-06-21. Legacy alias for check-sources. Redirect to check sources / check sources watchlist. See CHECK-STREAMS-DEPRECATED.md.
portable: true
version: 0.5.0
deprecated: 2026-06-21
see: docs/skill-work/work-strategy/CHECK-STREAMS-DEPRECATED.md
tags:
- operator
- deprecated
- youtube
portable_source: skills/check-streams/SKILL.md
synced_by: sync_portable_skills.py
---
# DEPRECATED — Check streams

**Status:** Deprecated **2026-06-21**. Do not treat **`check streams`** as the canonical skill name for new work.

Full spec: [CHECK-STREAMS-DEPRECATED.md](../../docs/skill-work/work-strategy/CHECK-STREAMS-DEPRECATED.md)

## Use instead

| Task | Skill / path |
|------|----------------|
| Daily / roster YouTube discovery + source-intake handoff | **`check sources`** ([`check-sources`](../check-sources/SKILL.md)) |
| Fast pass on six daily watchlist channels | **`check sources watchlist`** (same skill; filter `watchlist: true` in roster) |
| Machine roster | [`channel-index.json`](../../source-archive/statecraft/channel-index.json) via `load_check_sources_roster()` |
| Archive land | **`source-intake`** ([`statecraft-source-intake`](../statecraft-source-intake/SKILL.md)) |

## Legacy activation

When the operator says **`check streams`**, say you are following **`check sources`** and execute [check-sources/SKILL.md](../check-sources/SKILL.md).

`cognition streams` remains a separate legacy alias — also redirects to **`check sources`**.


## Cursor / strategy-codex instance

Grace-mar paths and commands for this repository (from `.cursor/skills/check-streams/`).

**Deprecated 2026-06-21** — redirect to [check-sources](../check-sources/SKILL.md). See [CHECK-STREAMS-DEPRECATED.md](../../../docs/skill-work/work-strategy/CHECK-STREAMS-DEPRECATED.md).

When **`check streams`** triggers, follow **`check sources`** per the canonical skill.
