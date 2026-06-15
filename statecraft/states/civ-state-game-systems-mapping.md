# CIV-STATE → Game Systems Mapping

WORK only; not Record.

One-page bridge for strategy-game developers: how public **Civilizational Statecraft** (`rbtkhn/civ-state`) maps to executable gameplay systems without treating the repo as a history encyclopedia.

**Canonical book:** five volumes (China → Persia → Rome → Russia → America), each `civilization → empire → statecraft`, with appendix retrieval apparatus. **Governing movement:** `memory → legitimacy → carrier → pressure → settlement`.

---

## Core thesis for games

Civ-state answers **why factions behave differently under the same map pressure**—continuity, legitimacy, overreach, humiliation, settlement legibility—not **what year a tech unlocks**. Import **mechanism templates**, not prose volumes.

| Civ-state layer | Game system role | Primary repo doors |
|-----------------|------------------|-------------------|
| Five volumes | Asymmetric faction packages (different rupture/recovery laws) | [Table of Contents](table-of-contents.md), [Volume map](volumes/README.md) |
| Part law (`civilization / empire / statecraft`) | Three-layer faction anatomy (legitimacy / reach / live diplomacy) | `volumes/civ-state-*/civilization-*.md`, `empire-*.md`, `statecraft-*.md` |
| Opener block (deep grammar · sovereign opening · current carrier) | Faction bootstrap: ideology · founding myth · government type | Volume `README.md`, [Sacred Grammar](sacred-grammar/README.md) |
| Framework pairs (civ/empire · faith/science · memory/desire) | AI misperception + offer rejection (wrong grammar = plausible non-deal) | [Framework](civilization-empire-faith-science-memory-desire.md) |
| Pattern library | Reusable AI state machines and victory scripts | [Pattern library](pattern-library/README.md) |
| Continuity mechanism | Defeat / collapse / recovery arcs (same loss, different futures) | [Continuity mechanism](continuity-mechanism.md) |
| Sub-lenses (geo · secret-history · game-theory) | Advisor / intel specialties narrowing pressure geometry | `geo-strategy-*.md`, `secret-history-*.md`, `game-theory-*.md` |
| Source-lattice | Cultural intel fog-of-war (primary before synthesis) | [Volume map — source-lattice](volumes/README.md#source-lattice-inside-every-volume) |
| Object contract (arc · counterweight · transaction hooks) | Treaty clause weights, failure modes, settlement DSL | [CIV-STATE README — Object Contract](README.md#object-contract) |

---

## Volume → default gameplay signature

| Vol | Civ | Continuity style | AI stress behavior | Distinct win / peace logic |
|-----|-----|------------------|--------------------|----------------------------|
| I | China | Reconcentration after fracture | Anti-chaos; reunification pressure | Order restored > maximal territory |
| II | Persia | Endurance under parity | Parity-rival fixation; dignity red lines | Survival + recognition without humiliation |
| III | Rome | Transformed carriers | Carrier mutation on collapse | Institutional spread / successor paths |
| IV | Russia | Depth + parity refusal | Encirclement memory; sacral endurance | Equilibrium; anti-managed humiliation |
| V | America | Contested late chain | Credibility theater; covenant strain | Legitimacy-bearing restraint or overreach snap |

Use as **defaults**, not stereotypes—counterweights in each volume exist to prevent flat national caricature.

---

## Pattern cards → mechanics (fast import)

| Pattern | Mechanic hook | Design test |
|---------|---------------|-------------|
| Parity rival | One neighbor locked as structural equal; annexation fantasy penalized | Does AI prefer endurance to map paint? |
| Transformed continuity | Defeat spawns successor institution, not game-over | Can faction “die” yet remain playable? |
| Bureaucratic restoration | Post-fracture events favor center reconstitution | Is fragmentation temporary by design? |
| Sacred reconcentration | Legitimacy spike when ritual order restored after loss | Are holy/legal restores separate from conquest? |
| Fractured sovereignty | Multiple claimants; occupation ≠ recognition | Do provinces have sovereign allegiance layers? |
| Corridor civilization | Routes/chokes dominate state formation | Is geography grammar, not just movement cost? |
| Survivable sovereignty | Minimum dignity preserved under pressure | Are there acceptable losses? |

---

## Three integration tiers

| Tier | What you ship | Fidelity | Start here |
|------|---------------|----------|------------|
| **A — Lore bible** | Events, advisor lines, scenario briefs grounded in volume parts | Low–medium | One volume + one pattern card |
| **B — Behavior profiles** | JSON/YAML: governing pair, continuity type, red-line clauses, recovery script | Medium | [Continuity mechanism](continuity-mechanism.md) + framework pairs |
| **C — Legitimacy core** | Separate meters for civilization / empire / carrier; settlement DSL; asymmetric victories | High | Full part law + pattern library + sub-lenses |

**Rule:** balance-critical paths (combat, economy) stay hard-coded; LLM/RAG only for dialogue and intel gloss.

---

## Minimal schema sketch (Tier B)

See **[Profile schema v0.1](game-substrate/profile-schema-v0.1.md)** and reference **[Persia.pkg.yaml](game-substrate/profiles/persia.pkg.yaml)**.

```yaml
faction_id: persia
volume: II
continuity_mechanism: endurance_under_parity
governing_pair_default: memory_desire
deep_grammar: sacred_grammar/persia.md
parity_rivals: [rome]
red_lines: [public_submission, sacred_humiliation]
acceptable_losses: [buffer_territory, tributary_status]
recovery_triggers: [dignity_restored, parity_acknowledged]
overreach_signal: empire_share_above_civilization_share
patterns: [parity_rival, survivable_sovereignty]
advisors: { geo: geo-strategy-persia, memory: secret-history-persia, incentives: game-theory-persia }
```

---

## Substrate evolution (high level)

Civ-state should evolve as **one human book + one machine companion**—same doctrine, different surfaces. Workshop home: [`game-substrate/`](game-substrate/README.md).

| Phase | Outcome | Status |
|-------|---------|--------|
| **0** | Mapping doc + manual examples | done |
| **1** | Profile schema v0.1 + Persia.pkg + parity-rival schema + clause library | **v0.1 workshop** |
| **2** | Continuity scripts + full pattern schemas | next |
| **3** | Engine adapter (Unciv or Freeciv) + validator script | planned |
| **4** | Playtest falsifiers → review queue | ongoing |
| **5** | Optional public substrate export | when stable |

**Target tree:**

```text
game-substrate/
├── profile-schema-v0.1.md
├── schemas/              # pattern state machines
├── profiles/             # *.pkg.yaml per volume
├── settlement/           # shared clause library
└── adapters/             # engine bindings (future)
```

**Guardrails:** do not flatten five volumes into generic traits; keep counterweights mandatory; book prose stays authoritative; machine layer references `book_anchors`; game adapters do not silently rewrite doctrine.

**Engine note:** Unciv for fastest JSON mod prototype; [Freeciv-web](https://github.com/freeciv/freeciv-web) for browser/PBEM distribution—neutral YAML core first, adapters second.

---

## Realism traps this avoids

- Flat “culture trait +10” factions  
- Religion as cosmetic modifier only  
- Defeat = delete faction  
- Economically optimal peace always accepted  
- One domination victory for all civs  

---

## Adoption path (one sprint)

1. Pick **one volume** + **one pattern** + **continuity mechanism** row.  
2. Implement **governing-pair tags** on diplomatic offers (framework).  
3. Add **one asymmetric recovery script** on capital loss (continuity mechanism).  
4. Playtest **non-transactions** (deals that look rational but fail legitimacy).  
5. Expand to second volume only after asymmetry reads true in play.

---

## Boundary

Public canonical text: **`rbtkhn/civ-state`**. Workshop drafts: `statecraft/states/`. Export via `scripts/export_civilizational_statecraft_public.py`. This note is an adjacent operator bridge—not part of the public book unless exported.

**Related:** [External boundary](../../docs/civilizational-statecraft-external-boundary.md) · [CIV-STATE README](README.md)
