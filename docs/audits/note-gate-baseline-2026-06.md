# Note gate baseline audit (2026-06)

Shadow-mode inventory before strict enforcement. Generated from check_statecraft_notes.py --warn.

## Summary

- **Date:** 2026-06-28
- **Command:** python3 scripts/check_statecraft_notes.py --warn
- **Result:** check_statecraft_notes (warn): 796 violation(s) across 328 note(s)
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

_… and 756 more._

## Rollout

1. Exemplar notes carry full contract (see statecraft/notes/README.md Note Contract).
2. --warn wired in repo health (non-blocking).
3. --strict --changed-only --tier-a-only fails CI on new/changed Tier A regressions only.
4. Full Tier A strict deferred until corpus backfill.

## Related

- [transaction-retirement-inventory-2026-06.md](./transaction-retirement-inventory-2026-06.md)
- [statecraft/notes/README.md](../../statecraft/notes/README.md)
