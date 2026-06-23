---
name: transcript-proper-noun-normalization
description: DEPRECATED 2026-06-21. Redirect to source-clean for statecraft archive captures. Legacy alias for post-land ASR/proper-noun normalization.
preferred_activation: proper noun normalization
activation: proper noun normalization
portable: true
version: 0.2.0
category: truth-pipeline
status: active
scope_class: repo-governed
tags:
  - transcript
  - raw-input
  - quality
  - cleanup
  - deprecated
deprecated: 2026-06-21
see: skills/source-clean/SKILL.md
---
# DEPRECATED — Transcript proper-noun normalization

**Status:** Deprecated **2026-06-21**. For landed **`source-archive/statecraft/**/source-*.md`** captures, use **[`source-clean`](../source-clean/SKILL.md)** instead.

## Use instead

| Task | Skill / CLI |
|------|-------------|
| Post-land ASR + proper-noun cleanup on archive captures | **`source-clean`** → `python scripts/source_clean_statecraft.py --path <capture>` |
| ASR-only (no scaffold) | `python scripts/normalize_statecraft_source_asr.py <path> --write` |
| First-pass land | **`source-intake`** ([`statecraft-source-intake`](../statecraft-source-intake/SKILL.md)) |

## Legacy activation

When the operator says **`proper noun normalization`** on a **statecraft archive** file, say you are following **`source-clean`** and execute [source-clean/SKILL.md](../source-clean/SKILL.md).

For **raw-input** files under `strategy-notebook/raw-input/` only (not yet archived), apply the same **conservative proper-noun** contract manually or land via intake first, then **`source-clean`**.
