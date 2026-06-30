# Deprecated raw-input pointer (2026-06-23)

**Status:** **Deprecated** for new strategy-codex capture. Do not add new files here.

Full spec: [RAW-INPUT-DEPRECATED.md](../../docs/skill-work/work-strategy/RAW-INPUT-DEPRECATED.md)

## Use instead

| Task | Path / skill |
|------|----------------|
| Land verbatim strategy input (essay, transcript, social, wire) | **`source-intake`** → [`source-archive/statecraft/`](../../source-archive/statecraft/README.md) |
| Inbox registry stub | [`continuity/daily-strategy-inbox.md`](../daily-strategy-inbox.md) — pointer to archive path |
| Gap check (advisory) | `python3 scripts/strategy_raw_input_gap_hint.py` |

## Legacy files on disk

Existing captures under `continuity/raw-input/` and `continuity/years/*/raw-input/` remain **read-only archaeology**. Do not delete or migrate unless the operator explicitly requests migration.
