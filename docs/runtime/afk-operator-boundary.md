# AFK vs operator boundary

**Purpose:** Separate **operator decision rights** from **scoped automation** so AFK workers and external runtimes do not silently become authority surfaces.

**Map:** [harness-architecture-map.md](../harness-architecture-map.md) · **Harness agent rule:** [intelligence-harness.md — Agent boundary](../intelligence-harness.md#intake-queue-agent-workbench-loop)

---

## Roles

| Role | Examples in this repo | Authority |
|------|----------------------|-----------|
| **Operator (human-in-loop)** | `PLAN` / `EXECUTE` / `DOCSYNC` lanes ([operator-agent-lanes.md](../operator-agent-lanes.md)); promotion to daily / transaction; ship / push; gate approve (`fork revive` only); acceptance criteria | Decision rights; canonical merge |
| **AFK / disposable workers** | [`grace_mar_runtime_worker.py`](../../scripts/runtime/grace_mar_runtime_worker.py) dry-run inspect; optional LLM summary | Proposals under `runtime/runtime-worker/` (gitignored); [runtime-worker.md](../runtime-worker.md) |
| **Advisory automation** | [`review_orchestrator.py`](../../scripts/runtime/review_orchestrator.py); validators; intake sidecar v0 scoring | Review packets / receipts; `non_canonical: true` |
| **External AFK** | [runtime-complements](runtime-complements.md) export/inbox; Cursor cloud / background agents; scheduled CI | Scoped tasks only; no silent Record merge |

---

## Rules

1. **Scoped task** — path caps, `--task-anchor`, worker lenses; no unbounded repo walks.
2. **Human defines acceptance** — constraints and promotion criteria before trusting output for daily / transaction / gate paths.
3. **Artifacts, not authority** — AFK output never substitutes Record, archive verbatim body, or daily synthesis canon.
4. **Agent boundary (harness)** — classify, score, and draft — **yes**; contact, publish, or canonical merge — **operator only**.

---

## Related

- [runtime-vs-record.md](../runtime-vs-record.md)
- [runtime/runtime-complements.md](runtime-complements.md)
- [statecraft-intake-queue.md](../statecraft-intake-queue.md)
