---
name: ph-civ-to-civ-state-promoter
preferred_activation: ph-civ-to-civ-state-promoter
description: >-
  Promote or evaluate public PH-CIV insight for CIV-STATE use. Use when the
  operator wants to decide whether a `ph-civ` chapter, card, corridor,
  commentary, or pattern should become a reusable `civ-state` mechanism; when a
  destination family must be chosen; or when a counterweight is needed before
  escalating into bridge doctrine, the promotion ledger, or the CIV-STATE
  review queue.
---

# PH-CIV to CIV-STATE Promoter

Use this skill to decide whether a public `ph-civ` insight deserves promotion into `civ-state`, and if so, where it should land.

This is a **membrane and conversion** skill. Its job is not to author PH-CIV and not to silently mutate CIV-STATE. Its job is to make the conversion step explicit, bounded, and auditable.

## Use this skill when

- a `ph-civ` chapter, card, corridor, commentary, or route seems to expose a reusable mechanism
- the operator wants to know whether an insight belongs in `ph-civ`, the promotion ledger, bridge doctrine, or the CIV-STATE review queue
- a destination family must be chosen among `civilization`, `empire`, `statecraft`, `geo-strategy`, `secret-history`, or `game-theory`
- a proposed insight feels strong but risks propaganda, false analogy, or overreach
- the membrane between public pattern and local doctrine needs a compact, disciplined judgment

## Do not use this skill when

- the task is simply summarizing a PH-CIV lecture or commentary surface
- the task is direct writing of a CIV-STATE chapter that already has a settled destination and mechanism
- the operator wants transaction drafting, lane routing, or statecraft diagnosis rather than membrane judgment
- the task is raw review-queue processing without a PH-CIV source question

## Core law

- `ph-civ` exposes
- `civ-state` distills
- `statecraft` drafts

The bridge is **mechanism transfer**, not transcript transfer.

Promotion is valid only when a public pattern survives compression into a reusable civilization-state mechanism with a real counterweight.

## Destination families

Valid destination families include:

- `civilization-<civ>.md`
- `empire-<civ>.md`
- `statecraft-<civ>.md`
- `geo-strategy-<civ>.md`
- `secret-history-<civ>.md`
- `game-theory-<civ>.md`
- sacred grammar
- state-memory
- review queue

## Promotion test

Before promoting anything, answer these in order:

1. What exactly is the public source surface?
2. What mechanism is actually extractable?
3. Does it survive compression out of lecture-local rhetoric?
4. What CIV-STATE destination family best fits it?
5. What counterweight prevents overreach or false analogy?

If the answer to `2`, `3`, or `5` is weak, do not promote yet.

## Workflow

1. **Name the PH-CIV source precisely.**
   Use chapter, card, corridor, commentary, route, or other source type clearly.

2. **Strip away commentary-local scaffolding.**
   Remove lecture sequencing, review caveats, rhetorical flourishes, and narrow news-moment framing.

3. **Compress to mechanism.**
   Rewrite the insight as one of:
   - continuity
   - legitimacy
   - geography / carrying condition
   - strategic interaction
   - symbolic activation
   - projection / overreach
   - present-tense diplomatic synthesis

4. **Choose the narrowest destination family.**
   Prefer the most exact landing surface rather than a vague volume-level destination.

5. **Add a counterweight.**
   State what keeps the pattern from hardening into:
   - propaganda
   - civilizational vanity
   - flat determinism
   - one-factor causality
   - false analogy

6. **Choose the membrane surface.**
   - still mainly public reading aid -> leave in `ph-civ`
   - mechanism plausible but not settled -> promotion ledger
   - bridge method needs tightening -> bridge doctrine
   - real upstream CIV-STATE mutation warranted -> review queue

## Family choice heuristics

- Use `civilization-<civ>` when the mechanism is continuity-bearing order or legitimacy-bearing civilizational core.
- Use `empire-<civ>` when the mechanism is outward instrument, projection stack, burden, or overreach.
- Use `statecraft-<civ>` when the mechanism is a present-tense diplomatic synthesis rather than a single lens.
- Use `geo-strategy-<civ>` when geography is the carrying pressure.
- Use `secret-history-<civ>` when hidden memory or symbolic activation is doing the work.
- Use `game-theory-<civ>` when recurring incentives, bargaining structure, or escalation logic are load-bearing.

## Failure modes

Avoid:

- moving lecture rhetoric across the membrane unchanged
- promoting unstable forecast language into doctrine
- treating one vivid example as a civilization-state mechanism by default
- choosing a destination family because it sounds grander rather than because it is structurally correct
- skipping the counterweight

## Default output shape

Use this shape unless the operator wants a different one:

```markdown
**PH-CIV promotion test**
- PH-CIV source:
- Source type:
- Extracted mechanism:
- Best CIV-STATE destination:
- Why it survives compression:
- Counterweight:
- Membrane surface:
- Next step:
```

## Success condition

This skill succeeds when the membrane becomes clearer rather than blurrier: the public PH-CIV insight is either left where it belongs or translated into a narrow, counterweighted, auditable CIV-STATE destination with no silent drift.

## strategy-codex instance notes

- Canonical membrane notes:
  - [PH-CIV to CIV-STATE bridge](../../../statecraft/states/ph-civ-to-civ-state-bridge.md)
  - [PH-CIV promotion ledger](../../../statecraft/states/ph-civ-promotion-ledger.md)
  - [CIV-STATE review queue](../../../statecraft/states/review-queue.md)
- Public local mirror:
  - [public/ph-civ/README.md](../../../public/ph-civ/README.md)
- Use this skill before direct CIV-STATE mutation when the conversion rule itself is still doing the hard work.

## Preferred validation commands after skill edits

```powershell
python scripts/validate_skills.py
```
