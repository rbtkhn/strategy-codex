# Root directory map — strategy-codex

**Work only; not Record.**

**Purpose:** Legibility hub for what lives at the repository root vs under `runtime/`, `docs/`, and frozen Grace-Mar archaeology. Link SSOT below; this page does not duplicate full doctrine.

**Related:** [harness-architecture-map.md](harness-architecture-map.md) · [operator-root-artifacts.md](operator-root-artifacts.md) · [runtime-vs-record.md](runtime-vs-record.md)

---

## Why the root looks busy

GitHub shows ~40 top-level directories plus many root files. That mix is intentional but uneven:

| Layer | Role |
|-------|------|
| **Frozen Record (Grace-Mar)** | `self.md`, `recursion-gate.md`, `bot/`, … — archaeology at root until Phase 5 relocation |
| **Operator ledgers** | Append-only JSONL moved to `runtime/operator-events/` (compat read from root) |
| **Dream handoff** | `daily-handoff/last-dream.json` (compat read from root `last-dream.json`) |
| **Doctrine / routing** | `AGENTS.md`, `LLM-ROUTING.md`, `docs/` |
| **Work channels** | `statecraft/`, `singularity/`, `codex/` |
| **Runtime / derived** | `runtime/` (observations, workflow-depth, operator-events, …) |
| **Apps / tooling** | `apps/`, `scripts/`, `src/` |

Local workspaces may look far noisier than GitHub (pytest temp dirs, `.codex-tmp`) — see [contributing.md](../contributing.md) hygiene section.

---

## Root file families (quick scan)

### Frozen Record (fork revive only)

Do not relocate without Phase 5 plan. Canonical names: [canonical-paths.md](canonical-paths.md).

- `self.md`, `self-archive.md`, `self-knowledge.md`, `recursion-gate.md`
- `self-skills.md`, `self-library.md`, `session-log.md`, `intent.md`
- `bot/`, `self-llm.txt`

### Operator event ledgers (canonical: `runtime/operator-events/`)

Append-only JSONL — **not** Record. Writers use `scripts/repo_io.py` resolvers; readers fall back to legacy root paths.

| File | Role |
|------|------|
| `pipeline-events.jsonl` | Staged / applied / rejected pipeline events |
| `merge-receipts.jsonl` | Merge batch receipts |
| `cadence-learning-events.jsonl` | Coffee / dream cadence learning |
| `business-ledger.jsonl` | Instance business transactions (root copy; per-user copy may live under `users/<id>/`) |
| `fork-lineage.jsonl` | Fork lineage ledger |
| `strategy-fold-events.jsonl` | Strategy notebook fold / weave learning |

See [runtime/operator-events/README.md](../runtime/operator-events/README.md).

### Dream continuity

| Path | Role |
|------|------|
| `daily-handoff/last-dream.json` | Canonical dream handoff (written by `auto_dream.py`) |
| `daily-handoff/night-handoff.json` | Compact night-to-morning coffee handoff |
| Root `last-dream.json` | Legacy compat (read fallback) |

### Other root JSONL (stay at root or under `runtime/`)

| Path | Policy |
|------|--------|
| `harness-events.jsonl` | Operator-local audit lane ([.gitignore](../.gitignore)) |
| `compute-ledger.jsonl` | Operator-local compute ledger |
| `continuity-log.jsonl` | Operator continuity |

---

## Top-level directories (selected)

| Directory | Lane |
|-----------|------|
| `statecraft/` | Geopolitical / judgment operator surface |
| `singularity/` | Acceleration / agency operator surface |
| `codex/` | Chronology and strategy-codex corpus |
| `docs/` | Doctrine, skill-work, workflows |
| `runtime/` | Derived runtime, operator-events, workflow-depth |
| `scripts/` | Operator automation |
| `artifacts/` | Derived operator dashboards (non-authoritative) |
| `archive/` | Grace-Mar corpus quarantine |
| `public/` | Public `ph-civ` publish tree |
| `essays/` | Cross-channel theses |

Full routing: [LLM-ROUTING.md](../LLM-ROUTING.md).

---

## Path resolution (scripts)

**SSOT:** `scripts/repo_io.py`

- `resolve_ledger_path(user_id, name)` — read / open-for-append with compat
- `operator_ledger_write_path(user_id, name)` — canonical write target
- `resolve_last_dream_path(user_id)` / `last_dream_write_path(user_id)` — dream handoff

**Migration:** `python3 scripts/migrate_operator_event_paths.py --dry-run` then `--apply`

---

## Deferred (Phase 5)

Relocating the frozen Grace-Mar Record bundle off the root (`self.md`, `recursion-gate.md`, `bot/`, …) is a separate high-risk project — `canonical-paths.md`, `assert_canonical_paths.py`, and many scripts assume `profile_dir()` → `REPO_ROOT`.

---

## Return path

- [harness-architecture-map.md](harness-architecture-map.md)
- [operator-root-artifacts.md](operator-root-artifacts.md)
- [start-here.md](start-here.md)
