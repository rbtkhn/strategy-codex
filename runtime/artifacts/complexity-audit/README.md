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

Regenerate:

```bash
python3 scripts/audit_repo_complexity.py --write-baseline runtime/artifacts/complexity-audit/baseline-YYYY-MM-DD.md
```

Policy: [docs/complexity-budget.md](../../docs/complexity-budget.md)
