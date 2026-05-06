# Root-vs-users migration audit — 2026-05-05

## Purpose

Isolate the current repo-root migration from the rest of the dirty tree and separate:

- what looks **intentional**
- what looks **dangerous**
- what should be treated as the next hardening slice

This is a `work-dev` audit note, not a Record change and not a gate artifact.

## Scope

This pass looked only at the migration family:

- repo-root governed surfaces
- `users/grace-mar/` removals and residual mirrors
- `users/_template/` removals
- scripts/docs that still assume `users/<id>/...`

It explicitly does **not** judge the large `codex/`, `docs/`, or strategy-content edits except where they interact with the migration.

## What looks intentional

### 1. Root governed surfaces now exist

The expected repo-root counterparts are present for the major deleted `users/grace-mar` files:

- `self.md`
- `self-library.md`
- `self-memory.md`
- `self-skills.md`
- `self-work.md`
- `intent.md`
- `instance-doctrine.md`
- `session-transcript.md`
- `openclaw-user.md`
- `pipeline-events.jsonl`
- `fork_state.json`
- `fork-lineage.jsonl`
- `work-jiang.md`
- plus related root runtime / audit files

That strongly suggests a **real root-layout migration**, not accidental disappearance.

### 2. Core governed files are active at root

Active modified root governed surfaces include:

- `recursion-gate.md`
- `self-archive.md`
- `session-log.md`

These are the surfaces the scripts should now treat as canonical.

### 3. `users/_template/` looks intentionally retired

The broad deletion of `users/_template/` is internally consistent with the root-layout direction:

- root-level record/state files are being established
- the old user-template tree is being removed rather than maintained in parallel

This is large, but it reads as one migration move, not random churn.

## What looks dangerous

### 1. Script path assumptions still lag the migration

Several scripts still hardcode `REPO_ROOT / "users" / user_id / ...` for gate or continuity surfaces.

Highest-risk hotlist from this audit:

- `scripts/analyze_rejection_feedback.py`
- `scripts/assess_session_load.py`
- `scripts/batch_ingest_observations.py`
- `scripts/detect_capture_gap.py`
- `scripts/generate_gate_dashboard.py`
- `scripts/import_working_identity_candidates.py`

These are dangerous because they operate near:

- `recursion-gate.md`
- continuity reads
- operator dashboards
- staging imports

They can silently recreate the same class of root-layout failure already seen in the John Adams bookshelf path.

### 2. `users/grace-mar/` still contains live-looking mirrors

Even though many files were deleted there, some still remain modified under `users/grace-mar/`, including:

- `compute-ledger.jsonl`
- `fork-lineage.jsonl`
- `fork_state.json`
- `intent_snapshot.json`
- `last-dream.json`
- `llms.txt`
- `manifest.json`
- `pipeline-events.jsonl`
- `runtime-bundle/*`

This creates an ambiguous state:

- some truth appears to have moved to root
- some generated/runtime mirrors still live under `users/grace-mar/`

That is not necessarily wrong, but it is risky until the contract is explicit:

- root-only
- root canonical plus `users/grace-mar` mirror
- or transitional dual-surface

### 3. Accidental compatibility residue reappeared

An unwanted `users/strategy-codex/` subtree was present again during this audit.

It contained:

- `compute-ledger.jsonl`
- `fork-lineage.jsonl`
- `fork_state.json`
- `harness-events.jsonl`
- `pipeline-events.jsonl`
- `review-queue/boundary-classifications/CANDIDATE-0058.json`
- `review-queue/boundary-classifications/CANDIDATE-0059.json`

This subtree was removed during this pass.

Why it matters:

- it directly conflicts with the operator’s stated rule that this workspace should not grow a fake `users/strategy-codex/` compatibility layer
- it can mask script bugs by making the wrong path appear to work

## Working interpretation

The migration appears to be:

- **conceptually intentional**
- **operationally incomplete**

The repo is no longer in a clean `users/grace-mar` world, but it is also not yet fully normalized to repo-root assumptions across tooling and derived mirrors.

So the right reading is:

- **not** “revert the migration”
- **not** “assume the migration is complete”
- **yes** “finish the path hardening before trusting the surrounding operator scripts”

## Recommended next hardening slice

Treat the next migration-only code slice as:

1. normalize the six high-risk scripts above to `profile_dir(...)`
2. verify they no longer create or expect `users/strategy-codex/`
3. document whether `users/grace-mar/` remaining runtime files are:
   - canonical mirrors
   - temporary compatibility artifacts
   - or stale residue to retire later

## Short verdict

The root migration is real.

The main danger is not the existence of root files.
The main danger is the **half-migrated control plane** around them.
