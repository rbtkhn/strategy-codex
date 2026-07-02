# Education — curriculum factory

WORK only; not Record.

**Curriculum factory** — one source spine → **human** teach artifacts + **agent** training corpora.

| Audience | Factory output (examples) |
|----------|---------------------------|
| **Humans** | Lessons, worksheets, quizzes, media packs, distribution packages, learner feedback |
| **AI systems / agents** | Structured training packs — rubrics, eval fixtures, skill seeds, context bundles, agent-readable course graphs |

```text
research (learn) → education (curriculum factory) → humans (publish) + agents (train)
```

## Operating core

Same intake and quality spine; **fork at publish** into human-facing vs agent-training shelves.

```text
subject intake → lesson brief → worksheet/quiz → media pack → quality gate → distribution (humans) + agent packs (systems)
                                      └→ feedback → revision (both lanes)
```

Loop YAML stays in [`singularity/loops/`](../singularity/loops/README.md); this tree holds **outputs** only (same split as [`operations/`](../operations/README.md)).

## Layer invariants

- **`research/`** = learn — subject study, frameworks, experiments; do not dump inward research here without a publish pass
- **`education/`** = curriculum factory — teach artifacts for people and other agents from a shared source spine
- **Agent lane:** Training packs educate **other** agents/systems — not Record, not member identity; promote to [`skills/`](../skills/README.md) only through explicit skill workflow ([knowledge-boundary](../docs/knowledge-boundary-framework.md))

## Suggested project layout (at migrate)

```text
education/<project>/
  lessons/          # human
  distribution/     # human publish
  agent-packs/      # structured corpora for other AI systems (name TBD per project)
```

## Projects

| Project | Status | Factory home today |
|---------|--------|-------------------|
| Predictive History | pilot (off-root) | [`singularity/education/predictive-history/`](../singularity/education/predictive-history/README.md) — 6 loops |

## Not the same as

| Path | Role |
|------|------|
| [`research/`](../research/README.md) | **Operator learns** — subject research, frameworks, spikes |
| [`singularity/education/`](../singularity/education/predictive-history/README.md) | **PH curriculum factory today** — prototype; migrates to `education/` when ready |
| [`skills/`](../skills/README.md) | Portable **skill** SSOT — promoted from factory only via explicit workflow |
| [`runtime/prepared-context/`](../runtime/prepared-context/) | Ephemeral harness context — generated; not factory output |
| [`public/`](../public/predictive-history/) | Inbound read-only mirrors |
| [`essays/`](../essays/) | Cross-channel theses — not the primary education factory |

## Related surfaces

| Surface | Role |
| --- | --- |
| [`singularity/loops/projects/`](../singularity/loops/projects/) | PH and future curriculum loop YAML |
| [`singularity/action-cards/`](../singularity/action-cards/README.md) | Dated loop work orders |
| [`docs/singularity/loop-system.md`](../docs/singularity/loop-system.md) | Loop system spec |
| [`docs/predictive-history-external-boundary.md`](../docs/predictive-history-external-boundary.md) | PH human corpus push boundary |

Legacy PH pilot under `singularity/education/` until migrate (parallel to [`operations/`](../operations/README.md) relocate from `singularity/business/`).
