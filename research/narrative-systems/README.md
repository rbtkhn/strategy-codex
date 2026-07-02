# Narrative Systems Research

work only; not Record.

Category-theoretic framework for modeling narratives, cognition, and geopolitical interpretation — WIP formal research under the singularity channel (not loop SSOT, not system invariants).

## Status

- **Stage:** Research / early formalization
- **Stability:** Non-axiomatic, evolving
- **Integration:** Not bound to runtime systems or loop execution

## Structure

| Layer | Path | Role |
| --- | --- | --- |
| System | [00_system/](00_system/) | Meta rules |
| Ontology | [01_ontology/](01_ontology/) | Primitives |
| Category backbone | [02_narrative_systems/](02_narrative_systems/) | NST formal core (functor F, Δ, monoidal extension) |
| Core models | [03_core_models/](03_core_models/) | Competing theories (PH, civilization-state) |
| Mappings | [04_mappings/](04_mappings/) | Inter-model translation |
| Geometric lenses | [05_geometric_lenses/](05_geometric_lenses/) | Epistemic geometry functor |
| Dynamics | [06_dynamics/](06_dynamics/) | Temporal evolution |
| Applications | [07_applications/](07_applications/) | Real-world modeling |
| Comparisons | [08_comparisons/](08_comparisons/) | Structured model contrast |
| Open problems | [09_open_problems/](09_open_problems/) | Unresolved research |

## Artifacts

| Artifact | Path | Role |
| --- | --- | --- |
| Epistemic Geometry | [05_geometric_lenses/epistemic_geometry/](05_geometric_lenses/epistemic_geometry/README.md) | Multi-agent narrative alignment as layered geometric structure |
| Predictive History | [03_core_models/predictive_history/](03_core_models/predictive_history/README.md) | External-system research overlay ([rbtkhn/predictive-history](https://github.com/rbtkhn/predictive-history)) — meta-analysis, non-modifying |
| Narrative Systems (NST) | [02_narrative_systems/](02_narrative_systems/) | Relational mapping between EG (structure) and PH (time) — not a container |
| Civilization State | [03_core_models/civilization_state/](03_core_models/civilization_state/README.md) | Synthetic geopolitical dynamics — discrete state-machine simulation layer |
| Model relations | [04_mappings/model_relations/](04_mappings/model_relations/README.md) | Parallel functors H → 𝔈 (P vs C) — open Rel(P,C) |

EG and PH are independent peers; NST defines coupling only. Civilization State is a **synthetic generative peer** to PH; NST and [coupling_notes.md](03_core_models/civilization_state/coupling_notes.md) define bridges.

## Core idea (NST)

NST: (EG, PH) → R — relational coupling between epistemic structure and temporal narrative evolution.

Formal specification: [02_narrative_systems/formal_model.md](02_narrative_systems/formal_model.md).

## Non-goals

- Not a substitute for [`singularity/loops/`](../../singularity/loops/README.md) (recurring job YAML SSOT)
- Not a production execution surface
- Not a Record or gate candidate pipeline

## Lifecycle

Promotion path (documentation only — not automated):

```text
research/narrative-systems/  →  stabilization  →  singularity definitions  →  statecraft/  →  loops/
```

## Classification

`research/narrative-systems/`
