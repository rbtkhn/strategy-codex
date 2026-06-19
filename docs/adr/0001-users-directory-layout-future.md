# ADR 0001 â€” Future optional `` directory layout

**Status:** Proposed (not implemented)  
**Date:** 2026-03-21  
**Context:** Repo layout refactor; `` remains **flat** per [canonical-paths.md](../canonical-paths.md).

## Decision (deferred)

A future migration **might** introduce subfolders under `` (e.g. `identity/`, `archive/placeholders/evidence/processed/`) for operator ergonomics or large binary layout. That would require:

1. **RFC** agreed with companion and operator â€” canonical filenames (`self.md`, `self-evidence.md`, `recursion-gate.md`, â€¦) stay authoritative **names**; only **directory** placement may change.
2. **One-shot migration script** updating every consumer: `scripts/process_approved_candidates.py`, `archive/grace-mar-instance/bot/`, `platform/apps/`, tests, and CI.
3. **Coordinated release** with git tag and changelog; no partial migration.

## Non-goals (this ADR)

- No change to on-disk paths until the RFC is approved and tooling exists.
- No change to the **gated merge** rule or companion sovereignty.

## Consequences

- New instances should continue to use **`platform/template/`** as a **documentation-only** mirror of required filenames until a migration ships.

