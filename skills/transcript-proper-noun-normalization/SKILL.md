---
name: transcript-proper-noun-normalization
description: DEPRECATED 2026-06-21. Redirect to source-clean for statecraft archive captures. Legacy alias for post-land ASR/proper-noun normalization.
preferred_activation: proper noun normalization
activation: proper noun normalization
portable: true
version: 0.2.1
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
portable_source: skills/transcript-proper-noun-normalization/SKILL.md
synced_by: sync_portable_skills.py
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

For captures not yet in the archive, land via **`source-intake`** first, then **`source-clean`**. Do not write new files to deprecated **`continuity/raw-input/`** — [RAW-INPUT-DEPRECATED.md](../../docs/archive/skill-work-legacy/work-strategy/RAW-INPUT-DEPRECATED.md).

## Verification / Proof Standard

Do not call this complete unless:

- the input source, file, paste, URL, or archive path is named
- the output surface is named
- skipped steps are explicitly marked with a reason
- uncertainty, missing evidence, or unresolved source defects are stated
- unresolved names must be listed

Evidence to report:

- files touched or produced
- scripts or commands run
- source URLs, archive paths, or transcript identifiers used
- confidence downgrade, if any

If verification cannot be completed:

- state what was not verified
- stop before archive land, synthesis, publication, or promotion
- return a bounded partial result for operator review

## Cursor / strategy-codex instance

_(appendix missing: .cursor/skills/transcript-proper-noun-normalization/CURSOR_APPENDIX.md)_
