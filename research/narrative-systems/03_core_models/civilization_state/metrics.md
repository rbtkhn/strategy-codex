# Metrics

Global observables D computed from S(t) = (C, E, R, D) at each timestep.

Related: [formal_model.md](formal_model.md), [coupling_notes.md](coupling_notes.md) (φ / ψ feeds).

---

# 1. Derived Metrics Vector

**D(t) = (power_dist, entropy, stability, conflict_density, expansion_velocity)**

Each component is a scalar or structured summary over C and R.

---

# 2. Power Distribution

**power(cᵢ) = f(Pᵢ, Kᵢ, Tᵢ, Mᵢ)** — weighted composite (weights scaffold)

**power_dist** metrics:

- **Gini(power)** — inequality across active civilizations
- **hegemon_share** — max(power) / sum(power)
- **effective_count** — 1 / sum((powerᵢ / sum(power))²) (Herfindahl-style inverse)

High hegemon_share → unipolar sim; low Gini → multipolar balance.

**φ feed:** power_dist snapshots align to PH narrative polarity epochs ([coupling_notes.md](coupling_notes.md)).

---

# 3. System Entropy

**entropy** — Shannon entropy over normalized power shares:

H_sys = −Σ pᵢ log(pᵢ), where pᵢ = power(cᵢ) / Σ power

Interpretation:

- High H_sys — diffuse power, many actors
- Low H_sys — concentration, potential brittleness or hegemonic stability

**ψ feed:** real-world polarity estimates may calibrate target H_sys bands.

---

# 4. Stability Index

**stability** ∈ [0, 1] — composite of:

- mean(H) across active civilizations (internal cohesion)
- 1 − normalized conflict_density
- 1 − collapse_rate (fraction collapsed in last W steps)

**stability < λ_c** triggers phase-transition labeling (link [formal_model.md](formal_model.md), NST [phase_transition_model.md](../../02_narrative_systems/phase_transition_model.md)).

---

# 5. Conflict Density

**conflict_density** = (count of war edges × mean(w)) / max_possible_edges

Sub-metrics:

- **active_wars** — |{ (cᵢ,cⱼ) : war ∈ R }|
- **mean_intensity** — average w on war edges

**φ feed:** conflict_density trajectories map to PH war/peace narrative phases.

---

# 6. Expansion Velocity

**expansion_velocity** — rate of territorial/control change:

- Δ controlled regions per timestep (net across C)
- Or: sum of |ΔP| weighted by conquest flags

High expansion_velocity — imperial phase; near zero — equilibrium or stagnation.

---

# 7. Metric Computation Order

After T applies at t:

1. Update C, E, R from rules
2. Compute per-civ power(cᵢ)
3. Aggregate D(t)
4. Expose D(t) to agents (partial) and coupling layer (full)

D is **derived** — not independent state ([formal_model.md](formal_model.md) invariant 3).

---

# 8. Coupling Summary

| Metric | φ (synthetic → real) | ψ (real → sim calibration) |
| --- | --- | --- |
| power_dist / Gini | Map to PH polarity structure | Tune power composite weights |
| entropy | Compare to narrative dispersion | Target entropy bands from inference |
| stability | Align to PH regime labels | Set λ_c, H thresholds |
| conflict_density | War/peace phase alignment | Calibrate war initiation θ |
| expansion_velocity | Imperial/expansion narrative epochs | Growth rule α, β |

Full mapping spec: [coupling_notes.md](coupling_notes.md).

---

# 9. Status

Formulas and weights are scaffold placeholders. No metric computation runtime exists.
