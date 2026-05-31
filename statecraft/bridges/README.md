# Arc-Conditioned CIV-STATE Retrieval

WORK only; not Record.

Purpose: connect speaker-arc interpretation to `civ-state` retrieval without collapsing speaker evidence into generic historical commentary or collapsing `civ-state` into transcript gloss.

This bridge layer is a quiet statecraft substrate. It lives under repo-root `statecraft/`, not on the speaker shelves, because its job is to regulate how statecraft retrieval uses speaker arcs rather than to redefine the arcs themselves.

For the system-wide input and protocol law behind this layer, open [statecraft.md](../statecraft.md).
For the canonical source/synthesis split behind that law, open [Statecraft Archive and Statecraft Synthesis](../archive-synthesis-law.md).

Short constitutional split:

- `speaker shelf` = Statecraft Synthesis object
- `bridge adapter` = statecraft-facing retrieval converter
- `source-archive/statecraft/` = Statecraft Archive source ground

Handoff chain:

`speaker shelf -> speaker claim -> bridge adapter -> civ-state retrieval -> lane translation -> statecraft output`

## Boundary

- Speaker shelves remain authoritative for speaker continuity, pressure, and recurring claims.
- Statecraft Archive remains authoritative for transcript-bearing and provenance-bearing source truth.
- `civ-state` remains the statecraft source base and lane-local translation substrate.
- These bridge notes do not replace lane `helix.md`, transactions, raw-input, PH-CIV, or speaker routing.
- Speaker shelves should not have to secretly perform retrieval conversion.
- Bridge adapters should not become biography shelves or chronology layers.
- Use this layer only when a live speaker claim needs to be converted into disciplined `civ-state` retrieval and then back into lane-local statecraft output.
- Operator-facing trigger: when Persia/Iran already owns the object and the remaining uncertainty is adapter choice rather than lane choice, invoke `statecraft-bridge` as the post-lane bridge workflow.

## Shared Retrieval Algorithm

Use this sequence whenever a live claim needs both speaker interpretation and statecraft source memory:

1. **Speaker claim classification**
   - classify the live claim as primarily `recognition/legitimacy` or `implementation/architecture`
2. **Adapter selection**
   - choose the Marandi-weighted or Parsi-weighted retrieval profile
3. **CIV-STATE retrieval**
   - open the narrowest relevant `civ-state` object first
4. **Lane translation**
   - open the Iran lane surfaces named by the adapter
5. **Counterweight check**
   - force one degradation, overreach, or failure-mode read before output
6. **Output formation**
   - produce either a positional diagnosis or a transaction-oriented artifact

This method is reusable statecraft discipline, not a one-off Iran-war move.

## Terminology Guard

Inside this bridge layer, keep these terms separate:

- `recognition threshold` = what can be politically or morally acknowledged without dishonor
- `settlement durability` = what can survive institutionally as review, guarantee, sequencing, and successor use
- `carry` in bridge usage = institutional carry unless otherwise specified
- `dignity carry` or `successor carry` = the broader Iran-lane civilizational or political-bearing sense

This guard matters because the Iran lane often uses `carry` for civilizational, sovereign, and split-authority bearing capacity, while the bridge layer uses it mainly for mechanism survival. Do not let those meanings collapse into one undifferentiated word.

## How To Read This Layer

Read the bridge in this order:

1. this root note for the method
2. the relevant adapter for the weighting profile
3. [worked examples](worked-examples.md) if the method needs a concrete proof run
4. the lane and transaction surfaces named by the adapter

For the compact doctrine note that explains why the Pape / Marandi / Parsi sequence is valuable as method rather than mere comparison, open [Recognition Threshold Vs Settlement Architecture](recognition-threshold-vs-settlement-architecture.md).

For the month-scale proof run that tests that method against the archive, open [Pape / Marandi / Parsi Backtest - May 2026](pape-marandi-parsi-backtest-may-2026.md).

For the earlier-cycle proof run that tests the same method against a more trap-dominant month, open [Pape / Marandi / Parsi Backtest - April 2026](pape-marandi-parsi-backtest-april-2026.md).

For the earliest hot-war proof run that tests whether the method still works before architecture fully matures, open [Pape / Marandi / Parsi Backtest - March 2026](pape-marandi-parsi-backtest-march-2026.md).

For the strict novelty pass that asks whether the tri-lens yields bridge insights not explicitly present in any single source, open [Pape / Marandi / Parsi Novelty Audit](pape-marandi-parsi-novelty-audit.md).

For the first bounded pressure test of the expanded `statecraft-multi-lens` preset bench, open [Statecraft Multi-Lens Bench Pressure Test - 2026-05](statecraft-multi-lens-bench-pressure-test-2026-05.md).

For the method note that governs when historical examples may support doctrine rather than merely appear in speaker rhetoric, open [Anchored Historical Citation Policy](anchored-historical-citation-policy.md).

## Pilot Pair

V1 is intentionally limited to two adapters:

- [Marandi CIV-STATE retrieval adapter](marandi-civ-state-retrieval-adapter.md)
- [Parsi CIV-STATE retrieval adapter](parsi-civ-state-retrieval-adapter.md)
- [Worked examples](worked-examples.md)

They are the right pilot pair because they repeatedly interpret the same Iran-centered crisis from two different conversion points:

- Marandi: pressure -> legitimacy -> recognition threshold
- Parsi: leverage -> guarantees -> settlement durability

Their combined method is summarized in [Recognition Threshold Vs Settlement Architecture](recognition-threshold-vs-settlement-architecture.md); Pape supplies the trap logic that often precedes both.

## Use Rule

Open these notes when the statecraft problem is not merely "what did the speaker say?" but "how should that kind of speaker claim change what I retrieve, test, and draft from `civ-state`?"

If the task is still just speaker comparison, remain on the speaker shelves.
If the task is already clause design with no need for speaker conditioning, remain on the lane and transaction surfaces.

If the task needs a concrete proof run before reuse, open [worked examples](worked-examples.md).
