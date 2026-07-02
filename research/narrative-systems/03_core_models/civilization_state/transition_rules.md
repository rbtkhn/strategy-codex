# Transition Rules

Declarative rule-engine catalog for T(S(t), A(t)). Not executable code — research scaffold only.

Related: [formal_model.md](formal_model.md), [agents.md](agents.md), [metrics.md](metrics.md).

---

# 1. Rule Engine Overview

Each timestep t:

1. Agents submit actions A(t)
2. Rules fire in **precedence order** (below)
3. Conflicts resolved by priority tier
4. D recomputed from resulting (C, E, R)

---

# 2. Economic Growth Rules

**R_growth:** For each active cᵢ with status = active:

- ΔP ∝ K^α · T^β · H · climate_modifier
- ΔK ∝ extraction(E, regions(cᵢ)) − consumption(P)
- K, P updated with floor at 0

Parameters α, β are calibration targets for ψ ([coupling_notes.md](coupling_notes.md)).

---

# 3. War Initiation

**R_war_start:** Agent action `declare_war(cᵢ, cⱼ)` fires when:

- R has no existing war edge (cᵢ, cⱼ)
- cᵢ.M ≥ M_min (minimum military threshold)
- Utility gain from war > utility cost ([agents.md](agents.md))

Effect:

- Add war edge (cᵢ, cⱼ) with w ← w₀
- Diplomacy label ← hostile

---

# 4. War Resolution

**R_war_resolve:** Each war edge (cᵢ, cⱼ) with intensity w:

- Compute outcome score: f(Mᵢ, Mⱼ, Tᵢ, Tⱼ, fortification, ξ)
- Attrition applied to P, M of both parties proportional to w
- If outcome score > threshold θ: annexation or tribute rules fire
- If w < w_min for N steps: **R_peace** — war edge removed, diplomacy ← neutral or trade

---

# 5. Alliance Formation

**R_alliance:** Agent action `propose_alliance(cᵢ, cⱼ)` when:

- No war edge active between cᵢ, cⱼ
- Mutual utility gain under shared threat or trade opportunity

Effect:

- Add diplomacy label friendly
- Optional mutual defense flag (war against one triggers agent response from ally)

---

# 6. Alliance Dissolution

**R_alliance_break:** Fires when:

- Betrayal action submitted, or
- H of either party drops below H_break, or
- Utility of alliance < utility of defection

Effect: diplomacy ← neutral or hostile; defense flag cleared.

---

# 7. Tech Progression

**R_tech:** For each cᵢ:

- ΔT ∝ K_invest · H · (T_max − T) / T_max
- Tech gates unlock rule variants (e.g. higher M cap, trade τ multiplier)

Gates are tier thresholds T₁, T₂, … (scaffold — values TBD).

---

# 8. Collapse Conditions

**R_collapse:** For each cᵢ, if any trigger fires:

| Trigger | Condition |
| --- | --- |
| Cohesion failure | H < H_collapse |
| Resource exhaustion | K = 0 for N consecutive steps |
| Military annihilation | M = 0 and under attack |
| Cascade | neighbor collapse count ≥ C_cascade in R |

Effect: cᵢ.status ← collapsed; merge/split/absorption sub-rules apply ([state_model.md](state_model.md)).

Phase transition link: collapse cascades may push D.stability below λ_c ([formal_model.md](formal_model.md)).

---

# 9. Rule Precedence

When multiple rules conflict at t, apply in order:

1. **Collapse** — R_collapse
2. **War resolution** — R_war_resolve
3. **War initiation** — R_war_start (after resolution clears stale wars)
4. **Alliance** — R_alliance, R_alliance_break
5. **Tech** — R_tech
6. **Growth** — R_growth

Within same tier: higher utility-weighted action wins (agent tie-break).

---

# 10. Status

Precedence and thresholds are scaffold placeholders. No runtime rule engine exists.
