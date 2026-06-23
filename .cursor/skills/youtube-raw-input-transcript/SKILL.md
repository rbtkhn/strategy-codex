---
name: youtube-raw-input-transcript
description: 'DEPRECATED 2026-06-20. Do not use for new strategy-codex capture. Redirect: source-intake for archive land; check sources for daily roster. See YOUTUBE-MATERIALIZE-DEPRECATED.md.'
preferred_activation: youtube transcript
activation: youtube transcript
portable: true
version: 0.2.0
category: truth-pipeline
status: active
scope_class: repo-governed
tags:
- operator
- deprecated
- youtube
portable_source: skills/youtube-raw-input-transcript/SKILL.md
synced_by: sync_portable_skills.py
deprecated: 2026-06-20
see: docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md
---
# DEPRECATED — YouTube raw-input / materialize skill

**Status:** Deprecated **2026-06-20**. Do not invoke **`youtube transcript`** or **`materialize_youtube_raw_input.py --apply`** for new work in strategy-codex.

Full spec: [YOUTUBE-MATERIALIZE-DEPRECATED.md](../../docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md)

## Use instead

| Task | Skill / path |
|------|----------------|
| Land pasted or fetched transcript to canonical archive | **`source-intake`** ([`statecraft-source-intake`](../statecraft-source-intake/SKILL.md)) |
| Daily YouTube roster → source-intake | **`check sources`** ([`check-sources`](../check-sources/SKILL.md)) → approved URLs → **`source-intake`** |
| Channel inventory | [`source-archive/statecraft/channel-index.md`](../../source-archive/statecraft/channel-index.md) · [`channel-index.json`](../../source-archive/statecraft/channel-index.json) |

## Legacy script (no new archive writes)

`python scripts/materialize_youtube_raw_input.py` remains on disk for archaeology and receipt replay only. New captures must use **`source-*`** filenames under `source-archive/statecraft/`.


## Cursor / strategy-codex instance

_(appendix missing: .cursor/skills/youtube-raw-input-transcript/CURSOR_APPENDIX.md)_
