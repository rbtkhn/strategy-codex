# Complexity audit snapshots

Baseline and final complexity metrics for the mitigation program.

| Snapshot | Path |
|----------|------|
| Baseline (Sprint 1) | [baseline-2026-06-21.md](baseline-2026-06-21.md) |

Regenerate:

```bash
python3 scripts/audit_repo_complexity.py --write-baseline runtime/artifacts/complexity-audit/baseline-YYYY-MM-DD.md
```

Policy: [docs/complexity-budget.md](../../docs/complexity-budget.md)
