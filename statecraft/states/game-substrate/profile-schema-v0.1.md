# Profile Schema v0.1


Faction package schema for **Tier B** game substrate. One file (`*.pkg.yaml`) per civilization-state volume. Prose authority remains in the book; profiles are **extracts with anchors**.

**Reference implementation:** [persia.pkg.yaml](profiles/persia.pkg.yaml)

---

## File shape

```yaml
schema_version: "0.1"
profile_id: string          # kebab-case, unique
volume: I | II | III | IV | V
volume_slug: china | persia | rome | russia | america
display_name: string
tier: B                       # A lore-only | B behavior | C legitimacy core

identity: { ... }
opener: { ... }
behavior: { ... }
patterns: [ ... ]
continuity: { ... }
settlement: { ... }
victory: { ... }
advisors: { ... }
counterweights: [ ... ]
book_anchors: [ ... ]
```

---

## Field definitions

### `identity`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `continuity_mechanism` | enum | yes | See continuity scripts below |
| `governing_pair_default` | enum | yes | `civilization_empire`, `faith_science`, `memory_desire` |
| `civilization_state_claim` | string | yes | One-line category membership |
| `failure_mode` | string | yes | When pattern hardens into pathology |

### `opener`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `deep_grammar_ref` | path | yes | e.g. `volumes/civ-state-persia/sacred-grammar.md` |
| `sovereign_opening` | string | yes | Founding chain label |
| `current_carrier_archetype` | string | yes | Present institution class (not named leader) |
| `parts` | object | yes | Keys: `civilization`, `empire`, `statecraft` → relative paths |

### `behavior`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `stress_bias` | list[string] | yes | Under pressure, AI/player leans here |
| `red_lines` | list[object] | yes | See red_line object |
| `acceptable_losses` | list[string] | yes | Material loss still legible |
| `overreach_signal` | string | yes | When empire outruns civilization |
| `offer_tags_accept` | list[string] | no | Diplomatic tags weighted positive |
| `offer_tags_reject` | list[string] | no | Diplomatic tags hard or soft reject |

**Red line object:**

```yaml
id: string                    # snake_case
label: string
clause_veto: string | null    # settlement clause_id, if any
severity: hard | soft
governing_pair: enum | null   # which pair triggers veto first
advisor_hint: string          # player-facing one line
book_anchor: path
```

### `patterns`

List of pattern bindings:

```yaml
- pattern_id: parity_rival    # matches schemas/*.schema.yaml
  role: primary | secondary | counterweight
  schema_ref: schemas/parity-rival.schema.yaml
  params: { ... }             # pattern-specific
  book_anchor: path
```

### `continuity`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `script_id` | enum | yes | Same as `continuity_mechanism` |
| `rupture_events` | list[object] | yes | capital_loss, humiliation_treaty, etc. |
| `recovery_triggers` | list[string] | yes | Conditions that close rupture arc |

**Rupture event object:**

```yaml
trigger: capital_captured | unequal_peace | parity_rival_war_end | carrier_overthrow
branch: string                # id of recovery branch
effects_hint: string          # for mod implementers
book_anchor: path
```

### `continuity scripts (enum)**

| `script_id` | Volume default | Game meaning |
|-------------|----------------|--------------|
| `reconcentration` | China | Fragmentation → center restoration |
| `endurance_under_parity` | Persia | Survive equal; dignity floor |
| `transformed_carrier` | Rome | Capital loss → successor institution |
| `depth_equilibrium` | Russia | Encirclement endurance; parity refusal |
| `contested_carrier` | America | Credibility / covenant strain |

### `settlement`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `clause_weights` | list[object] | yes | Per-volume weights on shared clause library |
| `hard_vetoes` | list[string] | yes | `clause_id` list |
| `preferred_clauses` | list[string] | no | AI favors when negotiating |

**Clause weight object:**

```yaml
clause_id: string             # from settlement/clauses-v0.1.yaml
weight: -100..100             # negative = distaste, positive = seek
notes: string
```

### `victory`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `preferred_type` | enum | yes | `endurance`, `reconstitution`, `transformed`, `equilibrium`, `domination`, `cultural`, `diplomatic` |
| `asymmetric_optional` | object | no | Scenario-specific win block |

### `advisors`

Map advisor role → book sub-lens path:

```yaml
geo: geo-strategy-<civ>.md
memory: secret-history-<civ>.md
incentives: game-theory-<civ>.md
```

### `counterweights`

Required when any `patterns[].role: primary`:

```yaml
- id: string
  summary: string             # when stereotype breaks down
  book_anchor: path
```

### `book_anchors`

Top-level index of all cited paths for lint.

---

## Tag vocabulary (v0.1)

Shared across profiles and settlement clauses:

| Tag | Meaning |
|-----|---------|
| `humiliation` | Public subordination, unequal symbolic rank |
| `recognition` | Sovereign equality acknowledged |
| `order_restoration` | Anti-chaos center restored |
| `buffer_territory` | Loss acceptable if dignity intact |
| `tributary_status` | Material inferiority without civilizational erasure |
| `religious_autonomy` | Sacred jurisdiction preserved |
| `foreign_garrison` | Occupation of holy/core city |
| `parity_acknowledged` | Equal rival accepts coexistence |
| `credibility_theater` | Symbolic commitment visible to third parties |
| `public_submission` | Explicit vassalage language |

---

## Validation rules

| Rule | Severity | Check |
|------|----------|-------|
| R1 | error | `schema_version` present and supported |
| R2 | error | `volume` matches `volume_slug` map (I=china … V=america) |
| R3 | error | All `book_anchors` paths exist on disk |
| R4 | error | Each primary pattern has ≥1 counterweight entry |
| R5 | error | Every `red_lines[].clause_veto` references valid `clause_id` |
| R6 | error | `hard_vetoes` ⊆ clause library ids |
| R7 | warn | `offer_tags_reject` overlaps `offer_tags_accept` |
| R8 | warn | No `recovery_triggers` for rupture events listed |
| R9 | warn | Pattern `params.parity_rivals` empty when `parity_rival` primary |
| R10 | info | Profile tier B without `settlement.clause_weights` (Tier A only) |

---

## Versioning

- **0.1** — Initial workshop schema; Persia reference pkg; no engine adapters.
- Breaking changes bump minor only after first public substrate export.
