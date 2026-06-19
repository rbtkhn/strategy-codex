# Statecraft War Room (derived dashboard)

Non-canonical **runtime / derived** rollup of live statecraft objects from intake sidecars, daily synthesis, and transaction surfaces.

**Phase 0 alignment:** [docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md](../../../docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md)

**Registry:** [docs/operator-surface-registry.md](../../../docs/operator-surface-registry.md) · `surface_id`: `statecraft-war-room`

## Layout

```text
runtime/artifacts/statecraft-war-room/latest.md
runtime/artifacts/statecraft-war-room/latest.json
runtime/artifacts/statecraft-war-room/YYYY-MM-DD.md   # optional snapshot
```

**Default:** `latest.*` and dated snapshots are **gitignored**. Regenerate on demand.

## Authority

> **Mode:** runtime / derived  
> **Authority:** advisory only — operator confirm required for transaction fit

**Does not replace:** [statecraft/README.md](../../../statecraft/README.md), [docs/statecraft-intake-queue.md](../../../docs/statecraft-intake-queue.md), daily synthesis files, or [statecraft/sheets/transaction-router.md](../../../statecraft/sheets/transaction-router.md).

## Rebuild (Phase 2+)

```bash
python3 scripts/statecraft_war_room.py \
  --out runtime/artifacts/statecraft-war-room/latest.md \
  --json-out runtime/artifacts/statecraft-war-room/latest.json \
  --latest-days 7 \
  --max-objects 12
```

Producer script lands in Phase 2. Until then, this bucket holds policy only.

## SSOT return paths

- [statecraft/README.md](../../../statecraft/README.md)
- [docs/statecraft-intake-queue.md](../../../docs/statecraft-intake-queue.md)
- [statecraft/sheets/transaction-router.md](../../../statecraft/sheets/transaction-router.md)
- [statecraft/patterns/README.md](../../../statecraft/patterns/README.md)
