---
audience: operator
authority: routing_aid
record_status: none
---

# Root directory map — strategy-codex

**Purpose:** Legibility hub for what lives at the repository root vs under consolidated subtrees (`runtime/`, `platform/`, `archive/`, …). Link SSOT below; this page does not duplicate full doctrine.

**Related:** [harness-architecture-map.md](harness-architecture-map.md) · [operator-root-artifacts.md](operator-root-artifacts.md) · [runtime-vs-record.md](runtime-vs-record.md) · [canonical-paths.md](canonical-paths.md)

---

## GitHub root layout (22 folders)

**Committed `main`:** exactly **22** top-level directories. SSOT list: `scripts/repo_io.py` → `TARGET_ROOT_FOLDERS`. CI: `python3 scripts/assert_root_folder_layout.py`.

| Folder | Lane |
|--------|------|
| `.cursor` | Cursor rules, skills, agent overlays |
| `.github` | CI workflows (includes layout cap + path-adoption check) |
| `library` | Local PD primary-text shelf (gitignored binaries; [library/README.md](../library/README.md)) |
| `archive` | Grace-Mar instance bundle, placeholders, review queues |
| `continuity` | Durable chronology and strategy-codex notebook layer (formerly `continuity/`) |
| `codex` | Legacy redirect only — [`continuity/README.md`](../continuity/README.md) |
| `docs` | Doctrine, skill-work, workflows |
| `education` | **Curriculum factory** — human teach + agent-training outputs ([education/README.md](../education/README.md)) |
| `essays` | Cross-channel theses (repo-root shelf) |
| `examples` | Sample / reference material |
| `operations` | Real-world operating shelves — Grace Gems, mountain homestead ([operations/README.md](../operations/README.md)) |
| `platform` | Apps, `src/`, deployment, config, per-user profiles |
| `public` | Inbound read-only mirrors (`public/predictive-history/` = canonical PH snapshot; not a live `ph-civ` publish tree) |
| `research` | Auto-research, bridges, external research lanes |
| `runtime` | Derived runtime, operator-events, artifacts, handoff |
| `schemas` | Schema registry (`schemas/registry/`) |
| `scripts` | Operator automation |
| `singularity` | Acceleration / agency operator surface |
| `skills` | Portable skills corpus (formerly `skills-portable/`) |
| `source-archive` | Verbatim statecraft source captures |
| `statecraft` | Geopolitical / judgment operator surface |
| `templates` | Template manifests and styles (formerly root `styles/`) |
| `tests` | Pytest suite |

Plus **root files** (budgeted at **23** via [`root-file-budget.yaml`](../root-file-budget.yaml)): `AGENTS.md`, `LLM-ROUTING.md`, `pyproject.toml`, `memory.md`, lane manifests, etc. Skill split surfaces live under **`continuity/`** (`skill-think.md`, `skill-write.md`, `skill-steward.md`).

**Retired paths (not root folders):**

- Root `operator-books` symlink removed; operator books live in misc homes per [continuity/README.md](../continuity/README.md) § Operator books
- Record glossary term `removed operator-books symlink` in [glossary.md](glossary.md) remains **Grace-Mar Record vocabulary** — do not conflate with GitHub root layout

Full routing: [LLM-ROUTING.md](../LLM-ROUTING.md) · [repo-map.yaml](../repo-map.yaml).

---

## Local vs GitHub

Local workspaces often look far noisier than GitHub: pytest temp dirs (`.tmp-pytest-*`, `.codex-pytest-*`), `.venv`, `.codex-tmp`, and other operator-local paths are **not** part of the 20-folder contract. See [contributing.md](../contributing.md) hygiene section.

---

## Grace-Mar Record bundle (fork revive only)

**Physical home:** `archive/grace-mar-instance/` — see [archive/grace-mar-instance/README.md](../archive/grace-mar-instance/README.md).

