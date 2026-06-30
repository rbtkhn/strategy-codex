---
audience: operator
authority: doctrine
record_status: frozen
---

# AGENTS.md — AI Coding Assistant Guardrails

This file is the **always-on contract** for coding assistants in **strategy-codex**. Extended fork, gate, MEMORY, and permission detail: [`docs/agent-rules/deep-rules.md`](docs/agent-rules/deep-rules.md).

## Identity and default lane

**Active repo:** `strategy-codex` — a **governed interpretive machine** ([`docs/product-identity.md`](docs/product-identity.md)): source archive → synthesis → notes → essays. **Not** default fork growth.

Grace-Mar is archived/frozen. Active strategy-codex work does not grow the fork. See [docs/archive/grace-mar.md](docs/archive/grace-mar.md).

**Default operator channel:** [`statecraft/`](statecraft/README.md) unless the operator names **singularity**, **work-dev**, or another territory. Two primary channels: [`docs/operator-two-channel-architecture.md`](docs/operator-two-channel-architecture.md).

**Do not** route live work through `companion-self` template sync or fork-vs-template reconciliation unless the operator explicitly invokes **`fork revive`** / archive lane.

## System design (read order)

| Topic | Doc |
|---|---|
| Active architecture | [`docs/architecture.md`](docs/architecture.md) |
| Harness / membrane / channels | [`docs/harness-architecture-map.md`](docs/harness-architecture-map.md) |
| Routing / discovery | [`LLM-ROUTING.md`](LLM-ROUTING.md) · [`repo-map.yaml`](repo-map.yaml) |
| Layer stack | [`docs/layer-architecture.md`](docs/layer-architecture.md) · [`instance-doctrine.md`](instance-doctrine.md) |
| Skills modularity | [`docs/skills-modularity.md`](docs/skills-modularity.md) |
| PH public boundary | [`docs/predictive-history-external-boundary.md`](docs/predictive-history-external-boundary.md) |

## Authority categories (four-way)

| Category | Meaning | Examples |
|---|---|---|
| **source** | Primary or canonical source material | `source-archive/statecraft/` captures |
| **work** | Active operator-authored surfaces | `statecraft/`, `singularity/`, `essays/`, voice indexes |
| **generated** | Rebuildable derived outputs | `runtime/artifacts/`, generated indexes |
| **archive** | Frozen historical / compatibility | `archive/grace-mar-instance/`, `docs/archive/` |

See [`docs/complexity-budget.md`](docs/complexity-budget.md) · [`docs/routing-reference.md`](docs/routing-reference.md).

## Operator model

**Mind** (operator) + **work execution layer** (assistant, scripts, `statecraft/`, `singularity/`). Assistants **route** WORK; they do **not** merge Record identity without human gate.

**Allowed without approval:** read surfaces, statecraft/singularity routing, archive→synthesis promotion, integrity/git/boundary stewardship. **Fork revive only:** stage gate candidates — never auto-merge.

Full permission table: [`docs/agent-rules/deep-rules.md`](docs/agent-rules/deep-rules.md#permission-boundaries).

## Do not edit directly

| Surface | Rule |
|---|---|
| Generated outputs | Regenerate via documented scripts; do not hand-edit drift-prone indexes |
| `archive/grace-mar-instance/` Record | No direct edits unless **`fork revive`**; merge via `process_approved_candidates.py --apply` only |
| `public/predictive-history/` | Inbound read-only — edit canonical `rbtkhn/predictive-history`; refresh via `sync_predictive_history_mirror.py` |

**Record merge invariant:** do not edit `archive/grace-mar-instance/self.md`, `self-archive.md`, `recursion-gate.md`, or `bot/prompt.py` by hand — merge through the gated pipeline after approval.

## Repository search (agents)

1. [`LLM-ROUTING.md`](LLM-ROUTING.md) → [`repo-map.yaml`](repo-map.yaml)
2. Calendar **day-index:** `source-archive/statecraft/YYYY-MM-DD/day-index.md` only
3. Analyst corpus: `statecraft/voices/**/**-source-index.md` · **voice index registry:** [`runtime/artifacts/voice-index-parity.md`](runtime/artifacts/voice-index-parity.md) ([`voice-index-registry.md`](statecraft/voices/voice-index-registry.md))
4. Zero grep hits ≠ proof of absence — check path family before "not found"

Full protocol: [`LLM-ROUTING.md`](LLM-ROUTING.md) · [`docs/source-lattice-beyond-the-repo.md`](docs/source-lattice-beyond-the-repo.md).

## Critical rules (summary)

1. **Knowledge boundary** — never leak LLM training data into Record/profile ([`docs/knowledge-boundary-framework.md`](docs/knowledge-boundary-framework.md)).
2. **Gated pipeline** — default **frozen**; stage/merge only on explicit **`fork revive`** ([`docs/archive/grace-mar.md`](docs/archive/grace-mar.md)).
3. **Record frozen default** — `"we [did X]"` in WORK lanes is normal phrasing; do not auto-stage gate candidates.
4. **Contradiction preservation** — do not flatten conflicting evidence.
5. **MEMORY ≠ Record** — `memory.md` is continuity only ([`docs/memory-template.md`](docs/memory-template.md)).
6. **Agent turn discipline (Windows)** — one write path + one Shell per turn; no parallel tool storms ([`.cursor/rules/agent-tool-latency-discipline.mdc`](.cursor/rules/agent-tool-latency-discipline.mdc)).

Rules 1–11 detail, triadic cognition, Lexile, humane purpose: [`docs/agent-rules/deep-rules.md`](docs/agent-rules/deep-rules.md).

## Layer architecture

| Layer | File |
|---|---|
| 1 Core | This file (`AGENTS.md`) |
| 2 Instance | [`instance-doctrine.md`](instance-doctrine.md) |
| 3 Lane | `docs/skill-work/work-*/` |
| 4 Mode | `.cursor/skills/*/SKILL.md` · `.cursor/rules/*.mdc` |

## Editing and validation

- **Proposal first** for non-trivial implementation; operator approves scope.
- **Commits:** only when the operator asks.
- **Preflight:** `python3 scripts/check_repo_health.py --quick`
- **Repo convergence:** [`docs/repo-convergence.md`](docs/repo-convergence.md) · `python3 scripts/run_repo_convergence.py --write` then health
- **Schema registry:** [`docs/system/schema-system.md`](docs/system/schema-system.md) · `python3 scripts/validate_all_schemas.py --scope prediction` · lifecycle: [`docs/statecraft/prediction-system.md`](docs/statecraft/prediction-system.md)
- **Notes gate:** `python3 scripts/check_statecraft_notes.py --warn` (corpus) · `--verify` before shelf-native promote · `--strict --changed-only --tier-a-only` on changed Tier A files
- **Skills:** `python3 scripts/validate_skills.py`
- **Contributor paths:** [`contributing.md`](contributing.md) · [`docs/contributors/`](docs/contributors/)

## What not to do (short)

- Merge unapproved Record knowledge · skip the gate · delete companion data · use "parent" as a system term · treat Voice as Record · use "cognitive twin" (use **fork**)

Full list: [`docs/agent-rules/deep-rules.md`](docs/agent-rules/deep-rules.md#what-not-to-do).
