# Dopamine / Flow Agency Benchmark

WORK only. Not Record. Not EVIDENCE. Not a gate substitute.

## Purpose

This benchmark tests whether an AI-assisted session increases creative agency instead of merely producing a quick reward loop.

The core question is:

> Did the session leave the operator more awake, more oriented, and more capable of making the next move?

This is adjacent to the Kleiber composition benchmark, especially `cm-2-dopamine-flow-ai-creation`, but it measures the session effect on judgment and creative momentum rather than the quality of one written artifact.

## Unit of analysis

One benchmark unit is a bounded AI-assisted creative or strategic session:

1. the operator enters with a live intention, question, or stuck point
2. the assistant helps generate, select, revise, or decide
3. the session produces a concrete next move or a principled stop
4. the evaluator scores the effect after a short distance, not only during the reward peak

Use this for coffee, conductor, dream, strategy-page, skill-design, benchmark, or repo-planning sessions where the danger is that speed and polish may feel like truth before judgment has caught up.

## Primary hypothesis

The strong version of the claim is not:

- AI makes creative work feel good

The strong version is:

- well-governed AI loops can turn reward energy into better orientation, sharper selection, and more durable creative agency

The benchmark should be willing to disconfirm that claim. A session can feel exciting and still fail the benchmark if it leaves only more motion, more polish, or more dependency on the tool.

## Source modes

Record the source mode for each run:

- `self_report`: the operator scores the session from memory or immediately after use
- `thread_review`: evaluator reviews the chat/session transcript
- `artifact_review`: evaluator reviews the durable artifact and surrounding diff
- `delayed_review`: evaluator re-scores after at least one sleep cycle or next working session

Prefer `thread_review` plus `delayed_review` when possible. Immediate self-report is useful, but it is also where dopamine inflation is most likely.

## Required metadata

| Field | Requirement |
|---|---|
| `benchmark_id` | `dopamine-flow-agency` |
| `rubric_version` | `dopamine-flow-agency-rubric-v1` |
| `run_date` | Local date of the evaluated session |
| `session_type` | `coffee`, `conductor`, `dream`, `strategy`, `coding`, `writing`, `skill-design`, or other short label |
| `source_mode` | One or more source modes from the list above |
| `evaluator` | Human or agent evaluator name |
| `entry_state` | One-line description of what the operator needed at the start |
| `output_state` | One-line description of what existed at the end |
| `next_move` | The next action, or `rest` / `stop` when the best move was not more generation |
| `notes` | Caveats, missing context, or source limits |

## Scorecard

Score each dimension from **1** to **5**. Each score must include a one-sentence rationale.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| **Orientation** | The session clarified what mattered and reduced ambiguity | Some clarity, but the frame still feels loose | More content appeared, but the real decision stayed hidden |
| **Momentum** | The next move became easier, concrete, and appropriately sized | There is a next move, but it is vague or overlarge | The session created motion without an executable next step |
| **Taste** | The operator's standards became more explicit or better protected | Standards were partly present but generic defaults leaked in | The assistant rewarded generic polish, speed, or compliance |
| **Selection pressure** | The session narrowed options using a real criterion | Options were listed, but the choice logic stayed weak | The loop expanded possibilities without helping choose |
| **Falsifiability** | Claims, plans, or outputs gained clear checks or failure conditions | Some risks were named, but tests are soft | The result feels true because it is fluent |
| **Afterglow** | After distance, the output still feels useful and worth returning to | Some value remains, but the initial excitement inflated it | The work collapses after the reward peak |
| **Human agency** | The operator has more authority, energy, and ownership afterward | Mixed: useful help, but some dependency or drift | The tool displaced judgment or made the operator more passive |

## Composite score

Use the unweighted average for quick runs:

```text
agency_score = average(orientation, momentum, taste, selection, falsifiability, afterglow, human_agency)
```

Closeout labels:

| Label | Rule |
|---|---|
| `Held` | No dimension below 4 |
| `Useful but hot` | Average at least 4, but `afterglow` or `falsifiability` is 3 |
| `Productive but shallow` | Any dimension at 3, none below 3, and no clear durable next move |
| `Broke` | Any core dimension below 3 |
| `Open` | Insufficient evidence, no delayed review yet, or evaluator cannot score confidently |

`Useful but hot` is the distinctive label for this benchmark: the session may have created real value, but the reward loop still needs a slower check before the work should guide decisions.

## Dopamine audit checklist

Use this quick check when an AI-assisted creative loop feels unusually energizing:

- Did the tool increase judgment, or only speed?
- What claim did the polished output make?
- What would make that claim false?
- Which part felt convincing because it sounded finished?
- What should receive slower human review before being treated as real work?
- Is the next move generation, selection, revision, or rest?

## Recommended prompt

```prompt
Evaluate this AI-assisted session using the Dopamine / Flow Agency Benchmark.

Session context:
- Entry state:
- Output state:
- Session type:
- Source mode:
- Durable artifacts or links:

Score these dimensions from 1 to 5, with one-sentence rationales:
- Orientation
- Momentum
- Taste
- Selection pressure
- Falsifiability
- Afterglow
- Human agency

Then provide:
- agency_score
- closeout label: Held / Useful but hot / Productive but shallow / Broke / Open
- strongest gain
- main dopamine-risk
- next slower check
- one sentence on whether the session improved creative agency or mainly created motion
```

## Failure modes

Watch especially for:

- **Polish substitution:** the answer reads finished, so the operator treats it as judged.
- **Menu intoxication:** many plausible options create a feeling of agency without selection.
- **Loop extension:** the system keeps generating because generation feels alive, not because the work needs it.
- **Authority drift:** the assistant's frame quietly becomes the operator's frame.
- **Premature doctrine:** one exciting session becomes a rule before a second case tests it.
- **Rest avoidance:** the correct next move is distance, but the loop keeps asking for another move.

## Relationship to existing benchmarks

- [kleiber-composition-benchmark.md](../work-dev/kleiber-composition-benchmark.md) tests composition quality and includes `cm-2-dopamine-flow-ai-creation` as a writing task.
- [conductor-recursive-improvement-benchmark.md](conductor-recursive-improvement-benchmark.md) tests whether conductor arcs increase recursive method power over time.
- This benchmark tests the operator-facing session effect: whether the AI loop improved creative agency.

The first local sample run is:

```text
artifacts/benchmarks/composition/2026-05-14/codex-gpt-5-prompt-only/cm-2-dopamine-flow-ai-creation/kleiber-run.md
```

That run scored a written strategy-page. Future agency benchmark runs should add a separate score block for the session itself instead of treating the composition score as enough.

## Acceptance check

After adding or running this benchmark, verify governed Record surfaces were not changed for this work:

```bash
git diff -- self.md self-archive.md recursion-gate.md session-log.md bot/prompt.py self-memory.md self-history.md
```

Any output must be explained as pre-existing residue or reverted if introduced by benchmark work.
