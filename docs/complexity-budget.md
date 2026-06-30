# Complexity budget — strategy-codex


This document defines anti-sprawl targets for the complexity mitigation program. Metrics are collected by `python3 scripts/audit_repo_complexity.py`.

## Product kernel (never simplify away)

```text
source-archive → generated indexes → daily synthesis → notes → essays
```

## Term law (note vs transaction)

SSOT for durable-work vocabulary:

```text
Use note for durable analytical work products. Use transaction only for operational receipts, business ledger entries, or legacy compatibility stubs.
```

Detail: [glossary.md](glossary.md) · [prose-index.md](prose-index.md) · [audits/transaction-retirement-inventory-2026-06.md](audits/transaction-retirement-inventory-2026-06.md).

Preserve as first-class: `source-archive/`, `statecraft/`, `singularity/`, `essays/`, `runtime/artifacts/`, `scripts/`, `docs/start-here.md`, `repo-map.yaml`.

## Authority categories (target: four)

| Category | Meaning |
|----------|---------|
| `source` | Primary or canonical source material |
| `work` | Active human/operator-authored working surfaces |
| `generated` | Derived, rebuildable, non-authoritative outputs |
| `archive` | Frozen historical or compatibility material |

Do not introduce new authority labels without updating this table and the audit script.

## Quantitative targets

| Metric | Baseline (2026-06-21) | Target | Fail CI (phase) |
|--------|----------------------:|-------:|-----------------|
| Root files | 25 (at target) | ≤ 25 (doctrine floor; was 20) | **Enforced** (`assert_root_file_budget.py --strict`) |
| Root directories (contract) | 20 | ≤ 20 | Enforced (`assert_root_folder_layout`) |
| Primary routing front doors | 8 listed | ≤ 3 | Phase 9 |
| Always-read agent doc lines (`AGENTS.md`) | ~286 | ≤ 150 | Phase 5 |
| Legacy path fallback tuples in `repo_io` | 29 | 0 | Phase 10 |
| Grace-Mar mentions outside archive docs (bounded scan) | ~11,785 | ≤ 3 (short pointers) | Phase 5 |
| Generated files without manifest entry | n/a | 0 | Phase 6 (**Enforced** — `check_generated_surfaces.py --check --strict`) |
| Transaction as default durable-work term (tier-1 doctrine) | n/a | 0 | Phase 7 (**Enforced** — `check_transaction_term_usage.py --strict --skills-strict`) |

Run `python3 scripts/check_generated_surfaces.py --check --strict` (required CI). Manifest: [`generated-manifest.yaml`](../generated-manifest.yaml).

## Generated surface header convention (Sprint 6)

Rebuildable outputs must declare their generator near the top of the file:

| Format | When | Example |
|--------|------|---------|
| HTML comment | Markdown routing/dashboard files | `<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. … -->` |
| HTML comment (short) | Derived dashboards | `<!-- GENERATED — run: python3 scripts/build_library_index.py -->` |
| Italic line | Statecraft archive inventory indexes | `_Generated inventory note. Rebuild with \`python scripts/refresh_statecraft_archive_indices.py\`._` |
| JSON field | Machine-readable indexes | `"generated_at"` and optional `"generated_by"` |

Do not hand-edit manifest-listed surfaces; regenerate via the script named in the header or manifest.

Run baseline: `python3 scripts/audit_repo_complexity.py --write-baseline runtime/artifacts/complexity-audit/baseline-YYYY-MM-DD.md`

## Grace-Mar / fork-revive mention budget

Grace-Mar and fork-revive material in **primary-path docs** (`README.md`, `AGENTS.md`, `contributing.md`, `instance-doctrine.md`, `docs/start-here.md`, `.cursor/rules` except fork-revive-only rules) should appear only as **short pointers**:

```text
Grace-Mar is archived/frozen. Active strategy-codex work does not grow the fork. See docs/archive/grace-mar.md.
```

