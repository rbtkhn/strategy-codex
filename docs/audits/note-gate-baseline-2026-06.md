# Note gate baseline audit (2026-06)

Shadow-mode inventory before strict enforcement. Generated from `check_statecraft_notes.py --warn`.

## Summary

- **Baseline date:** 2026-06-28 (note gate ship)
- **Baseline command:** `python3 scripts/check_statecraft_notes.py --warn`
- **Baseline result:** 796 violation(s) across 328 note(s)
- **Current (2026-06-28, post backfill batches):** **69 violation(s)** across 328 note(s) (−727 from baseline 796)
- **Sample violations (first 40):**

- statecraft/notes/2025-02-ritter-india-global-left-trump-pivot-arc.md: missing note_type
- statecraft/notes/2025-02-ritter-india-global-left-trump-pivot-arc.md: missing source_basis
- statecraft/notes/2025-02-ritter-india-global-left-trump-pivot-arc.md: missing authority_level
- statecraft/notes/2025-11-06-jermy-mercouris-pokrovsk-strategic-weave.md: missing note_type
- statecraft/notes/2025-11-06-jermy-mercouris-pokrovsk-strategic-weave.md: missing source_basis
- statecraft/notes/2025-11-06-jermy-mercouris-pokrovsk-strategic-weave.md: missing authority_level
- statecraft/notes/2025-12-12-jermy-mercouris-siversk-nss-weave.md: missing note_type
- statecraft/notes/2025-12-12-jermy-mercouris-siversk-nss-weave.md: missing source_basis
- statecraft/notes/2025-12-12-jermy-mercouris-siversk-nss-weave.md: missing authority_level
- statecraft/notes/2025-freeman-igl-gaza-ceasefire-register.md: missing note_type
- statecraft/notes/2025-freeman-igl-gaza-ceasefire-register.md: missing source_basis
- statecraft/notes/2025-freeman-igl-gaza-ceasefire-register.md: missing authority_level
- statecraft/notes/2025-freeman-igl-iran-war-push-register.md: missing note_type
- statecraft/notes/2025-freeman-igl-iran-war-push-register.md: missing source_basis
- statecraft/notes/2025-freeman-igl-iran-war-push-register.md: missing authority_level
- statecraft/notes/2025-vs-2026-freeman-igl-register-seam.md: missing note_type
- statecraft/notes/2025-vs-2026-freeman-igl-register-seam.md: missing source_basis
- statecraft/notes/2025-vs-2026-freeman-igl-register-seam.md: missing authority_level
- statecraft/notes/2025-vs-2026-ritter-india-global-left-register-seam.md: missing note_type
- statecraft/notes/2025-vs-2026-ritter-india-global-left-register-seam.md: missing source_basis
- statecraft/notes/2025-vs-2026-ritter-india-global-left-register-seam.md: missing authority_level
- statecraft/notes/2026-01-08-jermy-mercouris-crooke-greenland-venezuela-weave.md: missing note_type
- statecraft/notes/2026-01-08-jermy-mercouris-crooke-greenland-venezuela-weave.md: missing source_basis
- statecraft/notes/2026-01-08-jermy-mercouris-crooke-greenland-venezuela-weave.md: missing authority_level
- statecraft/notes/2026-01-20-davos-dmitriev-helmer-mercouris-comparison.md: missing note_type
- statecraft/notes/2026-01-20-davos-dmitriev-helmer-mercouris-comparison.md: missing source_basis
- statecraft/notes/2026-01-20-davos-dmitriev-helmer-mercouris-comparison.md: missing authority_level
- statecraft/notes/2026-01-20-greenland-same-day-weave-helmer-freeman.md: missing note_type
- statecraft/notes/2026-01-20-greenland-same-day-weave-helmer-freeman.md: missing source_basis
- statecraft/notes/2026-01-20-greenland-same-day-weave-helmer-freeman.md: missing authority_level
- statecraft/notes/2026-01-22-to-2026-03-18-jermy-neutrality-decision-naval-arc-weave.md: missing note_type
- statecraft/notes/2026-01-22-to-2026-03-18-jermy-neutrality-decision-naval-arc-weave.md: missing source_basis
- statecraft/notes/2026-01-22-to-2026-03-18-jermy-neutrality-decision-naval-arc-weave.md: missing authority_level
- statecraft/notes/2026-01-30-jermy-mercouris-iran-armada-kiev-weave.md: missing note_type
- statecraft/notes/2026-01-30-jermy-mercouris-iran-armada-kiev-weave.md: missing source_basis
- statecraft/notes/2026-01-30-jermy-mercouris-iran-armada-kiev-weave.md: missing authority_level
- statecraft/notes/2026-02-03-helmer-marandi-turkey-kurd-regional-wedge.md: missing note_type
- statecraft/notes/2026-02-03-helmer-marandi-turkey-kurd-regional-wedge.md: missing source_basis
- statecraft/notes/2026-02-03-helmer-marandi-turkey-kurd-regional-wedge.md: missing authority_level
- statecraft/notes/2026-02-17-freeman-mearsheimer-kabuki-vs-empire-geneva-week.md: missing note_type

