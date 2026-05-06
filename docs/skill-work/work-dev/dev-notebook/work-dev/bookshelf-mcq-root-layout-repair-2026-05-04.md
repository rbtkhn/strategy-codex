# Bookshelf MCQ root-layout repair — 2026-05-04

## Purpose

Record the failure pattern and the script-level audit from the John Adams bookshelf run so future agents do not improvise around an already-coded workflow or reintroduce `users/<id>/` assumptions into the root-layout repo.

## Failure pattern

The immediate miss was **protocol displacement**:

- the operator asked for **bookshelf knowledge**
- a coded **source-bound MCQ -> strictness pick -> stage to recursion-gate -> approve -> merge** path already existed
- the agent initially answered with open-ended elicitation instead of using the bookshelf path

That error then widened into a second class of mistake:

- root-governed surfaces (`self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`) were treated as if they lived under `users/<id>/`
- a compatibility directory was briefly created instead of fixing the path assumptions in scripts

The correct repo rule is simpler:

- `knowledge` and `recursion-gate` are governed root surfaces in this workspace
- `codex/` is the strategy notebook, not the approval membrane
- when the bookshelf workflow exists, use it before inventing a substitute

## Correct control surface

For bookshelf-to-knowledge work, the control surface is:

1. shelf anchor in `docs/skill-work/work-strategy/history-notebook/research/bookshelf-catalog.yaml`
2. source-bound quiz anchor in `docs/skill-work/work-strategy/history-notebook/research/bookshelf-quiz-anchors.yaml`
3. MCQ validation round
4. strictness choice (`top2`, `top4`, or `report-only`)
5. staged `CANDIDATE-*` blocks in root `recursion-gate.md`
6. governed merge via `scripts/process_approved_candidates.py`

Anything else is a fallback, not the default.

## What was fixed in this repair slice

### Bookshelf source binding

- Added John Adams quiz anchor:
  - `bq-john-adams-revolutionary-writings`
  - shelf refs: `HNSRC-0269`, `HNSRC-0270`

### Root-layout compatibility

- `scripts/repo_io.py`
  - restored `DEFAULT_USER_ID` as a back-compat alias to `DEFAULT_PROFILE_ID`
  - keeps canonical profile resolution at repo root

- `scripts/fork_checksum.py`
  - fixed UTF-8 read for `pipeline-events.jsonl`

- `scripts/refresh_derived_exports.py`
  - now respects `profile_dir(user_id)`
  - resolves root-layout PRP output to `grace-mar-llm.txt`

- `scripts/validate-integrity.py`
  - now resolves user roots through `profile_dir(...)`
  - no longer infers a fake `strategy-codex-llm.txt` path for the root-layout repo

- `scripts/check_gate_merge_readiness.py`
  - now defaults to `profile_dir(user_id) / "recursion-gate.md"` and `profile_dir(user_id) / "self.md"`
  - no longer emits false bookshelf blockers when `PyYAML` is unavailable; it downgrades those checks to warnings instead

## Audit: remaining fragility in the bookshelf MCQ pipeline neighborhood

These were found by searching for `REPO_ROOT / "users" / ... / "recursion-gate.md"` and related root-layout assumptions.

### High relevance to gate / staging / operator review

- `scripts/analyze_rejection_feedback.py`
- `scripts/assess_session_load.py`
- `scripts/batch_ingest_observations.py`
- `scripts/detect_capture_gap.py`
- `scripts/generate_gate_dashboard.py`
- `scripts/import_working_identity_candidates.py`

These touch gate parsing, staging, or operator-facing queue views. They should move to `profile_dir(...)` before being trusted in the root-layout repo.

### Medium relevance to auxiliary staging flows

- `scripts/cmc_lecture_helper.py`
- `scripts/emit_work_politics_gate_paste_snippet.py`
- `scripts/emit_work_strategy_gate_paste_snippet.py`
- `scripts/ingest_from_cmc.py`

These are not part of the narrow Adams merge path, but they can recreate the same error if used without repair.

### Lower-priority / indirect observability surfaces

- `scripts/audit_cadence_rhythm.py`
- `scripts/build_gate_board.py`
- `scripts/bridge_last_state.py`
- `scripts/contradiction_digest.py`

These should still be normalized eventually, but they were not on the critical path for the John Adams bookshelf merge.

## Operational rule for future agents

When the operator asks for bookshelf knowledge:

- do **not** start with generic elicitation
- first resolve whether a quiz anchor already exists
- if it does, run the source-bound MCQ path
- if it does not, add the anchor first, then run the same path
- stage only to root `recursion-gate.md`
- never create a fake `users/strategy-codex/` compatibility tree to satisfy broken scripts

## Short verdict

The John Adams outcome was recoverable, but the failure showed a durable risk:

- **inventing around encoded workflow**
- plus
- **papering over path bugs with directory workarounds**

The repair standard is:

- obey the existing workflow first
- fix the path assumption second
- only then add new logic
