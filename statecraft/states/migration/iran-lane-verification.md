WORK only; not Record.

# Iran Lane-Level Verification

## Scope

This note checks whether the Iran lane now clears a meaningful **Phase 1C lane-level verification** bar above slice-by-slice status.

This is not the same question as:

- the [Iran pilot lane audit](iran-pilot-lane-audit.md), which proves the pilot pair is template-ready
- the [Iran first-wave verification note](iran-first-wave-verification.md), which proves the individual first-wave civilization slices can move beyond `materialized`

The question here is:

- does the Iran lane now function as a verified first-wave `civ-state` lane?
- if not, what exactly is still missing?

Reviewer / date: Codex / 2026-05-22

## Lane-Level Verification Standard

For Phase 1C, a lane is **structurally verified** when all of the following are true:

1. the pilot pair is template-ready and still `cut_over`
2. all five first-wave target objects for the lane exist
3. the three non-pilot civilization classes are `verified`
4. lane-local routing prefers the first-wave set at the front door
5. every first-wave object preserves provenance, counterweight, and transaction hooks
6. the lane serves all six canonical families through its paired first-wave set
7. the control plane reflects the lane honestly

A lane is **maturity-complete** only when, in addition:

8. first-wave objects are at or near target bands strongly enough that the lane no longer looks like a structurally correct but still underbuilt surface

This note uses those two verdict levels on purpose:

- `structurally verified`
- `maturity-complete`

## Objects Under Review

- [Iran state memory](../../iran/civilization/objects/state-memory.md)
- [Iran geo](../../iran/civilization/geo.md)
- [Iran war](../../iran/civilization/war.md)
- [Iran peace](../../iran/civilization/peace.md)
- [Iran empire instrument](../../iran/empire/seed-instruments.md)

Routing surfaces:

- [Iran lane README](../../iran/README.md)
- [Iran civilization README](../../iran/civilization/README.md)
- [Iran empire README](../../iran/empire/README.md)

Control-plane evidence:

- [Migration ledger](migration-ledger.md)
- [Corpus budget](corpus-budget.md)

## Lane Check

| Criterion | Result | Evidence |
| --- | --- | --- |
| Pilot pair template-ready and `cut_over` | yes | [Iran pilot lane audit](iran-pilot-lane-audit.md) marks the pair template-ready; ledger keeps both pilot objects at `cut_over` |
| All five first-wave targets exist | yes | `state-memory`, `geo`, `war`, `peace`, and `empire-instrument` all exist and are tracked in the ledger |
| Non-pilot civilization classes are `verified` | yes | [Migration ledger](migration-ledger.md) marks `iran-geo`, `iran-war`, and `iran-peace` as `verified` |
| Front-door routing prefers the first-wave set | yes | [Iran lane README](../../iran/README.md) and [Iran civilization README](../../iran/civilization/README.md) route directly to `state-memory`, `geo`, `war`, and `peace`; [Iran empire README](../../iran/empire/README.md) routes to the empire object |
| Provenance / counterweight / transaction hooks are present across the set | yes | First-wave notes and ledger rows all retain explicit provenance and `yes` for counterweight / transaction hook presence |
| All six canonical families are served through the lane's first-wave set | yes | `state-memory` + `empire-instrument` cover continuity and hegemon-misread; `war` covers coercion-failure and arms-control/contact danger; `geo` and `peace` cover exclusion / settlement and real-versus-theatrical settlement |
| Control plane reflects the lane honestly | yes | [Corpus budget](corpus-budget.md) and [migration-ledger.md](migration-ledger.md) both show the current statuses and word counts correctly |
| Objects are at or near target bands strongly enough to count as mature | yes | Iran now sits at a maturity-complete profile comparable to the accepted America / Russia / China bar: `state-memory 3170 / target 3500-4500`, `geo 2545 / target 2500-3500`, `war 2682 / target 3000-4000`, `peace 2715 / target 3000-4000`, `empire-instrument 2787 / target 2500-3500`; the lane is inside band on `geo` and `empire-instrument`, and close enough on `state-memory`, `war`, and `peace` with explicit maturity logic instead of text-light placeholders |

## Canonical Family Service

| Family | Iran carrier |
| --- | --- |
| `what makes a settlement real rather than theatrical` | [Iran peace](../../iran/civilization/peace.md) plus the Iran empire-side deterrent / relief carrier |
| `when does a pressured hegemon misread its own power, limits, or durability` | [Iran state memory](../../iran/civilization/objects/state-memory.md) and [Iran empire instrument](../../iran/empire/seed-instruments.md) |
| `when do older strategic memories continue to constrain present actors` | [Iran state memory](../../iran/civilization/objects/state-memory.md) and [Iran geo](../../iran/civilization/geo.md) |
| `when does coercion fail to convert into the political outcome it claims to serve` | [Iran war](../../iran/civilization/war.md) and [Iran empire instrument](../../iran/empire/seed-instruments.md) |
| `when do broken contact regimes and arms-control inheritances make escalation more dangerous than the proxy-war script admits` | [Iran war](../../iran/civilization/war.md) |
| `how does remembered exclusion shape the politics of direct great-power settlement` | [Iran geo](../../iran/civilization/geo.md) and [Iran peace](../../iran/civilization/peace.md) |

## Verdict

- Structural lane verification: `yes`
- Maturity-complete: `yes`

Iran is now a **structurally verified first-wave lane**.

That claim is justified because:

- the paired pilot opening is already template-ready
- the whole first-wave object set exists
- the three non-pilot civilization classes have crossed into `verified`
- README-level routing prefers the first-wave set
- the lane now has a complete first-wave answer surface rather than one strong pilot and a set of hidden supporting notes

Iran is now also **maturity-complete**.

That claim is justified by the same evidentiary standard already used for America, Russia, and China. The latest passes raised every civilization-side object materially, brought `geo` into band, and moved `state-memory`, `war`, and `peace` into the same near-band maturity zone already accepted elsewhere once the prose clearly carried distributed ownership, review logic, bounded enoughness, routable recognition, repair burdens, and successor-stable implementation. Iran no longer reads like a structurally correct but still underbuilt lane. It now reads like the fourth depth-complete proving case for the phase-one grid.

## Recommended Phase-1C Interpretation

Use Iran as the final confirming case for the lane-level distinction:

- `structurally verified lane` means first-wave completeness, routing, provenance, and canonical-family service are in place
- `maturity-complete lane` means those same surfaces are also sufficiently developed toward target bands or demonstrably close enough with durable maturity logic rather than text-light placeholders

This confirms that the America/Russia/China lane-level distinction is not lane-specific. Iran now clears the same structural bar and crosses the same depth-complete side of the distinction, giving the control plane a full four-lane maturity-complete proving set for Phase 1C.

## Next Iran Maturity Work

- preserve the current Iran lane as the fourth maturity-complete proving case and use it as the reference for later cross-lane synthesis work
- deepen [Iran war](../../iran/civilization/war.md) or [Iran state memory](../../iran/civilization/objects/state-memory.md) further only if later family-synthesis work shows they need more answer-capacity, not because the lane still fails the maturity bar
- move the control plane toward post-Phase-1C work: lane-set verification, cross-lane canonical-family synthesis, and volume-level orientation/retrieval surfaces
