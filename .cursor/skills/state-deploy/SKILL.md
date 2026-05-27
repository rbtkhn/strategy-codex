---
name: state-deploy
preferred_activation: state-deploy
description: "Deploy a live object to the right statecraft lane. Use when the operator says state-deploy, deploy statecraft, which lane, which state skill, or asks whether a problem or named recent event belongs to America, China, Persia, Russia, a two-lane comparison, or a cross-lane compact."
---

# State Deploy

`state-deploy` is the repo-root statecraft deployment skill. It is a router with judgment, not a fifth civilizational lane.

Use it to decide which substantive lane should carry a live object now, whether the object is lane-local or cross-lane, and what work shape should open first.

Short doctrine: `state-deploy` decides the lane. The `state-*` skills decide the instrument.

## Boundary

- WORK only; not Record.
- Verify unstable facts first when the object is a named recent event.
- Do not restate America, China, Persia, or Russia doctrine in full.
- Do not replace lane READMEs, helixes, or transactions.
- Do not become a generic geopolitics commentary mode.
- Keep the handoff explicit: deployment judgment first, substantive drafting second.

## Constitutional Split

`state-deploy` is the routing layer. Its job is to answer `who owns this object now?`

The `state-*` skills are the substantive lane layer. Their job is to answer `what can this owner legitimately draft, carry, accept, reject, and institutionalize?`

Preserve that split:

- `state-deploy` chooses lane, arena, depth, and work shape.
- `state-deploy` may recommend one lane, two-lane comparison, or compact path.
- `state-deploy` must not become a fifth lane or a substitute for lane doctrine.
- `state-*` skills inherit once the handoff is clear and do the actual civilizational drafting.

## Source Surfaces

Open these first when the deployment call needs grounding:

1. `statecraft/README.md`
2. `statecraft/METHOD.md`
3. `statecraft/civ-emp/README.md`
4. `statecraft/sheets/transaction-router.md`

Use the lane front doors only as needed for the deployment judgment:

- `statecraft/america/README.md`
- `statecraft/china/README.md`
- `statecraft/iran/README.md`
- `statecraft/russia/README.md`

## Named Recent Event Rule

There is no longer a separate `current-event` function.

When the operator names a recent event, absorb it here:

1. verify date, actors, location, and what happened with current sources;
2. separate fact from interpretation briefly;
3. name the crisis object before lane judgment;
4. then run the normal deployment tests.

If lane ownership is already obvious after verification, hand directly to the owning `state-*` lane. If not, keep the deployer in charge.

If the event is verified but the governing layer is still being confused with lane ownership, use `statecraft-framework` as the pre-handoff diagnosis rather than guessing from salience.

## Decision Rules

Use these tests in order:

1. **Authority test** - whose legitimacy grammar governs the object?
2. **Carrier test** - which state can actually carry the instrument?
3. **Arena test** - is this lane-local or a cross-lane compact?
4. **Maturity test** - is the object still orientation, comparison, or draftable instrument?
5. **Depth test** - should the next move be one lane, two-lane comparison, or multi-lane compact?

Ask one transaction-aware reuse question before you widen the pass:

- does this object already resemble a known transit, guarantee, sanctions, quarantine, recognition, or settlement bundle strongly enough that the honest next move is fit-check or reuse rather than a fresh framework?

Use `statecraft-framework` only after the deployer can already name the live object honestly. Use it to clarify the governing pair, not to replace lane judgment.

## Misdeployment Warnings

`state-deploy` is most likely to drift when it mistakes:

- salience for ownership
- speaker force for lane ownership
- transaction maturity for real instrument readiness
- a cross-lane compact for something that has already been honestly owned by one lane
- a Persia/Iran bridge step for an ownership decision that has not yet been made

The deployer should slow down whenever the object sounds vivid before its legitimacy grammar, carrier, and arena are actually stable.

When that happens, run a short false-elegance check:

- what lane would a headline reader choose too quickly?
- what lane would a mechanism drafter choose too quickly?
- which ownership call still makes the next retrieval surface more obvious than the others?

## False-Ownership Recognizers

Use these corrections when the first instinct is probably wrong:

- `Taiwan quarantine`
  - do not route to Persia just because blockade or chokepoint language feels familiar
  - settle whether the object is quarantine, maritime access, customs exclusion, or convoy logic first
  - comparison or America-first ownership is more honest than a premature bridge call
- `Hormuz recognition transit`
  - Persia usually owns the object first
  - use the bridge only if speaker-conditioning remains unresolved after Persia ownership is already clear
- `sanctions relief and guarantees`
  - open the lane that must carry the guarantee architecture
  - do not route by commentator intensity or rhetorical fluency alone

## Routing Contract

- Route to `state-america` when lawful authority, burden-sharing, bounded coercion, or successor-stable settlement is central.
  Fast America signals: lawful-authority strain, burden-sharing or coalition-carriage problems, coercive-success but settlement-conversion problems, and clock-driven overreach risk under superior force.
- Route to `state-china` when continuity, order, anti-disorder legitimacy, route stability, or quiet leverage is central.
  Fast China signals: flow or corridor stabilization problems, visible-disorder ownership traps, administrative-carry questions, and market-calming needs without overt coercive theater.
- Route to `state-persia` when dignity, sovereignty, recognition, leverage under pressure, or verification without humiliation is central.
  Fast Persia signals: supervision-before-recognition sequencing, dignity pressure, reversible relief traps, and chokepoint or survivability leverage under coercive time pressure.
- Route to `state-russia` when depth, parity, anti-managed humiliation, disruption, or equilibrium-bearing recognition is central.
  Fast Russia signals: parity pressure, compliance-before-recognition sequencing, depth or buffer shrinkage, and escalation-calendar or entrapment traps.
- Route to a comparison or compact only when no single lane can honestly own the object.

If the crisis object is already strongly mechanism-shaped, the deployer should say so early and recommend transaction-aware reuse rather than pretending the first need is broad orientation.

Do not call `statecraft-bridge` from the deployer unless Persia/Iran ownership is already clear. If ownership is still contested, hand back to a lane judgment or comparison call first.

When ownership is clear but pair diagnosis is not, hand to the owning lane with an explicit note to run `statecraft-framework` before narrow descent.

## Default Output

When invoked without a settled lane, output exactly this shape:

```markdown
**State Deploy**
- Live object:
- Why lane choice matters:
- Deployment judgment: [single-lane ownership / comparison required / compact path after ownership split / transaction-aware reuse]
- Recommended handoff: [owning lane / comparison / compact path / transaction-fit check]

**Deploy Menu - reply A-D**
A. [single-lane handoff]
B. [two-lane comparison]
C. [compact or objection-matrix path]
D. [transaction or stress-test path]
```

The options must be specific to the named object. Do not use generic labels like `more analysis`.
Each option must reflect a genuinely different honest next move:

- `A` = owning lane handoff
- `B` = comparison because ownership is genuinely contested
- `C` = compact / objection path only after ownership is understood
- `D` = transaction / stress-test / mature-object reuse

Make the `Deployment judgment` line sound like a real decision, not a category reminder. Make the `Recommended handoff` line name the next surface or move directly.

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