_… and 598 more._

## Backfill progress (2026-06-28)

Bounded shelf-native batches via `scripts/backfill_note_contract_batch.py` (+ manual `archive_links` where routing notes lacked body anchors):

| Batch | Notes | Commits on `main` | Warn delta |
| --- | --- | --- | --- |
| `mou-enforcement` | 10 | `c1d057a8a` | 796 → 770 |
| `iran-theater` | 7 | `2bc07e887` | 770 → 748 |
| `ai-cluster` | 10 | `2bc07e887` | 748 → 719 |
| `month-maturity` | 6 | `a5b6c3e01` | 719 → 701 |
| `speaker-watchlist` | 15 | `a5b6c3e01` | 701 → 656 |
| `closure-audit` | 6 | `a5b6c3e01` | 656 → **638** |
| `weave-register` | 29 | *(local)* | 638 → **551** |
| `compare-wedge` | 26 | *(local)* | 551 → **474** |
| `prefixed-canonical` | 105 | *(local)* | 474 → **297** |
| `dated-slug` | 36 | *(local)* | 297 → **189** |
| `other-slug` | 40 | *(local)* | 189 → **69** |

**Remaining gap:** mostly legacy notes without contract (comparisons, wedges, mechanism stubs) — not README shelf-native clusters yet backfilled.

## Registry dashboard (2026-06-28)

Shipped: `scripts/notes_registry_lib.py` + extended `scripts/reindex_notes.py`.

| Artifact | Path |
| --- | --- |
| Operator dashboard (MD) | `runtime/artifacts/statecraft-notes-registry.md` |
| Machine registry (JSON) | `runtime/artifacts/statecraft-notes-registry.json` |
| Discovery stub | `statecraft/notes/INDEX.md` |

Regenerate: `python3 scripts/reindex_notes.py` · CI/preflight freshness: `python3 scripts/reindex_notes.py --check`.

Tier A health block surfaces orphan / weak-anchor / essay-queue / broken-link counts; Tier B is summary-only in MD.

## Rollout

1. Exemplar notes carry full contract (see statecraft/notes/README.md Note Contract).
2. --warn wired in repo health (non-blocking).
3. --strict --changed-only --tier-a-only fails CI on new/changed Tier A regressions only.
4. Full Tier A strict deferred until corpus backfill (638 warn violations remain; see backfill table above).

## Related

- `scripts/backfill_note_contract_batch.py` — batches: `mou-enforcement` … `other-slug` (discovered: `prefixed-canonical`, `dated-slug`, `other-slug`)
- [transaction-retirement-inventory-2026-06.md](./transaction-retirement-inventory-2026-06.md)
- [statecraft/notes/README.md](../../statecraft/notes/README.md)
