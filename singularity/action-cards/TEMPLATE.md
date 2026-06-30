# Singularity Action Card

Copy into `singularity/action-cards/<loop-id>/<YYYY-MM-DD>.md`.

## Loop

```yaml
loop_id:
date: "YYYY-MM-DD"
operator:
related_loops:
```

## Situation

```yaml
what_changed:
why_it_matters:
source_or_evidence:
```

## Decision

```yaml
recommended_next_action:
urgency: low | medium | high | critical
expected_benefit:
risk_if_ignored:
```

## Execution

```yaml
owner:
estimated_time:
required_inputs:
blocked_by:
```

## Review Gate

```yaml
human_approval_required: yes | no
reviewer:
acceptance_criteria:
proof_artifact_required:
```

## Outcome

```yaml
status: planned | done | blocked | skipped | revised | rejected
proof_artifact:
blocked_reason:
lessons_learned:
next_loop_ids:
```

Standard: [`docs/singularity/action-card-standard.md`](../../docs/singularity/action-card-standard.md)
