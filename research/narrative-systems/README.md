# Narrative Systems Research

Category-theoretic **meta-framework research** for modeling how narratives, cognition, and geopolitical interpretation relate — WIP formal research under the singularity channel (not loop SSOT, not system invariants).

Narrative Systems studies how multiple discourse models relate (Epistemic Geometry, Predictive History, civilization-state, …). It is **not** subject research about any one corpus. Predictive History subject research lives at [`../predictive-history/`](../predictive-history/).

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
| Core models | [03_core_models/](03_core_models/) | In-repo formal models used as study subjects (e.g. civilization-state) |
| Mappings | [04_mappings/](04_mappings/) | Inter-model translation |
| Geometric lenses | [05_geometric_lenses/](05_geometric_lenses/) | Epistemic geometry — fundamental NST structural component |
| Dynamics | [06_dynamics/](06_dynamics/) | Temporal evolution |
| Applications | [07_applications/](07_applications/) | Real-world modeling |
| Comparisons | [08_comparisons/](08_comparisons/) | Structured model contrast |
| Open problems | [09_open_problems/](09_open_problems/) | Unresolved research |

## Artifacts

| Artifact | Path | Role |
| --- | --- | --- |
| Epistemic Geometry | [05_geometric_lenses/epistemic_geometry/](05_geometric_lenses/epistemic_geometry/README.md) | Multi-agent narrative alignment — **fundamental part of NST** (stays nested) |
| Predictive History | [`../predictive-history/`](../predictive-history/README.md) | **External subject** — NST studies PH; subject research is not nested here |
| Narrative Systems (NST) | [02_narrative_systems/](02_narrative_systems/) | Relational mapping between EG (structure) and PH (time) — not a container |
| Civilization State | [03_core_models/civilization_state/](03_core_models/civilization_state/README.md) | Synthetic geopolitical dynamics — in-repo study subject |
| Model relations | [04_mappings/model_relations/](04_mappings/model_relations/README.md) | Parallel functors H → 𝔈 (P vs C) — open Rel(P,C) |

EG is a structural component of this meta-framework. PH is an **external subject** studied via links to [`../predictive-history/`](../predictive-history/). Civilization State is a **synthetic in-repo peer**; NST and [coupling_notes.md](03_core_models/civilization_state/coupling_notes.md) define bridges.

## Core idea (NST)

NST: (EG, PH) → R — relational coupling between epistemic structure and temporal narrative evolution.

Formal specification: [02_narrative_systems/formal_model.md](02_narrative_systems/formal_model.md).

## Non-goals

- Not a substitute for [`singularity/loops/`](../../singularity/loops/README.md) (recurring job YAML SSOT)
- Not a production execution surface
- Not a Record or gate candidate pipeline
- Not a home for Predictive History subject research (see [`../predictive-history/`](../predictive-history/))

## Lifecycle

Promotion path (documentation only — not automated):

```text
research/narrative-systems/  →  stabilization  →  singularity definitions  →  statecraft/  →  loops/
```

## Classification

`research/narrative-systems/`
