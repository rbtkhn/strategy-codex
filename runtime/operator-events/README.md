# Operator event ledgers

Append-only JSONL ledgers for pipeline, merge, cadence, and WORK learning — **not** Record.

**Authority:** Operator-local audit and continuity. Nothing here becomes Record truth without the gated pipeline.

**Canonical paths:** This directory (`runtime/operator-events/`).

**Compat:** `scripts/repo_io.py` — `resolve_ledger_path()` reads here first, then falls back to repository root copies until migrated.

| File | Role |
|------|------|
| `pipeline-events.jsonl` | Pipeline staged / applied / rejected |
| `merge-receipts.jsonl` | Merge batch receipts |
| `cadence-learning-events.jsonl` | Coffee / dream cadence learning |
| `business-ledger.jsonl` | Business transactions (instance root copy) |
| `fork-lineage.jsonl` | Fork lineage |
| `strategy-fold-events.jsonl` | Strategy notebook fold events |

**Migration:** `python3 scripts/migrate_operator_event_paths.py --dry-run` · `--apply`

**Docs:** [docs/root-directory-map.md](../../docs/root-directory-map.md) · [docs/operator-root-artifacts.md](../../docs/operator-root-artifacts.md)
