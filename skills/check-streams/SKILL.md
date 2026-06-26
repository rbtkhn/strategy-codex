---
name: check-streams
description: DEPRECATED 2026-06-21. Legacy alias for check-sources. Redirect to check sources / check sources watchlist. See CHECK-STREAMS-DEPRECATED.md.
preferred_activation: check streams
activation: check streams
portable: true
version: 0.5.0
category: legacy-redirect
status: redirect
replacement: check-sources
scope_class: repo-governed
review_date: 2026-12-31
tags:
  - operator
  - deprecated
  - youtube
portable_source: skills/check-streams/SKILL.md
synced_by: sync_portable_skills.py
deprecated: 2026-06-21
see: docs/skill-work/work-strategy/CHECK-STREAMS-DEPRECATED.md
---
# DEPRECATED — Check streams

**Status:** Deprecated **2026-06-21**. Do not treat **`check streams`** as the canonical skill name for new work.

Full spec: [CHECK-STREAMS-DEPRECATED.md](../../docs/skill-work/work-strategy/CHECK-STREAMS-DEPRECATED.md)

## Use instead

| Task | Skill / path |
|------|----------------|
| Daily / roster YouTube discovery + source-intake handoff | **`check sources`** ([`check-sources`](../check-sources/SKILL.md)) |
| Fast pass on six daily watchlist channels | **`check sources watchlist`** (same skill; filter `watchlist: true` in roster) |
| Machine roster | [`channel-index.json`](../../statecraft/channels/channel-index.json) via `load_check_sources_roster()` |
| Archive land | **`source-intake`** ([`statecraft-source-intake`](../statecraft-source-intake/SKILL.md)) |

## Legacy activation

When the operator says **`check streams`**, say you are following **`check sources`** and execute [check-sources/SKILL.md](../check-sources/SKILL.md).

`cognition streams` remains a separate legacy alias — also redirects to **`check sources`**.