Detailed doctrine belongs under `docs/archive/` and `archive/grace-mar-corpus/`.

## Legacy path fallback retirement (Sprint 4)

`scripts/repo_io.py` → `REPO_PATH_MIGRATIONS` maps logical keys to `(canonical, legacy…)`.

| Classification | Keys (examples) | Sprint 4 policy |
|---|---|---|
| `active_canonical` | `artifacts`, `src`, `skills`, `users`, … | Canonical under `runtime/`, `platform/`, `skills/` — retire root legacy when dual layout gone |
| `archive_placeholder` | `evidence`, `review-queue`, `reflection-proposals` | Keep under `archive/` until fork revive traffic is zero |
| `grace_mar_compat` | `bot`, `bootstrap`, `recursion-gate-staging` | Resolve via `strategy_codex.compat.grace_mar_paths` for Voice archaeology only |

**Strict mode:** `STRATEGY_CODEX_STRICT_PATHS=1` → `resolve_repo_path()` raises if legacy fallback would be used.

**CI (warn):** `python3 scripts/check_repo_path_strict.py` — reports dual/legacy-only layouts; `--strict` fails (Sprint 6+).

**Record bundle:** Profile / Record files → `archive/grace-mar-instance/` via `profile_dir()` — not repo root, not `platform/users/<id>` unless that tree holds `self.md`.

## Path fallback retirement budget

Active resolver fallback tuples are retired. CI must prevent reintroduction.

**SSOT:** [`path-fallback-retirement.yaml`](../path-fallback-retirement.yaml) (machine) · [`docs/path-fallback-retirement.md`](path-fallback-retirement.md) (human mirror).

### Policy

No new fallback tuple may be added without:

1. Classification in `REPO_PATH_CLASSIFICATION` ([`scripts/repo_io.py`](../scripts/repo_io.py))
2. Retirement entry in `path-fallback-retirement.yaml`
3. Test coverage in [`tests/test_repo_path_strict.py`](../tests/test_repo_path_strict.py)

### Target

| Metric | Current | Target |
|---|---:|---:|
| `REPO_PATH_MIGRATIONS` keys | 29 | 29 canonical-only keys |
| Fallback-bearing resolver keys | 0 | 0 |
| Unclassified migration keys | 0 | 0 |
| Grace-Mar compatibility fallbacks in active resolver | 0 | 0 |

### Enforcement

`python scripts/check_repo_path_strict.py --strict` is required CI.

No new fallback tuple may be added without an explicit operator-approved exception and an expiry date in this document.

### Wave 1 removal (2026-06-21)

Wave 1 active canonical fallback tails removed: **12** keys (`artifacts` through `bridges` — see [`docs/path-fallback-retirement.md`](path-fallback-retirement.md)).

Remaining fallback-bearing keys: **0** — path-fallback retirement program complete.

### Wave 2 removal (2026-06-21)

Wave 2 platform subpath fallback tails removed: **10** keys (`app` through `profile` — see [`docs/path-fallback-retirement.md`](path-fallback-retirement.md)). Readiness audit: [`wave-2-platform-readiness-2026-06-21.md`](../runtime/artifacts/complexity-audit/wave-2-platform-readiness-2026-06-21.md). Removal receipt: [`wave-2-path-fallback-removal-2026-06-21.md`](../runtime/artifacts/complexity-audit/wave-2-path-fallback-removal-2026-06-21.md).

### Wave 3 removal (2026-06-21)

Wave 3 archive placeholder fallback tails removed: **3** keys (`evidence`, `reflection-proposals`, `review-queue` — see [`docs/path-fallback-retirement.md`](path-fallback-retirement.md)). Readiness audit: [`wave-3-archive-placeholder-readiness-2026-06-21.md`](../runtime/artifacts/complexity-audit/wave-3-archive-placeholder-readiness-2026-06-21.md). Removal receipt: [`wave-3-path-fallback-removal-2026-06-21.md`](../runtime/artifacts/complexity-audit/wave-3-path-fallback-removal-2026-06-21.md).

