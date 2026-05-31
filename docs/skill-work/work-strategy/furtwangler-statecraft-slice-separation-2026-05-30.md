# Furtwangler statecraft slice separation - 2026-05-30

WORK only; not Record.

Purpose: record the main unresolved contradiction visible in the current `strategy-codex` tree after the recent CIV-STATE runs, and name the next bounded ship without pretending the broader disorder is already solved.

## Main contradiction

The repo is not mainly suffering from shapeless noise. It is carrying **more than one real coherence at once** inside the same dirty worktree.

Two distinct slices are live:

- a **CIV-STATE doctrine hardening slice** centered on the constitutional layer
- a **statecraft daily/archive method slice** centered on synthesis doctrine, proof fixtures, and archive-index support

The danger is not that either slice lacks substance. The danger is that they blur together and then force one commit to carry two different kinds of judgment.

## What the separation showed

The first slice proved clean enough to ship on its own:

- [statecraft/README.md](/C:/dev/strategy-codex/statecraft/README.md)
- [statecraft/civ-state/README.md](/C:/dev/strategy-codex/statecraft/civ-state/README.md)
- [statecraft/civ-state/power-truth-time-annex.md](/C:/dev/strategy-codex/statecraft/civ-state/power-truth-time-annex.md)
- [statecraft/civ-state/power-truth-time-retrieval-checklist.md](/C:/dev/strategy-codex/statecraft/civ-state/power-truth-time-retrieval-checklist.md)
- [statecraft/civ-state/civilization-empire-faith-science-memory-desire-retrieval-checklist.md](/C:/dev/strategy-codex/statecraft/civ-state/civilization-empire-faith-science-memory-desire-retrieval-checklist.md)
- [statecraft/civ-state/ph-civ-to-civ-state-bridge.md](/C:/dev/strategy-codex/statecraft/civ-state/ph-civ-to-civ-state-bridge.md)
- [statecraft/civ-state/era-hardening-checklist.md](/C:/dev/strategy-codex/statecraft/civ-state/era-hardening-checklist.md)
- [statecraft/civ-state/ph-civ-era-overlay-options.md](/C:/dev/strategy-codex/statecraft/civ-state/ph-civ-era-overlay-options.md)

That pass is now durably isolated in commit `5dcaaa52`.

The second slice is also real, but different in kind. Its visible center is:

- [statecraft/daily/README.md](/C:/dev/strategy-codex/statecraft/daily/README.md)
- [statecraft/daily/METHOD.md](/C:/dev/strategy-codex/statecraft/daily/METHOD.md)
- [statecraft/daily/2026-05.md](/C:/dev/strategy-codex/statecraft/daily/2026-05.md)
- [statecraft/daily/2026-05-29.md](/C:/dev/strategy-codex/statecraft/daily/2026-05-29.md)
- [statecraft/daily/2026-05-30.md](/C:/dev/strategy-codex/statecraft/daily/2026-05-30.md)
- [statecraft/bridges/statecraft-multi-lens-bench-pressure-test-2026-05.md](/C:/dev/strategy-codex/statecraft/bridges/statecraft-multi-lens-bench-pressure-test-2026-05.md)
- [statecraft/civ-lens/macgregor/macgregor-support-spine-2025-2026.md](/C:/dev/strategy-codex/statecraft/civ-lens/macgregor/macgregor-support-spine-2025-2026.md)

This is not spillover from the doctrine pass. It is a separate synthesis-and-method ship.

## Recommended next bounded ship

Ship the statecraft daily/archive method slice next, but keep it bounded to:

- daily shelf doctrine
- monthly and daily proof fixtures
- bridge/support notes that directly explain or validate that shelf
- archive index updates that are necessary for those notes to be truthful and navigable

Do not let that ship absorb unrelated skill edits, cadence edits, or ambient archive churn that is not actually part of the method surface.

## Falsifier

This note is wrong if the remaining statecraft daily/archive files turn out not to compress into one coherent method pass, or if the next clean staging attempt needs to pull large unrelated files from outside that synthesis cluster to make the ship honest.

### Conductor close
- **Stance / conductor:** furtwangler
- **Object:** separate the CIV-STATE doctrine hardening ship from the rival statecraft daily/archive method ship
- **What moved / seam:** The repo's main tension is now named correctly: not one blurry statecraft mess, but two real slices that needed different commits. The first is durably shipped; the second is now the honest next bounded move.
- **Falsify / next test:** If the next staging pass for the daily/archive cluster cannot stay centered on daily doctrine, proof fixtures, bridge support, and necessary archive indexes, then this separation was premature or misdrawn.
- **Next wedge:** stage and review the statecraft daily/archive method slice on its own, with no opportunistic spill-in from unrelated skill or cadence changes.
