---
name: handoff-check
preferred_activation: handoff check
description: Run operator_handoff_check.py for RECURSION-GATE pending, Predictive History night closeout, commits, worktree noise, re-entry prompt Ã¢â‚¬â€ read-only. On **coffee** with **signing-off** intent, this script (or `operator_coffee.py --mode closeout`) is **coffee Step 1**; **Step 2** is the **same** fixed **AÃ¢â‚¬â€œE** hub as work-start Ã¢â‚¬â€ **A Ã¢â‚¬â€ Steward** without gate/template split Ã¢â€ â€™ **system pick**. See [coffee/SKILL.md](../coffee/SKILL.md) and [menu-reference Ã¢â‚¬â€ signing-off intent](../../../docs/skill-work/work-coffee/menu-reference.md#signing-off-intent). Also use when resuming work or checking safe-to-ignore before commit/push.
---

# Handoff Check

**Preferred activation (operator):** say the exact phrase **`handoff check`**. **Alias:** **`use handoff-check`**.

Use this skill when the operator wants to pause or resume work without losing the active thread.

**Preset Ã¢â‚¬â€ signing-off `coffee`:** When the operator says **`coffee`** with **signing-off** intent (session end, wrapping the day; legacy **`hey`** still works), the agent runs **signing-off Step 1** (this command + short summary paragraph) then the **same** **AÃ¢â‚¬â€œE** hub as work-start. **A Ã¢â‚¬â€ Steward** with **no** gate vs template split named Ã¢â€ â€™ **system pick** (see [menu-reference Ã¢â‚¬â€ signing-off intent](../../../docs/skill-work/work-coffee/menu-reference.md#signing-off-intent)). On follow-up turns, **A**, **B**, **D**, or steward fork outcomes re-offer per [coffee SKILL](../coffee/SKILL.md); **C** exits to normal workflow unless **`stay in coffee`**. **No close letter** Ã¢â‚¬â€ exit the hub by normal workflow or **no menu**.

**Work-start `coffee`:** Re-offer and exit behavior for **AÃ¢â‚¬â€œE** match [coffee/SKILL.md](../coffee/SKILL.md) (**A**, **B**, **D** Ã¢â€ â€™ full hub by default; **C** Ã¢â€ â€™ exit unless **`stay in coffee`**; **A Ã¢â‚¬â€ Steward** Ã¢â€ â€™ steward fork when actionable).

## Default command

```bash
python3 scripts/operator_handoff_check.py -u strategy-codex
```

**Cold-thread stack (optional):** `python3 scripts/operator_reentry_stack.py -u strategy-codex` runs handoff check, then `operator_daily_warmup.py`, then `harness_warmup.py` (add `--compact` for a shorter harness). **One-line snapshot:** `python3 scripts/harness_warmup.py -u strategy-codex --receipt`. See the legacy re-entry stack notes.

## What to return

Summarize:

- **RECURSION-GATE** Ã¢â‚¬â€ pending totals (work-politics vs companion), listed items if any (script caps long queues), and the scriptÃ¢â‚¬â„¢s **proposed** processing steps (`operator_gate_review_pass` Ã¢â€ â€™ approve/reject in-file Ã¢â€ â€™ `process_approved_candidates.py`); remind that **merge requires companion approval**
- **Predictive History (work-jiang)** Ã¢â‚¬â€ **`## Predictive History Ã¢â‚¬â€ night closeout`**: where the lane rests, suggested first lever tomorrow, rotating **Spark** (edit `codex/predictive-history/metadata/warmup-sparks.yaml`), optional rebuild ritual; still read-only / not Record
- recently committed work
- meaningful local changes still in progress
- **`## Derived / export churn`** Ã¢â‚¬â€ PRP, manifest, ledger, etc. (regenerate or batch-commit vs editorial work)
- runtime-only noise that should stay uncommitted
- work-politics continuity if relevant
- the best next re-entry prompt
- **Skill discovery (one line, optional):** If the thread had a repeatable multi-step workflow, mention [skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md) and **menu H** (skills / meta pipeline) / [extract-skill-from-session](../extract-skill-from-session/SKILL.md) Ã¢â‚¬â€ do not block the handoff on it.

## Guardrails

- Distinguish runtime noise from real local work before recommending any commit or push.
- This is a summary workflow only. Do not stage, commit, or merge as part of the handoff.
- If local changes mix unrelated threads, say so clearly.

## Related files

- `docs/operator-skills.md`
- `docs/development-handoff.md`
- `recursion-gate.md`
