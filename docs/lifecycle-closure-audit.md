# Lifecycle Closure Audit

WORK documentation. Not Record.

Purpose: turn "where does this thing end its life?" into an explicit lens for completion, false completion, and closeout ownership.

## Relation To Architectural Fullness

This note is a supporting lens under [architectural-fullness.md](architectural-fullness.md), not a replacement for it.

`Fullness Before Closure` asks whether a surface has enough architecture to be treated as settled.

`Lifecycle Closure Audit` asks whether the objects moving through that surface actually reach a valid terminal state.

Short fit:

- architectural fullness = is the surface mature enough to close?
- lifecycle closure = did the object moving through it end in the right place?

Use this note when the higher-level closure doctrine is already right, but a subsystem still needs a sharper answer to "what is the real terminal state here?"

## Core Pattern

Use this compact sequence:

`object -> lifecycle -> valid terminal states -> false terminal states -> closeout owner`

The point is to make completion legible.

## What To Ask

For any architectural object, answer four questions:

1. What lifecycle does this object have?
2. Which terminal states are valid?
3. Which states only look terminal but are actually incomplete?
4. Which surface owns the completion check?

If those questions cannot be answered cleanly, closure is still thin.

## Valid And False Terminal States

A valid terminal state is one where the object has reached the surface that is meant to carry its durable architectural role.

A false terminal state is one where the object feels done because it was stored, named, mentioned, or routed nearby, but it has not actually reached the surface that owns closure.

Typical false-terminal patterns:

- `stored but not routed`
- `mentioned but not integrated`
- `found but never materialized`
- `template opened before object maturity`
- `important enough to keep` confused with `finished enough to close`

## First Concrete Applications

This lens already has three clear applications in the repo:

1. **Raw-input wiring**
   A valid materialized speaker capture does not end its life in `raw-input/`. Storage is an intermediate state; routed visibility is the real terminal state.
2. **Speaker routing**
   A speaker appearance does not end its life as a lattice mention, a discovery-memory note, or passing prose. It ends in the correct host lane, speaker bench, or comparable routed surface.
3. **Statecraft transaction threshold**
   A crisis note does not end its life as a transaction just because it is important or well written. It may validly end as commentary, braid, memo, objection matrix, router candidate, or, when the threshold is met, a true transaction.

## Compact Review Checklist

Use this review pass when a repo surface feels complete but may still be under-architected:

1. Name the object.
2. Describe its lifecycle in one short sentence.
3. List the valid terminal states.
4. List the false terminal states.
5. Name the surface that owns the closeout decision.
6. Check whether the current object has actually reached one of the valid terminal states.

If step 6 is unclear, the work is not ready to close.

## Boundary

This doctrine is meant to sharpen completion logic, not to force every note into heavy process language.

Use explicit lifecycle wording where it catches false completion. Elsewhere, the same logic may be expressed through ownership, obligations, and closeout rules.
