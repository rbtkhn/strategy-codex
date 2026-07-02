# Transaction retirement inventory (2026-06)

SSOT for [transaction terminology retirement](../strategy-codex-redesign-brief.md). Linked from [deprecated-surfaces.md](../deprecated-surfaces.md).

## Summary

| Class | Count | Action |
| --- | --- | --- |
| Multi-lane frameworks | 11 | Moved to `statecraft/notes/compacts/<slug>/`; stubs at `statecraft/transactions/<slug>/` |
| Lane singles | 6 | Moved to `statecraft/notes/`; stubs at legacy paths |
| Lane README benches | 4 | Tombstoned |
| Instrument router | 1 | Canonical: `statecraft/sheets/instrument-router.md`; stub: `transaction-router.md` |
| Workshop compact | 1 | `statecraft/compact/` unchanged (pre-promotion) |
| Business ledger | N/A | Excluded — unrelated "transaction" |
| Historical synthesis prose | many | Optional sweep; not blocking |

## Multi-lane compacts (canonical)

| Legacy path | Canonical path |
| --- | --- |
| `statecraft/transactions/hormuz-transit-sanctions-relief-compact/` | `statecraft/notes/compacts/hormuz-transit-sanctions-relief-compact/` |
| `statecraft/transactions/persia-nuclear-latency-recognition-framework/` | `statecraft/notes/compacts/persia-nuclear-latency-recognition-framework/` |
| `statecraft/transactions/protected-channel-non-regime-change-framework/` | `statecraft/notes/compacts/protected-channel-non-regime-change-framework/` |
| `statecraft/transactions/minab-civilian-harm-deescalation-framework/` | `statecraft/notes/compacts/minab-civilian-harm-deescalation-framework/` |
| `statecraft/transactions/zangezur-transit-sovereignty-framework/` | `statecraft/notes/compacts/zangezur-transit-sovereignty-framework/` |
| `statecraft/transactions/taiwan-quarantine-maritime-access-framework/` | `statecraft/notes/compacts/taiwan-quarantine-maritime-access-framework/` |
| `statecraft/transactions/baltic-shadow-fleet-infrastructure-damage-framework/` | `statecraft/notes/compacts/baltic-shadow-fleet-infrastructure-damage-framework/` |
| `statecraft/transactions/egypt-debt-suez-bread-legitimacy-framework/` | `statecraft/notes/compacts/egypt-debt-suez-bread-legitimacy-framework/` |
| `statecraft/transactions/pakistan-command-integrity-scare-framework/` | `statecraft/notes/compacts/pakistan-command-integrity-scare-framework/` |
| `statecraft/transactions/panama-canal-water-transit-sovereignty-framework/` | `statecraft/notes/compacts/panama-canal-water-transit-sovereignty-framework/` |
| `statecraft/transactions/us-digital-identity-collapse-sovereignty-framework/` | `statecraft/notes/compacts/us-digital-identity-collapse-sovereignty-framework/` |

## Lane singles (canonical)

| Legacy path | Canonical path |
| --- | --- |
| `statecraft/persia/transactions/hormuz-recognition-transit-transaction.md` | `statecraft/notes/hormuz-recognition-transit-transaction.md` |
| `statecraft/persia/transactions/lebanon-third-party-recognition-gate-transaction.md` | `statecraft/notes/lebanon-third-party-recognition-gate-transaction.md` |
| `statecraft/america/transactions/foreign-client-mesh-separation-and-command-review.md` | `statecraft/notes/foreign-client-mesh-separation-and-command-review.md` |
| `statecraft/america/transactions/digital-identity-continuity-before-platform-control.md` | `statecraft/notes/digital-identity-continuity-before-platform-control.md` |
| `statecraft/russia/transactions/zangezur-mediation-without-overbinding.md` | `statecraft/notes/zangezur-mediation-without-overbinding.md` |
| `statecraft/china/transactions/taiwan-inspection-pressure-without-blockade-ownership.md` | `statecraft/notes/taiwan-inspection-pressure-without-blockade-ownership.md` |

## Pending / optional

- `continuity/academy/statecraft/transactions/` — academy mirror stubs (read-only copy)
- Synthesis day files mentioning "transaction-fit" — historical prose
- `repo-map.yaml` essay tags — refresh `transactions` → `notes` where applicable

## Migration script

`python3 scripts/migrate_transactions_to_notes_compacts.py` — idempotent except stubs already in place.
