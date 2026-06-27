WORK only; not Record.

# Five-speaker statecraft shelf normalization - 2026-05-25

Purpose: record the new canonical shelf law after the Freeman, Crooke, Mercouris, Macgregor, and Ritter normalization pass.

## What is now true

These five speakers now sit at one canonical 2026 shelf level under `statecraft/voices/`:

- [Freeman](../../../statecraft/voices/civ-lens-freeman/README.md)
- [Crooke](../../../statecraft/voices/civ-lens-crooke/README.md)
- [Mercouris](../../../statecraft/voices/civ-lens-mercouris/README.md)
- [Macgregor](../../../statecraft/voices/civ-lens-macgregor/README.md)
- [Ritter](../../../statecraft/voices/civ-lens-ritter/README.md)

Shared shelf law:

- canonical home under `statecraft/voices/civ-lens-<speaker>/`
- `README.md` and `index.md` front doors
- arc, routing note, source index, and crossing surface
- speaker-owned support spine
- bounded monthly synthesis ladder for `2026-01` through `2026-05`
- historical audit and `themes/README.md`
- codex front doors reduced to compatibility pointers

## What remains codex-side

The normalization did not erase all codex residue.

- Freeman still has legacy continuity residue like [freeman-thread.md](../../../statecraft/voices/freeman/freeman-thread.md) and [freeman-transcript.md](../../../statecraft/voices/freeman/freeman-transcript.md).
- Crooke still has verbatim carryover residue like [crooke-transcript.md](../../../statecraft/voices/crooke/stream/crooke-transcript.md).
- Ritter still has the largest remaining codex-side pressure under [statecraft/voices/ritter/stream/](../../../statecraft/voices/ritter/stream), where month cross-host arcs, forecast surfaces, thread files, transcript files, pages, and manifests still coexist beside the new canonical statecraft shelf.

## Next migration pressure point

The next clean wedge is Ritter codex-stream residue, not more outer-shelf architecture.

Smallest credible next pass:

- decide which Ritter `statecraft/voices/ritter/stream/` files are true compatibility residue
- demote those files explicitly
- preserve only the minimum continuity needed while keeping the canonical shelf in `statecraft/voices/civ-lens-ritter/` as the first-open route

## Validation note

`validate_skills.py` passed during the normalization pass.

Speaker validators still report older repo-wide codex issues outside this wedge. Treat those as background cleanup, not as evidence that the five-speaker shelf law failed.
