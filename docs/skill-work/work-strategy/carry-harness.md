# Work-Strategy Carry Harness

**Lane:** WORK (`work-strategy`) - **not** durable Record. Receipts are **derived**, **rebuildable**, and **non-canonical**.

**Purpose:** Provide a **narrow, deterministic** check that a messy strategy task produced **minimum legible handoff artifacts** from intake toward review readiness without proving strategic correctness, approving merges, or staging gate candidates.

---

## What "carry" means

1. **Intake** - A task description file is readable, usually Markdown.
2. **Artifact expectations** - Explicit paths to sources and expected outputs are declared on the CLI and echoed in the receipt.
3. **Derived review posture** - The harness does not judge judgment quality. It only checks presence and non-trivial bulk where applicable.
4. **Gate-snippet readiness (optional)** - If you pass `--gate-snippet`, the harness checks that the snippet file exists and is non-empty. It does not stage or approve anything.
5. **Receipt** - A JSON document describes checks, summary counts, and overall `pass` / `fail` / `needs_review`.

Canonical doctrine for Record vs runtime: [runtime-vs-record.md](../../runtime-vs-record.md), [AGENTS.md](../../../AGENTS.md).

---

## Relationship to other strategy tooling

| Tool | Role |
|------|------|
| [`scripts/build_strategy_observability.py`](../../../scripts/build_strategy_observability.py) | Lane-wide notebook health metrics to `artifacts/work-strategy/strategy-observability.json`. |
| [`scripts/build_strategy_run_report.py`](../../../scripts/build_strategy_run_report.py) | Summarizes recent `artifacts/strategy-runs/*/state.json` runs. |
| **`run_carry_harness.py`** | **Task-scoped**: explicit `--task`, `--source`, `--artifact` paths and a carry receipt under `runtime/work-strategy/`. Optional `--build-review-packet` writes a consolidated review packet. |
| **`validate_strategy_packet.py`** | Optional `--run-validators` companion: writes [`work_strategy_validation_report.schema.json`](../../../schemas/work_strategy_validation_report.schema.json) JSON and embeds `validation_summary` plus `validation_report_path` when allowed. See [validator-contract.md](validator-contract.md). |
| **`classify_task_shape.py`** | Optional `--classify-task-shape` companion: writes [`work_strategy_task_shape_report.schema.json`](../../../schemas/work_strategy_task_shape_report.schema.json) JSON and embeds task-shape fields when a `--task-shape-report` path is allowed. See [task-shape-routing.md](task-shape-routing.md). |

These are different slices. The carry harness does not replace observability or strategy-run reports.

---

## What this harness measures

- Task file readable?
- Optional source paths exist?
- Expected artifact paths exist?
- For Markdown/text artifacts: word count >= 50 as a heuristic for non-trivial output?
- If `--gate-snippet` was passed: snippet non-empty?
- Output receipt path not under forbidden canonical roots or protected `bot/` files?
- This script never writes to Record surfaces or `recursion-gate.md`; it may include gate-ready paste text inside the receipt only as captured from your snippet file.

---

## What this harness does not do

- Prove strategic correctness or falsify geopolitical claims.
- Merge, approve, or stage `RECURSION-GATE` candidates.
- Call an LLM or the network.
- Replace [`scripts/emit_work_strategy_gate_paste_snippet.py`](../../../scripts/emit_work_strategy_gate_paste_snippet.py), which may write staging paste files when you run it operator-side.

---

## Schema

Receipt shape: [`schemas/work_strategy_carry_receipt.schema.json`](../../../schemas/work_strategy_carry_receipt.schema.json).

Top-level fields include the shared control-plane vocabulary:

- `receipt_family`
- `receipt_kind`
- `actor`
- `intent`
- `authority_class`
- `resources_read`
- `resources_written`
- `status`
- `review_surface`
- `rollback_surface`
- `record_authority`
- `gate_effect`

Those sit alongside the carry-specific `checks`, `summary`, `gate_snippet`, `record_boundary`, and `result`.

