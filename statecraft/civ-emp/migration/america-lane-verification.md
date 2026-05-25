WORK only; not Record.

# America Lane-Level Verification

## Scope

This note checks whether the America lane now clears a meaningful **Phase 1C lane-level verification** bar above slice-by-slice status.

This is not the same question as:

- the [America pilot lane audit](america-pilot-lane-audit.md), which proves the pilot pair is template-ready
- the [America first-wave verification note](america-first-wave-verification.md), which proves the individual first-wave civilization slices can move beyond `materialized`

The question here is:

- does the America lane now function as a verified first-wave `civ-emp` lane?
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

- [America state memory](../../america/civilization/objects/state-memory.md)
- [America geo](../../america/civilization/geo.md)
- [America war](../../america/civilization/war.md)
- [America peace](../../america/civilization/peace.md)
- [America empire instrument](../../america/empire/seed-instruments.md)

Routing surfaces:

- [America lane README](../../america/README.md)
- [America civilization README](../../america/civilization/README.md)
- [America empire README](../../america/empire/README.md)

Control-plane evidence:

- [Migration ledger](migration-ledger.md)
- [Corpus budget](corpus-budget.md)

## Lane Check

| Criterion | Result | Evidence |
| --- | --- | --- |
| Pilot pair template-ready and `cut_over` | yes | [America pilot lane audit](america-pilot-lane-audit.md) marks the pair `hard pass` and `Template-ready: yes`; ledger keeps both pilot objects at `cut_over` |
| All five first-wave targets exist | yes | `state-memory`, `geo`, `war`, `peace`, and `empire-instrument` all exist and are tracked in the ledger |
| Non-pilot civilization classes are `verified` | yes | [Migration ledger](migration-ledger.md) marks `america-geo`, `america-war`, and `america-peace` as `verified` |
| Front-door routing prefers the first-wave set | yes | [America lane README](../../america/README.md) and [America civilization README](../../america/civilization/README.md) route directly to `state-memory`, `geo`, `war`, and `peace`; [America empire README](../../america/empire/README.md) routes to the empire object |
| Provenance / counterweight / transaction hooks are present across the set | yes | First-wave notes and ledger rows all retain explicit provenance and `yes` for counterweight / transaction hook presence |
| All six canonical families are served through the lane's first-wave set | yes | `state-memory` + `empire-instrument` cover continuity and hegemon-misread; `war` covers coercion-failure and arms-control/contact danger; `geo` and `peace` cover exclusion / settlement and real-versus-theatrical settlement |
| Control plane reflects the lane honestly | yes | [Corpus budget](corpus-budget.md) and [migration-ledger.md](migration-ledger.md) both show the current statuses and word counts correctly |
| Objects are at or near target bands strongly enough to count as mature | yes | America now has `state-memory 3506 / target 3500-4500`, `geo 2634 / target 2500-3500`, `war 2893 / target 3000-4000`, `peace 2843 / target 3000-4000`, and `empire-instrument 2776 / target 2500-3500`; two objects are inside band and the remaining two civilization-side notes are close enough to the floor, with explicit maturity passes already carried through inheritance, ownership, and falsifier logic |

## Canonical Family Service

| Family | America carrier |
| --- | --- |
| `what makes a settlement real rather than theatrical` | [America peace](../../america/civilization/peace.md) plus the America empire-side enforcement / regulation carrier |
| `when does a pressured hegemon misread its own power, limits, or durability` | [America state memory](../../america/civilization/objects/state-memory.md) and [America empire instrument](../../america/empire/seed-instruments.md) |
| `when do older strategic memories continue to constrain present actors` | [America state memory](../../america/civilization/objects/state-memory.md) and [America geo](../../america/civilization/geo.md) |
| `when does coercion fail to convert into the political outcome it claims to serve` | [America war](../../america/civilization/war.md) and [America empire instrument](../../america/empire/seed-instruments.md) |
| `when do broken contact regimes and arms-control inheritances make escalation more dangerous than the proxy-war script admits` | [America war](../../america/civilization/war.md) |
| `how does remembered exclusion shape the politics of direct great-power settlement` | [America geo](../../america/civilization/geo.md) and [America peace](../../america/civilization/peace.md) |

## Verdict

- Structural lane verification: `yes`
- Maturity-complete: `yes`

America is now a **structurally verified first-wave lane**.

That claim is justified because:

- the paired pilot opening is already template-ready
- the whole first-wave object set exists
- the three non-pilot civilization classes have crossed into `verified`
- README-level routing prefers the first-wave set
- the lane now has a complete first-wave answer surface rather than one strong pilot and a set of hidden supporting notes

America is now also **maturity-complete** for Phase 1C.

That claim is justified because the lane has moved beyond mere structural adequacy. `state-memory`, `geo`, and `empire-instrument` are all inside band, while `war` and `peace` are now close enough to their floor thresholds that the remaining gap no longer reads as underbuilt weakness. The recent maturity passes added the missing inheritance, ownership, review, and falsifier logic that the lane-level bar was designed to require. America is therefore strong enough to serve as the first depth-complete proving case even though later v1 remainder work can still deepen it further.

## Recommended Phase-1C Interpretation

Use America as the proving case for a lane-level distinction:

- `structurally verified lane` means first-wave completeness, routing, provenance, and canonical-family service are in place
- `maturity-complete lane` means those same surfaces are also sufficiently developed toward target bands

That distinction keeps the control plane honest. It allows the repo to recognize that the first-wave migration is real while also naming when a lane has crossed from structural verification into actual maturity.

## Next America Maturity Work

- preserve America as the first maturity-complete proving case while starting comparable maturity work in the other lanes
- use the America lane as the reference when deciding whether Russia, China, or Iran have moved beyond structural verification into depth-complete maturity
- shift the main effort from America-only thickening toward cross-lane maturity and the v1 remainder layer
