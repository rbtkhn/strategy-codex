# Speaker Memory Benchmarks

**Status:** work-layer benchmark fixture bucket. Not Record. Not EVIDENCE.

These benchmarks test whether an agent can use the speaker-folder architecture to accumulate judgment without pushing interpretation back into the lattice.

Speaker-memory benchmarks are for:

- speaker objects as durable dossiers
- host-local speaker arcs as conversational-form notes
- helixes and cross-host notes as comparative surfaces
- routing restraint from daily ingest into the right speaker folder

They are not model-run outputs by themselves. A fixture becomes a run only when a model output, score, metadata, and closeout are added under a dated run folder.

## Fixture Layout

```text
runtime/artifacts/benchmarks/speaker-memory/
  README.md
  fixtures/
    sm-1-speaker-object-repair/
      metadata.json
      prompt.md
      source-pack.md
      expected-output-shape.md
      rubric.md
    sm-2-speaker-arc-ranking/
      metadata.json
      prompt.md
      source-pack.md
      expected-output-shape.md
      rubric.md
    sm-3-speaker-structure-metrics/
      metadata.json
      prompt.md
      source-pack.md
      expected-output-shape.md
      rubric.md
    sm-4-speaker-maturity-ranking/
      metadata.json
      prompt.md
      source-pack.md
      expected-output-shape.md
      rubric.md
```

## Benchmarks

`SM-1 speaker-object-repair` tests whether an agent can compose or repair a `*-speaker-object.md` note from existing speaker-folder evidence, templates, and boundary rules.

`SM-2 speaker-arc-ranking` tests whether an agent can rank a host x guest arc, choose the best open-first path, name a paired read, and keep lattice rows secondary.

`SM-3 speaker-structure-metrics` tests whether an agent can score a speaker shelf on quantitative and quasi-quantitative structure dimensions without collapsing recurrence, completeness, and maturity into one vague impression.

`SM-4 speaker-maturity-ranking` tests whether an agent can compare several speaker objects using the shared metric language and produce a defended ranking that does not confuse raw volume with maturity.

## Calibration Pack

For live repo-grounded examples rather than synthetic strong/weak harness samples, use:

- [calibration/README.md](calibration/README.md)
- [SM-3 Freeman calibration](calibration/sm-3-freeman-calibration.md)
- [SM-4 Freeman-Crooke-Baud calibration](calibration/sm-4-freeman-crooke-baud-calibration.md)

These are read-only doctrinal examples. They are not run artifacts and they do not replace scored benchmark runs.

## Metric Policy

For speaker quality work, prefer a **vector** over a single magic number.

Primary dimensions:

- `density`
- `completeness`
- `coherence`
- `maturity`

`Maturity` should remain a visible dimension in the score vector. A separate weighted composite may be reported only after all four dimensions are surfaced. A high-volume but incoherent shelf should not outrank a lower-volume but highly routeable one by file count alone.

See [speaker-structure-benchmark.md](speaker-structure-benchmark.md) for the metric definitions and weighting guidance.

## Closeout

Use one closeout label per run:

- `Held`: no dimension below 4
- `Weakened`: at least one dimension at 3, none below 3
- `Broke`: any core dimension below 3
- `Open`: incomplete run, insufficient evidence, source-mode problem, or evaluator cannot score confidently

## Recursive Scoring Loop

Use the deterministic scorer after a run has `metadata.json` and `output.md`:

```bash
python scripts/score_speaker_memory_benchmark.py --run runtime/artifacts/benchmarks/speaker-memory/runs/YYYY-MM-DD/<runner>/<benchmark-id>
```

The scorer writes:

- `score.json` - numeric checks, total score, closeout, failure codes, and repair actions
- `score.md` - human-readable scorecard
- `repair-queue.jsonl` - one advisory repair row per failure code

Use the repair queue as telemetry, not automation. Fix one target, rerun the scorer, and compare `percentage`, `closeout`, and `failure_codes`.

## Validation Commands

Use a two-tier validation model:

- **Primary operator path:** bundle-first harness that runs in the bundled Codex runtime
- **Secondary engineering path:** deeper component checks in a richer local dev interpreter or CI

Do not treat missing `pytest` in the bundled runtime as a benchmark-family failure. The canonical green-path command is the harness below.

Canonical bundle-first validation path:

```bash
python scripts/validate_speaker_memory_benchmark_family.py
```

This is the primary green-path command for the benchmark family. It is designed to run with the active repo interpreter in the bundled Codex environment and does not require `pytest`.

Expected success receipt:

- headline: `speaker-memory benchmark family: OK`
- required passing checks:
  - `fixture_completeness`
  - `registry_consistency`
  - `scorer_smoke`
  - `portable_skill_verify`
  - `speaker_object_baseline`
  - `benchmark_wiring`

Failure classes covered by the harness:

- missing or incomplete fixture packs
- scorer/fixture registry drift
- strong/weak benchmark sample misclassification
- portable skill verify regressions for `check-streams`
- speaker-object baseline validator failures
- benchmark id wiring gaps across artifacts, scripts, and tests

Secondary engineering checks for debugging, local-dev validation, or CI:

```bash
python scripts/validate_speaker_objects.py
python scripts/sync_portable_skills.py --verify --skill check-streams
python scripts/score_speaker_memory_benchmark.py --run runtime/artifacts/benchmarks/speaker-memory/runs/YYYY-MM-DD/<runner>/<benchmark-id>
rg -n "sm-1-speaker-object-repair|sm-2-speaker-arc-ranking|sm-3-speaker-structure-metrics|sm-4-speaker-maturity-ranking|speaker-memory-benchmark-v1" runtime/artifacts/benchmarks docs scripts tests
```

Optional deeper test-runner path when `pytest` is available in the active interpreter:

```bash
python -m pytest tests/test_score_speaker_memory_benchmark.py tests/test_validate_speaker_memory_benchmark_family.py -q --basetemp .codex-test-temp/speaker-memory-benchmark-pytest
```

Optional post-edit hygiene check:

```bash
git diff -- self.md self-archive.md recursion-gate.md session-log.md archive/grace-mar-instance/bot/prompt.py
```

The governed-surface diff should show no benchmark-introduced changes to Record surfaces.