**Fallback tuple count:** 6 → **3** → **0** keys with `len(entry) > 1`.

### Wave 4 removal (2026-06-21)

Wave 4 Grace-Mar compatibility fallback tails removed: **3** keys (`bot`, `recursion-gate-staging`, `bootstrap` — see [`docs/path-fallback-retirement.md`](path-fallback-retirement.md)). Readiness audit: [`wave-4-grace-mar-compat-readiness-2026-06-21.md`](../runtime/artifacts/complexity-audit/wave-4-grace-mar-compat-readiness-2026-06-21.md). Removal receipt: [`wave-4-path-fallback-removal-2026-06-21.md`](../runtime/artifacts/complexity-audit/wave-4-path-fallback-removal-2026-06-21.md). `BOT_DIR` now resolves via `GRACE_MAR_INSTANCE_DIR / "bot"` (canonical only).

Scan: `python3 scripts/check_repo_path_strict.py` · `--json` · `--strict`.

### Root file budget (Phase 9 — complete)

Active root file count **25** on disk (at `max_root_files` target). Phased relocations: [`root-file-budget-slice-plan-2026-06-21.md`](../runtime/artifacts/complexity-audit/root-file-budget-slice-plan-2026-06-21.md). **Program complete:** [`root-file-budget-program-complete-2026-06-21.md`](../runtime/artifacts/complexity-audit/root-file-budget-program-complete-2026-06-21.md). **`assert_root_file_budget.py --strict` is required CI** (promoted 2026-06-21). CI slice receipt: [`root-file-budget-ci-enforcement-2026-06-21.md`](../runtime/artifacts/complexity-audit/root-file-budget-ci-enforcement-2026-06-21.md).

Scan: `python3 scripts/assert_root_file_budget.py` · `--strict` · `--json`.

## CI rollout policy

1. **Warning mode** — new checks run in CI with `continue-on-error: true` or without `--check` for two clean passes.
2. **Fail mode** — promote to required after proof-slice gate (post Sprint 3) and operator legibility check.
3. **Exceptions** — time-boxed allowlist entries in this file with expiry date; no permanent exceptions.

**Workflow:** [`.github/workflows/repo-health.yml`](../.github/workflows/repo-health.yml) — **Required** job (routing, generated headers, layout, path adoption, **strict path scan**, **strict root file budget**, path/budget regression pytest) + **Advisory** job (archive boundary, complexity `--check`, drift orchestrator). Mirrors `python3 scripts/check_repo_health.py --quick` / `--full`.

**Promoted (2026-06-21):** `python3 scripts/check_repo_path_strict.py --strict` — required; no longer in advisory job.

**Promoted (2026-06-21):** `python3 scripts/assert_root_file_budget.py --strict` — required; no longer in advisory job.

## Related

- Complexity mitigation plan (Cursor): `complexity_mitigation_plan_e3d72ba0.plan.md`
- `scripts/audit_repo_complexity.py`
- `scripts/check_archive_boundary.py` (warn mode; `--strict` after Phase 5)
- `scripts/generate_llm_routing.py` — hybrid [`LLM-ROUTING.md`](../LLM-ROUTING.md) from [`repo-map.yaml`](../repo-map.yaml)
- `scripts/check_repo_path_strict.py` (**required** `--strict` in CI; promoted 2026-06-21)
- `scripts/check_generated_surfaces.py` — manifest + header + drift (`--strict` Sprint 9 fail)
- [`root-file-budget.yaml`](../root-file-budget.yaml) + `scripts/assert_root_file_budget.py` (**required** `--strict` in CI; promoted 2026-06-21)
- Phase 8 doc trim plan: [complexity-readme-start-here-trim-plan.md](complexity-readme-start-here-trim-plan.md) · `scripts/check_doc_duplication.py` (warn)
- `runtime/artifacts/complexity-audit/`
