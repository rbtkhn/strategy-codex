# Singularity Research

work only; not Record.

This shelf holds **work-in-progress formal and theoretical research** under the singularity channel — developing frameworks that are not yet operational, not loop SSOT, and not system invariants.

## Status

- **Stage:** Research / early formalization
- **Stability:** Non-axiomatic, evolving
- **Integration:** Not bound to runtime systems or loop execution

## Artifacts

| Artifact | Path | Role |
| --- | --- | --- |
| Epistemic Geometry | [epistemic-geometry/](epistemic-geometry/README.md) | Multi-agent narrative alignment as a layered geometric structure |
| Predictive History | [predictive-history/](predictive-history/README.md) | External-system research overlay ([rbtkhn/predictive-history](https://github.com/rbtkhn/predictive-history)) — meta-analysis, non-modifying |

## Non-goals

- Not a substitute for [`singularity/loops/`](../loops/README.md) (recurring job YAML SSOT)
- Not a production execution surface
- Not a Record or gate candidate pipeline

## Lifecycle

Promotion path for artifacts on this shelf (documentation only — not automated):

```text
singularity/research/  →  (stabilization)  →  singularity definitions  →  statecraft/ operationalization  →  loops/ execution
```

## Future (not required for initial scaffold)

Loops may declare `output_shelves` pointing here when a formalization cadence is needed. See [loop system spec](../../docs/singularity/loop-system.md).
