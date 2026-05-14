# Karajan CM-2 v2 writing benchmark review

WORK only. Not Record. Not EVIDENCE. Not a gate substitute.

## Metadata

| Field | Value |
|---|---|
| `benchmark_id` | `cm-2-dopamine-flow-ai-creation` |
| `prompt_version` | `composition-benchmark-v1-cm-2` |
| `rubric_version` | `cm-2-rubric-v2` |
| `run_date` | 2026-05-14 |
| `reviewed_run` | `artifacts/benchmarks/composition/2026-05-14/codex-gpt-5-prompt-only/cm-2-dopamine-flow-ai-creation/kleiber-run.md` |
| `evaluator` | Codex / Karajan pass |
| `source_mode` | `artifact_review` |
| `notes` | This review tests the existing CM-2 sample against the enhanced v2 writing rubric. It does not score session-level creative agency. |

## Whole-shape diagnosis

The existing CM-2 sample is compositionally strong, but the benchmark spec needed a cleaner long arc. Before this pass, CM-2 could reward a fluent page while leaving three structural risks under-specified:

- a decorative list of historical precedents could pass as a mechanism
- a general "slow down and review" recommendation could pass without a concrete counter-practice
- a high writing score could be mistaken for proof that the AI session improved human agency

The benchmark now names those as v2 scoring requirements rather than implicit evaluator taste.

## V2 score against current sample

| Dimension | Score | Rationale |
|---|---:|---|
| Template discipline | 5 | The sample uses Signal / Judgment / Prediction / Sources cleanly and keeps the public-facing structure legible. |
| Historical-pattern mechanism | 5 | "Mechanized amplification of skilled work" drives the distinction between amplification and judgment displacement. |
| Fit / mismatch balance | 5 | The sample explains why earlier amplification technologies fit and why AI differs by supplying provisional intention and confidence. |
| Falsifier quality | 4 | The falsifier is observable, though it requires longitudinal comparison and would benefit from sharper evidence thresholds. |
| Tension preservation | 5 | It holds flow benefits against judgment risk without collapsing into optimism or abstinence. |
| Strategic prediction quality | 5 | The prediction about rituals separating creative momentum from final judgment is actionable and revisit-ready. |
| Counter-practice architecture | 4 | The alternating-tempo practice is concrete enough to try, though future runs should name a tighter workflow protocol or checklist. |
| Agency boundary discipline | 4 | The sample mostly keeps artifact quality separate from human-agency claims, but the phrase "restore agency" should be handled carefully in prompt-only runs. |

`closeout label`: `Held`

Reason: no v2 dimension scored below 4. The sample still holds under the enhanced rubric, but the new rubric exposes where future CM-2 runs must be stricter.

## Enhancement receipt

Updated `docs/skill-work/work-dev/kleiber-composition-benchmark.md` to:

- mark new CM-2 runs as `cm-2-rubric-v2`
- define CM-2 as a writing benchmark, distinct from the dopamine / flow agency benchmark
- require one coherent historical-pattern family
- require a concrete counter-practice
- prevent polished artifact quality from standing in for improved human agency
- add v2 score dimensions for counter-practice architecture and agency boundary discipline
- add CM-2 shape checks before a run can close as `Held`

## Karajan close

Verdict: `Held`

Reason: the current CM-2 sample still lands as a strong composition run, and the benchmark now has a cleaner hierarchy: composition quality first, source discipline visible, counter-practice named, agency claims kept in their proper lane.

Falsifier: this enhancement fails if the next weak CM-2 sample can still close as `Held` while using only a decorative historical list, vague "use AI wisely" advice, or output-volume optimism as a proxy for human agency.

Next review condition: after the next two CM-2 runs, compare one strong sample and one weak sample against `cm-2-rubric-v2`; the rubric holds only if it preserves the separation between composition quality, source discipline, counter-practice architecture, and session-level agency.

Closeout receipt: `karajan-cm-2-v2-weak-stress.md` supplied the first weak-case check and scored `Broke`, so the v2 hierarchy has one passing positive case and one passing rejection case.
