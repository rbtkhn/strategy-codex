# Operator root artifacts — registry supplement

**Work only; not Record.**

Companion to [root-directory-map.md](root-directory-map.md) and [operator-surface-registry.md](operator-surface-registry.md). Lists **root-adjacent** operator artifacts that are easy to mistake for Record truth.

---

## Authority rule

| Class | Authority |
|-------|-----------|
| Frozen Record markdown at root | Canonical **only** after gated merge (fork revive) |
| `runtime/operator-events/*.jsonl` | Append-only operator ledgers — **not** Record |
| `runtime/daily-handoff/*.json` | Dream / coffee continuity — **not** Record |
| Root `*.jsonl` (harness, compute) | Operator-local — **not** Record |
| `drift-report.json`, `fork_state.json` | Derived posture — **not** Record |

---

## Operator event ledgers (`runtime/operator-events/`)

| Basename | Producer (typical) | Operator use |
|----------|-------------------|--------------|
| `pipeline-events.jsonl` | `emit_pipeline_event.py`, merge scripts | Correlate staged vs applied |
| `merge-receipts.jsonl` | `process_approved_candidates.py` | Merge batch audit |
| `cadence-learning-events.jsonl` | `cadence_learning.py`, coffee/dream | Cadence learning rollup |
| `business-ledger.jsonl` | `emit_business_transaction.py` (per-user path may differ) | Venture transactions |
| `fork-lineage.jsonl` | fork lineage tooling | Fork history |
| `strategy-fold-events.jsonl` | `log_strategy_fold.py` | Notebook weave learning |

**Rebuild:** not regenerated — append-only history. **Compat:** scripts read legacy root copies if present.

---

## Dream handoff (`runtime/daily-handoff/`)

| File | Producer | Operator use |
|------|----------|--------------|
| `last-dream.json` | `auto_dream.py` | Morning warmup, catch-up window |
| `night-handoff.json` | `auto_dream.py` | Coffee Step 1 compact handoff |

**Compat:** `resolve_last_dream_path()` reads root `last-dream.json` if daily-handoff copy missing.

---

## Root JSON / state (selected)

| Path | Class | Notes |
|------|-------|-------|
| `harness-events.jsonl` | machine_feed | Audit lane; gitignored when local |
| `compute-ledger.jsonl` | machine_feed | Token / compute accounting |
| `fork_state.json` | derived_non_authoritative | Fork posture snapshot |
| `drift-report.json` | derived_non_authoritative | Drift scoring |
| `intent_snapshot.json` | derived_non_authoritative | Intent export mirror |

---

## Related

- [runtime/operator-events/README.md](../runtime/operator-events/README.md)
- [runtime-vs-record.md](runtime-vs-record.md)
- [runtime/artifacts/README.md](../runtime/artifacts/README.md)
