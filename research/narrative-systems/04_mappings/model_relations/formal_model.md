# Model Relations — Formal Model

Proto-formal / WIP. Related: [README.md](README.md), [historiography.md](historiography.md).

---

# 1. Overview

Model Relations defines **P** and **C** as parallel candidate functors from **History** into **Epistemic Geometry**, and **Rel(P,C)** as an open object in relation space **ℛ**.

Narrative Systems (**N**) subsumes this sub-layer; see [narrative_interface.md](narrative_interface.md).

---

# 2. History (H)

**H** denotes History as source domain.

**Status:** informal and **plural** — events, processes, civilizational arcs, and narrative readings may coexist as valid historiographical lenses. H is **not fully axiomatized** in this scaffold.

Multiple readings of H are first-class; the formalism does not collapse them prematurely.

---

# 3. Codomain: Epistemic Geometry (𝔈)

**𝔈 = EG** — concretely [Epistemic Geometry](../../05_geometric_lenses/epistemic_geometry/README.md) structure space.

Legacy notation in NST [formal_model.md](../../02_narrative_systems/formal_model.md): **𝓔𝓰** denotes the same epistemic structure category where context aligns.

---

# 4. Candidate functors

## 4.1 P : H → 𝔈

**P** — [predictive-history](../../../predictive-history/README.md) as candidate functor.

- Anchored to a **completed, delivered lecture series** (Geo-Strategy classroom corpus; external [rbtkhn/predictive-history](https://github.com/rbtkhn/predictive-history))
- strategy-codex holds a **mixed overlay** — describes P's functor role without forcing one historiographical school
- Non-modifying constraint on external PH repo preserved

## 4.2 C : H → 𝔈

**C** — [civilization-state](../../03_core_models/civilization_state/README.md) as candidate functor.

- **Structural formalism** — civilizational configuration and change (S(t), T, A(t), D)
- **Work in progress** — formal docs evolving; not a delivered lecture series
- Delivers **structured descriptions**, not historical claims or predictions

**C is not:** simulation, hypothesis engine, prediction factory, synthetic history product.

---

# 5. Non-commitments on P and C

No axiom is asserted for:

- equivalence of P and C
- incompatibility of P and C
- hierarchy (P above C or vice versa)
- redundancy (one subsumes the other)

---

# 6. Relation object

**Rel(P, C) ∈ ℛ**

Where **ℛ** is relation hypothesis space (see [relationship_space.md](relationship_space.md)).

Rel is **open-ended** — not fixed to a morphism, equivalence, or conflict type. Default stance: **unknown structure**.

Hypothesis regions (agreement, divergence, partial overlap) apply to **Rel(P,C)**, not to outputs of C (C does not emit hypotheses).

---

# 7. Embedding scaffold

P and C share codomain **𝔈** but may use **different charts/embeddings** of H:

- Images im(P), im(C) ⊆ 𝔈 may overlap, diverge, or sit in incomparable regions
- Structure-preserving properties of P and C are **not assumed**
- Whether P and C land on comparable points in 𝔈 is an open question — see [open_questions.md](open_questions.md)

---

# 8. Material asymmetry (not epistemic rank)

| Fact | Consequence for analysis |
| --- | --- |
| P corpus **closed** (lectures delivered) | Stable citation, registry, Part II adjudication residue |
| C formalism **WIP** | Evolving definitions; Rel claims require version discipline |

Completion vs WIP affects **evidence stability** — it does **not** default Rel(P,C) toward agreement with P.

---

# 9. Status

Research scaffold only. No runtime enforcement.
