# Operator root artifacts — registry supplement

Companion to [root-directory-map.md](root-directory-map.md) and [operator-surface-registry.md](operator-surface-registry.md). Lists operator artifacts that are easy to mistake for Record truth.

---

## Authority rule

| Class | Authority |
|-------|-----------|
| Record markdown under `archive/grace-mar-instance/` | Canonical **only** after gated merge (fork revive) |
| `runtime/operator-events/*.jsonl` | Append-only operator ledgers — **not** Record |
| `runtime/daily-handoff/*.json` | Dream / coffee continuity — **not** Record |
| Root `*.jsonl` (harness, compute) | Operator-local — **not** Record |
| Profile derived exports (see below) | Regenerated — **not** Record |
| `platform/users/<id>/fork_state.json`, `drift-report.json` | Fork lifecycle posture — **not** Record |

---

## Profile-derived exports (`archive/grace-mar-instance/`)

Resolved via `scripts/repo_io.py` → `resolve_profile_export_path(user_id, basename)`.

| Basename | Class | Producer (typical) |
|----------|-------|-------------------|
| `manifest.json` | derived_non_authoritative | `export_manifest.py` |
| `llms.txt` | derived_non_authoritative | `export_manifest.py` |
| `intent_snapshot.json` | derived_non_authoritative | `export_manifest.py` / `export_runtime_bundle.py` |
| `fork-manifest.json` | machine_feed | `fork_checksum.py --manifest` |
| `session-transcript.md` | runtime continuity | bot, miniapp, `log_operator_choice.py` |
| `self-work.md` | WORK coordination | operator |
| `gate-dashboard.html` | review_support | `generate_gate_dashboard.py` |
| `evidence-graph.json` | derived_non_authoritative | `build_evidence_graph.py` |
| `symbolic_identity.json` | machine_feed | `export_symbolic.py` |

**Guard:** `python3 scripts/assert_root_profile_exports.py` — these basenames must not return to repo root.

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

## Fork lifecycle (`platform/users/<fork_id>/`)

| Path | Class | Notes |
|------|-------|-------|
| `fork_state.json` | derived_non_authoritative | Phase, counters — `fork_lifecycle.py init` |
| `drift-report.json` | derived_non_authoritative | Heuristic drift — `fork_lifecycle.py measure-drift` |

---

## Root JSONL (operator-local)

| Path | Class | Notes |
|------|-------|-------|
| `harness-events.jsonl` | machine_feed | Audit lane; gitignored when local |
| `compute-ledger.jsonl` | machine_feed | Token / compute accounting |

---

## Related

- [runtime/operator-events/README.md](../runtime/operator-events/README.md)
- [runtime-vs-record.md](runtime-vs-record.md)
- [runtime/artifacts/README.md](../runtime/artifacts/README.md)