Record markdown and bot code **no longer live at the repository root**. Scripts resolve paths via `scripts/repo_io.py` → `profile_dir()` (returns `archive/grace-mar-instance/` when `self.md` is present there).

| Path | Role |
|------|------|
| `archive/grace-mar-instance/self.md` | Identity shell + three-dimension mind overview |
| `archive/grace-mar-instance/recursion-gate.md` | Pipeline staging |
| `archive/grace-mar-instance/self-archive.md` | EVIDENCE / activity log |
| `archive/grace-mar-instance/self-skills.md` | Capability index |
| `archive/grace-mar-instance/bot/` | Telegram / WeChat emulation (deprecated runtime) |
| `archive/grace-mar-instance/bootstrap/` | Legacy bootstrap docs |
| `archive/grace-mar-instance/recursion-gate-staging/` | Gate staging aids |

Basenames unchanged — see [canonical-paths.md](canonical-paths.md). **Default:** Record is frozen; fork growth is not a system objective — [docs/archive/grace-mar.md](archive/grace-mar.md) · [grace-mar-instance-boundary.md](grace-mar-instance-boundary.md).

---

## Operator event ledgers (canonical: `runtime/operator-events/`)

Append-only JSONL — **not** Record. Writers use `scripts/repo_io.py` resolvers; readers fall back to legacy root paths.

| File | Role |
|------|------|
| `pipeline-events.jsonl` | Staged / applied / rejected pipeline events |
| `merge-receipts.jsonl` | Merge batch receipts |
| `cadence-learning-events.jsonl` | Coffee / dream cadence learning |
| `business-ledger.jsonl` | Instance business transactions (root copy; per-user copy may live under `platform/users/<id>/`) |
| `fork-lineage.jsonl` | Fork lineage ledger |
| `strategy-fold-events.jsonl` | Strategy notebook fold / weave learning |

See [runtime/operator-events/README.md](../runtime/operator-events/README.md).

**Agent handoff queue:** [`runtime/operator-queue/`](../runtime/operator-queue/README.md) — visible work handoffs between humans and agents ([`agent-handoff-queue.md`](agent-handoff-queue.md)).

---

## Dream continuity

| Path | Role |
|------|------|
| `runtime/daily-handoff/last-dream.json` | Canonical dream handoff (written by `auto_dream.py`) |
| `runtime/daily-handoff/night-handoff.json` | Compact night-to-morning coffee handoff |
| Root `last-dream.json` | Legacy compat (read fallback) |

---

## Other root JSONL (operator-local or compat)

| Path | Policy |
|------|--------|
| `harness-events.jsonl` | Operator-local audit lane ([.gitignore](../.gitignore)) |
| `compute-ledger.jsonl` | Operator-local compute ledger |
| `continuity-log.jsonl` | Operator continuity |

---

## Nested relocations (legacy → canonical)

Scripts resolve consolidated paths through `resolve_repo_path(key)` with legacy fallback. Key moves:

| Logical key | Canonical path | Legacy fallback(s) |
|-------------|----------------|---------------------|
| `artifacts` | `runtime/artifacts/` | `artifacts/` |
| `daily-handoff` | `runtime/daily-handoff/` | `daily-handoff/` |
| `prepared-context` | `runtime/prepared-context/` | `prepared-context/` |
| `runtime-bundle` | `runtime/bundle/` | `runtime-bundle/` |
| `apps` | `platform/apps/` | `apps/` |
| `src` | `platform/src/` | `src/` |
| `users` | `platform/users/` | `users/` |
| `skills` | `skills/` | `skills-portable/` |
| `schema-registry` | `schemas/registry/` | `schema-registry/` |
| `styles` | `templates/styles/` | `styles/` |
| `auto-research` | `research/auto-research/` | `auto-research/` |
| `bridges` | `research/bridges/` | `bridges/` |
| `evidence` | `archive/placeholders/evidence/` | `evidence/` |
| `review-queue` | `archive/queues/review-queue/` | `review-queue/` |
| `bot` | `archive/grace-mar-instance/bot/` | `bot/` |

