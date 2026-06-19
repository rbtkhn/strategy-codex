# CodeGraph Pilot Benchmark

**Status:** work-layer protocol. Not Record. Not a gate substitute.

## Purpose

This benchmark decides whether the bounded CodeGraph pilot should:

- **expand** into a richer code-intelligence path
- **contain** itself as a narrow local helper
- **retire** if the local gains are too small or too fragile

The benchmark is intentionally small. It is not trying to prove that CodeGraph is universally good for the whole repo. It is only trying to answer one operator-facing question:

**Does CodeGraph materially improve real `strategy-codex` code work enough to justify the maintenance surface it adds?**

## Smallest Real Loop

Run exactly **three tasks** against the same local checkout:

1. **Code exploration**
   Compare ordinary repo exploration versus CodeGraph-assisted exploration for one architecture question on `platform/src/` or `scripts/`.
2. **Pre-edit impact review**
   Compare ordinary repo exploration versus CodeGraph-assisted review for one change-impact question.
3. **Presentation prep**
   Compare the current repo method versus the CodeGraph export -> bundle path for one architecture-oriented presentation input.

If the loop cannot complete all three tasks, the result is at best `Open`.

## Canonical First Task Set

Use this default benchmark set unless there is a better live task that week:

### Task A - Presentation service architecture

Question:

`What are the key entry points, call relationships, and source files for the presentation service path?`

Default target files:

- `platform/src/grace_mar/presentations/service.py`
- `platform/src/grace_mar/presentations/presenton_client.py`
- adjacent helpers revealed during the run

### Task B - Presentation service impact review

Question:

`If we change platform/src/grace_mar/presentations/service.py, what other files and likely test surfaces should we inspect first?`

Default changed file:

- `platform/src/grace_mar/presentations/service.py`

### Task C - Architecture bundle prep

Question:

`Can we produce a more legible, traceable architecture bundle for the presentation path with less prep time than the ordinary manual route?`

Default output:

- one bounded bundle JSON under `runtime/artifacts/presentations/`

## Comparison Discipline

For each task, run two lanes:

- **Baseline lane:** ordinary repo methods (`rg`, file reads, manual synthesis)
- **CodeGraph lane:** local CodeGraph plus the pilot bridge

Keep the scope constant. Do not let the CodeGraph lane win by answering a broader question than the baseline lane.

## Required Measures

Record these for each lane and each task:

| Measure | Requirement |
|---------|-------------|
| `wall_minutes` | Rounded elapsed minutes from start to usable answer |
| `tool_calls` | Count command or inspection steps taken in the lane |
| `output_path` | Link to the resulting note, answer, or bundle |
| `answer_quality` | `strong`, `usable`, or `weak` |
| `notes` | One short line on friction, ambiguity, or failure mode |

Use truthful manual counts if automation is missing. Do not fake precision.

## Success Thresholds

The pilot holds as worth expanding only if all of these are true:

- **at least 20% lower cost or effort** on code-heavy work
- **at least 30% faster** on exploration or impact-review tasks
- **at least 15% lower prep time** on the architecture bundle task
- **no governance or sovereignty regressions**
- **no repeated environment brittleness** that makes the path feel lucky rather than reliable

If speed improves but quality falls, the benchmark does not hold.

## Verdicts

Use one of these close words:

- `Expand`: the pilot clearly helps and should earn the next integration step
- `Contain`: useful in a narrow lane, but not strong enough for broader doctrine
- `Retire`: the added surface is not paying for itself
- `Open`: the loop was incomplete or inconclusive

Every close must end with exactly one next action:

- `Expand`: name the next bridge or automation step
- `Contain`: name the narrow use case to keep
- `Retire`: name what to remove or stop maintaining
- `Open`: name the missing evidence

## Output Location

Store benchmark runs under:

```text
runtime/artifacts/benchmarks/code-intelligence/
```

Suggested run folder:

```text
runtime/artifacts/benchmarks/code-intelligence/YYYY-MM-DD/<runner>/codegraph-pilot-v1/
```

Minimum run contents:

- `metadata.json`
- `baseline-notes.md`
- `codegraph-notes.md`
- `closeout.md`

Optional:

- exported CodeGraph context
- generated presentation bundle
- small timing table or receipt

## Metadata

Every run should record:

| Field | Requirement |
|-------|-------------|
| `benchmark_id` | `codegraph-pilot-v1` |
| `runner` | human or agent runner label |
| `run_date` | local date |
| `repo_ref` | git ref or commit |
| `project_scope` | usually `strategy-codex` |
| `tasks` | the three task labels used |
| `codegraph_status` | initialized / stale / missing |
| `verdict` | `Expand`, `Contain`, `Retire`, or `Open` |
| `next_action` | one concrete operator action |

## Anti-Sprawl Rule

Do not widen this benchmark into a generic IDE or semantic-search bakeoff.

This protocol is only for one bounded question:

**Is the current local CodeGraph pilot compounding enough inside `strategy-codex` to deserve a larger place in the toolchain?**

If that answer becomes clearly yes or clearly no, stop expanding the benchmark and act on the result.

