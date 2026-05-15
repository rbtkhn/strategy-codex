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
artifacts/benchmarks/speaker-memory/
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
```

## Benchmarks

`SM-1 speaker-object-repair` tests whether an agent can compose or repair a `*-speaker-object.md` note from existing speaker-folder evidence, templates, and boundary rules.

`SM-2 speaker-arc-ranking` tests whether an agent can rank a host x guest arc, choose the best open-first path, name a paired read, and keep lattice rows secondary.

## Closeout

Use one closeout label per run:

- `Held`: no dimension below 4
- `Weakened`: at least one dimension at 3, none below 3
- `Broke`: any core dimension below 3
- `Open`: incomplete run, insufficient evidence, source-mode problem, or evaluator cannot score confidently

## Recursive Scoring Loop

Use the deterministic scorer after a run has `metadata.json` and `output.md`:

```bash
python scripts/score_speaker_memory_benchmark.py --run artifacts/benchmarks/speaker-memory/runs/YYYY-MM-DD/<runner>/<benchmark-id>
```

The scorer writes:

- `score.json` - numeric checks, total score, closeout, failure codes, and repair actions
- `score.md` - human-readable scorecard
- `repair-queue.jsonl` - one advisory repair row per failure code

Use the repair queue as telemetry, not automation. Fix one target, rerun the scorer, and compare `percentage`, `closeout`, and `failure_codes`.

## Validation Commands

After adding or scoring a speaker-memory benchmark, run:

```bash
python scripts/validate_speaker_objects.py
python scripts/sync_portable_skills.py --verify --skill check-streams
python -m pytest tests/test_speaker_routing_queue.py tests/test_validate_speaker_objects.py -q --basetemp .codex-test-temp/speaker-memory-benchmark-pytest
rg -n "sm-1-speaker-object-repair|sm-2-speaker-arc-ranking|speaker-memory-benchmark-v1" artifacts/benchmarks docs scripts tests
git diff -- self.md self-archive.md recursion-gate.md session-log.md bot/prompt.py
```

The final diff command should show no benchmark-introduced changes to governed Record surfaces.
