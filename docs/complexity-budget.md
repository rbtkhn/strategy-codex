# Complexity budget — strategy-codex

**Work only; not Record.**

This document defines anti-sprawl targets for the complexity mitigation program. Metrics are collected by `python3 scripts/audit_repo_complexity.py`.

## Product kernel (never simplify away)

```text
source-archive → generated indexes → daily synthesis → judgment / transaction object
```

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
| Root files | 32 | ≤ 20 | Phase 9 |
| Root directories (contract) | 20 | ≤ 20 | Enforced (`assert_root_folder_layout`) |
| Primary routing front doors | 8 listed | ≤ 3 | Phase 9 |
| Always-read agent doc lines (`AGENTS.md`) | ~286 | ≤ 150 | Phase 5 |
| Legacy path fallback tuples in `repo_io` | 28 | 0 | Phase 10 |
| Grace-Mar mentions outside archive docs (bounded scan) | ~11,785 | ≤ 3 (short pointers) | Phase 5 |
| Generated files without manifest entry | n/a | 0 | Phase 6 |

Run baseline: `python3 scripts/audit_repo_complexity.py --write-baseline runtime/artifacts/complexity-audit/baseline-YYYY-MM-DD.md`

## Grace-Mar / fork-revive mention budget

Grace-Mar and fork-revive material in **primary-path docs** (`README.md`, `AGENTS.md`, `contributing.md`, `instance-doctrine.md`, `docs/start-here.md`, `.cursor/rules` except fork-revive-only rules) should appear only as **short pointers**:

```text
Grace-Mar is archived/frozen. Active strategy-codex work does not grow the fork. See docs/archive/grace-mar.md.
```

Detailed doctrine belongs under `docs/archive/` and `archive/grace-mar-corpus/`.

## CI rollout policy

1. **Warning mode** — new checks run in CI with `continue-on-error: true` or without `--check` for two clean passes.
2. **Fail mode** — promote to required after proof-slice gate (post Sprint 3) and operator legibility check.
3. **Exceptions** — time-boxed allowlist entries in this file with expiry date; no permanent exceptions.

## Related

- Complexity mitigation plan (Cursor): `complexity_mitigation_plan_e3d72ba0.plan.md`
- `scripts/audit_repo_complexity.py`
- `scripts/check_archive_boundary.py` (warn mode; `--strict` after Phase 5)
- `scripts/generate_llm_routing.py` — hybrid [`LLM-ROUTING.md`](../LLM-ROUTING.md) from [`repo-map.yaml`](../repo-map.yaml)
- `runtime/artifacts/complexity-audit/`
