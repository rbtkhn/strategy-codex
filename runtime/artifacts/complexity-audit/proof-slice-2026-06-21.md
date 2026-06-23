# Proof-slice gate — 2026-06-21

**Scope:** After Sprints 1–4 (complexity mitigation). **Decision:** **Proceed to Sprint 5** on routing/archive axis; **hold** root-budget fail-mode and AGENTS slim fail-mode until Sprint 5 ships.

## Gate checks

| Check | Result |
|---|---|
| `audit_repo_complexity.py` vs baseline | See delta table below |
| `generate_llm_routing.py --check` | **Pass** (after regen — local WIP had drifted metrics footer) |
| `check_archive_boundary.py` | **Pass** (primary docs) |
| `check_repo_path_strict.py` | **Pass** (0 legacy/dual layouts on disk) |
| `validate_repo_routing.py` (non-strict) | **Pass** |
| `validate_repo_routing.py --strict` | **Pre-existing debt** — broken links in jiang/karaganov/mcgovern source-index files |

## Baseline → now (2026-06-21)

| Metric | Baseline | Now | Δ | Gate read |
|---|---:|---:|---:|---|
| Root files | 32 | 32 | 0 | No improvement yet (Sprint 7+) |
| Root dirs (contract) | 20 | 20 | 0 | At target |
| `pyproject` name | grace-mar → **strategy-codex** | strategy-codex | ✓ | Sprint 1 done |
| Grace-Mar refs (primary paths) | 11,785 | 11,826 | +41 | Expected: new archive doc + pointers; **not** slimmed until Sprint 5 |
| Grace-Mar refs (total) | 12,997 | 13,059 | +62 | Archive consolidation adds one SSOT; primary count still high |
| repo-map routes (approx) | 44 | 47 | +3 | Helmer/Karaganov/Lascaris registry — good |
| Legacy fallback tuples (code) | 28 | 28 | 0 | Sprint 4 classified; retirement Sprint 6–10 |
| **Legacy path layouts (disk)** | n/a | **0** | ✓ | Sprint 4 win |
| Always-read docs (lines) | 463 | 463 | 0 | AGENTS slim = Sprint 5 |
| Routing surfaces present | 5/5 | 5/5 | 0 | Stable |

## Legibility (routing / archive axis)

**Improved — operator-facing:**

1. **Single archive home** — [`docs/archive/grace-mar.md`](../../../docs/archive/grace-mar.md); boundary doc is a short pointer.
2. **Primary-doc noise down** — README Gated Pipeline block shortened; hand-curated routing shortcuts + generated registries in [`LLM-ROUTING.md`](../../../LLM-ROUTING.md).
3. **Machine routing** — [`repo-map.yaml`](../../../repo-map.yaml) + [`docs/routing-reference.md`](../../../docs/routing-reference.md) + generator drift CI.
4. **Path truth** — `profile_dir()` / handoff / warmup now reference `archive/grace-mar-instance/`, not `platform/users/<id>` or repo root.
5. **CI guardrails** — complexity audit, archive boundary (warn), path strict (warn), routing generator `--check`.

**Still noisy (expected pre–Sprint 5):**

- `AGENTS.md` still ~286 lines with fork doctrine embedded.
- Grace-Mar primary-path mention count unchanged in order of magnitude.
- Root file count unchanged (32 vs target 20).
- `--strict` link validation red on a few voice source-index files.

## Decision

| Track | Verdict |
|---|---|
| **Routing / archive / identity** | **Proceed** → Sprint 5 (active `docs/architecture.md`, AGENTS slim + `.cursor/rules` reconciliation) |
| **Root file budget fail-mode** | **Hold** until Sprint 7 inventory + writer updates |
| **Legacy fallback tuple removal** | **Hold** until Sprint 6–10 (zero strict-path warnings window) |
| **repo-routing `--strict` links** | **Optional parallel fix** — does not block Sprint 5 if non-strict CI stays green |

## Operator confirm

If the repo **feels** simpler when finding archive doctrine, routing entries, and Record paths — gate is **closed proceed**. If not, pause before Sprint 5 AGENTS split.

## Commands (re-run)

```bash
python3 scripts/audit_repo_complexity.py
python3 scripts/generate_llm_routing.py --check
python3 scripts/check_archive_boundary.py
python3 scripts/check_repo_path_strict.py
python3 scripts/validate_repo_routing.py
```
