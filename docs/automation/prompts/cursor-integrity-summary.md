# Cursor Automation prompt â€” integrity summary (Grace-Mar)

**Use when:** A **weekly** (or **manual**) run is configured to **summarize** derived-export / **integrity** health â€” **read-only**; no commits of regen in this pass.

**Product trigger (operator configures in Cursor):** e.g. *Scheduled* (weekly) or *workflow_dispatch* equivalent for the automation product.

**Not** a replacement for: local `dream`, `operator_coffee` integrity sections, or **companion** decisions about when to regen.

---

## Preamble: paste the contract

Include [../cursor-safe-automation-contract.md](../cursor-safe-automation-contract.md) at the top of the prompt. Summary line:

*You may only **read** or **instruct**; you do not commit, do not `git add`, and do not write derived artifacts. The operator runs commands locally or in CI. No Record or gate file edits.*

---

## Your task

1. In the **checked-out** repo for this run, if the environment allows, run **read-only** checks appropriate to the operatorâ€™s selection. Prefer:
   - `python scripts/validate-integrity.py --json` (or `python3` as on PATH), **or** interpret a **pasted** output if the operator runs it elsewhere.
2. If **integrity** reports failures, list **drift** categories (e.g. manifest, PRP, runtime bundle) in plain language, using **only** what the log shows.
3. Suggest **exact** next commands the **operator** can run in a dev shell, e.g. from [work-cadence README â€” stale derived](https://github.com/rbtkhn/grace-mar/blob/main/continuity/cadence/README.md#when-integrity-reports-stale-derived-exports):
   - `bash scripts/regen_grace_mar_derived.sh`
   - `python3 scripts/validate-integrity.py --json`
4. **Do not** `git commit` regen. **Do not** modify `manifest.json`, `self-llm.txt`, or bundle files in this automation.

**If the sandbox cannot run Python** â€” say so and ask the operator to **paste** `validate-integrity` output, or mark **uncertain**.

## Expected output format

```markdown
### Integrity summary (automated) â€” for operator

**Integrity status:** [pass / fail / unable to run â€” reason]

**Drift detected:** [bullet list from tool output, or "none" or "see pasted log"]

**Commands to run locally (operator):** [numbered list, exact]

**Files likely involved:** [from output paths, or *unclear*]

**Governance note:** Read-only; not Record merge, not regen commit. Operator owns regen and commits.
```

**Related:** [work-cadence â€” stale derived](https://github.com/rbtkhn/grace-mar/blob/main/continuity/cadence/README.md#when-integrity-reports-stale-derived-exports) Â· [docs/automation/cursor-automations.md](../cursor-automations.md) Â· [README.md](../README.md)