`checks` remain the authoritative per-condition outcomes. `summary` rolls up counts. `status` and `result` intentionally expose the same overall outcome so the receipt is readable both as a carry-specific artifact and as a normalized execution receipt. When `--run-validators` is used, optional `validation_summary` and `validation_report_path` are included. When `--build-review-packet` is used, optional `review_packet_path`, `review_packet_markdown_path`, and `review_readiness` are included after the review packet step.

---

## How to run

From repo root:

```bash
python3 scripts/work_strategy/run_carry_harness.py \
  --task examples/work-strategy/carry-harness/sample-task.md \
  --source examples/work-strategy/carry-harness/sample-source.md \
  --artifact examples/work-strategy/carry-harness/sample-artifact.md \
  --gate-snippet examples/work-strategy/carry-harness/sample-gate-snippet.md \
  --out runtime/work-strategy/carry-receipts/sample-receipt.json \
  --json
```

Options:

| Flag | Meaning |
|------|---------|
| `--task PATH` | Task intake file (recommended). |
| `--source PATH` | Repeatable; expected to exist (`needs_review` if missing). |
| `--artifact PATH` | Repeatable; expected outputs (`fail` if missing). |
| `--gate-snippet PATH` | Optional; if provided, must be non-empty (`needs_review` otherwise). |
| `--out PATH` | Receipt JSON output, refused under forbidden roots. |
| `--run-id STRING` | Stable id for logs (default: generated). |
| `--repo-root PATH` | Repo root (default: inferred from script location). |
| `--json` | Print receipt JSON to stdout. |
| `--fail-on-result fail\|needs_review\|never` | Exit code policy (default `fail`: nonzero only on `result == fail`). |
| `--run-validators` | Run [`validate_strategy_packet.py`](../../../scripts/work_strategy/validate_strategy_packet.py) with the same path arguments and embed `validation_summary`. |
| `--validation-report PATH` | Where to write validation JSON when `--run-validators` is set. |
| `--classify-task-shape` | Run [`classify_task_shape.py`](../../../scripts/work_strategy/classify_task_shape.py) and embed task-shape fields. |
| `--task-shape-report PATH` | Where to write task-shape JSON when `--classify-task-shape` is set. |
| `--build-review-packet` | After checks and optional validation/task-shape writes, emit a review packet JSON via `--review-packet`. |
| `--review-packet PATH` | Required when `--build-review-packet` is set. |
| `--review-packet-markdown PATH` | Optional Markdown companion when `--build-review-packet` is set. |

---

## Interpreting failures

- **`fail`** - Hard precondition broken, such as unreadable task, missing expected artifact, or forbidden `--out`.
- **`needs_review`** - Soft signal, such as missing optional source, thin text artifact, or empty gate snippet when requested.
- **`pass`** - All checks passed; still not proof of good strategy.

---

## Receipt field notes

- **`receipt_family` / `receipt_kind`** - Crosswalk alignment: this is an execution receipt of kind `work-strategy-carry-receipt`.
- **`actor` / `authority_class` / `intent`** - States who ran the harness, under what WORK authority class, and for what purpose.
- **`resources_read` / `resources_written`** - Explicit read/write envelope for task intake, source inputs, receipt output, and optional validator/task-shape/review-packet sidecars.
- **`review_surface` / `rollback_surface`** - Marks where the operator should inspect next and how the run is superseded: revise and rerun rather than merge the receipt.
- **`record_authority` / `gate_effect`** - Makes the boundary explicit: the receipt has no Record authority and no gate mutation effect, even when it carries paste-ready snippet text.
- **`record_boundary.canonical_write_violation`** - `true` if `--out` pointed at a forbidden path; no file is written there.
- **`record_boundary.canonical_paths_written`** - Always empty for this harness because it does not write Record paths.
- **`gate_snippet.text`** - Copy of snippet content when read successfully as a WORK-only paste aid.
- **`validation_summary` / `validation_report_path`** - Present when `--run-validators` runs.
- **`task_shape` / `task_shape_confidence` / `task_shape_expected_outputs` / `task_shape_report_path`** - Present when `--classify-task-shape` runs; see [task-shape-routing.md](task-shape-routing.md).
- **`review_packet_path` / `review_packet_markdown_path` / `review_readiness`** - Present when `--build-review-packet` runs; see [review-packet-template.md](review-packet-template.md).

---
