---
name: state-deploy
preferred_activation: state-deploy
description: "Deploy a live object to the right academy-statecraft lane. Use when the operator says state-deploy, deploy statecraft, which lane, which state skill, or asks whether a problem belongs to America, China, Persia, Russia, a two-lane comparison, or a cross-lane compact."
---

# State Deploy

`state-deploy` is the academy-statecraft deployment skill. It is a router with judgment, not a fifth civilizational lane.

Use it to decide which substantive lane should carry a live object now, whether the object is lane-local or cross-lane, and what work shape should open first.

## Boundary

- WORK only; not Record.
- Do not restate America, China, Persia, or Russia doctrine in full.
- Do not replace lane READMEs, helixes, or transactions.
- Do not become a generic geopolitics commentary mode.
- Keep the handoff explicit: deployment judgment first, substantive drafting second.

## Source Surfaces

Open these first when the deployment call needs grounding:

1. `codex/academy/statecraft/README.md`
2. `codex/academy/statecraft/METHOD.md`
3. `codex/academy/statecraft/civ-emp/README.md`
4. `codex/academy/statecraft/sheets/transaction-router.md`

Use the lane front doors only as needed for the deployment judgment:

- `codex/academy/statecraft/america/README.md`
- `codex/academy/statecraft/china/README.md`
- `codex/academy/statecraft/iran/README.md`
- `codex/academy/statecraft/russia/README.md`

## Decision Rules

Use these tests in order:

1. **Authority test** - whose legitimacy grammar governs the object?
2. **Carrier test** - which state can actually carry the instrument?
3. **Arena test** - is this lane-local or a cross-lane compact?
4. **Maturity test** - is the object still orientation, comparison, or draftable instrument?
5. **Depth test** - should the next move be one lane, two-lane comparison, or multi-lane compact?

## Routing Contract

- Route to `state-america` when lawful authority, burden-sharing, bounded coercion, or successor-stable settlement is central.
- Route to `state-china` when continuity, order, anti-disorder legitimacy, route stability, or quiet leverage is central.
- Route to `state-persia` when dignity, sovereignty, recognition, leverage under pressure, or verification without humiliation is central.
- Route to `state-russia` when depth, parity, anti-managed humiliation, disruption, or equilibrium-bearing recognition is central.
- Route to a comparison or compact only when no single lane can honestly own the object.

## Default Output

When invoked without a settled lane, output exactly this shape:

```markdown
**State Deploy**
- Live object:
- Why lane choice matters:
- Deployment judgment:
- Recommended handoff:

**Deploy Menu - reply A-D**
A. [single-lane handoff]
B. [two-lane comparison]
C. [compact or objection-matrix path]
D. [transaction or stress-test path]
```

The options must be specific to the named object. Do not use generic labels like `more analysis`.

## Handoff Rule

When the operator replies with a letter after a `state-deploy` output, execute that calibrated path rather than reprinting the menu.

- `A` = recommended single-lane handoff
- `B` = two-lane comparison
- `C` = compact / comparison surface
- `D` = transaction or stress-test path

## Recursive-Update Membrane

If a deployment call exposes a durable cross-lane pattern, compact type, or routing lesson, suggest a reviewable update candidate. Do not directly rewrite lane books from the deployment turn.

Live work may suggest candidates, but must not directly rewrite:

- `helix.md`
- `civilization/`
- `empire/`
- `state/`
- `transactions/`

Stage lane-local discoveries in the relevant `<lane>/updates/pending.md`.