Full registry: `REPO_PATH_MIGRATIONS` in `scripts/repo_io.py`.

---

## Root files policy (~31 tracked)

GitHub `main` keeps **doctrine, build, deploy, and lane-governance** files at the repository root (not counted in the 20-folder cap). **Profile-derived exports** (`manifest.json`, `session-transcript.md`, `gate-dashboard.html`, …) live under **`archive/grace-mar-instance/`** via `profile_dir()` / `resolve_profile_export_path()`.

| Stay at root | Examples |
|--------------|----------|
| Doctrine / routing | `AGENTS.md`, `LLM-ROUTING.md`, `instance-doctrine.md`, `README.md` |
| Build / deploy | `pyproject.toml`, `Dockerfile`, `requirements*.txt`, `render.yaml` |
| Lane / template governance | `lanes.yaml`, `platform/template/template-manifest.json`, `platform/template/template-source.json` |
| Skill split surfaces | `continuity/skill-think.md`, `continuity/skill-write.md`, `continuity/skill-steward.md` |

| Nest under profile bundle | Examples |
|---------------------------|----------|
| Policy / agent exports | `manifest.json`, `llms.txt`, `intent_snapshot.json`, `fork-manifest.json` |
| Runtime continuity | `session-transcript.md`, `self-work.md` |
| Derived views | `gate-dashboard.html`, `evidence-graph.json`, `symbolic_identity.json` |

**Fork lifecycle** (`fork_state.json`, `drift-report.json`) → `platform/users/<fork_id>/` per `grace_mar.fork_state` — not repo root.

**CI:** `python3 scripts/assert_root_profile_exports.py` fails if any `PROFILE_DERIVED_EXPORTS` basename reappears at root.

---

## Path resolution (scripts)

**SSOT:** `scripts/repo_io.py`

| Helper | Role |
|--------|------|
| `resolve_repo_path(key)` | Consolidated dir by logical key + legacy fallback |
| `profile_dir(user_id)` | Grace-Mar Record root (`archive/grace-mar-instance/`) |
| `user_profile_dir(user_id)` | Per-fork dir under `platform/users/<id>/` |
| `artifacts_dir(base)` | Repo `runtime/artifacts/` or profile-scoped nested artifacts |
| `src_dir(base)` | Repo `platform/src/` or profile-scoped nested src |
| `resolve_ledger_path` / `operator_ledger_write_path` | Operator JSONL ledgers |
| `resolve_profile_export_path(user_id, basename)` | Profile-derived export with optional legacy root read fallback |
| `derived_export_dir(user_id)` | Alias for `profile_dir(user_id)` (export home) |

**Module constants** (prefer over string paths): `ARTIFACTS_DIR`, `SRC_DIR`, `PREPARED_CONTEXT_DIR`, `SKILLS_DIR`, `APPS_DIR`, … — from `scripts/repo_io.py`. Voice archaeology bot paths: `scripts/grace_mar_compat_paths.py` → `strategy_codex.compat.grace_mar_paths`.

**Checks:**

- Layout cap: `python3 scripts/assert_root_folder_layout.py`
- Root file budget: `python3 scripts/assert_root_file_budget.py` (warn) · `--strict` (Phase 9)
- Adoption: `python3 scripts/check_repo_path_adoption.py` (CI: `--max-literals 0`)
- Profile exports: `python3 scripts/assert_root_profile_exports.py`
- Batch adopt: `python3 scripts/adopt_repo_path_constants.py --apply`

**Migration tooling:** `python3 scripts/migrate_root_layout.py --apply` · path rewrites: `apply_root_path_rewrites.py` · operator ledgers: `migrate_operator_event_paths.py`

---

## Return path

- [harness-architecture-map.md](harness-architecture-map.md)
- [operator-root-artifacts.md](operator-root-artifacts.md)
- [start-here.md](start-here.md)
