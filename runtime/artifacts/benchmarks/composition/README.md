# Composition Benchmarks

**Status:** work-layer artifact bucket. Not Record. Not EVIDENCE.

This folder stores Strategy-codex composition benchmark prompts, outputs, scores, and closeouts generated through the Kleiber composition benchmark protocol:

```text
docs/skill-work/work-dev/kleiber-composition-benchmark.md
```

V1 benchmark execution route:

```text
Kleiber Conductor Action Menu -> D. Finale: Run composition benchmark
```

Coffee may route to Kleiber, and dream may carry forward eligible results, but neither runs benchmarks directly.

For session-level evaluation of whether the AI loop improved creative agency rather than merely producing a polished artifact, use:

```text
docs/skill-work/work-strategy/dopamine-flow-agency-benchmark.md
```

## Suggested Layout

```text
runtime/artifacts/benchmarks/composition/
  README.md
  YYYY-MM-DD/
    <model-or-provider>/
      prompt.md
      output.md
      score.md
      metadata.json
```

## Required Metadata

Record these fields for each run:

- `benchmark_id`
- `prompt_version`
- `rubric_version`
- `model`
- `provider`
- `model_version`
- `run_date`
- `temperature`
- `seed`
- `source_mode`
- `evaluator`
- `notes`

Allowed source modes:

- `prompt_only`
- `source_pack`
- `live_lookup`

## Closeout

Each run closes as:

- `Held`: no dimension below 4
- `Weakened`: at least one dimension at 3, none below 3
- `Broke`: any core dimension below 3
- `Open`: incomplete run, insufficient evidence, or source-mode problem

Do not store governed Record changes here. This bucket is for benchmark calibration artifacts only.
