---
name: transcript-cleanup
preferred_activation: transcript cleanup
description: 'DEPRECATED 2026-06-21. Redirect to source-clean for statecraft archive captures. Legacy raw-input cleaned-80 derivative workflow superseded for archive lane.'
portable: true
version: 0.2.0
deprecated: 2026-06-21
see: skills/source-clean/SKILL.md
tags:
  - transcript
  - raw-input
  - quality
  - cleanup
  - deprecated
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
