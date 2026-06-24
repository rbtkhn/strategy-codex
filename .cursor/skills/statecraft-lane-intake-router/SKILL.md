---
name: statecraft-lane-intake-router
description: Open transcript-grounded intake menus for repo-root statecraft lanes before helix, state, bridge, or transaction drafting. Use when the operator enters America, China, Persia, or Russia statecraft and the next honest move is to choose the governing transcript-bearing intake family rather than jump straight to polished lane surfaces.
preferred_activation: statecraft-lane-intake-router
activation: statecraft-lane-intake-router
category: domain-pack
status: active
scope_class: repo-governed
---
# Statecraft Lane Intake Router

Use this skill when a statecraft lane is already known, but the lane still needs a truthful first intake menu.

This skill exists to stop lane entry from skipping directly into `helix`, `state`, `transactions`, or a polished bridge split before the transcript-bearing intake layer has actually been resolved.

## Core law

The live intake sequence is:

`Statecraft Source Archive -> transcript-bearing intake family -> host law / synthesis if needed -> bridge if needed -> lane drafting`

That is the governing law for lane entry.

The first honest submenu should ask which transcript-grounded intake family governs now, not which downstream lane note looks most elegant.

## Use this skill when

- the operator says `statecraft america`, `statecraft china`, `statecraft persia`, or `statecraft russia`
- lane ownership is already clear
- the next move is choosing host or speaker intake families
- the assistant is about to generate a lane menu
- a previous menu drifted too quickly into doctrine-first or transaction-first branching

## Do not use this skill when

- lane ownership is unresolved — use inline deploy judgment via [`transaction-router.md`](../../../statecraft/sheets/transaction-router.md), a direct `state-*` lane pick, or archived [`state-deploy`](../state-deploy/SKILL.md) legacy one-turn routing
- the object is already clearly cross-lane or objection-shaped and belongs in `compact`
- the operator explicitly wants a downstream lane surface such as `helix`, `state`, or `transactions`
- the operator is explicitly asking for CIV-STATE retrieval rather than lane intake
- the operator is explicitly writing a volume chapter or book surface

## Output law

When this skill triggers, the first lane reply should have three parts:

1. one short lane identity line
2. one short statement of the real intake bottleneck
3. a fixed `A-D` intake menu

Do not lead with a deeper doctrinal summary when the operator really needs the intake split.

If chronology or continuity from prior days is the real bottleneck, name `/codex` as the continuity layer beneath `statecraft/`, but do not substitute it for transcript-family routing.

## Menu law

The menu should be transcript-grounded and intake-specific.

It should not default to:

- `Helix`
- `State`
- `Transactions`
- `Bridge`

unless the intake layer is already resolved.

Those are downstream surfaces.

## Lane-specific intake families

### America

Use this submenu:

- `Davis` - feasibility, bargaining geometry, and whether command can still produce room
- `Napolitano` - authorization, constitutional carry, legal absurdity, and procedural collapse
- `Pape` - coercive leverage, escalation timing, and whether pressure is changing the adversary's room
- `Parsi` - off-ramp design, sanctions-relief sequencing, protected channels, and successor-stable settlement

Default logic:

- choose `Davis` when the problem is practical room
- choose `Napolitano` when the problem is authority or legality
- choose `Pape` when the problem is coercive leverage or escalation clocks
- choose `Parsi` when the problem is settlement design or off-ramp architecture

### China

Use this submenu:

- `Jiang` - China-facing strategic framing, regime reading, and civilizational self-description
- `Sachs` - system-economic effects, sanctions spillover, and energy / market disorder
- `Crooke / Diesen` - order transition, anti-coercion structure, and civilizational-system comparison
- `Pape` - shock clocks, coercive leverage, and adversary pressure timing

Default logic:

- choose `Jiang` for internal Chinese frame and self-description
- choose `Sachs` for world-system and market spillover
- choose `Crooke / Diesen` for order-transition and anti-coercion structure
- choose `Pape` for pressure timing and coercive stress

### Persia

Use this submenu:

