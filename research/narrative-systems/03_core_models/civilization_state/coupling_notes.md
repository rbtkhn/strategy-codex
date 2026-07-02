# Coupling Notes

Integration points between Civilization State and sibling research modules.

Related: [README.md](README.md), [metrics.md](metrics.md), [formal_model.md](formal_model.md).

---

# 1. Module Roles

| Module | Layer | Role |
| --- | --- | --- |
| **civilization-state** | Synthetic | Generative dynamics engine — counterfactual trajectories |
| **narrative-systems** | Interpretation | Relational coupling (EG ↔ PH); extends to synthetic inputs |
| **epistemic-geometry** | Structure | Multi-agent belief / claim geometry |
| **predictive-history** | Real-world | Temporal narrative inference from external system |

Civilization State is a **synthetic generative peer** to Predictive History — not a replacement. NST remains the coupling framework; civ-state adds a third input stream.

---

# 2. civilization-state → narrative-systems

Synthetic trajectories S(0), S(1), …, S(T) produce **interpretable narrative inputs**:

- Collapse cascades → phase-transition candidates (compare NST [phase_transition_model.md](../../02_narrative_systems/phase_transition_model.md))
- Power redistribution → structural-temporal coupling in NST mapping space R
- Agent actions → pseudo-agents / pseudo-claims for EG-style alignment tests

**Non-goal:** NST formalism in [formal_model.md](../../02_narrative_systems/formal_model.md) is not rewritten. Civ-state feeds **additional morphisms** into the interpretation layer via coupling notes only.

---

# 3. civilization-state → predictive-history

Uses synthetic runs for:

- **Structural invariant testing** — do PH inference patterns hold on simulated D(t) series?
- **Counterfactual baselines** — "what if alliance had held?" scenario branches
- **Calibration targets** — distribution of conflict_density, stability under known rule sets

**Non-modification constraint:** This module does **not** modify the external [predictive-history](https://github.com/rbtkhn/predictive-history) repo. Same boundary as [predictive-history/README.md](../03_core_models/predictive_history/README.md) — interpretive overlay only.

Canonical PH homes (do not duplicate):

| Surface | Path |
| --- | --- |
| External repo | [rbtkhn/predictive-history](https://github.com/rbtkhn/predictive-history) |
| Inbound mirror | [`public/predictive-history/`](../../../../public/predictive-history/) |
| Research overlay | [`research/narrative-systems/03_core_models/predictive_history/`](../03_core_models/predictive_history/README.md) |

---

# 4. φ — Synthetic → Real Mapping

**φ: D_sim × trajectory → PH narrative state**

Maps simulated observables to comparable PH temporal narrative states H_t.

Scaffold mapping (research — not implemented):

| Sim observable | PH target (conceptual) |
| --- | --- |
| hegemon_share, Gini | Polarity / balance-of-power epoch |
| conflict_density | War vs peace narrative phase |
| stability | Regime stability / crisis labels |
| expansion_velocity | Imperial expansion vs retrenchment |
| collapse events | Systemic transition markers |

φ enables **cross-validation**: if PH infers a transition at t_real, does a calibrated sim show analogous D(t_sim) under matched initial conditions?

φ is **lossy** — sim abstractions do not preserve full narrative richness; NST mediates residual interpretation.

---

# 5. ψ — Real → Simulation Calibration

**ψ: PH inference × evidence → rule parameters**

Tunes civ-state rule engine from real-world inference:

| PH output / evidence | Sim parameter target |
| --- | --- |
| War frequency, duration | R_war_start thresholds, w₀, attrition rates |
| Alliance persistence | R_alliance, R_alliance_break, H_break |
| Tech diffusion rates | R_tech gates, ΔT coefficients |
| Collapse / state failure patterns | R_collapse H_collapse, C_cascade |
| Power concentration history | power() composite weights, growth α, β |

ψ operates as a **feedback loop** (conceptual):

```text
PH inference → ψ → rule params → sim run → D_sim → φ → compare to PH → adjust ψ
```

No runtime wiring in this scaffold.

---

# 6. civilization-state → epistemic-geometry

Optional structural bridge:

- Sim agents cᵢ as **pseudo-agents** in EG object set A
- Trajectory events (wars, collapses) as **event anchors** E
- Claims derived from sim logs as **claims** C for alignment geometry tests

EG remains independent peer per [epistemic-geometry/README.md](../05_geometric_lenses/epistemic_geometry/README.md). Civ-state supplies **synthetic fixtures** for EG formal experiments — not operational EG state.

Operational shadow stack (conceptual only, not promoted from this artifact): [`statecraft/epistemic/`](../../../statecraft/epistemic/README.md).

---

# 7. System Stack (integrated view)

```text
civilization-state (synthetic dynamics)
        ↓  φ, ψ
predictive-history (real-world inference)     narrative-systems (coupling)
        ↘                    ↗
              epistemic-geometry (structure)
```

Data flow:

1. **ψ** calibrates sim from PH
2. Sim produces S(t), D(t)
3. **φ** compares D_sim to PH states
4. NST interprets structural-temporal coupling across EG, PH, and synthetic streams

---

# 8. Future Integration

Intended evolution: loop declarations per [`docs/singularity/loop-system.md`](../../../docs/singularity/loop-system.md) — e.g. periodic sim calibration cadence writing to research shelf only until stabilized.

**Out of scope for this scaffold:** loop YAML, orchestrator code, statecraft/states/ volume changes.

---

# 9. Status

φ and ψ are formal sketches only. No coupling runtime exists.
