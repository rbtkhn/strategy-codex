# `runtime/prepared-context/` (repository root)

This directory is a **placeholder** for the [state model](../docs/state-model.md) **prepared context layer** at the grace-mar **repo root**. Prepared context in practice appears as drafts, tool bundles, MEMORY, and normalized extracts under **``**, **`docs/skill-work/`**, and related WORK surfaces — not necessarily as files dropped here.

**Why it exists:** Same as root [`archive/placeholders/evidence/`](../archive/placeholders/evidence/): tracked minimal footprint, no false promise of automated pipelines into this folder yet.

See [State model — Repo layout (grace-mar)](../docs/state-model.md#repo-layout-grace-mar).

## Progressive disclosure (runtime + WORK)

For **index-first** prepared context (runtime observation summaries before full notebook reads), see [progressive-disclosure.md](../docs/runtime/prepared-context/progressive-disclosure.md), `scripts/prepared_context/build_context_index.py`, and **`scripts/prepared_context/build_context_from_observations.py`** (expanded IDs → bounded Markdown). Example/template: [runtime-observation-context.md](runtime-observation-context.md). See [observation-expansion.md](../docs/runtime/observation-expansion.md).

**Operator-generated brief:** `python3 scripts/runtime/memory_brief.py ... --output runtime/prepared-context/memory-brief.md` may write a **runtime-only** Markdown brief here (not Record truth). The repo root `.gitignore` ignores `runtime/prepared-context/memory-brief.md` by default.

**Budgeted context:** `python3 scripts/prepared_context/build_budgeted_context.py` writes bounded Markdown with an explicit budget report; optional `--budgeted-follow-on` on `memory_brief.py` chains into it. Receipt for lane dashboards: `runtime/prepared-context/last-budget-builds.json`. See [context-budgeting.md](../docs/runtime/context-budgeting.md). **Policy modes** (`--policy-mode` / `GRACE_MAR_POLICY_MODE`): [policy-modes.md](../docs/policy-modes.md).

**Working folders (ephemeral):** For heavy multi-file EXECUTE, the [**context-folder-assembly**](../skills/_drafts/context-folder-assembly/SKILL.md) draft ritual assembles bounded task context under `runtime/prepared-context/working/<slug>/` (gitignored). PLAN uses [questions-as-spec](../docs/skill-work/questions-as-spec-template.md); shipped work still commits to normal repo paths. Orthogonal to bridge (session continuity) and harvest (midstream paste).
