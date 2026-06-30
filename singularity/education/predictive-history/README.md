# Predictive History — education outputs

WORK only; not Record.

**Source-grounded curriculum factory** for Predictive History — lecture-first, media-assisted, feedback-driven.

**Strategic plan (operating SSOT):** [STRATEGIC-PLAN.md](STRATEGIC-PLAN.md)

## Operating core

Each historical prediction case becomes a lesson, each lesson becomes a media pack, each media pack passes a quality gate, and each published artifact feeds learner feedback back into the curriculum.

```text
lecture/chapter intake → lesson brief → worksheet/quiz → media pack → quality gate → distribution → feedback → revision
```

## Loops and shelves

| Loop | Shelf | Artifacts |
| --- | --- | --- |
| `predictive-history-education` | (umbrella intake) | Lecture/chapter selection, routing to pipeline |
| `predictive-history-lesson-pipeline` | [`lessons/`](lessons/README.md), [`worksheets/`](worksheets/), [`quizzes/`](quizzes/), [`source-packets/`](source-packets/) | Lesson brief, worksheet, quiz, source packet |
| `predictive-history-media-pack` | [`media-packs/`](media-packs/README.md) | Slides, storyboard, narration, visual prompts |
| `predictive-history-media-quality-gate` | [`media-review/`](media-review/README.md) | Factual, pedagogy, rights review; approve/revise/hold/reject |
| `predictive-history-distribution-pack` | [`distribution/`](distribution/README.md) | YouTube, Shorts, Substack, podcast packages |
| `predictive-history-learner-feedback-review` | [`feedback/`](feedback/README.md) | Monthly revision queue, scorecard |

**Templates:** [`lessons/lesson-template.md`](lessons/lesson-template.md) · [`media-packs/media-pack-template.md`](media-packs/media-pack-template.md) · [`media-review/media-quality-gate-template.md`](media-review/media-quality-gate-template.md) · [`feedback/learner-feedback-review-template.md`](feedback/learner-feedback-review-template.md)

**Tool notes:** [`tool-notes/`](tool-notes/README.md)

**Action cards:** [`../../action-cards/predictive-history-lesson-pipeline/`](../../action-cards/predictive-history-lesson-pipeline/) · [standard](../../../docs/singularity/action-card-standard.md)

## Hard dependencies

```text
predictive-history-education → predictive-history-lesson-pipeline
predictive-history-lesson-pipeline → predictive-history-media-pack
predictive-history-media-pack → predictive-history-media-quality-gate
predictive-history-media-quality-gate → predictive-history-distribution-pack
predictive-history-distribution-pack → predictive-history-learner-feedback-review
```

## Soft feeds (not schema dependencies)

| From | To | What flows |
| --- | --- | --- |
| `predictive-history-learner-feedback-review` | `predictive-history-lesson-pipeline` | Content revision queue |
| `predictive-history-learner-feedback-review` | `predictive-history-media-quality-gate` | Asset/process revision queue |
| `predictive-history-media-quality-gate` | `predictive-history-distribution-pack` | Approved assets only |

## Upstream sources (read / cite; do not treat this shelf as corpus SSOT)

- Canonical repo: [rbtkhn/predictive-history](https://github.com/rbtkhn/predictive-history)
- In-repo mirror: [`continuity/predictive-history/`](../../continuity/predictive-history/README.md)

Corpus edits belong in the canonical clone; this shelf holds learner-facing artifacts only.

## Month 1 target (operator-created)

First full pipeline run → `lessons/lesson-001/` (not pre-filled in repo).
