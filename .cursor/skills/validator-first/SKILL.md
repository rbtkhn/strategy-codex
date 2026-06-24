---
name: validator-first
description: Run repo validators and check scripts before reading their source. Use when the operator picks a menu letter for validate_*, sync_*, handoff-check, routing pass, pin-cite validate, study-edition validate, or says run/check/pass on a named script under scripts/.
category: truth-pipeline
status: active
scope_class: repo-governed
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
| Essay template slop | `strategy-codex`: `python3 scripts/prose_slop_lint.py essays/<file>.md` or `--diff base...head essays/` |
| Prose Forge (slop + optional Vale) | `strategy-codex`: `python3 scripts/prose_forge.py lint essays/<file>.md` |
| CIV-STATE public export | `strategy-codex`: `python3 scripts/export_civilizational_statecraft_public.py` then `python3 scripts/validate_civilizational_statecraft_public.py runtime/artifacts/civilizational-statecraft-public` — **not** `--validate` on the export script |

Use **`python`** or **`python3`** per host; Windows repo root paths as in session.

## Civ-lens profile SSOT wedge (strategy-codex)

Use when shipping **speaker profile migration** (`codex/profiles/` → `statecraft/voices/<speaker>/` or `statecraft/hosts/<host>/` + redirect stub). One **pair or single speaker** per commit — not the whole migration wave.

**Procedure (one validator run + one git Shell when executing):**

1. **Run first** (do not read validator source):
   ```bash
   python3 scripts/validate_repo_routing.py --strict
   ```
2. **Stage only** the wedge: canonical profile + shelf `README.md` / `index.md` + `*-source-index.md` when new + `codex/profiles/*-profile.md` redirect + `INDEX.md` / `repo-map.yaml` wiring if touched.
3. **Commit** with a message naming the speaker pair and “voices SSOT” or “hosts SSOT”.
4. **`git push origin main`** when the menu pick includes push; report network failure separately from validator failure.
5. On pass after ship: optional `operator_handoff_check.py --fast` receipt.

**Do not** mix telemetry (`work-cadence-events.md`, `memory.md`), `.gitignore`, or unrelated validator WIP into the same commit unless the operator names that combo.

## Stall recovery

If Shell hangs or interrupts:

1. Retry **only** the run command (no parallel reads).
2. If still blocked, switch to **`fast tools`**: Read/Write the target files, then one narrow Shell (see [coffee SKILL — Harness hang recovery](../coffee/SKILL.md#harness-hang-recovery)).
3. If still blocked, report and suggest operator run locally with the exact one-liner.

## Verification / Proof Standard

Do not call this complete unless:

- the input source, file, paste, URL, or archive path is named
- the output surface is named
- skipped steps are explicitly marked with a reason
- uncertainty, missing evidence, or unresolved source defects are stated
- validator or check command and exit code must be reported

Evidence to report:

- files touched or produced
- scripts or commands run
- source URLs, archive paths, or transcript identifiers used
- confidence downgrade, if any

If verification cannot be completed:

- state what was not verified
- stop before archive land, synthesis, publication, or promotion
- return a bounded partial result for operator review