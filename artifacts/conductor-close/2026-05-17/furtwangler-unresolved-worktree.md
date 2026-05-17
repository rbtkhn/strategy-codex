# Furtwangler Close - Unresolved Worktree Tensions

WORK only. Not Record. Artifact-first conductor close.

## Object

Remaining dirty tree after the transcript-cleanup commits and Karajan closeout.

## Tension

The worktree is not simply unfinished; it contains several different kinds of unfinishedness.

- **Capture completion vs capture history:** the final May 16 target verdict says the requested day is complete, while earlier intermediate audit dirs still preserve the path by which it became complete.
- **Raw-input durability vs provenance hygiene:** several May 16 raw-inputs are useful, but some related metadata and host-quality updates still carry unresolved provenance or scope questions.
- **Benchmark learning vs capture shipping:** the May 16/17 benchmark artifacts are valid work-layer receipts, but they do not belong inside a May capture commit.
- **Runtime continuity vs commit hygiene:** memory, dream, handoff, cadence, and Cici files may be meaningful in their own lanes, but they would blur a capture or benchmark commit.

## Evidence

Final target-day audit:

- `artifacts/cognition-streams/check-streams-2026-05-16-cached-four-target-verdict/`
- `target_date_status: complete`
- `target_date_main_total: 9`
- `target_date_captured_main: 9`
- `target_date_must_capture_remaining: 0`
- `overall_backlog_status: below-threshold`

Superseded contradiction:

- `artifacts/cognition-streams/check-streams-2026-05-16-davis-post-intel-briefing/` still reports `captured_main: 3` / `main_total: 4` and `must_capture_remaining: 1`.
- `artifacts/cognition-streams/check-streams-2026-05-16-davis-complete/` later reports `captured_main: 4` / `main_total: 4` and `must_capture_remaining: 0`.

This contradiction is not a bug in the final verdict; it is process history. The final artifact should govern ship decisions, while the intermediate artifact should be parked unless preserving audit chronology is explicitly desired.

## Parked Family Inspection

The benchmark family is not capture residue:

- `artifacts/benchmarks/composition/2026-05-16/codex/ph-public-front-door-kleiber.md` is an adapted PH public-front-door benchmark with `closeout: Held`.
- `artifacts/benchmarks/composition/2026-05-17/codex-gpt-5/task-10-ai-writing-got-worse/` is a standard Task 10 composition benchmark with `Verdict: Held`.

Their incompleteness is classification only: they need a benchmark-receipts commit boundary, not more capture work.

## Falsify / Next Test

This close is wrong if a staged May capture slice cannot exclude the intermediate audit dirs while still proving `target_date_status: complete`, or if benchmark artifacts turn out to be dependencies of the final capture receipt rather than separate calibration receipts.

## Escalation

`[watch]` Preserve the tension. Do not collapse the dirty tree into one cleanup commit. The next commit should name one family:

1. May 16 target-day capture completion.
2. Benchmark receipts.
3. Substack raw-inputs.
4. Runtime/memory/cadence continuity.
5. Cici notebook lane.

## Verdict

Open.

The structure is clearer, but no ship decision should be forced until one family is staged and the staged diff tells one story.
