# Repo Surgeon (derived report)

Non-canonical **runtime / derived** structural health report for `strategy-codex`. Consolidates existing check scripts and scoped link/portability scans — does not replace them.

**Phase 0 alignment:** [docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md](../../../docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md)

**Registry:** [docs/operator-surface-registry.md](../../../docs/operator-surface-registry.md) · `surface_id`: `repo-surgeon`

## Layout

```text
runtime/artifacts/repo-surgeon/latest.md
runtime/artifacts/repo-surgeon/latest.json
runtime/artifacts/repo-surgeon/YYYY-MM-DD.md   # optional snapshot
```

**Default:** `latest.*` and dated snapshots are **gitignored**. Regenerate on demand.

## Authority

> **Mode:** runtime / derived  
> **Authority:** advisory only — not Record, not merge authority

**Does not replace:** [`docs/root-directory-map.md`](../../../docs/root-directory-map.md), individual check scripts, or [`docs/harness-architecture-map.md`](../../../docs/harness-architecture-map.md).

## Rebuild (Phase 1+)

```bash
python3 scripts/repo_surgeon.py \
  --out runtime/artifacts/repo-surgeon/latest.md \
  --json-out runtime/artifacts/repo-surgeon/latest.json \
  --run-existing-checks
```

## SSOT return paths

- [docs/root-directory-map.md](../../../docs/root-directory-map.md)
- [docs/harness-architecture-map.md](../../../docs/harness-architecture-map.md)
- [runtime/artifacts/README.md](../README.md)
- [skills/README.md](../../../skills/README.md)
