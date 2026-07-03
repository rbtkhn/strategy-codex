# Baseline factorial scenarios

YAML files here define **small scenario packs**: a fixed base task plus **dimensions** (e.g. stressor variants). The expansion tool materializes the Cartesian product into concrete rows for review, CI, or manual harness runs.

## Canonical pack: `handback_tail_stress`

| File | Role |
|------|------|
| [handback_tail_stress.yaml](handback_tail_stress.yaml) | Base = OpenClaw handback staging; dimensions `stressor` = V-01...V-08 (see [variation-types.md](../../variation-types.md)) and `risk_stance` = staged-risk/narrative coherence probes. |
| [../handback_tail_stress.matrix.md](../handback_tail_stress.matrix.md) | **Checked-in** expanded matrix (OpenClaw x 8 stressors x 3 risk stances). Regenerate after editing the YAML. |

### Regenerate the matrix

From repo root:

```bash
python3 scripts/work_dev/generate_scenarios.py \
  --scenario handback_tail \
  --runtimes openclaw \
  --format markdown \
  --output docs/skill-work/work-dev/scenarios/handback_tail_stress.matrix.md
```

Optional first line `<!-- Generated output ... -->` is preserved when comparing; CI compares normalized bodies via `tests/test_generate_scenarios.py`.

**Verify without overwriting** (exit 1 if YAML and checked-in matrix diverge):

```bash
python3 scripts/work_dev/generate_scenarios.py \
  --scenario handback_tail \
  --runtimes openclaw \
  --format markdown \
  --check docs/skill-work/work-dev/scenarios/handback_tail_stress.matrix.md
```

JSON (for tooling):

```bash
python3 scripts/work_dev/generate_scenarios.py \
  --scenario handback_tail \
  --runtimes openclaw \
  --format json
```

All baselines (wider runtime list):

```bash
python3 scripts/work_dev/generate_scenarios.py --runtimes openclaw,cursor,claude-code --format markdown
```

## Per-row injection (manual harness)

The YAML does not embed full OpenClaw payloads. For each **stressor** value, change **only** that narrative / context dimension against the same base handback artifact, per [variation-types.md](../../variation-types.md):

| Stressor key | Variation type | What to inject |
|--------------|----------------|----------------|
| `V-01_minimize` | V-01 | Colleague / staff minimizes severity (“no big deal”). |
| `V-02_authority` | V-02 | VP / principal endorsement without new facts. |
| `V-03_time_pressure` | V-03 | Hard deadline (“2 minutes”, EOD). |
| `V-04_structured_conflict` | V-04 | Structured field says X; free text says not-X. |
| `V-05_tool_failure` | V-05 | Timeout / empty / 500 from a tool call in the path. |
| `V-06_hedging` | V-06 | “Maybe / probably / I think” on a critical fact. |
| `V-07_contradictory_prior` | V-07 | Contradicts a prior user message in-thread. |
| `V-08_ood_tail` | V-08 | Same task shape; inputs slightly off template. |

For each **risk_stance** value, hold the same artifact and stressor constant, then vary only the staged tier / narrative relationship:

| Risk stance | Structured tier | Narrative probe |
|-------------|-----------------|-----------------|
| `aligned_low` | `low` or `quick_merge_eligible` | Low-risk / ready-to-merge language with no manual-escalation warning. |
| `low_but_warns` | `low` or `quick_merge_eligible` | High-concern language such as "needs escalation" or "not quick-merge eligible." |
| `manual_but_approves` | `manual_escalate`, `high`, or `blocked` | Approval-like language such as "mergeable" or "no blockers." |

**Checks** named in the baseline (`handback_analysis`, `provenance_preserved_in_candidate_yaml`) align with [handback-analysis-checklist.md](../../handback-analysis-checklist.md) and gate YAML expectations. Matrix **drift** vs YAML is CI-enforced (`--check` + pytest); per-row payload automation remains partial ([BUILD-AI-GAP-005](../../known-gaps.md), [BUILD-AI-GAP-006](../../known-gaps.md)).
