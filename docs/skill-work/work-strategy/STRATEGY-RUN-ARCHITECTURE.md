# Strategy run wrapper — architecture (WORK)

**Purpose:** Give [work-strategy](README.md) an **inspectable session envelope** (`run_id`, status, resolved input paths, proposal pointers) without changing the **canonical** strategy notebook model (page-primary; **experts / watches / days / minds** per [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md)).

## Why this preserves doctrine

- **Runtime vs. Record:** Run state and receipts live under `runtime/artifacts/` and are **derived**. They are not SELF, EVIDENCE, MEMORY, or Voice. Nothing in a run **auto-merges** into Record; the gate in [AGENTS.md](../../../AGENTS.md) still governs profile changes. See [runtime-vs-record.md](../../runtime-vs-record.md).
- **No silent notebook mutation:** `strategy_run.py` **does not** write `days.md`, inbox, or expert `thread.md`. Applying a **proposal** (when you add sidecar JSON) remains a **separate, explicit** step by the operator or an approved script they run.
- **Two receipt channels (complementary):**
  - **Session scope:** `runtime/artifacts/strategy-runs/<run_id>/state.json` + `runtime/artifacts/run-receipts/*.json` — one **run** lifecycle.
  - **Script scope:** [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](../../../codex/STRATEGY-NOTEBOOK-TRACE-CONTRACT.md) JSONL — which files **`strategy_page`** / **`compile_strategy_view`** touched on a given invocation.

## Shared vocabulary

[docs/run-contract.md](../../run-contract.md) defines the generic **run grammar** (`status`, `approval_state`, …). Strategy is the first consumer; schemas are in `schemas/registry/strategy-run-state.v1.json` and `schemas/registry/run-receipt.v1.json`.

## Links

- [STRATEGY-RUN-OPERATOR.md](STRATEGY-RUN-OPERATOR.md) — commands and paths
- [STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md](../../../codex/STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md) — page operation names vs. proposal `operation` field (`new` / `append` / `refine`)
