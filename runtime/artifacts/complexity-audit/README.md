# Complexity audit snapshots

Baseline and final complexity metrics for the mitigation program.

| Snapshot | Path |
|----------|------|
| Baseline (Sprint 1) | [baseline-2026-06-21.md](baseline-2026-06-21.md) |
| Routing category normalization | [routing-category-normalization-2026-06-21.md](routing-category-normalization-2026-06-21.md) |
| Path fallback retirement prep | [path-fallback-retirement-2026-06-21.md](path-fallback-retirement-2026-06-21.md) |
| Wave 1 path fallback removal | [wave-1-path-fallback-removal-2026-06-21.md](wave-1-path-fallback-removal-2026-06-21.md) |
| Wave 2 platform readiness | [wave-2-platform-readiness-2026-06-21.md](wave-2-platform-readiness-2026-06-21.md) |
| Wave 2 path fallback removal | [wave-2-path-fallback-removal-2026-06-21.md](wave-2-path-fallback-removal-2026-06-21.md) |
| Wave 3 archive placeholder readiness | [wave-3-archive-placeholder-readiness-2026-06-21.md](wave-3-archive-placeholder-readiness-2026-06-21.md) |
| Wave 3 path fallback removal | [wave-3-path-fallback-removal-2026-06-21.md](wave-3-path-fallback-removal-2026-06-21.md) |
| Wave 4 Grace-Mar compat readiness | [wave-4-grace-mar-compat-readiness-2026-06-21.md](wave-4-grace-mar-compat-readiness-2026-06-21.md) |
| Wave 4 path fallback removal | [wave-4-path-fallback-removal-2026-06-21.md](wave-4-path-fallback-removal-2026-06-21.md) |
| Path fallback CI enforcement | [path-fallback-retirement-ci-enforcement-2026-06-21.md](path-fallback-retirement-ci-enforcement-2026-06-21.md) |
| Root file budget slice plan | [root-file-budget-slice-plan-2026-06-21.md](root-file-budget-slice-plan-2026-06-21.md) |
| Root file budget CI enforcement | [root-file-budget-ci-enforcement-2026-06-21.md](root-file-budget-ci-enforcement-2026-06-21.md) |

Regenerate:

```bash
python3 scripts/audit_repo_complexity.py --write-baseline runtime/artifacts/complexity-audit/baseline-YYYY-MM-DD.md
```

Policy: [docs/complexity-budget.md](../../docs/complexity-budget.md)
