# Civilization State
## Formal Model Specification

---

# 1. Overview

Civilization State formalizes geopolitical and historical dynamics as a **discrete-time state machine** over a multi-agent civilization system.

This is a **proto-formal / WIP** specification. Definitions may evolve; no runtime enforcement exists.

Related: [state_model.md](state_model.md) (state vector structure), [transition_rules.md](transition_rules.md) (rule engine), [agents.md](agents.md) (action vector A(t)).

---

# 2. Global State

At discrete timestep t, the system state is:

**S(t) = (C, E, R, D)**

Where:

| Component | Meaning |
| --- | --- |
| **C** | Set of civilizations {c₁, c₂, …, cₙ} |
| **E** | Environment — resources, climate proxy, geography abstraction |
| **R** | Relational graph over C — diplomacy, war, trade edges |
| **D** | Derived metrics — power, entropy, stability (global observables) |

Each civilization cᵢ ∈ C carries a local state vector (see [state_model.md](state_model.md)).

---

# 3. Transition Function

System evolution is defined by:

**S(t+1) = T(S(t), A(t))**

Where:

- **T** — deterministic transition operator (rule engine)
- **A(t)** — joint action vector from all active agents at t

A(t) = (a₁(t), a₂(t), …, aₙ(t)) where aᵢ(t) is the action chosen by civilization cᵢ.

Agent decision model: [agents.md](agents.md).

Rule catalog: [transition_rules.md](transition_rules.md).

---

# 4. Stochastic Extension

For Monte Carlo and ensemble simulation, define:

**S(t+1) = T_σ(S(t), A(t), ξ(t))**

Where:

- **T_σ** — stochastic transition operator
- **ξ(t)** — noise term drawn from distribution Ξ (event shocks, resource variance, diplomatic uncertainty)

Properties (scaffold):

- ξ(t) independent across t (Markov noise)
- T_σ → T as Var(ξ) → 0 (deterministic limit)

---

# 5. Phase Transitions

Sudden systemic shifts (collapse cascades, rapid hegemonic transition, alliance realignment) are modeled as **phase transitions** in D:

- Stable regime: D components within nominal bounds
- Critical threshold: one or more D metrics cross λ_c
- Transition: T applies collapse / reorganization rules (see [transition_rules.md](transition_rules.md))

Conceptual link to Narrative Systems phase model: [phase_transition_model.md](../../02_narrative_systems/phase_transition_model.md) (curvature K, critical threshold λ_c). Civ-state phase transitions operate on **simulated power/entropy/stability**; NST phase transitions operate on **narrative alignment curvature**. Coupling between the two is defined in [coupling_notes.md](coupling_notes.md).

---

# 6. Observables

Global metrics D are computed from (C, E, R) at each t. Full catalog: [metrics.md](metrics.md).

D(t) feeds:

- **φ** — synthetic → real mapping (coupling to Predictive History)
- Internal stability and collapse triggers

---

# 7. Invariants (scaffold)

Proto-invariants under revision:

1. **Conservation of identity** — civilization IDs persist unless merge/split rules fire
2. **Graph consistency** — R edges reference valid cᵢ ∈ C
3. **Metric derivability** — D is a function of (C, E, R), not independent state
4. **Action boundedness** — A(t) actions are drawn from per-agent feasible sets

---

# 8. Status

Research scaffold only. Not bound to runtime loops or statecraft operationalization.
