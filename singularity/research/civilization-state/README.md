# Civilization State (Synthetic Dynamics)

work only; not Record.

## Status

Research scaffold — not wired to [`singularity/loops/`](../../loops/README.md) or runtime execution.

## Classification

`singularity/research/civilization-state/`

## Purpose

Civilization State formalizes **civ-state** as a discrete civilization dynamics system: civilizations as state machines evolving under rule-based constraints. It complements [Predictive History](../predictive-history/README.md) (real-world inference) and integrates with [Narrative Systems](../narrative-systems/README.md) (interpretation layer).

## Motivation

The system currently separates:

- **real-world event inference** — [Predictive History](../predictive-history/README.md)
- **narrative interpretation** — [Narrative Systems](../narrative-systems/README.md)

This module adds a missing layer: a **generative civilization dynamics model** for counterfactual and synthetic history production.

## Use cases

- Synthetic history generation
- Geopolitical simulation
- Counterfactual scenario modeling
- Calibration of predictive-history models
- Testing structural invariants across simulated vs real systems

## Stack position

Civilization State is a **synthetic generative peer** to Predictive History. Narrative Systems remains the relational coupling layer between [Epistemic Geometry](../epistemic-geometry/README.md) (structure) and Predictive History (time); civ-state adds a third input stream (synthetic trajectories) for calibration and counterfactuals.

```text
civilization-state (synthetic dynamics engine)
        ↓
narrative-systems (interpretation layer)
        ↓
epistemic-geometry (belief structure)
        ↓
predictive-history (real-world inference)
```

Cross-module coupling: [coupling_notes.md](coupling_notes.md) (φ / ψ mappings).

## Disambiguation

| Surface | Path | Role |
| --- | --- | --- |
| Operational civ-state memory | [`statecraft/states/`](../../../statecraft/states/README.md) | Five-volume civilizational source memory for drafting |
| Public book | [`public/civ-state/`](../../../public/civ-state/) | Ship-bound Civilizational Statecraft prose |
| **This module** | `singularity/research/civilization-state/` | **Synthetic** discrete dynamics / simulation formalism |

Use **civilization-state** as the folder name; **civ-state** as shorthand in prose only when this disambiguation block is visible.

## Research files

| File | Role |
| --- | --- |
| [formal_model.md](formal_model.md) | Core formalism: S(t), T, stochastic extension |
| [state_model.md](state_model.md) | Civilization state vector, hierarchy, persistence |
| [transition_rules.md](transition_rules.md) | Rule engine: growth, war, alliance, collapse |
| [agents.md](agents.md) | Bounded-rational agents, heuristics, utility |
| [metrics.md](metrics.md) | Global observables over S(t) |
| [coupling_notes.md](coupling_notes.md) | Integration with NST, PH, EG; φ and ψ mappings |

## Non-goals

- Not loop SSOT or production execution surface
- Not a substitute for [`statecraft/states/`](../../../statecraft/states/README.md) civilizational source memory
- Not a Record or gate candidate pipeline
- Not modifying the external [predictive-history](https://github.com/rbtkhn/predictive-history) repo

## Future evolution

Intended integration into the loop system per [`docs/singularity/loop-system.md`](../../../docs/singularity/loop-system.md). No orchestrator code in this scaffold.
