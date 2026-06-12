---
name: validator-first
description: >-
  Run repo validators and check scripts before reading their source. Use when
  the operator picks a menu letter for validate_*, sync_*, handoff-check,
  routing pass, pin-cite validate, study-edition validate, or says run/check/pass
  on a named script under scripts/.
---

# Validator-first

**Goal:** Deliver **exit code + summary** in the **same turn** as the operator's pick. Avoid read/grep archaeology before the first run.

## Triggers

- Menu pick mapped to a **run** (e.g. routing pass → `validate_repo_routing.py`)
- Operator: **run E**, **validate routing**, **handoff check**, **pin-cite ok?**, **sync manifest**
- Before ship: quick integrity commands named in the menu benefit clause

## Procedure

1. **Identify script** from pick or menu stub (path under `scripts/`).
2. **Run from repo root** (one Shell call):
   ```bash
   python scripts/<script>.py
   ```
   Add flags only if the menu or prior thread named them (e.g. `--part 05`, `--compact`).
3. **Reply with:** exit code, pass/fail line, first 5–10 error lines if fail.
4. **Read source** only if exit ≠ 0 and fix is in scope, or operator asked to edit the validator.

## Do not

- Read the full validator file before step 2 when the job is **run only**
- Parallel **Read + Grep + Shell** on the same script in one turn
- End the turn without stdout/exit code when the pick was a run fork
- Repeat a stalled batch; use **narrow retry** (see [agent-execution-hygiene.mdc](../../rules/agent-execution-hygiene.mdc))

## Common scripts (strategy-codex / ph-civ)

| Intent | Script (cwd) |
|--------|----------------|
| Repo routing | `strategy-codex`: `scripts/validate_repo_routing.py` |
| Pin-cite manifest | `ph-civ`: `scripts/validate_pin_cite.py` |
| Manifest sync all | `ph-civ`: `scripts/sync_all_parts_to_manifest.py` |
| Study edition | `ph-civ`: `scripts/validate_study_edition.py --part NN` |
| Handoff / ship | `strategy-codex`: `python3 scripts/operator_handoff_check.py` |

Use **`python`** or **`python3`** per host; Windows repo root paths as in session.

## Stall recovery

If Shell hangs or interrupts:

1. Retry **only** the run command (no parallel reads).
2. If still blocked, report and suggest operator run locally with the exact one-liner.
