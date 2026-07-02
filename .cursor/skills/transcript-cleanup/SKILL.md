---
name: transcript-cleanup
description: DEPRECATED 2026-06-21. Redirect to source-clean for statecraft archive captures. Legacy raw-input cleaned-80 derivative workflow superseded for archive lane.
preferred_activation: transcript cleanup
activation: transcript cleanup
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
portable_source: skills/transcript-cleanup/SKILL.md
synced_by: sync_portable_skills.py
---
# DEPRECATED — Transcript cleanup

**Status:** Deprecated **2026-06-21**. For **`source-archive/statecraft/`** transcript captures, use **[`source-clean`](../source-clean/SKILL.md)** — in-place cleanup with provenance on the canonical capture.

## Use instead

| Task | Skill / path |
|------|----------------|
| Post-land study-grade ASR cleanup on archive captures | **`source-clean`** |
| First-pass land | **`source-intake`** |
| Wire hook triage | **`wire-verify`** |

## Legacy note

The v0 **`*.cleaned.md` sidecar** pattern beside raw-input is **not** the default for statecraft archive work. Prefer one canonical `source-*.md` object updated by **`source-clean`**.

When the operator says **`transcript cleanup`** on an archive path, execute **`source-clean`**.

## Verification / Proof Standard

Do not call this complete unless:

- the input source, file, paste, URL, or archive path is named
- the output surface is named
- skipped steps are explicitly marked with a reason
- uncertainty, missing evidence, or unresolved source defects are stated
- before/after cleanup delta must be summarized

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

_(appendix missing: .cursor/skills/transcript-cleanup/CURSOR_APPENDIX.md)_
