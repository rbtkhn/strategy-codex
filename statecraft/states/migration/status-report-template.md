
# Migration Status Report Template

Use this template to close each migration wave deterministically from the ledger and dependency inventory.

## Snapshot

- Report date:
- Wave:
- Objects planned:
- Objects `materialized`:
- Objects `cut_over`:
- Objects `verified`:
- Remaining direct `civ-mem` references:

## Symmetry Check

- Civilization-side first-wave objects present:
- Empire-side first-wave objects present:
- First-wave pairs fully cut over:
- Canonical families represented on both sides:

## By Lane

| Lane | Planned first-wave objects | Materialized | Cut over | Verified | Remaining direct `civ-mem` dependencies | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| America | 5 |  |  |  |  |  |
| Russia | 5 |  |  |  |  |  |
| China | 5 |  |  |  |  |  |
| Iran | 5 |  |  |  |  |  |

## Canonical Family Coverage

| Canonical family | Civilization-side carrier present | Empire-side carrier present | Hinge/restoration note | Notes |
| --- | --- | --- | --- | --- |
| What makes a settlement real rather than theatrical? |  |  |  |  |
| When does a pressured hegemon misread its own power, limits, or durability? |  |  |  |  |
| When do older strategic memories continue to constrain present actors? |  |  |  |  |
| When does coercion fail to convert into the political outcome it claims to serve? |  |  |  |  |
| When do broken contact regimes and arms-control inheritances make escalation more dangerous than the proxy-war script admits? |  |  |  |  |
| How does remembered exclusion shape the politics of direct great-power settlement? |  |  |  |  |

## Acceptance Checks

- [ ] no lane is marked complete with civilization-side objects only
- [ ] no canonical family maps only to one volume side
- [ ] every verified slice preserves explicit upstream provenance
- [ ] every verified slice includes counterweight and transaction hook
- [ ] lane-local citation order now prefers `civ-state` over direct `civ-mem`

## Next Wave

- blockers:
- next paired slice:
- direct `civ-mem` dependencies still lacking a first-wave replacement:
