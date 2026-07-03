---
name: handoff-check
preferred_activation: handoff check
description: >-
  Run operator_handoff_check.py for RECURSION-GATE pending, Predictive History
  night closeout, commits, worktree noise, re-entry prompt — read-only. On
  **coffee** with **signing-off** intent, this script (or
  `operator_coffee.py --mode closeout`) is **coffee Step 1**; **Step 2** is the
  same fixed **A–D** hub (**Confirm / Test / Deepen / Reframe**). See
  [coffee/SKILL.md](../coffee/SKILL.md) and [menu-reference — signing-off
  intent](../../../continuity/coffee/menu-reference.md#signing-off-intent).
  Also use when resuming work or checking safe-to-ignore before commit/push.
category: operator-coherence
status: active
scope_class: repo-governed
---

# Handoff Check

**Preferred activation (operator):** say the exact phrase **`handoff check`**. **Alias:** **`use handoff-check`**.

Use this skill when the operator wants to pause or resume work without losing the active thread.

**Preset — signing-off `coffee`:** When the operator says **`coffee`** with **signing-off** intent (session end, wrapping the day; legacy **`hey`** still works), the agent runs **signing-off Step 1** (this command + short summary paragraph) then the **same** **A–D** hub as work-start: **Confirm / Test / Deepen / Reframe**. There is **no** separate closeout menu and **no** closeout-only letter — exit the hub by normal workflow or **no menu**. On follow-up turns, **A**, **B**, and **D** re-offer the full hub after the branch settles; **C** exits to normal workflow unless **`stay in coffee`**. Per-letter signing-off add-ons: [menu-reference — signing-off intent](../../../continuity/coffee/menu-reference.md#signing-off-intent).

**Work-start `coffee`:** Re-offer and exit behavior for **A–D** match [coffee/SKILL.md](../coffee/SKILL.md): **A**, **B**, and **D** → full hub by default after the branch settles; **C** → exit unless **`stay in coffee`**. Hub letters choose a **learning action first**; downstream steward / engineer / statecraft / singularity routing is second-layer only when that action needs a specific bench.

**Legacy compatibility:** Older notes may still say **A–E**, **Steward / Engineer / Statecraft / Singularity** as hub labels, or **menu H**. Treat those as residue. Live coffee hub is **A–D** only; Conductor is standalone by master name or **`conductor`**.

## Default command

```bash
python3 scripts/operator_handoff_check.py -u strategy-codex
```

**Cold-thread stack (optional):** `python3 scripts/operator_reentry_stack.py -u strategy-codex` runs handoff check, then `operator_daily_warmup.py`, then `harness_warmup.py` (add `--compact` for a shorter harness). **One-line snapshot:** `python3 scripts/harness_warmup.py -u strategy-codex --receipt`. See the legacy re-entry stack notes.

## What to return

Summarize:

- **RECURSION-GATE** — pending totals (work-politics vs companion), listed items if any (script caps long queues), and the script's **proposed** processing steps (`operator_gate_review_pass` → approve/reject in-file → `process_approved_candidates.py`); remind that **merge requires companion approval**
- **Predictive History (work-jiang)** — **`## Predictive History — night closeout`**: where the lane rests, suggested first lever tomorrow, rotating **Spark** (edit `continuity/predictive-history/metadata/warmup-sparks.yaml`), optional rebuild ritual; still read-only / not Record
- recently committed work
- meaningful local changes still in progress
- **`## Derived / export churn`** — PRP, manifest, ledger, etc. (regenerate or batch-commit vs editorial work)
- runtime-only noise that should stay uncommitted
- work-politics continuity if relevant
- the best next re-entry prompt
- **Skill discovery (one line, optional):** If the thread had a repeatable multi-step workflow, mention [skills/skill-candidates.md](../../../skills/skill-candidates.md) and route through **B Test** (Engineer) or explicit **`write`** / **`skill-write`** — do not block the handoff on it.

## Guardrails

- Distinguish runtime noise from real local work before recommending any commit or push.
- This is a summary workflow only. Do not stage, commit, or merge as part of the handoff.
- If local changes mix unrelated threads, say so clearly.

## Related files

- `docs/operator-skills.md`
- `docs/development-handoff.md`
- `recursion-gate.md`
