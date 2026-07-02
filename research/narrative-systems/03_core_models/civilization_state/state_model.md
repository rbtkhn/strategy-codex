# State Model

Defines the structure of civilization state vectors, spatial hierarchy, and persistence rules.

Related: [formal_model.md](formal_model.md) (S(t) = (C, E, R, D)).

---

# 1. Civilization State Vector

Each civilization cᵢ ∈ C at timestep t carries:

**cᵢ(t) = (id, P, K, T, H, M, status)**

| Field | Type | Meaning |
| --- | --- | --- |
| **id** | identifier | Persistent civilization key |
| **P** | scalar ≥ 0 | Population (abstract units) |
| **K** | scalar ≥ 0 | Resource stock (aggregate) |
| **T** | scalar ∈ [0, T_max] | Technology level |
| **H** | scalar ∈ [0, 1] | cohesion / internal stability |
| **M** | scalar ≥ 0 | military capacity |
| **status** | enum | {active, declining, collapsed, absorbed} |

All scalars are **placeholders** — calibration via ψ mapping ([coupling_notes.md](coupling_notes.md)) is future work.

---

# 2. Spatial Hierarchy

Three-level nesting:

```text
civilization (cᵢ)
    └── region (rⱼ)
            └── city (kₗ)
```

### Civilization level

- Owns aggregate P, K, T, H, M (sum or weighted rollup from regions)
- Primary agent decision unit ([agents.md](agents.md))

### Region level

**rⱼ(t) = (id, parent_civ, P_r, K_r, terrain)**

- Terrain modifier affects growth and conflict rules
- May be contested (multiple civ claims) — edge case for transition rules

### City level

**kₗ(t) = (id, parent_region, P_k, K_k, fortification)**

- Smallest persistent spatial unit
- Fortification affects local defense in war resolution

Resource abstractions at city level roll up to region, then civilization.

---

# 3. Environment State

**E(t) = (G, climate, resource_field)**

| Field | Meaning |
| --- | --- |
| **G** | Geography graph — adjacency between regions/cities |
| **climate** | Scalar or vector proxy (growth modifier, collapse stress) |
| **resource_field** | Spatial distribution of extractable resources |

E evolves slowly relative to C (optional E sub-step in T).

---

# 4. Relational Graph

**R(t)** is a labeled multigraph over C:

Edge types:

- **diplomacy** — neutral, friendly, hostile
- **war** — active conflict with intensity w ∈ [0, 1]
- **trade** — flow capacity τ ≥ 0

Edge (cᵢ, cⱼ) may carry multiple labels simultaneously (e.g. trade + hostile).

---

# 5. Persistence Rules

### What survives a timestep

- **id** — unchanged unless merge/split
- **Hierarchy** — city → region → civ links preserved unless conquest/collapse
- **R edges** — persist unless explicitly dissolved by rules

### Merge

When civilization cⱼ is absorbed into cᵢ:

1. cⱼ.status ← absorbed
2. P, K, M of cⱼ added to cᵢ (with attrition factor)
3. R edges of cⱼ reassigned to cᵢ
4. cⱼ removed from active agent set

### Split

When cᵢ fragments into cᵢa, cᵢb:

1. New ids assigned
2. P, K, M partitioned by rule (cohesion-weighted or random under T_σ)
3. R edges split proportionally or by region ownership

### Collapse

When cᵢ.status ← collapsed:

1. cᵢ removed from active C
2. Regions/cities may become ungoverned or be annexed by neighbors
3. R edges involving cᵢ dissolved or transferred

### Serialization invariants

1. Every city references exactly one region; every region references exactly one active civilization (or ungoverned marker)
2. No orphaned edges in R
3. D recomputed from (C, E, R) after every merge/split/collapse

---

# 6. Status

Research scaffold. Field definitions and rollup formulas are not yet stabilized.
