> **ARCHIVED (Grace-Mar corpus).** Fork growth is **not** default strategy-codex routing. **`fork revive` only** — see [grace-mar-instance-boundary.md](../../docs/grace-mar-instance-boundary.md).

﻿# Companion-self Seed Phase v2 â†” Grace-Mar instance tools

## Purpose

Align mental models between the **template** ([companion-self](https://github.com/rbtkhn/companion-self) Seed Phase v2) and **Grace-Mar**â€™s operator-facing [seed-phase-wizard.md](seed-phase-wizard.md) / `scripts/seed-phase-wizard.py`. The template owns **schemas and stages**; the instance owns **live paths** and **operator workflow**.

---

## Boundary

| Surface | Repo | Role |
|---------|------|------|
| Seed Phase v2 JSON artifacts | companion-self `platform/template/seed-phase/`, `demo/seed-phase/` | Pre-activation **formation** package; schemas in `schemas/registry/seed-*.v1.json`. |
| `seed-phase-wizard.py` | grace-mar | Interactive **instance** bootstrap: `archive/queues/reflection-proposals/`, `seed/minimal-core.json`, `self-memory.md` tone â€” **does not** replace template seed JSON set. |

Neither replaces the other: the template defines **portable, validatable** artifacts; Grace-Mar defines **live operator workflow** under canonical instance paths.

---

## Why Grace-Mar has historical â€œseedâ€ language

Grace-Marâ€™s README and session history sometimes describe seeding as **six thematic phases** (identity, personality, academics, creativity, writing voice, core personality) plus a **bifurcation** milestone. That narrative predates the templateâ€™s **numbered 0â€“7** stage list. **Canonical alignment** for new docs and audits uses **Seed Phase v2** stages in [companion-self `docs/seed-phase-stages.md`](https://github.com/rbtkhn/companion-self/blob/main/docs/seed-phase-stages.md). The old six-phase story is **legacy color**, not a second protocol.

---

## Canonical stage mapping

| Stage | Name (template) | Typical artifact(s) |
|-------|-----------------|---------------------|
| **0** | Intake | `seed_intake.json` |
| **1** | Identity Scaffold | `seed_identity.json` |
| **2** | Curiosity Scaffold | `seed_curiosity.json` |
| **3** | Pedagogy Scaffold | `seed_pedagogy.json` |
| **4** | Expression Scaffold | `seed_expression.json` |
| **5** | Memory Contract | `seed_memory_contract.json` |
| **6** | Trial Interactions | `seed_trial_report.json` |
| **7** | Readiness Gate | `seed_readiness.json`, `seed_dossier.md` |

Activation still follows the **sovereign merge** and instance pipeline; this table is **formation**, not post-seed Record edits.

---

## Which files correspond to which stages

Rough correspondence (instance today â€” not a one-to-one file rename):

| Template artifact | Grace-Mar analogue (today) | Notes |
|-------------------|----------------------------|--------|
| `seed_intake.json` | Wizard prompts + `minimal-core.json` fields | Future: optional export to template JSON from wizard. |
| `seed_identity.json` | `SEED-founding-intent.md` + SELF baseline (post-gate) | Template artifact is **pre**-Record; SELF merge is **post**-activation gate. |
| `seed_curiosity.json` | IX-B seeds via pipeline | Same separation: formation vs merged Record. |
| `seed_pedagogy.json` / `seed_expression.json` | Voice/prompt stance (post-merge) + operator reflection | Largely **post-activation** in grace-mar; template front-loads scaffolds. |
| `seed_memory_contract.json` | [memory-template.md](memory-template.md) + policy in AGENTS / operator practice | Instance MEMORY is **non-Record** / rotatable (shortâ€“long horizons); rules align to template. |
| `seed_trial_report.json` | Operator trials + bot conversation (informal) | Template encodes structured trials; instance may adopt JSON when syncing. |
| `seed_readiness.json` / dossier | Operator judgment + RECURSION-GATE | Template encodes **explicit** readiness JSON; instance may adopt when syncing docs. |

---

## What remains instance-specific

- **Paths:** `â€¦`, `archive/queues/reflection-proposals/`, `SEED-PHASE-COMPLETED.json`, validators (`validate-integrity.py`, `governance_checker.py`).
- **Wizard behavior:** Interactive prompts; optional `--require-proposal-class` for CI parity.
- **Historical milestones:** Bifurcation date and six-phase language live in **narrative**; they do not override template stage numbering for **compatibility** work.

---

## Sync recommendation

When merging from companion-self ([MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md)):

1. Pull `docs/seed-phase*.md`, `schemas/registry/seed-*.v1.json`, and validation scripts if instances should reuse them.
2. Do **not** overwrite `` with template seed-phase **demo** data.
3. Optionally add a `seed-phase/` (or repo-local) directory for a **real** run, validated with `validate-seed-phase.py` copied from template.

---

## See also

- [seed-phase-wizard.md](seed-phase-wizard.md) â€” scripts and paths  
- [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md) â€” template sync  

*Living note Â· update when wizard emits template-aligned JSON.*