- `Marandi` - recognition-first, legitimacy-first, sovereignty-pressure, and anti-humiliation reads
- `Parsi` - settlement-first, guarantee-first, architecture, and sanctions-relief sequencing
- `Pape` - fourth-center leverage, shortage clocks, and coercive-system stress
- `Crooke / Ritter` - Western misreading, regime-change skepticism, and military-risk classification

Default logic:

- choose `Marandi` when the problem is dignity and recognition
- choose `Parsi` when the problem is settlement architecture
- choose `Pape` when the problem is leverage under scarcity or system stress
- choose `Crooke / Ritter` when the problem is misreading, regime-change pressure, or military danger

### Russia

Use this submenu:

- `Crooke` - order rupture, Western misreading, and restoration-pressure interpretation
- `Diesen` - multipolar structure, recognition geometry, and anti-hegemonic system framing
- `Ritter / Macgregor / Martyanov` - force constraints, escalation limits, and overbinding risk
- `Parsi / Freeman` - settlement architecture, recognition formula, and diplomatic carry

Default logic:

- choose `Crooke` for order rupture and restoration pressure
- choose `Diesen` for system structure and recognition geometry
- choose `Ritter / Macgregor / Martyanov` for force limits and overbinding risk
- choose `Parsi / Freeman` for settlement architecture and diplomatic carry

## Recommended output shape

Use this structure:

```markdown
**[Lane] Statecraft**
- Lane identity:
- Core intake question:
- Best default read:

**[Lane] Intake Menu - reply A-D**
A. ...
B. ...
C. ...
D. ...
```

The `Best default read` line should name one intake family, not a downstream lane note.

## Bridge rule

Use a bridge only after the intake family is already known and the remaining uncertainty is retrieval posture, weighting, or settlement-vs-recognition conversion.

Do not use the bridge as a substitute for intake.

## Handoff rule

After the operator replies with a letter:

- open the chosen intake family directly
- explain briefly why it governs now
- only then descend toward `helix`, `state`, `transactions`, or a bridge if that second move is actually warranted

Do not regenerate the same lane menu unless the operator asks to restart.

## Failure modes

Avoid these:

- lane menu opens with `Helix / State / Transactions / Bridge`
- lane menu ignores transcript-bearing host or speaker intake
- lane menu uses elegant doctrine labels with no source-bearing grounding
- bridge opens before the intake family is actually known
- lane summary replaces the actual routing question

## Canonical companions

- repo-root front door: [statecraft/README.md](../../../statecraft/README.md)
- source-truth layer: [source-archive/README.md](../../../source-archive/README.md)
- continuity layer: [codex/README.md](../../../codex/README.md)
- speaker synthesis home: [statecraft/voices/README.md](../../../statecraft/voices/README.md)
- host-law layer: [statecraft/hosts/README.md](../../../statecraft/hosts/README.md)
- lane front doors:
  - [America](../../../statecraft/america/README.md)
  - [China](../../../statecraft/china/README.md)
  - [Persia](../../../statecraft/persia/README.md)
  - [Russia](../../../statecraft/russia/README.md)

## Routing law

This skill routes objects; it does not process them.

A successful route names the next surface or skill. It does not silently perform the downstream work.

## Verification / Proof Standard

Do not call this complete unless:

- the incoming object is named
- the candidate lane or route family is named
- the source floor or evidence basis is named
- the output class is named: routing recommendation, lane handoff, no-route verdict, runbook handoff, or advisory memo
- the authority boundary is stated: advisory routing only, no archive write, no synthesis write, no transaction creation, no Record-facing change
- uncertainty, missing evidence, stale context, or competing route candidates are stated

Evidence to report:

- files, indexes, or route maps read
- candidate lanes considered
- final recommended route and rejected alternatives
- downstream skill, runbook, or surface named
- confidence downgrade, if any

If verification cannot be completed:

- state what was not verified
- do not create or modify lane surfaces
- do not publish, promote, merge, or create a transaction object
- return a bounded routing recommendation for operator review
