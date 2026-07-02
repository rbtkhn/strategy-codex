# Agents

Defines civilizations as bounded-rational agents, decision heuristics, and the joint action vector A(t).

Related: [formal_model.md](formal_model.md), [transition_rules.md](transition_rules.md).

---

# 1. Agent Model

Each active civilization cᵢ ∈ C is a **bounded-rational agent**:

- Observes local state cᵢ(t), neighborhood in R, and aggregate D (partial observability optional)
- Selects one action aᵢ(t) from feasible set **F(cᵢ, S(t))**
- Does not global-optimize — uses heuristics and utility proxies

---

# 2. Action Space

Per-agent action types (scaffold):

| Action | Parameters | Rule hook |
| --- | --- | --- |
| `grow` | investment split (P vs K vs T) | R_growth, R_tech |
| `declare_war` | target cⱼ | R_war_start |
| `propose_alliance` | target cⱼ | R_alliance |
| `betray` | target ally cⱼ | R_alliance_break |
| `fortify` | region rⱼ | war resolution modifier |
| `expand` | target region (neutral/contested) | conquest sub-rule |
| `stabilize` | internal focus | ΔH boost, reduced ΔP |

**A(t) = (a₁(t), …, aₙ(t))** — one action per active agent per timestep.

---

# 3. Utility Proxies

Agent cᵢ evaluates actions via:

**Uᵢ(a) = w_s · survival(a) + w_e · expansion(a) + w_t · stability(a)**

| Component | Proxy (scaffold) |
| --- | --- |
| **survival(a)** | P(cᵢ) + M(cᵢ) − threat_penalty(R, neighbors) |
| **expansion(a)** | expected Δ territory, ΔK from conquest/trade |
| **stability(a)** | H(cᵢ) − war_cost − collapse_risk |

Weights w_s, w_e, w_t vary by agent **personality profile** (scaffold enum: survivalist, expansionist, balancer).

Default heuristic: **survival-first** — if H < H_warn or M < M_min, w_s dominates.

---

# 4. Decision Heuristics

Bounded-rational selection (not full game-theoretic equilibrium):

1. **Threat scan** — if neighbor war edge or hostile diplomacy with M_neighbor > Mᵢ, bias toward fortify / alliance
2. **Opportunity scan** — if weak neighbor and U(declare_war) > θ_war, bias toward war
3. **Growth default** — if no threat/opportunity, `grow` with split favoring weakest dimension (low K → invest K)
4. **Stabilize override** — if H < H_warn, `stabilize` regardless of expansion utility

Stochastic extension: softmax over Uᵢ(a) with temperature τ for ensemble diversity under T_σ.

---

# 5. Interaction Model

### Bilateral

Actions `declare_war`, `propose_alliance`, `betray` require target cⱼ. Target may not accept alliance (accept/reject sub-action on cⱼ's turn — turn order scaffold TBD).

### Multilateral

- Trade benefits scale with friendly edges in R
- Cascade collapse: agents observe D.stability and neighbor status; may preemptively stabilize or exploit

### Feasible set F

Action a forbidden if:

- Insufficient K or M for action cost
- cᵢ.status ≠ active
- Target invalid (absorbed civ, self)
- Rule precedence blocks action (e.g. war while collapsing)

---

# 6. Link to Formal Model

**S(t+1) = T(S(t), A(t))** — T consumes joint actions and applies [transition_rules.md](transition_rules.md) in precedence order.

Agent policies are **not** part of S(t); they are exogenous generators of A(t) unless policy learning is added in future work.

---

# 7. Status

Heuristic weights and personality profiles are research placeholders. No agent runtime exists.
